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

### 3. socialy_runlog.py - the run-log validator (DONE)

Validates run-log files against the schema and failure taxonomy in
SPEC-run-log.md:

```
python3 tools/socialy_runlog.py [--spec SPEC_RUN_LOG_MD] FILE [FILE ...]
```

The taxonomy code list is extracted from SPEC-run-log.md section 2 at
run time (13 codes today), never hardcoded in the tool, so the
validator cannot drift from the spec. --spec defaults to the repo's
SPEC-run-log.md, resolved relative to the script, so the tool runs
from any working directory.

Format contract (the encodings the validator reads): the run header is
a fenced ```yaml block (or --- frontmatter) carrying the spec's fields
in its flow style ([a, b] lists, {k: v} maps); action rows are a
markdown table whose header row names the spec's fields (id, channel,
target, action, locator, verification, outcome, notes).

Exit 0 = every file conforms, 1 = any violation. Checks, by rule name:

| Rule | What it catches |
|---|---|
| HEADER | header absent/unparseable; a required field missing (run_id, date, kind, channels, operator, config_ref, status, totals, failure_tally); run_id outside the YYYYMMDD-<kind>-<seq> format or disagreeing with the date/kind fields; kind/status outside the spec's vocabularies; malformed totals/failure_tally |
| ROW | an action row with an empty required field (channel, target, action, locator, verification, outcome), or no action rows in the file |
| OUTCOME | an outcome outside the spec's grammar; a failed/blocked/parked outcome with no code; success carrying a code; skipped_policy naming no policy rule |
| VERIF_NONE | `verification: none` paired with `success` - the spec's hard rule, nothing ships unverified |
| CODE | a code not defined in the taxonomy; UNCLASSIFIED used as blocked:/parked: (the spec allows only failed:UNCLASSIFIED), or failed:UNCLASSIFIED without the full description the spec requires in notes |
| TALLY | the header failure_tally disagrees with the codes actually used in the action rows |

One reading of check 4 worth recording: `skipped_policy` is a
non-success outcome that names a policy rule rather than a taxonomy
code - that is the spec's own grammar (section 1), so the validator
requires the rule to be named (outcome qualifier or notes) instead of
demanding a code there.

Tested 2026-10-23 (fixtures in /tmp/runlog-fixtures, not shipped): a
fully conforming sample log exits 0; five broken variants - bad
header, empty row field, verification-none success, unknown code +
UNCLASSIFIED-without-notes, tally mismatch - are each caught under
exactly their own rule, exit 1.

Legacy finding (reported, NOT fixed - historical logs are never
edited): the canonical logs/ directory holds no run logs yet, and the
two pre-schema prose records - the day-1 engagement log
(goals/that70sda-evangelism-plan/hidden_files/engagement-log-2026-10-22.md)
and the 2026-10-20 post-3 ship record (hidden_files/run-logs/) - both
fail validation (no schema header, no action-row table; exit 1). They
predate the schema, which itself carries them as legacy (SPEC-run-log
section 1); the validator's domain is new runs written to logs/.

### 4. BOOTSTRAP wiring (DONE)

BOOTSTRAP.md carries the toolkit in its transfer inventory, in the
new-account stand-up parity step, and in a "The toolkit in daily
operation" section that states exactly when each tool runs: the linter
on every draft before it ships (nonzero exit blocks the ship), the
parity checker whenever the catalogue changes and at each weekly audit
(a NEW GAP exit means stop and reconcile), and the validator on every
run log before it is filed in `logs/`. All three are stdlib-only, so a
fresh environment - Muse account or fully offline - runs them with no
setup beyond the repo itself.

## Known ambiguities in the rule sources

- The directive (verbatim, 2026-10-14) says to sign posts "— That70s Da."
  with an em dash; the standing written sign-off, which the linter
  enforces, is "- That70s Da." (spaced hyphen, per the em dash ban).
- The SEO length caps (title 60, description 160) come from the standing
  SEO rule recorded 2026-10-22, not from SPEC-studio.md, which caps only
  subtitles (C1). If the caps move into the studio spec, this table
  should point there instead.

- socialy_check.py (Phase 5): the gate runner. `ship FILE...` = pre-ship
  gate (lint + unresolved-placeholder scan + subtitle/SEO presence);
  exit 1 blocks the ship. `state` = platform self-check (parity, run-log
  validation for post-2026-10-23 logs, LESSONS.md coverage of every
  taxonomy code). Run by the daily ops watchdog and the Sunday review.
