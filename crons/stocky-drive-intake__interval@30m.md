---
id: stocky-drive-intake
title: Stocky Drive intake
enabled: true
owner: goal:that70sda-evangelism-plan
mode: task
schedule:
  kind: interval
  timezone: America/Los_Angeles
  at: 2026-10-23T11:33:13
  every: 30m
timeout_secs: 3600
delivery:
  - chat_id: ade0a270-00ab-44ac-8780-86b82c43a95c
metadata:
  tags: [cron:automatic-interval-anchor]
  originating_chat_context_json: '{"chat_id":"ade0a270-00ab-44ac-8780-86b82c43a95c","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"ba9716f0-0c27-7ba2-5c9c-36a1690f9b66"}'
  presentation_locale: en-US
---
Poll the Stocky draft intake on Google Drive and consume any new drop. The full protocol is ~/workspace/goals/that70sda-evangelism-plan/files/stocky-drive-intake-prompt.md - follow it; this body is the operator summary.

Drive folders (that70sda@gmail.com Drive): Intake root "Stocky Intake" id 13Y3x2vP2OREJ_W8DoOYENM99cNO9Rr5W; inbox id 1AAUcEBEPGD8U910t_P1g10A2F8c7CEel; consumed id 1jTLB5W2Lm7R8KlhZCfjQn3E4de5uhfS1; acks id 1bjyfLWZz34EgUBTuR7ZOo7RJpmlsIr-m. Use /opt/hatch/bin/hatch_gws_cli drive for all Drive operations.

1. List the inbox folder. If it holds no files, end silently - no report.
2. A drop = a manifest (name contains "MANIFEST") plus post files. Group files by drop (date + batch). If a drop is malformed (no manifest, or a post file without the protocol's YAML front matter), write an ack (step 5) naming exactly what is missing, consume nothing from that drop, and report the problem in your summary. Other well-formed drops in the same poll still proceed.
3. For each well-formed drop: download every file to ~/workspace/goals/that70sda-evangelism-plan/hidden_files/posts/ (keep the Drive filenames; add a local "intake-<date>" copy if a name collides). For versioned files (-v2, -v3), consume only the highest version of each post; note superseded ones in the ack.
4. Inspect like the standing batch inspections: run python3 ~/workspace/socialy-ink/tools/socialy_lint.py on each post file and record the result; do a content-level dedup comparison (full paragraphs, not titles) against the published catalogue in ~/MEMORY.md and personas/that70sda/catalogue.yaml in the socialy-ink repo; extract the cross-reference obligations (builds_on, forward_refs_promised) and any verify: items. Write the inspection to hidden_files/posts/<drop-date>-stocky-drive-inspection.md. Decide a ship slot for each piece yourself (posting timing is Meo's under the standing delegation; Stocky's timing lines are suggestions; never let a later sequence piece ship before an earlier one it depends on, and keep forward references landing as promised).
5. Move the drop's Drive files from inbox to consumed (files update with addParents=<consumed id>, removeParents=<inbox id>). FILING PATH (L-29, 2026-10-25): these moves ride THIS job's own approved scope - they are this run's work, never an ad-hoc manual move from an interactive shell (those spawn separate approval cards, and the call can hang behind a stuck equivalent write; the Oct 24 batches sat unfiled a full day that way). If a move fails inside this run, note it in the run log and let the next poll or the watchdog's stale-intake remedy retry it here. Ravi's standing permission (2026-10-25) covers reorganizing the Stocky handshake folders without asking. Write the ack as a local markdown file named ACK-<drop-date>-<batch-name>.md with the protocol's ack contents (received files + versions, lint + dedup results, fact-check plan, ship slots with one-line basis where they differ from Stocky's suggestion, questions for Stocky or Ravi), then upload it to the acks folder with drive +upload.
6. Deliver ONE compact summary to the main chat: batch name, pieces received, your planned slots, and any flags or questions. If nothing was consumed and nothing was malformed, stay silent.
