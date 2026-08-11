import subprocess
import tempfile
import os
from pathlib import Path

DESCRIPTION = "Evaluate MeTTa code using ~/PeTTa/run.sh. Pass multi-line MeTTa code as a string."

RUN_SH = str(Path.home() / "PeTTa" / "run.sh")
PETTA_DIR = str(Path.home() / "PeTTa")

# Default imports prepended to every eval - NAL and PLN inference libraries
DEFAULT_IMPORTS = """!(import! &self lib_nal)
!(import! &self lib_pln)
"""

def run(code):
    """
    code: str - multi-line MeTTa code to evaluate
    returns: str - output from run.sh
    """
    code = code.strip()
    if not code:
        return "No MeTTa code provided"
    
    full_code = DEFAULT_IMPORTS + code
    
    # Write temp file to ~/PeTTa/ so working_dir resolves correctly for imports
    with tempfile.NamedTemporaryFile(mode="w", suffix=".metta", delete=False, dir=PETTA_DIR, prefix="tmp_metta_") as f:
        f.write(full_code)
        f.flush()
        temp_path = f.name
    
    try:
        result = subprocess.run(
            ["bash", RUN_SH, temp_path, "-s"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout
        if result.stderr:
            output += "\n[STDERR]\n" + result.stderr
        if not output.strip():
            output = "(no output)"
        return output
    except subprocess.TimeoutExpired:
        return "Timeout: MeTTa evaluation took longer than 30 seconds"
    except Exception as e:
        return f"Error: {e}"
    finally:
        os.unlink(temp_path)
