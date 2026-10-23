#!/usr/bin/env python3
"""socialy_runlog.py - Socialy.INK run-log validator (Phase 4, tool 3).

Validates run-log files against the schema and failure taxonomy in
SPEC-run-log.md. Standard library only.

Usage:
    python3 socialy_runlog.py [--spec SPEC_RUN_LOG_MD] FILE [FILE ...]

The taxonomy code list is extracted from SPEC-run-log.md section 2 at
run time (the bold code entries), never hardcoded here, so the validator
cannot drift from the spec. --spec defaults to the SPEC-run-log.md in
the repo root, resolved relative to this script.

Log format contract (the encodings this validator reads):

- Header: a fenced ```yaml block (or --- frontmatter) carrying the
  spec's fields: run_id (YYYYMMDD-<kind>-<seq>), date, kind, channels,
  operator, config_ref, status, totals, failure_tally. Values use the
  spec's flow style: [a, b] lists and {k: v} maps.
- Action rows: a markdown table whose header row names the spec's
  fields (id, channel, target, action, locator, verification, outcome,
  notes). The six outcome-relevant fields (channel, target, action,
  locator, verification, outcome) must be present and non-empty in
  every row; notes is enforced where the outcome grammar requires it.

Checks (rule names as printed):

- HEADER - header absent or unparseable; a required field missing;
  run_id not in the SPEC format, or its date/kind disagreeing with the
  date/kind fields; kind or status outside the spec's vocabularies;
  channels not a non-empty list; totals/failure_tally malformed.
- ROW - an action row with an empty required field, or no action rows
  found in the file at all.
- OUTCOME - an outcome string outside the spec's grammar (success,
  skipped_policy, failed:<CODE>, blocked:<CODE>, parked:<CODE>); a
  code-carrying outcome with no code; success carrying a code; a
  skipped_policy that names no policy rule (no qualifier, empty notes).
- VERIF_NONE - verification "none" paired with a success outcome (the
  spec's hard rule: nothing ships unverified).
- CODE - a failed/blocked/parked outcome whose code is not in the
  taxonomy; UNCLASSIFIED used with blocked/parked (the spec allows it
  only as failed:UNCLASSIFIED), or failed:UNCLASSIFIED without the
  full description the spec requires in notes.
- TALLY - the header failure_tally does not match the codes actually
  used in the action rows.

Exit code: 0 when every file conforms, 1 when any violation is found.
"""

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

KINDS = ("engagement", "publishing", "production")
STATUSES = ("completed", "partial", "blocked", "aborted")
TOTALS_KEYS = ("attempted", "succeeded", "skipped_policy", "failed", "parked")
ROW_FIELDS = ("channel", "target", "action", "locator", "verification", "outcome")
HEADER_FIELDS = ("run_id", "date", "kind", "channels", "operator",
                 "config_ref", "status", "totals", "failure_tally")

RUN_ID_RE = re.compile(
    r"^(\d{4})(\d{2})(\d{2})-(engagement|publishing|production)-(\d{2,})$")
OUTCOME_RE = re.compile(
    r"^(success|skipped_policy|failed|blocked|parked)"
    r"(?::([A-Z][A-Z0-9-]*))?(\s.*)?$")
CODE_ENTRY_RE = re.compile(r"^\*\*([A-Z][A-Z0-9-]*)\*\*")


def shorten(text, limit=100):
    text = text.strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


# ---------------------------------------------------------------- spec

def load_taxonomy(spec_path):
    """Extract the taxonomy codes from SPEC-run-log.md section 2.

    Codes are the bold entry heads (`**GATE-CODE** - ...`) between the
    section 2 and section 3 headings. UNCLASSIFIED is deliberately not
    a taxonomy code: the spec defines it in section 3 as an escape
    hatch for failures that match no code, and the validator handles
    it as a special case.
    """
    text = Path(spec_path).read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    start = end = None
    for idx, line in enumerate(lines):
        if line.startswith("## 2."):
            start = idx
        elif start is not None and line.startswith("## 3."):
            end = idx
            break
    if start is None:
        raise ValueError("no '## 2.' taxonomy section in %s" % spec_path)
    codes = []
    for line in lines[start:end]:
        match = CODE_ENTRY_RE.match(line)
        if match:
            codes.append(match.group(1))
    if not codes:
        raise ValueError("no taxonomy codes found in %s section 2" % spec_path)
    return codes


# ------------------------------------------------------------- parsing

def _scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _flow_value(value):
    """Parse the header's flow style: [a, b] lists, {k: v} maps, scalars."""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part) for part in inner.split(",")]
    if value.startswith("{") and value.endswith("}"):
        inner = value[1:-1].strip()
        result = {}
        if inner:
            for part in inner.split(","):
                key, sep, val = part.partition(":")
                if not sep:
                    raise ValueError("malformed flow map entry: %r" % part)
                result[key.strip()] = _scalar(val)
        return result
    return _scalar(value)


def parse_header(lines):
    """Return (header dict, first line no) or (None, None) if absent.

    Raises ValueError when a block that looks like the header cannot
    be parsed.
    """
    block = None  # (list of (lineno, text), first lineno)
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                block = ([(i + 1, lines[i]) for i in range(1, idx)], 1)
                break
    if block is None:
        idx = 0
        while idx < len(lines):
            if lines[idx].strip().lower() in ("```yaml", "```yml"):
                body = []
                j = idx + 1
                while j < len(lines) and lines[j].strip() != "```":
                    body.append((j + 1, lines[j]))
                    j += 1
                if any(text.lstrip().startswith("run_id:") for _n, text in body):
                    block = (body, idx + 1)
                    break
                idx = j
            idx += 1
    if block is None:
        return None, None
    body, first_lineno = block
    header = {}
    for lineno, raw in body:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep or not key.strip():
            raise ValueError("header line %d is not 'key: value': %r"
                             % (lineno, raw))
        value = re.split(r"\s+#", value, maxsplit=1)[0]
        header[key.strip()] = _flow_value(value)
    return header, first_lineno


def _cells(line):
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def _norm_name(cell):
    return re.sub(r"[\s_]+", "", cell.lower())


_FIELD_ALIASES = {
    "id": "id",
    "channel": "channel",
    "target": "target",
    "action": "action",
    "locator": "locator",
    "verification": "verification",
    "verificationmethod": "verification",
    "outcome": "outcome",
    "notes": "notes",
}


def parse_rows(lines):
    """Collect action rows from markdown tables naming the spec fields."""
    rows = []
    idx = 0
    while idx < len(lines):
        if lines[idx].lstrip().startswith("|"):
            header_cells = [_FIELD_ALIASES.get(_norm_name(c))
                            for c in _cells(lines[idx])]
            if (None not in header_cells
                    and all(f in header_cells for f in ROW_FIELDS)):
                columns = header_cells
                idx += 1
                while idx < len(lines) and lines[idx].lstrip().startswith("|"):
                    cells = _cells(lines[idx])
                    if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                        idx += 1
                        continue
                    row = {"_lineno": idx + 1}
                    for pos, field in enumerate(columns):
                        row[field] = cells[pos] if pos < len(cells) else ""
                    rows.append(row)
                    idx += 1
                continue
        idx += 1
    return rows


# ---------------------------------------------------------- validation

def _as_int(value):
    if isinstance(value, str) and re.fullmatch(r"-?\d+", value.strip()):
        return int(value)
    return None


def validate(path, lines, taxonomy):
    """Return a list of (path, line_no, rule, message)."""
    violations = []

    def add(lineno, rule, message):
        violations.append((path, lineno, rule, message))

    # ---- header ------------------------------------------------------------
    header = None
    header_lineno = 1
    try:
        header, header_lineno = parse_header(lines)
    except ValueError as exc:
        add(1, "HEADER", "run header unparseable: %s" % exc)
    if header is None and not violations:
        add(1, "HEADER",
            "no run header found (expected a fenced yaml block or "
            "frontmatter carrying run_id)")

    if header is not None:
        for field in HEADER_FIELDS:
            if field not in header:
                add(header_lineno, "HEADER",
                    "required header field missing: %s" % field)

        run_id = header.get("run_id")
        run_date = run_kind = None
        if isinstance(run_id, str):
            match = RUN_ID_RE.match(run_id)
            if not match:
                add(header_lineno, "HEADER",
                    "run_id %r is not in the SPEC format "
                    "YYYYMMDD-<kind>-<seq>" % run_id)
            else:
                try:
                    run_date = date(int(match.group(1)), int(match.group(2)),
                                    int(match.group(3)))
                except ValueError:
                    add(header_lineno, "HEADER",
                        "run_id %r carries an invalid date" % run_id)
                run_kind = match.group(4)
        elif run_id is not None:
            add(header_lineno, "HEADER", "run_id is not a scalar: %r" % (run_id,))

        date_field = header.get("date")
        if isinstance(date_field, str):
            try:
                parsed = date.fromisoformat(date_field)
            except ValueError:
                add(header_lineno, "HEADER",
                    "date %r is not an ISO local date" % date_field)
            else:
                if run_date is not None and parsed != run_date:
                    add(header_lineno, "HEADER",
                        "date %s disagrees with run_id date %s"
                        % (date_field, run_date.isoformat()))
        kind_field = header.get("kind")
        if kind_field is not None:
            if kind_field not in KINDS:
                add(header_lineno, "HEADER",
                    "kind %r is not one of %s" % (kind_field, "/".join(KINDS)))
            elif run_kind is not None and kind_field != run_kind:
                add(header_lineno, "HEADER",
                    "kind %r disagrees with run_id kind %r"
                    % (kind_field, run_kind))
        channels = header.get("channels")
        if channels is not None and (
                not isinstance(channels, list) or not channels):
            add(header_lineno, "HEADER",
                "channels is not a non-empty list: %r" % (channels,))
        status = header.get("status")
        if status is not None and status not in STATUSES:
            add(header_lineno, "HEADER",
                "status %r is not one of %s" % (status, "/".join(STATUSES)))
        totals = header.get("totals")
        if totals is not None:
            if not isinstance(totals, dict):
                add(header_lineno, "HEADER",
                    "totals is not a flow map: %r" % (totals,))
            else:
                for key in TOTALS_KEYS:
                    if key not in totals:
                        add(header_lineno, "HEADER",
                            "totals is missing key: %s" % key)
                    elif _as_int(totals[key]) is None:
                        add(header_lineno, "HEADER",
                            "totals.%s is not an integer: %r"
                            % (key, totals[key]))
        tally = header.get("failure_tally")
        if tally is not None:
            if not isinstance(tally, dict):
                add(header_lineno, "HEADER",
                    "failure_tally is not a flow map: %r" % (tally,))
            else:
                for code, count in tally.items():
                    if _as_int(count) is None:
                        add(header_lineno, "HEADER",
                            "failure_tally[%s] is not an integer: %r"
                            % (code, count))

    # ---- action rows ---------------------------------------------------------
    rows = parse_rows(lines)
    if not rows:
        add(1, "ROW",
            "no action rows found (expected a markdown table naming the "
            "spec's fields: %s)" % ", ".join(ROW_FIELDS))
    row_codes = Counter()
    for pos, row in enumerate(rows):
        lineno = row["_lineno"]
        label = row.get("id") or "row %d" % (pos + 1)
        for field in ROW_FIELDS:
            if not row.get(field):
                add(lineno, "ROW",
                    "%s: required field is empty: %s" % (label, field))
        outcome_text = row.get("outcome", "")
        if not outcome_text:
            continue
        match = OUTCOME_RE.match(outcome_text)
        if not match:
            add(lineno, "OUTCOME",
                "%s: outcome %r is outside the spec's grammar (success | "
                "skipped_policy | failed:<CODE> | blocked:<CODE> | "
                "parked:<CODE>)" % (label, shorten(outcome_text)))
            continue
        word, code = match.group(1), match.group(2)
        verification = row.get("verification", "")
        method = re.split(r"[\s+,]+", verification.strip())[0].lower() \
            if verification.strip() else ""
        if word == "success":
            if code:
                add(lineno, "OUTCOME",
                    "%s: success outcome carries a code: %r"
                    % (label, outcome_text))
            if method == "none":
                add(lineno, "VERIF_NONE",
                    "%s: verification 'none' paired with success - nothing "
                    "ships unverified (SPEC-run-log.md section 1)"
                    % label)
        elif word == "skipped_policy":
            if not code and not row.get("notes"):
                add(lineno, "OUTCOME",
                    "%s: skipped_policy names no policy rule (no qualifier "
                    "on the outcome and notes is empty)" % label)
        else:  # failed | blocked | parked
            if not code:
                add(lineno, "OUTCOME",
                    "%s: %s outcome carries no taxonomy code: %r"
                    % (label, word, outcome_text))
                continue
            row_codes[code] += 1
            if code == "UNCLASSIFIED":
                if word != "failed":
                    add(lineno, "CODE",
                        "%s: UNCLASSIFIED is allowed only as "
                        "failed:UNCLASSIFIED (spec section 3), not %s:"
                        % (label, word))
                elif not row.get("notes"):
                    add(lineno, "CODE",
                        "%s: failed:UNCLASSIFIED without the full "
                        "description the spec requires in notes" % label)
            elif code not in taxonomy:
                add(lineno, "CODE",
                    "%s: unknown taxonomy code %s (not defined in "
                    "SPEC-run-log.md section 2)" % (label, code))

    # ---- failure_tally vs rows ----------------------------------------------
    if header is not None and isinstance(header.get("failure_tally"), dict):
        tally = {code: _as_int(count)
                 for code, count in header["failure_tally"].items()}
        if all(v is not None for v in tally.values()):
            for code in sorted(set(tally) | set(row_codes)):
                in_tally = tally.get(code, 0)
                in_rows = row_codes.get(code, 0)
                if in_tally != in_rows:
                    add(header_lineno, "TALLY",
                        "failure_tally[%s] = %d but the action rows use "
                        "it %d time(s)" % (code, in_tally, in_rows))

    violations.sort(key=lambda v: v[1])
    return violations


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate run-log files against the SPEC-run-log.md "
                    "schema and failure taxonomy.")
    parser.add_argument("files", nargs="+", metavar="FILE",
                        help="run-log files (markdown) to validate")
    parser.add_argument("--spec", default=None,
                        help="path to SPEC-run-log.md (default: the one in "
                             "the repo root, relative to this script)")
    args = parser.parse_args(argv)

    spec_path = args.spec or str(
        Path(__file__).resolve().parent.parent / "SPEC-run-log.md")
    try:
        taxonomy = load_taxonomy(spec_path)
    except (OSError, ValueError) as exc:
        print("ERROR: cannot load taxonomy: %s" % exc, file=sys.stderr)
        return 1
    print("Taxonomy: %d codes loaded from %s"
          % (len(taxonomy), spec_path))

    all_violations = []
    for path in args.files:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError as exc:
            print("%s: ERROR: %s" % (path, exc), file=sys.stderr)
            all_violations.append((path, 0, "READ_ERROR", str(exc)))
            continue
        found = validate(path, lines, set(taxonomy))
        if found:
            print("%s:" % path)
            for _p, lineno, rule, text in found:
                print("  line %d: %s: %s" % (lineno, rule, text))
        else:
            print("%s: conforms" % path)
        all_violations.extend(found)

    counts = Counter(rule for _p, _l, rule, _t in all_violations)
    by_rule = ", ".join("%s: %d" % (rule, counts[rule]) for rule in sorted(counts))
    print("Summary: %d file(s) checked, %d violation(s)%s"
          % (len(args.files), len(all_violations),
             (" (%s)" % by_rule) if by_rule else ""))
    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
