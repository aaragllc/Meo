# Socialy.INK - daily runbook

One run per day (scheduled ~09:20 PT, start jittered up to 2h inside the run).
Read config.yaml and POLICY.md first; N and toggles come from config only.

## Per channel, in order

1. Confirm the session is signed in as the right account. If signed out, note it
   in the report and skip the channel (LinkedIn sign-in is manual-takeover only).
2. Discover targets: in-lane conversations from the last ~24h
   (lanes: Fed/rates, VIX/fear gauge, AI infrastructure and semis, oil/Hormuz,
   market breadth, macro data reactions, tech leadership/management for LinkedIn).
3. Filter: drop bots/aggregators/spam, drop escalation triggers (POLICY.md),
   drop authors above the follower ceiling.
4. Draft one comment per target in voice; run the critique pass against
   POLICY.md; revise or drop failures.
5. Post up to N comments, randomized 2-6 min gaps, verifying each live and
   capturing its URL before moving on.
6. Follows/connects up to N (where supported): prefer accounts/publications/
   channels engaged with in step 5, then standing candidate lists.
7. Stop conditions end the channel's run immediately; log what posted and what
   did not, with the exact stop reason.

## Channel notes

- X: replies under the configured char limit; threads and owned posts are a
  separate publishing pipeline, not this run.
- LinkedIn page: check the composer identity switcher on EVERY post (selection
  is per-post); group posts are unreachable - skip them. Follows go through the
  page's Manage following (pages only).
- Substack: comments on other publications' posts; follows are free
  subscribes/follows only, never paid.
- YouTube: read the video's description/transcript enough to reference a
  specific point; no links in comments; subscribes from the channel account.

## Reporting

One consolidated report per run in chat: per channel - targets posted (URLs),
follows made, skips and why, any stop reason, and anything escalated for a
human call. Per-run detail log: engagement-log-<date>.md in the operating
goal's hidden_files.
