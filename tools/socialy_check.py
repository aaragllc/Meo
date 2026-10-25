#!/usr/bin/env python3
"""socialy_check.py - Socialy.INK gate runner (Phase 5, SPEC-self-learning.md).

One command that runs the platform's codified checks.

Usage:
    python3 socialy_check.py ship FILE [FILE ...]
        Pre-ship gate: lints every file (socialy_lint.py), scans body
        lines for unresolved placeholders, reports subtitle/SEO
        presence on article prep files, measures numbered tweet lines
        and COMMUNITY POST blocks against the platform limit (280)
        AND the prep ceiling (272, config tweet_prep_char_limit), and
        runs the SPEC-seo-growth checks: episode metadata must carry
        the follow line and an article link, a declared YouTube title
        must carry its " - " search clause, and article prep (a file
        with a subtitle marker) must carry an SEO block. Exit 1
        blocks the ship. The gate must be run on the WHOLE pack
        (article, thread, script, metadata, LinkedIn and community
        drafts) - the 2026-10-24 scorecard miss happened because the
        thread file was never in the gate's file list (L-23c).

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
# L-23 extension: the live article URL (~64 chars for the Substack pattern)
# replaces [ARTICLE LINK] at ship time, so a tweet that fits at prep can
# break at post. Tweet lengths are measured with every placeholder
# substituted by a 64-char proxy; the placeholder itself is still reported
# (and filled) separately.
URL_PROXY = "x" * 64
# Placeholder patterns that stand in for a URL at prep time (used for
# length measurement only; TODO/TBD tokens are NOT substituted - they are
# not URLs and inflating them would skew the count).
MEASURE_RES = [PLACEHOLDER_RES[0], PLACEHOLDER_RES[1], PLACEHOLDER_RES[3]]
# L-23c (2026-10-24 scorecard incident): X's hard limit is 280, but drafts
# are held to a prep ceiling (default 272, config defaults.
# tweet_prep_char_limit) so ship-day substitutions and counting drift
# cannot push a tweet over. Python len() on the persona's ASCII text
# matched X's own counter exactly in the incident (294 == 294), so the
# raw count is the arbiter; the ceiling is the safety margin.
TWEET_HARD_MAX = 280
TWEET_PREP_MAX_FALLBACK = 272
COMMUNITY_MARKER_RE = re.compile(r"^COMMUNITY( POST)?\b", re.IGNORECASE)


def load_prep_max():
    try:
        cfg = open(CONFIG, encoding="utf-8").read()
    except OSError:
        return TWEET_PREP_MAX_FALLBACK
    m = re.search(r"tweet_prep_char_limit:\s*(\d+)", cfg)
    return int(m.group(1)) if m else TWEET_PREP_MAX_FALLBACK


def measure(line):
    """Length of a post line as X will see it: URL placeholders proxied."""
    measured = line
    for rx in MEASURE_RES:
        measured = rx.sub(URL_PROXY, measured)
    return len(measured)
SUBTITLE_RE = re.compile(r"^\s*#?\s*Subtitle\b", re.IGNORECASE)
SEO_BLOCK_RE = re.compile(r"SEO title", re.IGNORECASE)
CODE_RE = re.compile(r"`([A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+)`")

# SPEC-seo-growth.md ship checks. The follow line's source of truth is
# config.yaml (growth.episode_follow_line); the constant is a fallback.
CONFIG = os.path.join(ROOT, "config.yaml")
FOLLOW_LINE_FALLBACK = ("If this was useful, follow the show - "
                        "a new episode lands with every piece.")
SUBTITLE_LINE_RE = re.compile(r"^\s*#?\s*Subtitle\b", re.IGNORECASE)
YT_TITLE_RE = re.compile(r"^\s*#?\s*YouTube title\s*:\s*(.+?)\s*$",
                         re.IGNORECASE | re.MULTILINE)
ARTICLE_LINE_RE = re.compile(r"^Article:\s*\S+", re.MULTILINE)
ARTICLE_URL_RE = re.compile(r"https?://\S*substack\.com/p/\S+")


def load_follow_line():
    try:
        cfg = open(CONFIG, encoding="utf-8").read()
    except OSError:
        return FOLLOW_LINE_FALLBACK
    m = re.search(r'episode_follow_line:\s*"([^"]+)"', cfg)
    return m.group(1) if m else FOLLOW_LINE_FALLBACK


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
    follow_line = load_follow_line()
    for path in files:
        print(f"== ship check: {path}")
        # Narration scripts (podcast/*/<...>-script.md) carry the sign-off
        # phonetically for TTS; lint them as kind="script" so the written
        # sign-off rule does not false-positive on them.
        kind = "script" if "script" in os.path.basename(path).lower() else "article"
        rc, out = run([sys.executable, LINT, "--kind", kind, path])
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
        prep_max = load_prep_max()
        long_tweets = []
        for i, line in body_lines(path):
            if not re.match(r"^\d+/ ", line):
                continue
            n = measure(line)
            if n > TWEET_HARD_MAX:
                long_tweets.append((i, n, TWEET_HARD_MAX, line.strip()[:60]))
            elif n > prep_max:
                long_tweets.append((i, n, prep_max, line.strip()[:60]))
        if long_tweets:
            failures += 1
            for i, n, limit, line in long_tweets:
                kind = "hard limit" if limit == TWEET_HARD_MAX else "prep ceiling"
                print(f"  TWEET LENGTH line {i}: {n} chars > {limit} ({kind}): {line}")
        else:
            print(f"  tweet lengths: all <= {prep_max} (prep ceiling; "
                  f"hard limit {TWEET_HARD_MAX})")
        # L-27: derivative texts get the same measurement as tweets.
        # A block starting with a "COMMUNITY POST" marker line is one
        # post: its following non-blank lines are measured as a single
        # text (placeholders proxied) against the same ceilings.
        community_over = []
        lines_list = list(body_lines(path))
        for idx, (i, line) in enumerate(lines_list):
            if not COMMUNITY_MARKER_RE.match(line.strip()):
                continue
            block = []
            for j in range(idx + 1, len(lines_list)):
                nxt = lines_list[j][1]
                if not nxt.strip():
                    break
                block.append(nxt)
            if not block:
                continue
            n = measure("\n".join(block))
            if n > prep_max:
                community_over.append((i, n, block[0].strip()[:60]))
        if community_over:
            failures += 1
            for i, n, line in community_over:
                print(f"  COMMUNITY LENGTH line {i}: {n} chars > {prep_max} "
                      f"(prep ceiling): {line}")
        elif any(COMMUNITY_MARKER_RE.match(ln.strip()) for _i, ln in lines_list):
            print("  community posts: all within prep ceiling")
        print(f"  subtitle marker: {'present' if has_subtitle else 'absent'}; "
              f"SEO block: {'present' if has_seo else 'absent'}")
        # SPEC-seo-growth checks (presence of the growth wiring that
        # prep files declare; lengths are the linter's SEO_LEN rules).
        is_metadata = "metadata" in os.path.basename(path).lower()
        has_subtitle_line = any(SUBTITLE_LINE_RE.match(ln)
                                for ln in text.splitlines())
        growth_misses = []
        if is_metadata:
            if follow_line not in text:
                growth_misses.append("episode metadata: follow line missing")
            if not (ARTICLE_LINE_RE.search(text) or ARTICLE_URL_RE.search(text)):
                growth_misses.append("episode metadata: no article link")
        for m in YT_TITLE_RE.finditer(text):
            title = m.group(1).strip()
            parts = title.rsplit(" - ", 1)
            if len(parts) < 2 or not parts[1].strip():
                growth_misses.append(
                    f"YouTube title lacks the ' - ' search clause: {title[:80]}")
        if not is_metadata and has_subtitle_line and not has_seo:
            growth_misses.append("article prep: subtitle present but no SEO block")
        if growth_misses:
            failures += 1
            for miss in growth_misses:
                print(f"  SEO/GROWTH: {miss}")
        else:
            print("  SEO/growth checks: ok")
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
