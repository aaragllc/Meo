#!/usr/bin/env python3
"""socialy_lint.py - Socialy.INK draft linter (Phase 4, tool 1).

Lints persona post drafts against the written rules in POLICY.md, the
persona directive, and SPEC-studio.md. Standard library only.

Usage:
    python3 socialy_lint.py [--kind article|comment] FILE [FILE ...]

Exit code: 0 when every file is clean, 1 when any violation is found.

Prep-file convention: lines whose first non-space character is '#' are
prep/metadata comments, not post text. The content rules (EM_DASH, TICKER,
HYPE) apply to body lines only; the structural rules read their marked
lines directly (Subtitle marker, SEO block) or the file as a whole
(SIGNOFF).
"""

import argparse
import re
import sys
from collections import Counter

EM_DASH_CHAR = "\u2014"  # —
SIGNOFF_TEXT = "- That70s Da."
# Narration scripts carry the sign-off phonetically for the TTS render
# (standing podcast audio rule: brand never fed to TTS as written).
SCRIPT_SIGNOFF_TEXT = "That seventies day"
SUBTITLE_MAX = 200      # SPEC-studio.md C1
SEO_TITLE_MAX = 60      # standing SEO rule (see tools/README.md)
SEO_DESC_MAX = 160

# Banned hype words/phrases, exactly as listed in POLICY.md ("Hard bans")
# and the persona directive section 1. "disrupt" is matched as a word
# prefix so its inflections (disrupts, disrupted, disruption) fire too.
HYPE_PATTERNS = [
    ("revolutionary", re.compile(r"\brevolutionary\b", re.IGNORECASE)),
    ("game-changer", re.compile(r"\bgame[- ]changer\b", re.IGNORECASE)),
    ("disrupt", re.compile(r"\bdisrupt\w*\b", re.IGNORECASE)),
    ("paradigm shift", re.compile(r"\bparadigm shifts?\b", re.IGNORECASE)),
    ("the future is here", re.compile(r"\bthe future is here\b", re.IGNORECASE)),
]

CASHTAG_RE = re.compile(r"\$[A-Z]{1,5}\b")
EXCHANGE_PAREN_RE = re.compile(r"\((?:NASDAQ|NYSE|Nasdaq|Nyse)\s*:\s*[A-Z][A-Z0-9.]*\)")
TICKER_PAREN_RE = re.compile(r"\(([A-Z]{2,5})\)")
SIGNOFF_RE = re.compile(r"(?<!\S)" + re.escape(SIGNOFF_TEXT))

SUBTITLE_MARKER_RE = re.compile(r"^\s*#?\s*Subtitle\b[^:]*:\s*(.*)$", re.IGNORECASE)
SEO_TITLE_RE = re.compile(r"^\s*SEO title\s*(?:\([^)]*\)\s*)?:\s*(.+?)\s*$")
SEO_DESC_RE = re.compile(r"^\s*SEO description\s*(?:\([^)]*\)\s*)?:\s*(.+?)\s*$")


def shorten(text, limit=100):
    text = text.strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def is_prep_line(line):
    return line.lstrip().startswith("#")


def lint_lines(path, lines, kind):
    """Return a list of (path, line_no, rule, offending_text)."""
    violations = []

    for idx, line in enumerate(lines):
        lineno = idx + 1
        if is_prep_line(line):
            continue
        for match in re.finditer(re.escape(EM_DASH_CHAR), line):
            violations.append((path, lineno, "EM_DASH", shorten(line)))
        for regex in (CASHTAG_RE, EXCHANGE_PAREN_RE, TICKER_PAREN_RE):
            for match in regex.finditer(line):
                violations.append((path, lineno, "TICKER", match.group(0)))
        for _name, regex in HYPE_PATTERNS:
            for match in regex.finditer(line):
                violations.append((path, lineno, "HYPE", match.group(0)))

    # SUBTITLE_LEN: the marked subtitle (inline after the marker's colon,
    # or the next non-blank line with its '#' stripped).
    for idx, line in enumerate(lines):
        marker = SUBTITLE_MARKER_RE.match(line)
        if not marker:
            continue
        text = marker.group(1).strip()
        text_lineno = idx + 1
        if not text:
            for j in range(idx + 1, len(lines)):
                nxt = lines[j].strip()
                if nxt:
                    text = nxt[1:].strip() if nxt.startswith("#") else nxt
                    text_lineno = j + 1
                    break
        if text and len(text) > SUBTITLE_MAX:
            violations.append(
                (path, text_lineno, "SUBTITLE_LEN",
                 "%d chars (max %d): %s" % (len(text), SUBTITLE_MAX, shorten(text)))
            )
        break

    # SEO_LEN: the SEO block lines, text after the label's colon.
    for idx, line in enumerate(lines):
        for regex, label, limit in (
            (SEO_TITLE_RE, "SEO title", SEO_TITLE_MAX),
            (SEO_DESC_RE, "SEO description", SEO_DESC_MAX),
        ):
            match = regex.match(line)
            if match:
                text = match.group(1)
                if len(text) > limit:
                    violations.append(
                        (path, idx + 1, "SEO_LEN",
                         "%s is %d chars (max %d): %s"
                         % (label, len(text), limit, shorten(text)))
                    )

    # SIGNOFF: articles/threads must carry the exact sign-off; comments exempt.
    # Narration scripts (kind="script") carry the sign-off phonetically for
    # the TTS render - the written "- That70s Da." must never appear in a
    # script, so it must not be required there.
    if kind == "script":
        if not any(SCRIPT_SIGNOFF_TEXT in line for line in lines):
            violations.append(
                (path, max(len(lines), 1), "SCRIPT_SIGNOFF",
                 "missing phonetic sign-off '%s'" % SCRIPT_SIGNOFF_TEXT)
            )
    elif kind == "article":
        if not any(SIGNOFF_RE.search(line) for line in lines):
            violations.append(
                (path, max(len(lines), 1), "SIGNOFF",
                 "missing exact sign-off '%s'" % SIGNOFF_TEXT)
            )

    violations.sort(key=lambda v: v[1])
    return violations


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Lint persona post drafts against the Socialy.INK rules "
                    "(POLICY.md, persona directive, SPEC-studio.md).",
    )
    parser.add_argument("files", nargs="+", metavar="FILE",
                        help="draft files (markdown or plain text) to lint")
    parser.add_argument("--kind", choices=("article", "comment", "script"),
                        default="article",
                        help="draft kind: 'article' (default) requires the exact "
                             "sign-off; 'comment' drafts are exempt from it; "
                             "'script' narration scripts carry the sign-off "
                             "phonetically ('That seventies day')")
    args = parser.parse_args(argv)

    all_violations = []
    for path in args.files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError as exc:
            print("%s: ERROR: %s" % (path, exc), file=sys.stderr)
            all_violations.append((path, 0, "READ_ERROR", str(exc)))
            continue
        found = lint_lines(path, lines, args.kind)
        if found:
            print("%s:" % path)
            for _p, lineno, rule, text in found:
                print("  line %d: %s: %s" % (lineno, rule, text))
        else:
            print("%s: clean" % path)
        all_violations.extend(found)

    counts = Counter(rule for _p, _l, rule, _t in all_violations)
    by_rule = ", ".join("%s: %d" % (rule, counts[rule]) for rule in sorted(counts))
    print("Summary: %d file(s) checked, %d violation(s)%s"
          % (len(args.files), len(all_violations),
             (" (%s)" % by_rule) if by_rule else ""))
    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
