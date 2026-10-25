#!/usr/bin/env python3
"""Regression tests for socialy_check.py ship mode (L-23 / L-23c / L-27).

Run: python3 tools/test_socialy_check.py  (exit 0 = all pass)

Fixtures (tools/fixtures/):
- thread-overlimit.txt - reconstruction of the ORIGINAL Scorecard W43
  thread as prepped on 2026-10-24. X's counter measured its tweets 3/4/6
  at 294/310/291; the live thread stopped after tweet 2. The gate MUST
  fail this file and name those counts. (The prep record that day said
  "ship gate PASS on article/script/metadata" - the thread was never in
  the gate's file list. The code measured correctly when finally run;
  L-23c adds the 272 prep ceiling and these fixtures so the miss
  cannot recur silently.)
- thread-scorecard-corrected.txt - the thread as actually completed
  (8 tweets, every fact preserved). MUST pass.
- thread-week-ahead.txt - the 2026-10-25 Week Ahead thread, ship-ready
  form (link filled), all tweets <= 233 raw. MUST pass.
- community-ok.txt - a COMMUNITY POST block within the prep ceiling.
  MUST pass. (Real URLs are counted raw - conservative: X counts a
  URL at t.co length, so passing this gate guarantees fitting X.)
- community-overlimit.txt - the original 2026-10-24 community text
  (288 by X's counter with the URL at t.co length; 310 raw here).
  MUST fail with a COMMUNITY LENGTH line.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "socialy_check.py")
FIX = os.path.join(HERE, "fixtures")

CASES = [
    ("thread-overlimit.txt", 1, ["294 chars", "310 chars", "291 chars",
                                 "TWEET LENGTH"]),
    ("thread-scorecard-corrected.txt", 0, ["SHIP GATE: PASS"]),
    ("thread-week-ahead.txt", 0, ["SHIP GATE: PASS"]),
    ("community-ok.txt", 0, ["SHIP GATE: PASS"]),
    ("community-overlimit.txt", 1, ["COMMUNITY LENGTH"]),
]


def main():
    failures = 0
    for name, want_rc, needles in CASES:
        path = os.path.join(FIX, name)
        r = subprocess.run([sys.executable, CHECK, "ship", path],
                           capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        problems = []
        if r.returncode != want_rc:
            problems.append(f"exit {r.returncode}, want {want_rc}")
        for needle in needles:
            if needle not in out:
                problems.append(f"missing in output: {needle!r}")
        if problems:
            failures += 1
            print(f"FAIL {name}: " + "; ".join(problems))
        else:
            print(f"ok   {name} (exit {r.returncode})")
    print(f"{'ALL PASS' if failures == 0 else f'{failures} CASE(S) FAILED'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
