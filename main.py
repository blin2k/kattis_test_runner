import sys
import subprocess
from pathlib import Path
import difflib

SOLUTION_DIR = Path("solutions")
PY = sys.executable
TIMEOUT_SEC = 10

def norm(s):
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in s.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)

def run_case(problem_name, algorithm, infile, expfile):
    case_id = infile.stem
    if case_id == problem_name:
        label = f"[{problem_name}]"
    else:
        label = f"[{problem_name}:{case_id}]"

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
        return False, f"{label} ⏱️ Overtime（>{TIMEOUT_SEC}s）"

    out = proc.stdout
    err = proc.stderr
    rc = proc.returncode

    with expfile.open("r", encoding="utf-8") as f:
        expected = f.read()

    out_n = norm(out)
    exp_n = norm(expected)

    if rc != 0:
        msg = f"{label} ❌ Return code: {rc}"
        if err:
            msg += f"\nstderr:\n{err}"
        return False, msg

    if out_n == exp_n:
        return True, f"{label} ✅ Pass"
    else:
        diff = "\n".join(
            difflib.unified_diff(
                exp_n.splitlines(),
                out_n.splitlines(),
                fromfile=f"{expfile.name} (expected)",
                tofile=f"{expfile.name} (actual)",
                lineterm=""
            )
        )
        detail = f"{label} ❌ Output not matching\n" + (f"{diff}" if diff.strip() else "(diff can't display)")
        if err.strip():
            detail += f"\n\nstderr:\n{err}"
        return False, detail

def main():
    solution_dirs = sorted([p for p in SOLUTION_DIR.iterdir() if p.is_dir()])
    passed = 0
    total = 0
    logs = []
    had_failure = False

    for problem_dir in solution_dirs:
        problem_name = problem_dir.name
        algorithm = problem_dir / "algorithm.py"

        if not algorithm.exists():
            logs.append(f"[{problem_name}] ❌ Missing algorithm.py")
            had_failure = True
            continue

        testcase_dir = problem_dir / "testcases"
        if not testcase_dir.exists():
            logs.append(f"[{problem_name}] ⚠️ No testcase directory found")
            had_failure = True
            continue

        case_inputs = sorted(testcase_dir.glob("*.in"))
        if not case_inputs:
            logs.append(f"[{problem_name}] ⚠️ No testcase inputs found")
            had_failure = True
            continue

        for infile in case_inputs:
            expfile = infile.with_suffix(".out")
            if not expfile.exists():
                logs.append(
                    f"[{problem_name}:{infile.stem}] ❌ Missing expected output file {expfile.name}"
                )
                had_failure = True
                continue

            ok, msg = run_case(problem_name, algorithm, infile, expfile)
            logs.append(msg)
            total += 1
            if ok:
                passed += 1
            else:
                had_failure = True

    print("\n".join(logs))
    if total == 0:
        summary = "No testcases were executed"
    else:
        summary = f"Passed: {passed}/{total}"
    print(f"\n=== Summary ===\n{summary}")

    all_ok = total > 0 and passed == total and not had_failure
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
