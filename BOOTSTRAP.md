# BOOTSTRAP - continuing Socialy.INK in a new environment

This repo is the complete, self-contained harness for **Socialy.INK**, a
persona-publishing and audience platform. Persona #1 is **that70sda**.
It was built and operated inside one Muse account (operator agent "Meo",
owner Ravi) and is designed to be picked up by a fresh agent - in another
Muse account, or offline (e.g. Claude Code) - with nothing lost except
live sessions and credentials, which are re-established by the steps below.

## What transfers in this repo

- `README.md`, `PLAN.md`, `ROADMAP.md` - what the platform is and where it stands.
- `config.yaml` - operating config (per-channel daily engagement N=5, etc.).
- `POLICY.md` - the engagement policy: 50K-follower ceiling on every channel,
  skip-and-report triggers (press, money/partnership offers, complaints,
  legal/regulatory, identity probing, heated exchanges, personal-finance
  advice), identity protection, human pacing, stop-on-any-platform-warning.
- `RUNBOOK.md` - how a day runs.
- `SPEC-foundation-adapters.md`, `SPEC-pipelines.md` - Phase 1 specs (accepted v1).
- `SPEC-studio.md` - the production studio standard, FROZEN v1.
- `SPEC-run-log.md` - run-log schema + failure taxonomy (13 codes).
- `SPEC-parity-audit.md` + `parity-audit-2026-10-22.md` - parity definition
  and the first audit snapshot.
- `target-registry.yaml` - every engagement target, channel, and response signal.
- `engagement-run-*.md`, `logs/` - run packs and run logs.
- `personas/that70sda/` - the persona pack:
  - `that70sda-meo-directive.md` - the governing directive (voice, rules,
    escalation triggers, monetization thresholds).
  - `skills/` - the two production skills (publishing, TTS narration).
  - `files/` - LinkedIn post template, welcome-email draft, Stocky calendar prompt.
  - `STATE-2026-10-22.md` - where the operation stands at export.
  - `OPERATING-LESSONS-agents.md` - hard-won platform lessons (Substack
    editor hazards, LinkedIn session rules, pacing). READ THIS before
    touching any platform.
- `crons/` - the two live scheduled jobs (daily engagement run, inbox
  filing) exported as definitions; recreate them in the new environment
  with the same ids, schedules, and bodies.
- `templates/` - the onboarding templates (persona-pack skeleton +
  channel-adapter spec) for adding a persona or channel; see
  `templates/README.md`. `dry-run-*.md` at the root - the most recent
  onboarding dry-run report; read it for the gaps the last fresh-operator
  walk found and how they were closed.
- `tools/` - the Phase 4 toolkit: the platform's deterministic checks as
  runnable code (Python 3, standard library only - no install step).
  `tools/socialy_lint.py` (draft linter: the policy gate as code),
  `tools/socialy_parity.py` (parity checker against
  `personas/that70sda/catalogue.yaml`), `tools/socialy_runlog.py`
  (run-log validator against `SPEC-run-log.md`). See `tools/README.md`
  for each tool's rules and exit codes, and "The toolkit in daily
  operation" below for when each one runs.

## What does NOT transfer (by design)

- **Credentials and sessions.** No passwords, cookies, or tokens are in this
  repo, ever. In the new environment: reconnect Gmail/Calendar/Drive for
  `that70sda@gmail.com` and `entclaw@gmail.com`; save the X and Spotify
  website logins in the new account's secure vault; sign in to LinkedIn
  ONCE by hand (automated password logins trigger a security-check loop -
  see OPERATING-LESSONS) and reuse the warm session.
- **The content catalogue's media.** Published audio/video lives on the
  platforms (Substack, Spotify, YouTube) - they are the masters. Local
  scripts, metadata, and post sources are in the operator's goal workspace
  (`workspace/goals/that70sda-evangelism-plan/hidden_files/`), not in this
  repo; copy `hidden_files/posts/` and `hidden_files/podcast/*/` text files
  across if the new environment should hold production sources too (the
  rendered .mp3/.mp4 files are ~300 MB and re-derivable or downloadable
  from the platforms).
- **The operator's memory.** Distilled into `personas/that70sda/STATE-*.md`
  and the directive; anything else is conversation, not state.

## Standing up in a new Muse account

1. Place this repo at `~/workspace/socialy-ink/`.
2. Install the two skills from `personas/that70sda/skills/` into the new
   environment's custom-skills folder.
3. Reconnect the accounts (above) and recreate the two crons from `crons/`.
   Recreation notes: the exported files are verbatim snapshots of the live
   jobs - their `delivery` chat id and `metadata` (device id, originating
   chat) belong to the OLD environment, so re-point delivery at the new
   main chat (or drop it) and drop the metadata block; the `owner` goal
   slug works only if the goal is recreated under the same slug. The
   inbox-filing job also depends on a processor script that is NOT a
   platform file: it ships in the pack at
   `personas/that70sda/files/inbox_processor.py`. Copy it to a stable path
   (its `state.json` lives beside it - start with an empty state), set the
   Gmail account id at its top to the new environment's id for the persona
   inbox, make sure the host's Gmail CLI path in it matches the new
   environment, and point the recreated job's body at the new path.
4. Read, in order: `POLICY.md`, `personas/that70sda/that70sda-meo-directive.md`,
   `personas/that70sda/OPERATING-LESSONS-agents.md`, `SPEC-studio.md`,
   `personas/that70sda/STATE-*.md` (newest).
5. Verify parity before publishing anything new: read `parity-audit-*.md`
   (newest), then run the toolkit against the shipped state -
   `python3 tools/socialy_parity.py` (exit 0 = the catalogue still
   matches the audit register; exit 1 = a new gap or unregistered
   exception - reconcile against the register before shipping) and
   `python3 tools/socialy_runlog.py <log file>` on any run logs you
   inherit. The full toolkit routine is under "The toolkit in daily
   operation" below.
6. Non-negotiables from day one: never attach the owner's real name,
   employer, or identity to the persona; never mention AI/automation in
   public persona content; no em dash character in persona writing (spaced
   hyphen " - "); every post signs off "- That70s Da."; human pacing with
   randomized timing; stop instantly on any platform warning.

## Standing up offline (coding project)

The repo is plain markdown + YAML - clone it and work. `PLAN.md` and
`ROADMAP.md` carry the phase plan (Phase 2 in progress at export: parity
audit standing, run-log taxonomy adopted, studio frozen; Phase 3 = this
repo's migration to GitHub + adapter/persona-pack templates + onboarding
dry run). The specs are written to be implemented against; the failure
taxonomy in `SPEC-run-log.md` is the test plan's seed list.

## The toolkit in daily operation

The three tools in `tools/` are not optional extras - they are how the
written rules get enforced day to day. All three are Python 3 standard
library only: no install step, no dependencies, which is what makes the
offline route work. Run them from the repo root.

- **Linter - on every post or thread draft, before it ships.**
  `python3 tools/socialy_lint.py <file...>`
  Exit 0 = clean. A nonzero exit BLOCKS the ship: fix the draft (em dash,
  ticker, hype word, missing sign-off, over-length subtitle or SEO
  field) and re-run until it passes. Comments lint with
  `--kind comment` (sign-off exempt).
- **Parity checker - whenever the catalogue changes, and at each weekly
  audit.**
  `python3 tools/socialy_parity.py`
  Exit 0 = the computed gap register matches the audit baseline. A NEW
  GAP exit (1) means stop and reconcile against the audit register
  (`SPEC-parity-audit.md` + the newest `parity-audit-*.md`): either the
  catalogue is wrong, or a surface genuinely regressed and the register
  needs a new entry with a disposition.
- **Run-log validator - on every run log, before it is filed in `logs/`.**
  `python3 tools/socialy_runlog.py <log file>`
  Exit 0 = the log conforms to `SPEC-run-log.md` (header, action rows,
  taxonomy codes, tally). A nonconforming log gets fixed at write time,
  not later - the weekly reporting counts these codes, and a malformed
  log silently corrupts the counts.

## Export provenance

Exported 2026-10-22 from the operating Muse account at the owner's
request, as a git repository (this .git history starts at the export
commit) plus a dated zip archive. Regenerate the archive after any
milestone: `zip -r socialy-harness-<date>.zip socialy-ink -x '*/\.*'` -
or simply push the repo.
