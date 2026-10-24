---
id: socialy-ops-watchdog
title: Socialy ops watchdog
enabled: true
owner: goal:that70sda-evangelism-plan
mode: task
schedule:
  kind: daily
  timezone: '@user.current'
  time: 07:20:00
timeout_secs: 3600
delivery:
  - chat_id: ade0a270-00ab-44ac-8780-86b82c43a95c
metadata:
  tags: [cron:flexible-time]
  originating_chat_context_json: '{"chat_id":"ade0a270-00ab-44ac-8780-86b82c43a95c","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"ba9716f0-0c27-7ba2-5c9c-36a1690f9b66"}'
  presentation_locale: en-US
---
Socialy.INK ops watchdog - the daily self-check from SPEC-self-learning.md. Run these checks in order:

1. Platform state: run `python3 ~/workspace/socialy-ink/tools/socialy_check.py state` and capture its exit code and output.
2. Intake freshness: list the Stocky Intake Drive inbox (that70sda@gmail.com Drive; inbox folder id 1AAUcEBEPGD8U910t_P1g10A2F8c7CEel; acks id 1bjyfLWZz34EgUBTuR7ZOo7RJpmlsIr-m) with /opt/hatch/bin/hatch_gws_cli drive. If a drop's files have sat un-consumed for over 2 hours (no matching ACK file in acks/), HEAL it: run the full intake consumption for that drop exactly as the stocky-drive-intake job body describes (inspect, lint, dedup, slots, move to consumed, write and upload the ack), and note the heal in your report.
3. Backup freshness: read ~/workspace/goals/that70sda-evangelism-plan/hidden_files/socialy-backup-state.txt. If the last successful Drive backup is older than 26 hours, HEAL it: perform the same archive-and-upload the socialy-drive-backup job does (commit dirty repo state in ~/workspace/socialy-ink, zip the repo, upload to the Drive "Socialy.INK" folder id 131XnJ39w9uWFiXTqdL6ch98vRBCyw23g, verify byte size, update the state file), and note the heal in your report.

Report to the main chat ONLY if something failed a check or a heal was executed: one compact message naming what failed, what was healed and verified, and what still needs a human. If everything is healthy and nothing was healed, stay completely silent.
