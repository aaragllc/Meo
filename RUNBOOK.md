# Socialy.INK - daily runbook

One run per day (scheduled ~09:20 PT, start jittered up to 2h inside the run).
Read config.yaml and POLICY.md first; N and toggles come from config only.

## Step 0 - session preflight (EVERY run, EVERY ship) - L-25

Before any posting, commenting, following or uploading, run the
publish_session_preflight skill: list every platform the run will
touch, open each in the live browser, and confirm the signed-in
identity from the profile name or handle. A redirect to a login page
or a missing profile identity means EXPIRED. Report each platform as
passed or expired BEFORE reporting any posting result. An expired
session stops that platform only: ask the user to sign in manually
in the live browser (LinkedIn is always manual-takeover, L-10), never
retry a password programmatically, and resume only after re-verifying
the identity. Weekend of 2026-10-24/25 is the standing example:
LinkedIn expired both mornings and the failures were found mid-run
because no preflight ran - that gap is named in the run's report
whenever it happens, never silently absorbed as a platform failure.

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
human call. Per-run detail log: `~/workspace/socialy-ink/logs/`
(engagement-<date>.md; see SPEC-run-log.md - day-1 legacy logs live in the
operating goal's hidden_files).

## Publishing ships - standing notes

- **Preflight first (L-25):** a ship is a run - step 0 applies to
  every platform the ship touches (Substack, X, LinkedIn, YouTube)
  before the first publish step, sessions verified in fresh windows.
- **Gate the WHOLE pack (L-23c):** `socialy_check.py ship` runs on
  every file in the ship pack - article, X thread, episode script,
  metadata, LinkedIn draft, community texts - never just the article
  set. A file carrying an unfilled placeholder still gets its length
  and lint measurements read; a PLACEHOLDER failure is filled at
  ship, never used as a reason the file skipped the gate. Tweets and
  community posts draft to the 272 prep ceiling
  (config defaults.tweet_prep_char_limit).
- **Substack code gate (L-06, extended 2026-10-24):** if a publish
  or edit hits the "Check your email" gate while Ravi is present,
  the primary path is manual takeover - he clicks Resend in the live
  window and enters the fresh code himself (proven P2 + P3). The
  sealed Gmail relay is the fallback for when he is not present; its
  round trips can exceed the code's ~10-minute life. One dialog at a
  time, newest code only, budget the day's code requests (L-08).
- **Substack body edits (L-02/L-03):** listen-line inserts use the
  caret-created empty paragraph above the sign-off + individual key
  presses - paste and fill are both banned on the body field - and
  the FULL live body is verified after any edit publish.
- **Site errors (L-28):** a bare platform "Something went wrong"
  (Substack subscribes/Notes, 2026-10-23/25) follows the decaying
  cadence in config (skip next run, then every other day) and is
  logged as a standing site issue. Warnings are a different animal:
  full stop, no retry (POLICY.md).
- **Drive filing (L-29):** Stocky intake filing moves (inbox ->
  consumed) ride the stocky-drive-intake job's own approved scope -
  the cron path moves the files. Do NOT improvise manual `files
  update` moves from an interactive shell: they spawn separate
  approval cards and the call can hang behind a stuck equivalent
  write. Ravi's standing permission (2026-10-25) covers Meo
  reorganizing the Stocky handshake folders without asking; the
  permission does not change which execution path to use.
