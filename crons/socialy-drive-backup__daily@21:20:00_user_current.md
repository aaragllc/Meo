---
id: socialy-drive-backup
title: Socialy.INK auto-backup to Drive
enabled: true
owner: goal:that70sda-evangelism-plan
mode: task
schedule:
  kind: daily
  timezone: '@user.current'
  time: 21:20:00
timeout_secs: 3600
delivery:
  - chat_id: ade0a270-00ab-44ac-8780-86b82c43a95c
metadata:
  tags: [cron:flexible-time]
  originating_chat_context_json: '{"chat_id":"ade0a270-00ab-44ac-8780-86b82c43a95c","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"ba9716f0-0c27-7ba2-5c9c-36a1690f9b66"}'
  presentation_locale: en-US
---
Back up the Socialy.INK harness to Google Drive. Ravi's standing permission (2026-10-22): copying the harness to Drive is always allowed; no approval needed.

Steps:
1. Read the state file ~/workspace/goals/that70sda-evangelism-plan/hidden_files/socialy-backup-state.txt - it records last_head (the git commit last uploaded) and the Drive folder id.
2. In ~/workspace/socialy-ink: if `git status --porcelain` is non-empty, commit the work in progress: `git add -A` then `git commit -m "Socialy.INK progress backup <YYYY-MM-DD>"`. Never force-add media files; .gitignore already excludes *.mp3/*.mp4.
3. Let HEAD = `git log -1 --format=%H`. If HEAD equals last_head in the state file, nothing new has developed - end silently, no report.
4. Otherwise build the archive: `cd ~/workspace && zip -qr backups/socialy-harness-<YYYY-MM-DD>.zip socialy-ink` (include the .git directory). Upload it: `/opt/hatch/bin/hatch_gws_cli drive +upload /home/hatch/workspace/backups/socialy-harness-<YYYY-MM-DD>.zip --parent <drive_folder_id from the state file>`. The upload can take several minutes - wait for it. Verify by listing that Drive folder and confirming the new file is there with a nonzero size. If the upload fails or cannot be verified, retry ONCE; if it still fails, report the failure to the main chat in one short message and stop.
5. On success, update the state file: last_head = HEAD, last_uploaded_archive, last_uploaded_at (user's local time), drive_file_id from the upload result.
6. RETENTION (Ravi's policy, 2026-10-23, refined same day): after a successful upload, list every socialy-harness-*.zip in the Drive folder (drive files list with q: name contains 'socialy-harness', fields id/name/createdTime). Group archives by their LOCAL calendar date and month (from createdTime). Keep an archive if ANY rule keeps it:
   (a) DAILY PINS: it is the newest archive of one of the last 14 calendar days (today plus the 13 days before it) - one restore point per day, guaranteed; intra-day extras never evict another day's pin.
   (b) IN-FLIGHT SLOTS: it is among the 3 newest archives overall, whatever day they fall on - today's manual or watchdog burst backups stay available.
   (c) MONTHLY PINS: for any calendar month older than the 14-day window, it is the newest archive of that month.
   Move every other archive to Drive trash (NEVER permanently delete): /opt/hatch/bin/hatch_gws_cli drive files update --params '{"fileId":"<id>"}' --json '{"trashed": true}'. Trashed files stay recoverable in Drive trash for 30 days.
7. Report to the main chat ONLY when an upload happened (one line: the archive name and its Drive webViewLink from a files get call, plus a clause naming how many old archives were pruned if step 6 trashed any) or when step 4 failed after the retry. Silence otherwise.
