---
id: that70sda-inbox-filing
title: that70sda inbox filing (3x daily)
enabled: true
owner: goal:that70sda-evangelism-plan
mode: task
schedule:
  kind: interval
  timezone: America/Los_Angeles
  at: 2026-10-19T00:04:41
  every: 8h
timeout_secs: 600
delivery:
  - chat_id: ade0a270-00ab-44ac-8780-86b82c43a95c
metadata:
  tags: [cron:automatic-interval-anchor]
  predicted_connector_permissions:
  - connector: gmail
    method: users.labels.list
  - connector: gmail
    method: users.messages.list
  - connector: gmail
    method: users.messages.modify
  originating_chat_context_json: '{"chat_id":"ade0a270-00ab-44ac-8780-86b82c43a95c","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false}'
  presentation_locale: en-US
---
Run the that70sda@gmail.com inbox filing processor: execute `python3 ~/workspace/.jarvis/idea-executions/cb4fd50d-8f46-43bc-9601-700d4464b358/inbox_processor.py` via the shell. The script labels platform notification noise (Persona/Notifications) and engagement pings (Persona/Engagement) and archives them, labels Stocky drafts (Persona/Stocky) leaving them in the inbox, and leaves personal mail and Google security alerts untouched. It records processed message IDs in its state.json so reruns are idempotent. Do not send any email. If the script prints "Mail needing a reply" with entries, report those senders/subjects in your final message. If it prints nothing or only a filing count, the run is routine — keep the final message to one quiet line.
