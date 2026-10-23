#!/usr/bin/env python3
"""socialy_check.py - Socialy.INK gate runner (Phase 5, SPEC-self-learning.md).

One command that runs the platform's codified checks.

Usage:
    python3 socialy_check.py ship FILE [FILE ...]
        Pre-ship gate: lints every file (socialy_lint.py), scans body
        lines for unresolved placeholders, and reports subtitle/SEO
        presence on article prep files. Exit 1 blocks the ship.

    python3 socialy_check.py state
        Platform self-check: parity checker against the live catalogue,
        run-log validation over logs/, and a coverage check that every
        taxonomy code in SPEC-run-log.md is registered in LESSONS.md.
        Exit 1 lists what is unwell.

Standard library only.
"""

import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LINT = os.path.join(HERE, "socialy_lint.py")
PARITY = os.path.join(HERE, "socialy_parity.py")
RUNLOG = os.path.join(HERE, "socialy_runlog.py")
SPEC_RUNLOG = os.path.join(ROOT, "SPEC-run-log.md")
LESSONS = os.path.join(ROOT, "LESSONS.md")
LOGS_DIR = os.path.join(ROOT, "logs")

PLACEHOLDER_RES = [
    re.compile(r"\[[A-Z][A-Za-z0-9 ]*\sURL\]"),          # [P2 URL], [ARTICLE LINK]
    re.compile(r"<[A-Z][A-Za-z0-9 ]*\sURL>"),            # <P2 URL>
    re.compile(r"\bTODO\b|\bTBD\b|\bXXX+\b"),
    re.compile(r"\[ARTICLE LINK\]|\[LINK\]|\[URL\]"),
]
SUBTITLE_RE = re.compile(r"^\s*#?\s*Subtitle\b", re.IGNORECASE)
SEO_BLOCK_RE = re.compile(r"SEO title", re.IGNORECASE)
CODE_RE = re.compile(r"`([A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+)`")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def body_lines(path):
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.lstrip().startswith("#"):
                continue  # prep headers may legitimately mention placeholders
            yield i, line.rstrip("\n")


def check_ship(files):
    failures = 0
    for path in files:
        print(f"== ship check: {path}")
        rc, out = run([sys.executable, LINT, path])
        print(out.strip())
        if rc != 0:
            failures += 1
            print("  LINT: FAIL")
        hits = []
        has_subtitle = has_seo = False
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if SUBTITLE_RE.search(text):
            has_subtitle = True
        if SEO_BLOCK_RE.search(text):
            has_seo = True
        for i, line in body_lines(path):
            for rx in PLACEHOLDER_RES:
                if rx.search(line):
                    hits.append((i, line.strip()[:90]))
                    break
        if hits:
            failures += 1
            for i, line in hits:
                print(f"  PLACEHOLDER line {i}: {line}")
        else:
            print("  placeholders: none")
        long_tweets = [(i, len(line), line.strip()[:60]) for i, line in body_lines(path)
                       if re.match(r"^\d+/ ", line) and len(line) > 280]
        if long_tweets:
            failures += 1
            for i, n, line in long_tweets:
                print(f"  TWEET LENGTH line {i}: {n} chars > 280: {line}")
        else:
            print("  tweet lengths: all <= 280")
        print(f"  subtitle marker: {'present' if has_subtitle else 'absent'}; "
              f"SEO block: {'present' if has_seo else 'absent'}")
    print(f"SHIP GATE: {'PASS' if failures == 0 else 'FAIL'}")
    return 0 if failures == 0 else 1


def check_state():
    failures = 0
    print("== parity")
    rc, out = run([sys.executable, PARITY])
    print(out.strip()[-1500:])
    if rc != 0:
        failures += 1
        print("  PARITY: FAIL")
    print("== run logs")
    logs = sorted(glob.glob(os.path.join(LOGS_DIR, "*.md")))
    if not logs:
        print("  (no canonical run logs yet - expected until runs file here)")
    else:
        # Logs dated on/before 2026-10-23 predate schema adoption in the
        # engagement cron body; they are reported as legacy warnings, not
        # failures. Newer logs validate strictly.
        strict = [p for p in logs if os.path.basename(p)[-13:-3] > "2026-10-23"]
        legacy = [p for p in logs if p not in strict]
        for p in legacy:
            print(f"  legacy (pre-schema, warn only): {os.path.basename(p)}")
        if strict:
            rc, out = run([sys.executable, RUNLOG] + strict)
            print(out.strip()[-1500:])
            if rc != 0:
                failures += 1
                print("  RUNLOG: FAIL")
        else:
            print("  (no post-adoption logs to validate yet)")
    print("== lessons coverage")
    spec = open(SPEC_RUNLOG, encoding="utf-8").read()
    m = re.search(r"^## 2\..*?^## 3\.", spec, re.MULTILINE | re.DOTALL)
    section2 = m.group(0) if m else spec
    codes = sorted(set(re.findall(r"\*\*([A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+)\*\*", section2)))
    lessons = open(LESSONS, encoding="utf-8").read() if os.path.exists(LESSONS) else ""
    missing = [c for c in codes if c not in lessons]
    if missing:
        failures += 1
        for c in missing:
            print(f"  UNREGISTERED CODE: {c}")
    else:
        print(f"  all {len(codes)} taxonomy codes registered in LESSONS.md")
    print(f"STATE: {'HEALTHY' if failures == 0 else 'UNWELL'}")
    return 0 if failures == 0 else 1


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    mode = sys.argv[1]
    if mode == "ship":
        if len(sys.argv) < 3:
            print("ship mode needs at least one FILE")
            return 2
        return check_ship(sys.argv[2:])
    if mode == "state":
        return check_state()
    print(f"unknown mode: {mode}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
