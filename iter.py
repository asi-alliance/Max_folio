import datetime
import inspect
import json
import os
import sys
import openai
import time
import importlib.util
import signal
import subprocess
import tempfile
from pathlib import Path

# --------------------------------------------------------------------
# 0. Configuration:
# --------------------------------------------------------------------
LLM_TIMEOUT=30
PRINT_CALLS = False
MAX_MEMORY_CHARS = 50000
MAX_TOOL_OUTPUT_CHARS = 10000
EXPERIENCE_SIZE = 100
MAX_FAST_STEPS = 50
SLOW_STEP_DELAY = 60
ERROR_RECOVERY_TIME = 1 #after how long to retry when exception occurs
RETURN_VALUE_PRESERVE = 2000
DEFAULT_DELAY = 0 #default delay added irregard of whether in slow mode
MAX_TOKENS = 3000
INIT_WAIT = 10
MAX_TOOLS = 20
MAX_TOOL_DESCRIPTION_CHARS = 500
DYNAMIC_TIMEOUT = 5
MODEL = os.getenv("LLM_MODEL", "ggml-org/gemma-4-26B-A4B-it-GGUF:Q4_0")
BASE_URL = os.getenv("BASE_URL", "http://192.168.64.1:2277/v1")
API_KEY = os.getenv("AI_API_KEY", "dummy")

# --------------------------------------------------------------------
# 1. Dynamic execution:
# --------------------------------------------------------------------
def dynamic_worker():
    path = Path(sys.argv[2])
    function = sys.argv[3]
    result_path = Path(sys.argv[4])
    payload_path = Path(sys.argv[5])
    try:
        payload = json.loads(payload_path.read_text())
        spec = importlib.util.spec_from_file_location("_dynamic_" + path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if function == "__tool_metadata__":
            parameters = inspect.signature(module.run).parameters.values()
            description = str(module.DESCRIPTION)
            if len(description) > MAX_TOOL_DESCRIPTION_CHARS:
                description = description[:MAX_TOOL_DESCRIPTION_CHARS] + " [DESCRIPTION TRUNCATED]"
            result = {"description": description, "parameters": [parameter.name for parameter in parameters]}
        else:
            result = getattr(module, function)(*payload.get("args", []), **payload.get("kwargs", {}))
            if function != "transform" and result is not None:
                result = str(result)
        output = {"ok": True, "result": result}
    except BaseException as error:
        output = {"ok": False, "error": f"{type(error).__name__}: {error}"}
    try:
        result_path.write_text(json.dumps(output, ensure_ascii=False))
    except BaseException as error:
        result_path.write_text(json.dumps({"ok": False, "error": f"Result serialization failed: {type(error).__name__}: {error}"}, ensure_ascii=False))

def invoke_dynamic(path, function, *args, **kwargs):
    result_fd, result_file = tempfile.mkstemp(prefix="iter-result-", suffix=".json")
    payload_fd, payload_file = tempfile.mkstemp(prefix="iter-payload-", suffix=".json")
    try:
        os.close(result_fd)
        os.close(payload_fd)
        Path(payload_file).write_text(json.dumps({"args": args, "kwargs": kwargs}, ensure_ascii=False))
        inherit_stdin = Path(path).stem == "terminal" and function == "receive"
        process = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--invoke", str(Path(path).resolve()), function, result_file, payload_file],
            stdin=None if inherit_stdin else subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=not inherit_stdin,
            close_fds=True
        )
        try:
            process.wait(timeout=DYNAMIC_TIMEOUT)
        except subprocess.TimeoutExpired:
            if inherit_stdin:
                process.kill()
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            process.wait()
            return {"ok": False, "error": f"TIMEOUT after {DYNAMIC_TIMEOUT}s"}
        try:
            return json.loads(Path(result_file).read_text())
        except Exception:
            return {"ok": False, "error": f"Dynamic process exited with code {process.returncode} without a valid result"}
    finally:
        for file in (result_file, payload_file):
            try:
                os.unlink(file)
            except FileNotFoundError:
                pass

if len(sys.argv) > 1 and sys.argv[1] == "--invoke":
    dynamic_worker()
    sys.exit(0)

# --------------------------------------------------------------------
# 2. Local tool helpers:
# --------------------------------------------------------------------
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def receive():
    events = []
    paths = [path for path in sorted(Path("channels").glob("*.py")) if not path.name.startswith("_")]
    for path in paths:
        try:
            result = invoke_dynamic(path, "receive")
            if not result["ok"]:
                raise RuntimeError(result["error"])
            event = result["result"]
            if event:
                events.append("[" + path.stem + "] " + str(event))
        except Exception as error:
            events.append(f"[CHANNEL ERROR in {path}: {type(error).__name__}: {error}. Repair {path} if needed.]")
    return "\n".join(events)

def slow_wait_for_input():
    for second in range(SLOW_STEP_DELAY):
        time.sleep(1)
        event_append = receive()
        if event_append:
            return event_append
    return ""

# --------------------------------------------------------------------
# 3. Local tools:
# --------------------------------------------------------------------
def load_tools():
    inops = {}
    errors = []
    paths = [path for path in sorted(Path("tools").glob("*.py")) if not path.name.startswith("_")]
    for path in paths[:MAX_TOOLS]:
        try:
            result = invoke_dynamic(path, "__tool_metadata__")
            if not result["ok"]:
                raise RuntimeError(result["error"])
            metadata = result["result"]
            inops[path.stem] = (path, metadata["description"], metadata["parameters"])
        except Exception as error:
            errors.append(f"[TOOL ERROR in {path}: {type(error).__name__}: {error}. Repair {path} if needed.]")
    return inops, len(paths) - MAX_TOOLS, "\n".join(errors)

def native_tools(inops):
    tools = []
    for name, (path, description, parameters) in inops.items():
        tools.append({"type": "function", "function": {"name": name, "description": description, "parameters": {"type": "object", "properties": { parameter: { "type": "string" } for parameter in parameters }, "required": [parameter for parameter in parameters], "additionalProperties": False}}})
    return tools

def apply_transformation(messages, tools):
    errors = []
    paths = sorted(path for path in Path("transformations").glob("*.py") if not path.name.startswith("_"))
    for path in paths:
        try:
            result = invoke_dynamic(path, "transform", messages, tools)
            if not result["ok"]:
                raise RuntimeError(result["error"])
            messages, tools = result["result"]
        except Exception as error:
            errors.append(f"[RUNTIME ERROR in {path}: {type(error).__name__}: {error}. Repair {path} if needed.]")
    return messages, tools, "\n".join(errors)

def save_experience(experience):
    with open("experience.tmp", "w", encoding="utf-8") as file:
        json.dump(experience, file, ensure_ascii=False, indent=2)
    os.replace("experience.tmp", "experience.json")

# --------------------------------------------------------------------
# 4. Main loop
# --------------------------------------------------------------------
try:
    with open("experience.json", "r", encoding="utf-8") as file:
        experience = json.load(file)
except FileNotFoundError:
    experience = []
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=LLM_TIMEOUT, max_retries=0)
time.sleep(INIT_WAIT)
Path("memory").mkdir(exist_ok=True)
Path("transformations").mkdir(exist_ok=True)
post_task_mode, autonomous_steps, new_burst, pending_event_append = False, 0, True, ""
while True:
    experience = experience[-EXPERIENCE_SIZE:]
    while experience and experience[0].get("role") == "tool":
        experience = experience[1:]
    history_checkpoint = len(experience) #before user input
    try:
        time.sleep(DEFAULT_DELAY)
        print("BEFORE RECEIVE")
        event_append = pending_event_append or receive()
        print("AFTER RECEIVE")
        temporary_message = []
        if event_append:
            autonomous_steps, new_burst, post_task_mode = 0, False, False
            print("IN FROM CHANNEL " + event_append)
            experience += [{"role": "user", "content": "Step " + get_current_time() + ": " + event_append}]
            save_experience(experience)
            pending_event_append = ""
        elif new_burst:
            post_task_mode, new_burst = True, False
            temporary_message += [{"role": "user", "content": "Step " + get_current_time() + ": [TASK COMPLETED. DO NOT RE-SEND THE COMPLETED RESPONSE. NOW QUERY FOR AND PICK A TASK BASED ON YOUR GOALS, PREFERABLY MEMORY CONSOLIDATION: FINDING EPISODES WHICH SUPPORT / CONTRADICT LTM ITEMS, LINKING EPISODES, PROMOTING USEFUL MEMORIES]"}]
        elif post_task_mode:
            temporary_message += [{"role": "user", "content": "Step " + get_current_time() + ": [NO NEW USER INPUT. CONTINUE AUTONOMOUS WORK. DO NOT REPEAT THE PREVIOUS RESPONSE. ONLY USE send FOR GENUINELY NEW INFORMATION OR WHEN USER INPUT IS NEEDED.]"}]
        else:
            temporary_message += [{"role": "user", "content": "Step " + get_current_time() + ": [NO ADDITIONAL USER INPUT. CONTINUE THE CURRENT USER TASK.]"}]
        history_checkpoint = len(experience) #as we want not to loose user input even when exception
        while True:
            INOPS, omitted_tools, tool_load_error = load_tools()
            if tool_load_error:
                temporary_message += [{"role": "user", "content": tool_load_error}]
            if omitted_tools > 0:
                temporary_message += [{"role": "user", "content": f"[TOOL LIMIT REACHED: {omitted_tools} tools are currently omitted. Consolidate or remove tools if they are needed.]"}]
            TOOLS = native_tools(INOPS)
            MEMORY = "\n\n".join(path.name + ":\n" + path.read_text().strip() for path in Path("memory").iterdir() if path.is_file() and not path.name.startswith("_"))
            if len(MEMORY) > MAX_MEMORY_CHARS:
                omitted = len(MEMORY) - MAX_MEMORY_CHARS
                MEMORY = MEMORY[:MAX_MEMORY_CHARS] + f"\n[MEMORY TRUNCATED: {omitted} chars omitted, REDUCE MEMORY FILES!]"
            request_messages = [{"role": "system", "content": "prompt.txt:\n" + open("prompt.txt").read().strip() + "\n\n" + "reprogramming.txt:\n" + open("reprogramming.txt").read().strip() + "\n\n" + MEMORY}] + experience + temporary_message
            request_messages, request_tools, transformation_error = apply_transformation(request_messages, TOOLS)
            if transformation_error:
                request_messages += [{"role": "user", "content": transformation_error}]
            print("BEFORE LLM")
            response = client.client.chat.completions.create(model=MODEL, messages=request_messages, tools=request_tools, tool_choice="required", max_tokens=MAX_TOKENS)
            print("AFTER LLM")
            message = response.choices[0].message
            if message.tool_calls:
                break
            temporary_message += [{"role": "user", "content": "Your previous response was invalid. Do not answer in plain text. Call at least one tool now."}]
        print(f"RESPONSE {response}\nFINISH_REASON {response.choices[0].finish_reason}\nUSAGE {response.usage}")
        experience = [{**old_message, "content": old_message.get("content", "")[:RETURN_VALUE_PRESERVE] + " [TRUNCATED]"} if old_message.get("role") == "tool" and len(old_message.get("content", "")) > RETURN_VALUE_PRESERVE else old_message for old_message in experience]
        experience += [{**{key: value for key, value in message.model_dump(exclude_none=True).items() if key not in ("reasoning", "reasoning_details", "reasoning_content")}, "content": "Step " + get_current_time() + ": [TOOL CALL]"}]
        tool_outputs = []
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as error:
                tool_arguments = tool_call.function.arguments
                ret = f"Invalid tool arguments from model: {error}"
            else:
                try: #unless tool unknown/args formatting issue, we use the tool's INOPS function return value:
                    if tool_name not in INOPS:
                        ret = f"Unknown tool: {tool_name!r}"
                    elif not isinstance(tool_arguments, dict):
                        ret = "Tool arguments must be a JSON object"
                    else:
                        result = invoke_dynamic(INOPS[tool_name][0], "run", **tool_arguments)
                        ret = result["result"] if result["ok"] else f"Tool execution failed: {result['error']}"
                except Exception as error:
                    ret = f"Tool execution failed: {type(error).__name__}: {error}"
            ret = str(ret)
            if len(ret) > MAX_TOOL_OUTPUT_CHARS:
                ret = ret[:MAX_TOOL_OUTPUT_CHARS] + " [TRUNCATED]"
            experience += [{"role": "tool", "tool_call_id": tool_call.id, "content": "Step " + get_current_time() + ": " + ret}]
            tool_outputs += ["tool call: " + tool_name + " " + str(tool_arguments) + "\n" "tool return: " + ret]
        history_checkpoint = len(experience) #tool calls succeeded, even on later exception we won't unroll them
        save_experience(experience)
        print("Output> " + "\n".join(tool_outputs))
        autonomous_steps = 0 if event_append else autonomous_steps + 1
        if tool_name == "nop" or autonomous_steps >= MAX_FAST_STEPS:
            new_burst, autonomous_steps = True, 0
            pending_event_append = slow_wait_for_input()
    except Exception as error:
        print(f"Output> {type(error).__name__}: {error}")
        experience = experience[:history_checkpoint]
        time.sleep(ERROR_RECOVERY_TIME)
