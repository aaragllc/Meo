# that70sda-publishing

Workflow for taking a Stocky draft (Ravi's stock Claude Code agent) and publishing it
as the that70sda persona on X (@That70sDa) and the LinkedIn company page (That70sDa).

## Voice ownership

- Stocky decides content, tone, and style. Meo adopts it.
- Meo's job: smooth language minimally (typos, small grammar fixes), verify
  factual claims (historical market figures, Fed history, consensus numbers),
  and format for each platform. Never rewrite Stocky's voice.
- If a line conflicts with a standing Ravi preference (e.g. phrasing he
  rejected before), keep Stocky's text but flag it for Ravi at approval time.

## Standing rules

- Sign-off on every post: `- That70s Da.` (spaced hyphen, name, period).
  Both platforms. (Was an em dash until Ravi replaced it 2026-10-20 - see
  the separator rule below.)
- Nothing posts without Ravi's explicit approval of the final formatted drafts.
- Anonymity: never attach Ravi's real name, employer, or offline identity.
- Finance guardrails: education, never advice. No stock picks, no buy/sell
  calls, no personalized recommendations, no guarantees. Keep Stocky's
  "Not financial advice." placement.
- Banned hype words: revolutionary, game-changer, disrupt, paradigm shift,
  "the future is here". No partisan politics. No shilling.
- Separators (Ravi, 2026-10-20): never use an em dash (—) to separate
  clauses - it reads as AI formatting. Use a spaced hyphen " - " instead.
  Convert Stocky's em dashes during the humanize pass. Applies to articles,
  threads, comments, episode descriptions, and Meo's own chat text.
- Brand pronunciation in narration (Ravi, 2026-10-21 - current default,
  supersedes the 2026-10-20 "daaa" + treated-master and blended-trial
  recipes): the brand name is always fed to TTS as "That seventies day" -
  the word "day" renders clean with no clipped ending. Treatment is
  blended: the sign-off sits inside the final narration chunk, same take
  as the closing lines, normal speed, no stretch, no 1s gap; tail fade +
  trailing silence only. Full recipe: tts_narration_humanization skill.
  No catalogue re-renders. AUDIO ONLY: the written post signature stays
  exactly "- That70s Da." in all text (articles, threads, descriptions).
- Episode metadata (Ravi, 2026-10-20): every podcast episode gets an
  episode-specific summary line and a real description (what it covers, key
  points, links to the article and any related earlier post). The fixed
  one-line description "This is the audio version of the article." is retired.
  Once the episode is live, edit the article to link it.
- YouTube parity (Ravi, 2026-10-20): every episode also ships to YouTube
  alongside its Substack release. NEW episodes get an animated video -
  data/visual cards in the 70s palette synced to the narration chunks (the
  EP1 pilot format), never a static-image video. Titles and descriptions
  match the episode's Substack metadata.
- Video QC - audio included (Ravi, 2026-10-21, extending the animation
  must-have): a video passes QC only if BOTH checks pass. (1) Animation:
  frame-change check across the runtime shows real changing boundaries
  (a static render scores ~0). (2) Audio: the narration track must be a
  single consistent render under the no-editing rule - never patched or
  chunk-spliced audio with audible cuts or loudness jumps between
  sections; verify with per-section loudness measurements before upload.
  A video built on a flawed audio render fails QC: remake the audio
  fresh (or live with it, by the ROI rule), rebuild the video, re-check.
  FROZEN BASELINE (Ravi, 2026-10-21): the EP15 single-take remake was
  judged "near perfect" (attribution corrected by Ravi from EP16 to EP15
  the same evening) and frozen as the baseline for all future video
  builds - videos are built only on audio meeting the TTS narration
  skill's frozen-baseline numbers (single take, per-30s-window RMS
  spread ~2 dB or less, catalogue level, clean tail).
- Overview-description gate (Ravi, 2026-10-21): every post on every
  channel that supports an overview/description must carry its post
  overview description before publishing - mandatory gate, no description
  means no post. Backlog/old video uploads also carry the original
  publish date, as a dated line at the top of the description overview.
- Lateness bridge (Ravi, 2026-10-20): if a post is late, a day is missed, or a
  promised article slips, the next post opens with a brief human bridge in the
  persona's voice — a plausible everyday reason (work, travel, life), short,
  vague, varied, unembarrassed. Never let a slip pass silently.

## Platform formatting

### X (no Premium on the account)
- 280 characters per post. Long-form goes out as a thread: first post is the
  hook, each following post is a reply to the previous one, in order.
- Split at sentence/paragraph boundaries. Keep punchlines on their own where
  Stocky wrote them that way. No inline numbering (the reply chain shows order).
- Verify every post is ≤ 280 chars before handing to the browser task
  (programmatic check, not eyeballing).
- PREP CEILING (L-23c, 2026-10-25): draft every tweet to ≤ 272 raw
  characters, counted by script (config defaults.tweet_prep_char_limit;
  the ship gate enforces it). 280 is the platform's hard limit, not
  the drafting target - the Scorecard W43 thread prepped to 280
  shipped tweets at 294/310/291 by X's counter and stopped live.
  Community posts and other derivative texts follow the same ceiling
  and get DISTINCT wording per community (L-27).
- PACING (learned 2026-10-15): never fire a full 13–19 tweet thread in one
  burst on this young, unverified account. The 16:35 PT rate-limit hit after
  17 + 19 tweets in ~24h — the trigger is burst/hourly throttle plus
  new-account scrutiny, not the daily cap. Post tweets sequentially at human
  composition rhythm (~2–3 minutes between tweets), OR post the first ~5–6
  via the composer, wait 20–30 minutes, then continue the remainder as
  chained self-replies. Keep daily original-post volume comfortably under
  ~40 while the account is young and unverified. Then visually verify the
  thread rendered as a chain.
- STOP-ON-WARNING (hard rule): if X shows any limit notice, CAPTCHA,
  verification, warning, restriction, or block — stop immediately, post
  nothing more, no refreshes or workarounds, report plainly.
- Posting: live browser task signed in as @That70sDa (that70sda@gmail.com).

### LinkedIn
- Single long-form post, full text as approved. Same sign-off.
- Posting: live browser task on the That70sDa company page (the "Daniel Ashford" personal account is blocked/retired - never use or sign into it).

## Timing
- Coordinate with the market calendar (e.g. CPI eve → CPI morning).
- When a draft written for a later day posts sooner, shift day references
  ("Wednesday" → "tomorrow") and note the change at approval time.

## Routine (per post)
0. SESSION PREFLIGHT (L-25, 2026-10-25): before the first publish step,
   run the publish_session_preflight skill for every platform this
   ship touches (Substack, X, LinkedIn, YouTube) - confirm each
   signed-in identity in the live browser and report pass/expired
   BEFORE any posting result. An expired session stops that platform
   (manual-takeover sign-in ask; never a password retry), never the
   whole ship silently.
1. Receive Stocky draft. Note which post it is and intended timing. Record provenance in the batch inspection file: the source (Stocky batch date, or a Ravi special sequence), the piece's sequence position if it belongs to a multi-post group, and the scheduling basis actually used — Ravi's own instruction governs over Stocky's Timing lines, and the file states which one won and why.
2. Verify numbers Stocky flagged or that look checkable (search).
3. Minimal language smoothing only.
4. Continuity pass (Ravi, 2026-10-19 — see directive Resolution 4): before formatting, check the draft against the previous 2–3 posts. Ensure (a) at least one callback to an earlier post or named system (dashboard, scorecard, rotation map) where natural, (b) an open-loop close ("what I'm watching" / "what would change my mind"), (c) at least one cross-channel bridge — X thread ends on the article link, article links the episode, episode description links back. Preserve the piece's native narrative frame (map day / odds day / story day / grading day); never flatten drafts into one template. (d) Lateness check (Ravi, 2026-10-20): if the previous post was late, a day was missed, or a promise slipped, add a brief lateness bridge near the top in the persona's voice (everyday reason — work, travel, life; short, reasonably personal in feel but never any specific personal detail, and varied). (e) Forward reference (Ravi, 2026-10-20 — directive Resolution 6): every post points ahead to what is coming — the next post or segment, the calendar event being watched, what the persona will check next and when — so readers have a reason to return; and when a post fulfills an earlier forward reference, say so, so the promises visibly land. (f) Sequence cross-references (Ravi, 2026-10-22): when a post belongs to a related group (a trio, a series, a two-parter), record the group's cross-reference obligations in the batch inspection file at intake — which earlier pieces each post must name and link, which forward references each piece must plant, and which promises the later pieces must visibly fulfill. At each piece's ship time, add or edit the cross-references so they name the actually-published earlier pieces with their live links; never ship a later piece whose promised callbacks are missing or point at the wrong day.
5. Build LinkedIn full text + X thread splits; check X lengths programmatically. Then run the ship gate (socialy_check.py ship) on the WHOLE pack - article, thread, episode script, metadata, LinkedIn draft, community texts - never the article set alone (L-23c: the scorecard thread escaped the gate exactly this way). A placeholder in a file does not excuse it from the gate; fill placeholders at ship and re-run until clean.
6. Present final formatted drafts to Ravi for approval. Flag any conflicts
   with his standing preferences.
7. On approval: post to both platforms via browser tasks, verify live,
   report links.
