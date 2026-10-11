import re
import json

DESCRIPTION = "Auto-update space.metta with formalizations from chroma_query results and formalize_metta tool calls"

def check_parens(s):
    depth = 0
    for ch in s:
        if ch == '(': depth += 1
        elif ch == ')': depth -= 1
    return depth == 0

def is_type_decl(s):
    """Check if line is a MeTTa type declaration like (: max agent)."""
    return s.strip().startswith('(:')

def is_valid_metta(line):
    """Only accept valid MeTTa formalization lines."""
    s = line.strip()
    if not s or s.startswith(';;'):
        return False
    if is_type_decl(s):
        return False
    if not check_parens(s):
        return False
    if not s.startswith('('):
        return False
    if not s.endswith(')'):
        return False
    if '"' in s:
        return False
    # Reject if outermost paren closes before end (e.g. Content: leakage)
    depth = 0
    for i, ch in enumerate(s):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0 and i != len(s) - 1:
                return False
    return True

def wrap_default_stv(line):
    s = line.strip()
    if '(stv ' in s:
        return s
    if is_type_decl(s):
        return s
    return f"({s} (stv 1.0 0.5))"

def transform(messages, tools):
    from pathlib import Path

    space_path = Path.home() / "iter" / "transformations" / ".runtime" / "space.metta"
    if not space_path.exists():
        return messages, tools

    formalizations = []

    # 1. Parse formalizations from chroma_query results in tool messages
    for msg in messages:
        if msg.get("role") != "tool":
            content = msg.get("content", "")
        else:
            content = str(msg.get("content", ""))
        if "Formalization:" not in content:
            continue
        lines = content.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i]
            if "Formalization:" in line:
                idx = line.index("Formalization:")
                formalization = line[idx + len("Formalization:"):].strip()
                if not is_valid_metta(formalization):
                    i += 1
                    continue
                # Search backwards for STV in same result block
                stv_str = None
                for j in range(i - 1, max(i - 10, -1), -1):
                    if "STV:" in lines[j]:
                        stv_str = lines[j].strip()
                        break
                if stv_str:
                    stv_match = re.search(r'STV:\s*\(([^,]+),\s*([^)]+)\)', stv_str)
                    if stv_match:
                        strength = stv_match.group(1).strip()
                        confidence = stv_match.group(2).strip()
                        wrapped = f"({formalization} (stv {strength} {confidence}))"
                    else:
                        wrapped = wrap_default_stv(formalization)
                else:
                    wrapped = wrap_default_stv(formalization)
                if check_parens(wrapped) and '"' not in wrapped:
                    formalizations.append(wrapped)
            i += 1

    # 2. Parse formalizations from formalize_metta tool calls in assistant messages
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        tool_calls = msg.get("tool_calls", [])
        if not tool_calls:
            continue
        for tc in tool_calls:
            try:
                func = tc.get("function", tc) if isinstance(tc, dict) else None
                if func is None:
                    continue
                name = func.get("name", "")
                if name != "formalize_metta":
                    continue
                args_str = func.get("arguments", "{}")
                args = json.loads(args_str) if isinstance(args_str, str) else args_str
                formalization = args.get("formalization", "")
                if not formalization or not is_valid_metta(formalization):
                    continue
                wrapped = wrap_default_stv(formalization)
                if check_parens(wrapped) and '"' not in wrapped:
                    formalizations.append(wrapped)
            except Exception:
                continue

    # Read current space.metta
    with open(space_path, "r") as f:
        lines = f.readlines()

    header = ";; === Formalizations (auto-updated) ===\n"
    formalization_lines = [f + "\n" for f in formalizations]

    # Filter existing lines: only keep valid MeTTa lines with stv
    existing_non_header = []
    for l in lines:
        stripped = l.strip()
        if stripped.startswith(";;"):
            continue
        if not stripped:
            continue
        if not check_parens(stripped):
            continue
        if '"' in stripped:
            continue
        if not stripped.startswith('('):
            continue
        if is_type_decl(stripped):
            existing_non_header.append(stripped + "\n")
            continue
        # Wrap with default stv if missing
        if '(stv ' not in stripped:
            stripped = wrap_default_stv(stripped)
        existing_non_header.append(stripped + "\n")

    # Load base atoms from memory/metta/space.metta (hand-curated knowledge)
    base_space_path = Path.home() / "iter" / "memory" / "metta" / "space.metta"
    base_lines = []
    if base_space_path.exists():
        with open(base_space_path) as bf:
            for bl in bf:
                bs = bl.strip()
                if not bs or bs.startswith(';;') or bs.startswith('#'):
                    continue
                if not check_parens(bs) or '"' in bs or not bs.startswith('('):
                    continue
                if is_type_decl(bs):
                    base_lines.append(bs + "\n")
                    continue
                if '(stv ' not in bs:
                    bs = wrap_default_stv(bs)
                base_lines.append(bs + "\n")

    # Combine: base atoms first, then formalizations, then existing
    all_lines = [header] + base_lines + formalization_lines + existing_non_header

    # Dedup
    seen = set()
    deduped = []
    for l in all_lines:
        stripped = l.strip()
        if not stripped:
            continue
        if stripped not in seen:
            seen.add(stripped)
            deduped.append(l)

    if len(deduped) > 500:
        deduped = deduped[:500]

    with open(space_path, "w") as f:
        f.writelines(deduped)

    return messages, tools
