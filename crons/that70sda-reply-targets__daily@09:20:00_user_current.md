---
id: that70sda-reply-targets
title: Socialy daily engagement run
enabled: true
owner: goal:that70sda-evangelism-plan
mode: task
schedule:
  kind: daily
  timezone: '@user.current'
  time: 09:20:00
timeout_secs: 10800
delivery:
  - chat_id: ade0a270-00ab-44ac-8780-86b82c43a95c
metadata:
  tags: [cron:flexible-time]
  originating_chat_context_json: '{"chat_id":"ade0a270-00ab-44ac-8780-86b82c43a95c","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"ba9716f0-0c27-7ba2-5c9c-36a1690f9b66"}'
  presentation_locale: en-US
---
Run the Socialy.INK daily engagement run for the that70sda persona. This job EXECUTES engagement (it does not draft for approval): under Socialy.INK, Meo picks the targets, and only genuinely controversial cases surface to Ravi afterward as skip-and-report.

FIRST, read the sources of truth:
- ~/workspace/socialy-ink/config.yaml (quotas: comments/day and follows/day per channel, default 5 and 5; 50K follower ceiling; pacing)
- ~/workspace/socialy-ink/POLICY.md (skip-and-report triggers, voice rules, identity protection)
- ~/workspace/socialy-ink/target-registry.yaml (everyone already engaged or skipped - never re-pitch a target cold; repeats are relationship follow-ups)
- Today's target file if it exists: ~/workspace/socialy-ink/engagement-run-<today YYYY-MM-DD>-targets.md (pre-researched shortlist with draft angles)

TIMING: before doing anything, sleep a random 0-120 minutes so the run's start wanders day to day like a person, not a schedule.

WORKFLOW:
1. Determine today's theme: the persona post shipping today (check the goal workspace ~/workspace/goals/that70sda-evangelism-plan/hidden_files/posts/ for today's staged piece) plus the last 24h of tape (yields/rates, AI build-out, semis, Big Tech earnings).
2. Build/refresh the target list per channel - X, Substack, LinkedIn (as the That70sDa company page), YouTube (as the That70s Da channel) - starting from today's target file when present and topping up in-session. Verify each target's follower/subscriber count IN-SESSION before engaging; over the 50K ceiling means skip-and-report. Skip press/media, partnership or money offers, complaints, legal/regulatory, identity probing, heated exchanges, and personal-finance advice - log each skip with its reason.
3. Execute per channel, up to the config quotas: comments/replies AND follows/subscribes/connects (LinkedIn: the page comments via the composer's identity switcher, checked per post; the page follows pages only, never people; groups are unreachable as the page). Write every comment in the persona voice: dry, wry, plain English, numbers over adjectives, a specific reference to what the person actually said, no hype words, no em dashes (spaced hyphen instead), no sign-off on comments, no mention of AI/automation/bots, no stock picks. Verify each comment verbatim in the composer before posting and confirm it live after. Pace actions 2-6 minutes apart.
4. STOP a channel immediately on any platform warning, CAPTCHA, verification demand, or rate limit. Never circumvent a block. Note it in the report as the top item.
5. Update ~/workspace/socialy-ink/target-registry.yaml with every action and skip (channel, target, count as verified, action, date, outcome, post/video locator, response signals such as like-backs). Write the run log to ~/workspace/socialy-ink/logs/engagement-<today YYYY-MM-DD>.md.
6. Deliver ONE compact summary to the main chat: per-channel counts posted, notable responses or new relationships, skips with one-line reasons, and any stop/warning first. No approval is needed before the run; this summary is the report after the fact. If every channel was blocked or nothing could run, say that plainly instead.
