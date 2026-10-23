# Socialy.INK

Ravi's social engagement platform. It industrializes what was built by hand for the
that70sda persona (Oct 2026): daily, in-voice engagement across every supported
channel - comments/replies and, where a channel supports it, follows/connects -
run as a framework instead of one-off manual sessions.

## What it does

- Every day, for each enabled channel: post N comments/replies (default 5,
  configurable per channel) and make N follows/connects (default 5, where the
  channel supports it).
- Targets are found live each run (in-lane conversations from the last ~12-24h),
  drafted in the account's voice, passed through a critique/QC gate, posted with
  human-plausible pacing, verified live, and logged.
- Escalation triggers (see POLICY.md) are never auto-posted: the target is
  skipped, logged, and surfaced in the daily report for a human call.
- Any platform warning, rate limit, CAPTCHA, or verification challenge stops
  that channel's run immediately. Blocks are never circumvented.

## Channels (adapters)

- X - replies + follows. Live since 2026-10-19 (reply-targets runs).
- LinkedIn (company page) - feed comments as the page + page-to-page follows.
  Pages cannot comment inside Groups; the page follows pages only, never people.
- Substack - comments on other publications + free subscribes/follows.
- YouTube - comments on other channels' videos + subscribes.
- Future channels plug in as new adapters with the same engine contract:
  discover -> draft -> critique -> policy gate -> post -> verify -> log.

## Layout

- `config.yaml` - the knobs: N per action per channel, pacing, enabled flags.
- `POLICY.md` - voice rules, banned content, escalation/skip triggers, stop rules.
- `RUNBOOK.md` - the daily run procedure, per channel.
- Runs are executed by the daily scheduled job and reported in chat; per-run
  logs land in `logs/` in this repo (see SPEC-run-log.md; day-1 legacy logs
  live in the operating goal's hidden_files).
- `tools/socialy_lint.py` - the draft linter (policy gate as code; runs on
  every draft before it ships).
- `tools/socialy_parity.py` - the parity checker (catalogue vs the audit
  register; runs whenever the catalogue changes and at each weekly audit).
- `tools/socialy_runlog.py` - the run-log validator (SPEC-run-log.md schema
  and taxonomy; runs on every run log before it is filed in `logs/`).

## Status

- 2026-10-22: platform founded at Ravi's direction; first full run today
  (X replies already in flight; LinkedIn, Substack, YouTube runs launched).
- GitHub repo: Ravi will provide details; code/docs move there when they land.
