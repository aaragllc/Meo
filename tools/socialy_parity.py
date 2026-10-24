#!/usr/bin/env python3
"""socialy_parity.py - Socialy.INK parity checker (Phase 4, tool 2).

Mechanizes SPEC-parity-audit.md: reads the machine-readable catalogue
(personas/that70sda/catalogue.yaml, transcribed from audit #1) and prints
the parity table, headline counts, and the gap register - the surfaces
that are Missing (MISS) or unverifiable (NR, "no record") and NOT covered
by an accepted exception (EXC).

Usage:
    python3 socialy_parity.py [CATALOGUE]

CATALOGUE defaults to personas/that70sda/catalogue.yaml, resolved
relative to this script's location in the repo.

Exit code semantics (the regression signal for future audits):
    0 - the computed gap register matches audit #1's baseline register
        (or baseline gaps have only closed since). Accepted exceptions
        match the registered set.
    1 - a NEW gap or an UNREGISTERED exception was found: something audit
        #1 does not have. Also 1 on malformed catalogue data (unknown
        field values, unreadable file).

"No record" is a finding, not an assumption (SPEC-parity-audit.md): NR
cells are gaps with a VERIFY disposition until a live check confirms the
surface (record updated) or converts it to Missing.

Standard library only. The catalogue uses a restricted YAML subset
(flat records, plain scalars, full-line comments) parsed by the small
parser below, so the tool runs anywhere - including fully offline.
"""

import argparse
import sys
from pathlib import Path

SURFACES = ("article", "episode", "spotify", "youtube", "x_thread",
            "linkedin", "article_listen_link")
SURFACE_LABELS = {
    "article": "Article",
    "episode": "Episode",
    "spotify": "Spotify",
    "youtube": "YouTube",
    "x_thread": "X thread",
    "linkedin": "LinkedIn",
    "article_listen_link": "Listen link",
}

VOCABULARY = {
    "spotify": {"confirmed", "unconfirmed", "n/a"},
    "x_thread": {"no-record", "n/a"},          # or a URL
    "linkedin": {"present", "n/a"},
    "article_listen_link": {"present", "parked-exception", "n/a"},
}

# Audit #1's gap register, in catalogue terms: (piece id, surface, code).
# These are the gaps the 2026-10-22 audit already carries (its register
# items 1 and 4 - the items expressible in this catalogue; items 2, 3 and
# 5 concern surfaces/records outside the catalogue's fields).
BASELINE_GAPS = {
    ("intro", "x_thread", "NR"),
    ("record-high", "x_thread", "NR"),
    ("fridays-alarm", "x_thread", "NR"),
    ("grading", "x_thread", "NR"),
    ("dashboard", "x_thread", "NR"),
    ("yield", "spotify", "NR"),
    ("era-file", "spotify", "NR"),
    ("rotation-p1", "spotify", "NR"),
    # Registered after audit #1, at the rotation-p2 ship (2026-10-23):
    # Spotify unconfirmed in the records is expected RSS lag for the
    # newest episode, already carried as an audit #2 VERIFY item (the
    # audit #2 gap register lists Spotify EP15-EP18 unconfirmed). Same
    # disposition as register item 4; it leaves the register when audit
    # #2 verifies the landing or closes the item.
    ("rotation-p2", "spotify", "NR"),
}

# Audit #1's accepted exceptions in catalogue terms: (piece id, surface).
BASELINE_EXCEPTIONS = {
    ("record-high", "article_listen_link"),
    ("fridays-alarm", "article_listen_link"),
    ("grading", "article_listen_link"),
    ("dashboard", "article_listen_link"),
    ("yield", "article_listen_link"),
    ("era-file", "article_listen_link"),
    ("rotation-p1", "article_listen_link"),
}


def parse_catalogue(text):
    """Parse the restricted YAML subset used by catalogue.yaml.

    Supports: full-line comments, top-level `key: value` scalars, nested
    `key: value` maps (indent 2), and lists of flat records introduced by
    `- ` (indent 2) with `key: value` fields (indent 4, first field may be
    inline after the dash). All values are returned as strings.
    """
    meta = {}
    lists = {}
    section = None      # current top-level key whose value is a block
    section_is_list = False
    current = None      # current record dict inside a list section

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        if indent == 0:
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            current = None
            if value:
                meta[key] = _scalar(value)
                section = None
            else:
                section = key
                section_is_list = False
            continue

        if section is None:
            raise ValueError("indented line outside any section: %r" % raw)

        if line.startswith("- ") or line == "-":
            if not section_is_list:
                lists[section] = []
                section_is_list = True
            current = {}
            lists[section].append(current)
            line = line[1:].strip()
            if not line:
                continue

        if section_is_list:
            if current is None:
                raise ValueError("field line before any record: %r" % raw)
            key, _, value = line.partition(":")
            current[key.strip()] = _scalar(value.strip())
        else:
            # Nested flat map (e.g. exception_provenance).
            nested = meta.setdefault(section, {})
            if not isinstance(nested, dict):
                raise ValueError("conflicting section type: %r" % section)
            key, _, value = line.partition(":")
            nested[key.strip()] = _scalar(value.strip())

    return meta, lists


def _scalar(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def cell_code(piece, surface):
    """Derive the audit cell code (OK / MISS / NR / EXC / n/a) for a surface."""
    value = piece.get(surface, "")
    has_episode = piece.get("episode", "n/a") != "n/a"
    if surface == "article":
        return "OK" if value.startswith("http") else "MISS"
    if surface == "episode":
        if value != "n/a":
            return "OK"
        # An episode is expected for every article except the intro.
        if piece.get("kind") == "article" and piece.get("id") != "intro":
            return "MISS"
        return "n/a"
    if surface == "spotify":
        return {"confirmed": "OK", "unconfirmed": "NR", "n/a": "n/a"}[value]
    if surface == "youtube":
        if value != "n/a":
            return "OK"
        # A video is expected whenever the piece has audio (an episode,
        # or the trailer itself).
        if has_episode or piece.get("kind") == "trailer":
            return "MISS"
        return "n/a"
    if surface == "x_thread":
        if value == "n/a":
            return "n/a"
        return "NR" if value == "no-record" else "OK"
    if surface == "linkedin":
        return {"present": "OK", "n/a": "n/a"}[value]
    if surface == "article_listen_link":
        if value == "present":
            return "OK"
        if value == "parked-exception":
            return "EXC"
        # n/a: only truly not applicable when there is no episode.
        return "MISS" if has_episode else "n/a"
    raise KeyError(surface)


def validate(pieces):
    """Return a list of data errors (unknown values, duplicates, gaps in
    the record structure) that make the catalogue uninterpretable."""
    errors = []
    seen = set()
    for piece in pieces:
        pid = piece.get("id", "?")
        if pid in seen:
            errors.append("%s: duplicate piece id" % pid)
        seen.add(pid)
        for field in ("id", "title", "kind") + SURFACES:
            if field not in piece:
                errors.append("%s: missing field %r" % (pid, field))
        for field, allowed in VOCABULARY.items():
            value = piece.get(field, "")
            if value not in allowed and not value.startswith("http"):
                errors.append("%s: %s has unknown value %r" % (pid, field, value))
    return errors


def headline_counts(pieces, additional_audio):
    """Reproduce audit #1's headline counts from the catalogue records."""
    articles = [p for p in pieces if p["kind"] == "article"]
    with_episode = [p for p in articles if p["episode"] != "n/a"]
    youtube_in_catalogue = sum(
        1 for p in pieces if p["youtube"] != "n/a")
    youtube_total = youtube_in_catalogue + len(additional_audio)
    audio_total = len(pieces) - 1 + len(additional_audio)  # minus intro (no audio)
    x_recorded = sum(1 for p in articles if p["x_thread"] not in ("n/a", "no-record"))
    listen_present = sum(
        1 for p in pieces if p["article_listen_link"] == "present")
    listen_exc = sum(
        1 for p in pieces if p["article_listen_link"] == "parked-exception")
    spotify_confirmed = sum(1 for p in pieces if p["spotify"] == "confirmed")
    spotify_unconfirmed = sum(1 for p in pieces if p["spotify"] == "unconfirmed")
    return [
        "Pieces checked: %d (%d articles + trailer)" % (len(pieces), len(articles)),
        "Article -> episode: %d of %d applicable" % (
            len(with_episode),
            len([p for p in articles if p["id"] != "intro"])),
        "YouTube: %d of %d audio pieces (%d in catalogue + %d audit-context "
        "episodes)" % (youtube_total, audio_total, youtube_in_catalogue,
                       len(additional_audio)),
        "LinkedIn overview posts: %d of %d articles" % (
            sum(1 for p in articles if p["linkedin"] == "present"),
            len(articles)),
        "X threads: recorded for %d of %d articles; no record for %d" % (
            x_recorded, len(articles), len(articles) - x_recorded),
        "Article -> episode listen links: %d present; %d parked "
        "(accepted exceptions)" % (listen_present, listen_exc),
        "Spotify: %d confirmed; %d unconfirmed in the records" % (
            spotify_confirmed, spotify_unconfirmed),
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check the that70sda catalogue against SPEC-parity-audit.md "
                    "and audit #1's baseline gap register.",
        epilog="Exit 0: gap register matches audit #1's baseline (or has only "
               "closed since) and exceptions match the registered set. "
               "Exit 1: a NEW gap or UNREGISTERED exception - the regression "
               "signal for future audits - or malformed catalogue data.",
    )
    default_catalogue = (Path(__file__).resolve().parent.parent
                         / "personas" / "that70sda" / "catalogue.yaml")
    parser.add_argument("catalogue", nargs="?", default=str(default_catalogue),
                        help="catalogue YAML (default: %(default)s)")
    args = parser.parse_args(argv)

    try:
        text = Path(args.catalogue).read_text(encoding="utf-8")
        _meta, lists = parse_catalogue(text)
    except (OSError, ValueError) as exc:
        print("%s: ERROR: %s" % (args.catalogue, exc), file=sys.stderr)
        return 1
    pieces = lists.get("pieces", [])
    additional_audio = lists.get("additional_audio", [])

    errors = validate(pieces)
    if errors:
        for error in errors:
            print("ERROR: %s" % error)
        print("Summary: catalogue invalid (%d error(s))" % len(errors))
        return 1

    # Parity table.
    table = {}
    for piece in pieces:
        table[piece["id"]] = {s: cell_code(piece, s) for s in SURFACES}
    label = {}
    for piece in pieces:
        suffix = "" if piece["episode_no"] in ("none", "trailer") \
            else " (%s)" % piece["episode_no"]
        label[piece["id"]] = piece["title"] + suffix
    width = max(len(v) for v in label.values())
    col = 6
    header = "%-*s" % (width, "Piece") + "".join(
        " %-*s" % (col, SURFACE_LABELS[s]) for s in SURFACES)
    print(header)
    print("-" * len(header))
    for piece in pieces:
        row = table[piece["id"]]
        print("%-*s" % (width, label[piece["id"]]) + "".join(
            " %-*s" % (col, row[s]) for s in SURFACES))
    print()

    # Headline counts.
    print("Headline counts:")
    for line in headline_counts(pieces, additional_audio):
        print("- %s" % line)
    print()

    # Gap register: NR / MISS cells not covered by an accepted exception.
    gaps = {(p["id"], s, table[p["id"]][s])
            for p in pieces for s in SURFACES
            if table[p["id"]][s] in ("NR", "MISS")}
    exceptions = {(p["id"], s)
                  for p in pieces for s in SURFACES
                  if table[p["id"]][s] == "EXC"}
    new_gaps = gaps - BASELINE_GAPS
    closed_gaps = BASELINE_GAPS - gaps
    new_exceptions = exceptions - BASELINE_EXCEPTIONS

    print("Gap register (computed):")
    x_nr = sorted(pid for pid, s, _c in gaps if s == "x_thread")
    sp_nr = sorted(pid for pid, s, _c in gaps if s == "spotify")
    other = sorted(g for g in gaps if g[1] not in ("x_thread", "spotify"))
    if x_nr:
        print("- X thread, no record (%d): %s [audit #1 register item 1 - "
              "VERIFY at audit #2]" % (len(x_nr), ", ".join(x_nr)))
    if sp_nr:
        print("- Spotify, unconfirmed in records (%d): %s [audit #1 register "
              "item 4 - VERIFY at audit #2]" % (len(sp_nr), ", ".join(sp_nr)))
    for pid, surface, code in other:
        print("- %s: %s is %s" % (pid, SURFACE_LABELS[surface], code))
    if not gaps:
        print("- (none)")
    if closed_gaps:
        print("Baseline gaps closed since audit #1: %d (%s)"
              % (len(closed_gaps),
                 ", ".join("%s/%s" % (g[0], g[1])
                           for g in sorted(closed_gaps))))

    findings = []
    for pid, surface, code in sorted(new_gaps):
        findings.append("NEW GAP: %s: %s is %s - not in audit #1's register"
                        % (pid, SURFACE_LABELS[surface], code))
    for pid, surface in sorted(new_exceptions):
        findings.append("UNREGISTERED EXCEPTION: %s: %s - absent under no "
                        "registered decision" % (pid, SURFACE_LABELS[surface]))
    for finding in findings:
        print(finding)

    print("Summary: %d piece(s) checked, %d gap(s) (%d new), %d accepted "
          "exception(s) (%d unregistered)"
          % (len(pieces), len(gaps), len(new_gaps), len(exceptions),
             len(new_exceptions)))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
