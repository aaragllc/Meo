# Socialy.INK tools - the Phase 4 toolkit

Phase 4 ("make it code") turns the platform's deterministic written rules
into a small, tested, dependency-free local toolkit that runs anywhere -
including fully offline, with no agent account. Python 3 standard library
only.

## Tools

### 1. socialy_lint.py - the draft linter (DONE)

The policy gate as code. Lints persona post drafts (markdown or plain
text) against POLICY.md, the persona directive, and SPEC-studio.md:

```
python3 tools/socialy_lint.py [--kind article|comment] FILE [FILE ...]
```

Exit 0 = clean, 1 = violations found. Each violation is reported with
file, line number, rule name, and the offending text, followed by a
summary line.

| Rule | What it catches | Source |
|---|---|---|
| EM_DASH | the em dash character anywhere in body text (use " - ") | POLICY.md, Voice |
| TICKER | cashtags ($SPCX) and ticker parentheticals - (CRWV), (NASDAQ: X), (NYSE: X) | POLICY.md, Hard bans ("companies are named, not tickered") |
| HYPE | revolutionary, game-changer, disrupt (incl. inflections), paradigm shift, "the future is here" | POLICY.md, Hard bans; directive section 1 (identical list) |
| SIGNOFF | article/thread drafts missing the exact sign-off "- That70s Da." (comments exempt via --kind comment) | standing sign-off rule |
| SUBTITLE_LEN | a marked subtitle over 200 characters | SPEC-studio.md C1 |
| SEO_LEN | SEO title over 60 chars or SEO description over 160 in the SEO block | standing SEO rule (adopted 2026-10-22; not in SPEC-studio.md - see below) |

Prep-file convention: lines starting with '#' are prep/metadata comments,
not post text, so the content rules (EM_DASH, TICKER, HYPE) skip them -
a note like "(CRWV) stripped" in a humanize header is not a violation.
The structural rules read their marked lines directly (the "Subtitle:"
marker line plus the following line; the "SEO title"/"SEO description"
lines), and SIGNOFF searches the whole file.

Tested 2026-10-22: the three prepped weekend posts (P2, P3, P4 humanized
files) lint clean; a synthetic dirty draft in /tmp fired all six rules.

### 2. socialy_parity.py - the parity checker (DONE)

Mechanizes SPEC-parity-audit.md. Reads the machine-readable catalogue
(`personas/that70sda/catalogue.yaml`, transcribed faithfully from
parity-audit-2026-10-22.md) and prints the parity table (piece x surface,
using the audit's OK / MISS / NR / EXC / n/a codes), the headline counts,
and the computed gap register:

```
python3 tools/socialy_parity.py [CATALOGUE]
```

CATALOGUE defaults to the that70sda catalogue, resolved relative to the
script. The catalogue uses a restricted YAML subset (flat records, plain
scalars), parsed by a small stdlib parser in the tool, so the toolkit
stays dependency-free; the file is also valid YAML for other consumers.

Exit code semantics - the regression signal for future audits:

- **0** - the computed gap register matches audit #1's baseline register
  (or baseline gaps have only closed since), and every accepted
  exception is in the registered set.
- **1** - a NEW gap or an UNREGISTERED exception (something audit #1
  does not have), or malformed catalogue data.

Transcription notes (fidelity to audit #1 over live truth):

- The five earliest articles' X threads are `no-record` exactly as audit
  #1 records them (its register item 1, disposition VERIFY at audit #2),
  even where other run notes mention thread URLs - the catalogue is the
  audit's state, not a re-audit.
- Audit #1's YouTube headline (18/18) spans three episodes (EP1, EP6,
  EP7) whose source posts are not among its 15 tabled articles. They are
  carried in the catalogue's `additional_audio` block so the count
  reproduces exactly without inventing article rows.
- Audit register items 2 (LinkedIn listen lines) and 3 (episode ->
  article description links) concern surfaces the catalogue has no field
  for; they stay prose-only in the audit files.

Tested 2026-10-22: the shipped catalogue reproduces audit #1 exactly -
16 pieces, article -> episode 14/14, YouTube 18/18, LinkedIn 15/15, X
recorded 10/15, listen links 7 present + 7 EXC, gap register = audit
items 1 and 4, exit 0. A /tmp copy with one YouTube id removed flips
that cell to MISS, drops the count to 17/18, flags a NEW GAP, exit 1.

### 3. Run-log validator (planned)

Validates run logs under logs/ against the SPEC-run-log.md schema and
failure taxonomy (required header fields, known codes only, no
`verification: none` paired with `success`).

### 4. BOOTSTRAP wiring (planned)

A single entry point that runs the toolkit's checks in order for the
offline route, so a fresh environment verifies itself with no agent
account involved.

## Known ambiguities in the rule sources

- The directive (verbatim, 2026-10-14) says to sign posts "— That70s Da."
  with an em dash; the standing written sign-off, which the linter
  enforces, is "- That70s Da." (spaced hyphen, per the em dash ban).
- The SEO length caps (title 60, description 160) come from the standing
  SEO rule recorded 2026-10-22, not from SPEC-studio.md, which caps only
  subtitles (C1). If the caps move into the studio spec, this table
  should point there instead.
