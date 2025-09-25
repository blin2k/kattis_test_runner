import sys
import subprocess
from pathlib import Path
import difflib

SOLUTION_DIR = Path("solutions")
TESTCASE_DIR = Path("testcases")
PY = sys.executable
TIMEOUT_SEC = 10

def norm(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in s.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)

def run_case(stem):
    algorithm = SOLUTION_DIR / f"{stem}.py"
    infile = TESTCASE_DIR / f"{stem}.in"
    expfile = TESTCASE_DIR / f"{stem}.out"

    try:
        with infile.open("r", encoding="utf-8") as fin:
            proc = subprocess.run(
                [PY, str(algorithm)],
                stdin=fin,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SEC,
                check=False,
            )
    except subprocess.TimeoutExpired:
        return False, f"[{stem}] ⏱️ Overtime（>{TIMEOUT_SEC}s）"

    out = proc.stdout
    err = proc.stderr
    rc = proc.returncode

    with expfile.open("r", encoding="utf-8") as f:
        expected = f.read()

    out_n = norm(out)
    exp_n = norm(expected)

    if rc != 0:
        msg = f"[{stem}] ❌ Return code: {rc}"
        if err:
            msg += f"\nstderr:\n{err}"
        return False, msg

    if out_n == exp_n:
        return True, f"[{stem}] ✅ Pass"
    else:
        diff = "\n".join(
            difflib.unified_diff(
                exp_n.splitlines(),
                out_n.splitlines(),
                fromfile=f"{stem}.out (expected)",
                tofile=f"{stem}.out (actual)",
                lineterm=""
            )
        )
        detail = f"[{stem}] ❌ Output not matching\n" + (f"{diff}" if diff.strip() else "(diff can't display)")
        if err.strip():
            detail += f"\n\nstderr:\n{err}"
        return False, detail

def main():
    stems = [chr(x) for x in range(ord('A'), ord('E') + 1)]
    total = 5
    passed = 0
    logs = []

    for stem in stems:
        ok, msg = run_case(stem)
        logs.append(msg)
        if ok:
            passed += 1

    print("\n".join(logs))
    print(f"\n=== Summary ===\nPassed: {passed}/{total}")

    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()