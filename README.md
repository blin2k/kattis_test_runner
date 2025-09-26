# kattis_test_runner

## TLDR
1. Write your code to `solutions/Problem_*/algorithm.py` under the problem folder.
2. Copy and paste testcases to `solutions/Problem_*/testcases/sample_*.in` and `solutions/Problem_*/testcases/sample_*.out` from Kattis. It is okay to leave one empty if there are less than 3 testcases on Kattis. You can also add more test files.
3. Run `python3 main.py`

## Overview
A lightweight CLI harness for running CMPUT 403 Kattis-style solutions against curated samples. It auto-discovers each problem, executes its `algorithm.py`, and reports unified diffs when output mismatches are encountered.

## Prerequisites
- Python 3.8+ (the runner invokes whatever interpreter launches `main.py`).

## Repository Layout
- `main.py` – orchestrates discovery and execution of solutions and their testcases.
- `solutions/Problem_X/`
  - `algorithm.py` – Python entry point expected to read from `stdin` and write to `stdout`.
  - `testcases/` – six files named `sample_1.in/.out` through `sample_3.in/.out` holding paired inputs and expected outputs. Additional `*.in/.out` pairs are also picked up automatically if needed.

## Usage
```bash
python3 main.py
```
The runner locates every `solutions/Problem_*/algorithm.py`, streams each `sample_*.in` into the script, and compares the captured stdout with the corresponding `.out`. Results are printed per sample with a final summary. A non-zero exit code indicates at least one failure, timeout, or missing artifact.

Each test execution inherits a 10 second timeout. When a timeout or runtime error occurs, stderr (if any) is reported with the failure message.

## Adding or Updating Problems
1. Create a new folder `solutions/Problem_<NAME>/`.
2. Add an `algorithm.py` that exposes a `main()` style entry point (reading stdin, writing stdout).
3. Populate `testcases/` with at least the canonical `sample_1.in/.out`, `sample_2.in/.out`, and `sample_3.in/.out`. You can add more `*.in/.out` pairs for stress or edge cases—the runner will execute them all.
4. (Optional) Include helper functions like `solve()` and inline unit tests to streamline manual verification.

## Extending the Runner
- Adjust `TIMEOUT_SEC` in `main.py` to change per-sample execution limits.
- Introduce additional validation or scripting (e.g., formatting, linting) by extending `main.py` or wrapping it with shell scripts.

## Troubleshooting
- **Missing files**: The summary flags absent `algorithm.py`, `testcases/` folders, or unmatched `.in/.out` pairs.
- **Unexpected diffs**: The runner normalizes line endings and trims trailing blank lines before comparison to reduce false positives.
- **Different interpreter**: Set `PYTHONPATH` or launch with the desired interpreter via `python3 main.py` to control imports and runtime.

## Development Tips
- Co-locate quick assertions (e.g., `test_solve`) inside each `algorithm.py` for fast feedback.
- Use descriptive sample cases that mirror Kattis “Sample Input/Output” plus custom edge cases so the harness doubles as regression protection.
- Consider scripting additional samples (stress tests) and naming them clearly (e.g., `large_01.in`)—the runner accepts any `*.in/.out` pair.

