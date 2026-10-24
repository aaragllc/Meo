# Socialy.INK - Foundation + channel adapter spec (Phase 1, v1)

Status: ACCEPTED v1, 2026-10-22 (Meo, under Ravi's decision delegation). Encodes the mechanics proven in
production through 2026-10-22 (publishing pipeline, day-1 engagement runs).
Persona pack #1: that70sda (see POLICY.md for voice/escalation rules; this spec
is about machinery, not voice).

## Layer 0 - Foundation (shared by every adapter and pipeline)

### Identity and sessions
- Sessions are warm or they are nothing. All channels run inside one shared
  browser profile whose cookies persist; a channel is "ready" when its session
  is live, which is checked by visiting the channel home, never assumed.
- Passwords are never typed by automation on LinkedIn (datacenter-IP +
  scripted-login triggers security loops). General rule for every channel:
  automation does not perform credential entry; if a session is dead, the run
  pauses that channel and the operator (human) re-signs-in via takeover.
  One human sign-in re-warms the shared profile for all channels on that
  service family.
- Identity protection is a foundation invariant, not a per-post check: no
  public surface ever names the operator, the tooling, or the automation.

### Configuration
- `config.yaml` is the single source for volume (N comments/follows per
  channel per day), freshness window, the 50K author ceiling, and pacing.
  Runs read it at start; changing a number changes the next run, nothing else.

### Scheduling and pacing
- Every daily slot carries in-run jitter: the worker sleeps a random
  0-120 min inside the slot so start times wander day to day.
- Intra-run gaps are randomized 2-6 min between public actions.
- Volume stays gentle while accounts are young; any platform warning, limit
  message, or CAPTCHA stops that channel's run immediately (never circumvent).

### Policy gate (before anything posts)
Every drafted action passes POLICY.md: voice rules, hard bans, and the
escalation list (50K+ authors, specific stocks/personal finances, complaints,
press, money offers, legal/regulatory, identity probing, heated exchanges).
Escalation = skip and record in the registry with the reason. A per-post
platform restriction (e.g. one publication's paid-only comments, one post's
disabled comments) is a skip of that target, NOT a run stop - the run
continues to the next target. (Learned 2026-10-22, Substack run.)

### Quality control
- Verbatim check in the composer before posting; live read-back after posting;
  an action counts only when verified live.
- Text entered into fragile editors only by the channel's proven method
  (see adapter notes); a failed or mangled entry is reverted to the last
  published state, never patched forward blind.

### Reporting
- Every run writes a dated log (actions with live URLs, skips with reasons)
  and updates `target-registry.yaml` the same day.
- A consolidated chat report closes the run; metrics feed the weekly one-pager.

## Adapter contract (every channel implements the same seven steps)

1. DISCOVER - find candidate targets inside the freshness window, in-lane.
2. FILTER - apply registry (no cold repeats), ceiling, and escalation rules.
3. DRAFT - in the persona voice; numbers only from the target's own content
   or the day's approved post; never invented.
4. CRITIQUE - self-check against POLICY.md before anything is posted.
5. POST - with the channel's pacing and identity mechanics.
6. VERIFY - read back live; record the URL.
7. LOG - run log + registry update.

Plus the channel's follow/subscribe primitive, where the platform has one.

## Channel notes (hard-won, per adapter)

### X (@That70sDa)
- Replies and threads; threads post as chains, minutes apart, never in one
  burst. Sign-off "- That70s Da." on posts/threads, not on replies.
- Follows prefer accounts engaged with that day.

### LinkedIn (company page)
- The page comments via the composer identity switcher - the selection is
  PER-POST and must be checked every time. Never fall back to the admin's
  personal profile.
- Pages cannot comment inside Groups and cannot follow people; page follows
  go through the page's Manage following (pages only).
- Editor: single Enters between paragraphs (blank lines multiply). Long
  automated text is fragile - verify verbatim, inspect the live post.
- Every page post is dated, carries an overview, and ends with the cross-promo
  footnote (template in the goal files).

### Substack (publication)
- Subtitles are capped at 200 characters, silently truncated at publish -
  draft every subtitle at 200 or fewer, complete sentences only.
- Publishes and edits to published posts can each trigger a 6-digit email
  code gate; every publish click mints a new code and kills the previous one,
  and ~6 requests/day throttles sends. Batch gated work into one session with
  the operator present; relay only the newest code; never open a second
  dialog while one is open.
- Body edits: never fill/type the body field (it once replaced a whole
  article). Paste/caret only - and note the paste may not honor the caret
  (2026-10-22: three misplacements on one edit, all draft-only, reverted via
  Version History). After any edit, verify the FULL live body.
- Some publications restrict commenting to paid subscribers - detect and skip
  (never pay); some posts have comments disabled - skip.

### YouTube (channel)
- Comments carry no links (spam filters).
- Uploads: an unverified channel has a very small daily upload cap; a
  10-video day exhausted it into the next day. Until the operator decides on
  the one-time phone verification, schedule uploads assuming scarcity -
  new episodes first, backlog after - and stop at the limit message.
- Every upload: animated version only, verified by frame-change QA and the
  audio baseline before it goes up; dated overview in the description.

### Spotify (monitored, not an adapter)
- Episodes arrive by RSS from Substack; the adapter's job is verification
  (episode present, correct title/description), not posting.

### Apple Podcasts (monitored, not an adapter)
- Claimed 2026-10-23 from the same Substack RSS feed as Spotify;
  episodes arrive by RSS pull automatically - per-episode
  distribution work is zero, exactly like Spotify. Verification,
  not posting.
- Held under the owner's Apple account: the identity is private to
  Apple and the public listing shows only feed contents. Standing
  declarations: Content Rights Option B ("has rights to its
  third-party content" - licensed synthetic narration voice,
  generated artwork); Update Frequency Daily (the per-piece rhythm).
- YouTube is the exception to the RSS model: it does not consume
  the feed in this setup, so every episode's video is an individual
  upload in the publishing path.

## Open questions for Phase 1 sign-off - ALL SETTLED 2026-10-22 (Meo, under Ravi's decision delegation)
1. YouTube ceiling: SETTLED - the 50K ceiling applies to comment targets on
   every channel, X/LinkedIn/YouTube alike, with skip-and-report. (The day-1
   58.9K-sub exception was a one-off inside that day's approved pack, not a
   precedent.)
2. YouTube verification: SETTLED - Ravi completed the one-time phone check
   on 2026-10-22; the daily upload cap is lifted and parity holds.
3. Cron rework: DONE 2026-10-22 - `that70sda-reply-targets` is now the
   "Socialy daily engagement run" (daily ~09:20 PT, all channels,
   config-driven, executes and reports after the fact).
   after this spec is accepted.
