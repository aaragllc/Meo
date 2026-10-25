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
  originating_chat_context_json: '{"chat_id":"ade0a270-00ab-44ac-8780-86b82c43a95c","origin_provider":"main","chat_kind":"direct","provider":"main","event_kind":"message","require_mention":false,"device_id":"ba9716f0-0c27-7ba2-5c9c-36a1690f9b66"}'
  presentation_locale: en-US
---
Run the Socialy.INK daily engagement run for the that70sda persona. This job EXECUTES engagement (it does not draft for approval): under Socialy.INK, Meo picks the targets, and only genuinely controversial cases surface to Ravi afterward as skip-and-report.

FIRST, read the sources of truth:
- ~/workspace/socialy-ink/config.yaml (quotas: comments/day and follows/day per channel, default 5 and 5; 50K follower ceiling; pacing; the growth section - recommendations list, tag taxonomy, notes_per_day, communities test window, quote-post flag)
- ~/workspace/socialy-ink/POLICY.md (skip-and-report triggers, voice rules, identity protection)
- ~/workspace/socialy-ink/target-registry.yaml (everyone already engaged or skipped - never re-pitch a target cold; repeats are relationship follow-ups)
- Today's target file if it exists: ~/workspace/socialy-ink/engagement-run-<today YYYY-MM-DD>-targets.md (pre-researched shortlist with draft angles)

TIMING: before doing anything, sleep a random 0-120 minutes so the run's start wanders day to day like a person, not a schedule.

STEP 0 - SESSION PREFLIGHT (L-25, added 2026-10-25): before any engagement action, run the publish_session_preflight skill for every channel this run touches (X, Substack, LinkedIn page, YouTube): open each platform in the live browser and confirm the signed-in identity from the profile name or handle. Report each channel as passed or expired in the run log and in the summary BEFORE any posting result. An expired session skips that channel for the day (LinkedIn sign-in is manual-takeover only - never retry a password) and is reported as a session expiry, never absorbed as a platform failure. A run that starts without this preflight names that gap in its report.

WORKFLOW:
1. Determine today's theme: the persona post shipping today (check the goal workspace ~/workspace/goals/that70sda-evangelism-plan/hidden_files/posts/ for today's staged piece) plus the last 24h of tape (yields/rates, AI build-out, semis, Big Tech earnings).
2. Build/refresh the target list per channel - X, Substack, LinkedIn (as the That70sDa company page), YouTube (as the That70s Da channel) - starting from today's target file when present and topping up in-session. Verify each target's follower/subscriber count IN-SESSION before engaging; over the 50K ceiling means skip-and-report. Skip press/media, partnership or money offers, complaints, legal/regulatory, identity probing, heated exchanges, and personal-finance advice - log each skip with its reason.
3. Execute per channel, up to the config quotas: comments/replies AND follows/subscribes/connects (LinkedIn: the page comments via the composer's identity switcher, checked per post; the page follows pages only, never people; groups are unreachable as the page). Write every comment in the persona voice: dry, wry, plain English, numbers over adjectives, a specific reference to what the person actually said, no hype words, no em dashes (spaced hyphen instead), no sign-off on comments, no mention of AI/automation/bots, no stock picks. Verify each comment verbatim in the composer before posting and confirm it live after. Pace actions 2-6 minutes apart.
4. GROWTH ACTIONS (from config.yaml growth section; these do not count against the comment/follow quotas):
   a. Substack Note: post ONE original Note per day - the sharpest line from today's piece or the day's tape, one number worth arguing with, or a question to the room - in the persona voice, with a link to today's piece when it is live. Additionally restack (with a one-line comment) one in-lane post from a warm publication when something genuinely fits; never force it. SITE-ERROR BACKOFF (L-28): if Notes (or free subscribes) are failing with bare Substack site errors ("Something went wrong" / "Failed to send note", no warning attached), follow config safety.site_error_backoff - skip the next run, then retry every other day, logged as a standing site issue; do not burn daily retries on a platform-side error.
   b. X quote-post: if yesterday shipped a thread and today's tape gives it a fresh angle, quote-post yesterday's thread opener with one new line. Skip when it would be a stretch - an honest skip beats a forced post.
   c. X Communities (only inside the config test window; the joined communities and their link rules are recorded in target-registry.yaml): if a community's rules allow members to share their own analysis, post today's thread opener + link there once. Log impressions/replies signals in the registry for the test review date. WORDING + LENGTH (L-27): write DISTINCT text for each community (identical text trips X's duplicate check) and measure it before handoff like a tweet - at or under the 272 prep ceiling in config defaults.tweet_prep_char_limit, URL counted at t.co length.
5. STOP a channel immediately on any platform warning, CAPTCHA, verification demand, or rate limit. Never circumvent a block. Note it in the report as the top item.
6. Update ~/workspace/socialy-ink/target-registry.yaml with every action and skip (channel, target, count as verified, action, date, outcome, post/video locator, response signals such as like-backs; growth actions logged with kind: note / quote-post / community-post). Write the run log to ~/workspace/socialy-ink/logs/engagement-<today YYYY-MM-DD>-01.md in the SPEC-run-log.md schema: a yaml header (run_id, date, kind: engagement, channels, operator, config_ref, started_local, failure_tally) and an action-row table (channel, target, action, locator, verification, outcome), classifying every non-success outcome with a taxonomy code from SPEC-run-log.md (verification is never "none" on a success row). Before finishing, validate it: python3 ~/workspace/socialy-ink/tools/socialy_runlog.py on the log must exit 0 - fix the log until it does.
7. Deliver ONE compact summary to the main chat: per-channel counts posted, growth actions taken, notable responses or new relationships, skips with one-line reasons, and any stop/warning first. No approval is needed before the run; this summary is the report after the fact. If every channel was blocked or nothing could run, say that plainly instead.
