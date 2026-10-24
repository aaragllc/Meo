---
id: socialy-major-backup-sentinel
title: Socialy major-change backup sentinel
enabled: true
owner: goal:that70sda-evangelism-plan
mode: task
schedule:
  kind: interval
  timezone: America/Los_Angeles
  at: 2026-10-23T21:44:00
  every: 2h
timeout_secs: 3600
delivery:
  - chat_id: ade0a270-00ab-44ac-8780-86b82c43a95c
metadata:
  tags: [cron:automatic-interval-anchor]
  originating_chat_context_json: '{"chat_id":"ade0a270-00ab-44ac-8780-86b82c43a95c","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"ba9716f0-0c27-7ba2-5c9c-36a1690f9b66"}'
  presentation_locale: en-US
---
Socialy.INK major-change backup sentinel - enforces the Backups project rule in ~/workspace/socialy-ink/POLICY.md. Ravi's standing permission (2026-10-22): copying the harness to Drive is always allowed; no approval needed.

Steps:
1. Read the state file ~/workspace/goals/that70sda-evangelism-plan/hidden_files/socialy-backup-state.txt - it records last_head, last_uploaded_at and the Drive folder id.
2. In ~/workspace/socialy-ink run `git status --porcelain`. If the tree is DIRTY, the current workstream has not reached its logical checkpoint - end silently. (The nightly backup sweeps dirty state; never commit here.)
3. Let HEAD = `git rev-parse HEAD`. If HEAD equals last_head, end silently - nothing new.
4. Inspect the range: `git log <last_head>..HEAD --name-only --format='COMMIT %ct %s'`. The range is MAJOR if any changed path matches: POLICY.md, SPEC-*.md, config.yaml, BOOTSTRAP.md, RUNBOOK.md, templates/*, tools/*, crons/*, personas/*/catalogue.yaml, or a new personas/<name>/ directory; OR any commit subject mentions a phase, a spec, an adapter, a migration, or a project rule. Routine logs (logs/*), engagement records, target-registry.yaml edits and ordinary content drafts are NOT major - they ride the nightly backup. If nothing in the range is major, end silently.
5. Settle check: the newest commit in the range must be at least 45 minutes old (its %ct against now). If younger, the workstream may still be landing - end silently; the next pass decides.
6. Coalesce check: if last_uploaded_at is less than 2 hours ago, end silently - this checkpoint merges into the recent backup's window. The nightly run still captures everything.
7. Back it up: `cd ~/workspace && zip -qr backups/socialy-harness-<YYYY-MM-DD>.zip socialy-ink` (include .git; media renders are already gitignored). Upload: `/opt/hatch/bin/hatch_gws_cli drive +upload /home/hatch/workspace/backups/socialy-harness-<YYYY-MM-DD>.zip --parent <drive_folder_id from the state file>`. Verify by listing the Drive folder: the new file present with a size equal to the local byte count. If the upload fails or cannot be verified, retry ONCE; if it still fails, report one short failure message to the main chat and stop.
8. On success, update the state file (last_head = HEAD, last_uploaded_archive, last_uploaded_at in the user's local time, drive_file_id), then enforce retention exactly as step 6 of the socialy-drive-backup job: keep (a) the newest archive of each of the last 14 calendar days (daily pins), (b) the 3 newest archives overall (in-flight), (c) the newest archive of each older month (monthly pins); move every other socialy-harness-*.zip to Drive trash (never permanent delete).
9. Report one line to the main chat only when an upload happened (archive name + that it was a major-change intraday backup) or when step 7 failed after the retry. Silence in every other case.
