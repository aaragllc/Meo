# Socialy.INK - LESSONS registry

The single registry of operational lessons. Every entry: the rule in
one sentence, where it came from, and where it is enforced. Enforcement
classes per SPEC-self-learning.md: CODE > GATE > TEMPLATE > PROSE.
The gate runner's state mode verifies every taxonomy code from
SPEC-run-log.md appears here.

## Publishing mechanics

- **L-01 | EDIT-SUBTITLE-TRUNC | 2026-10-22.** Substack silently cuts
  subtitles at 200 characters mid-sentence. Rule: draft subtitles at
  200 chars or fewer, complete sentences, verify the live ending.
  Enforced: CODE (lint SUBTITLE_LEN) + live verify in the ship path.
- **L-02 | EDIT-FILL-REPLACE | 2026-10-21.** Fill/typing entry on the
  Substack body editor replaced an entire published article with one
  line. Rule: body text enters by paste/caret only, never fill/typing.
  Enforced: TEMPLATE (every browser publish/edit task states it) +
  full-body verify after any edit publish.
  EXTENDED 2026-10-24: on the P3 and Scorecard listen-line inserts,
  the paste path ALSO corrupted the body (fill-action paste merged
  the line into adjacent paragraphs and once replaced body text;
  every attempt undone before publish). Rule update: for body
  inserts, paste is no longer a verified method either - see L-03.
- **L-03 | EDIT-PASTE-DRIFT | 2026-10-22/23.** Pasted lines drift to
  the wrong paragraph in the Substack editor. Rule: the listen-line
  method is click sign-off, Home, Enter, verified caret in the new
  empty paragraph, then paste (confirmed clean 2026-10-23 on P2).
  Enforced: TEMPLATE (edit tasks carry the method verbatim).
  SUPERSEDED METHOD 2026-10-24: the paragraph setup stands (click
  the "- That70s Da." sign-off paragraph, Home, Enter, verify the
  caret sits in the new empty paragraph above it), but the line
  itself is entered with INDIVIDUAL KEY PRESSES, not paste - paste
  and fill both misbehaved on the 2026-10-24 inserts, key-press
  entry produced the exact text and paragraph structure on both
  P3 and the Scorecard, each followed by a full live-body verify.
  Enforced: TEMPLATE (edit tasks carry the key-press method
  verbatim) + SPEC-studio C6 caution.
- **L-04 | EDIT-DRAG-SHORT | 2026-10-22.** Drag-based text placement
  in the Substack settings editor (welcome email) drops short lines
  and desyncs visual from saved state. Rule: no drag placement for
  text; if a settings editor can't be verified, discard and hand the
  human the 30-second manual path. Enforced: PROSE + RUNBOOK note.
- **L-05 | CTRL-DEAD | 2026-10-22.** A UI control can be dead across
  sessions (Substack test-draft Delete button, two sessions). Rule:
  two genuine attempts max, then park it and route around; never loop
  on a dead control. Enforced: PROSE.

## Verification gates and sessions

- **L-06 | GATE-CODE | 2026-10-20/22.** Substack publish AND edit
  actions can each demand a fresh 6-digit email code. Rule: never
  trigger a code before the dialog is in front of someone who can
  enter it; one dialog at a time. Enforced: TEMPLATE (browser tasks
  stop at the gate) + the sealed Gmail relay.
  EXTENDED 2026-10-24 (CODE-RELAY-LATENCY): the sealed relay lost
  TWO codes on the P3 publish - handoff latency plus approval round
  trips exceed the code's ~10-minute life (13:34 code expired in
  transit; ~14:55 resend expired before entry). Rule: when Ravi is
  present, the MANUAL TAKEOVER path is primary - he clicks Resend
  in the live window and types the fresh code himself (proven on
  P2 2026-10-23 and P3 2026-10-24, zero drama both times). The
  sealed relay is fallback only, for when he is not present.
  Enforced: TEMPLATE (RUNBOOK ship section + healing table remedy
  rewritten) + operator practice.
- **L-07 | GATE-CODE-STALE | 2026-10-20.** Every publish click mints a
  new code and kills the last; only the NEWEST code email is valid.
  Rule: relay the newest email's reference only. Enforced: TEMPLATE
  (relay instructions) + operator practice.
- **L-08 | QUOTA-CODE-SEND | 2026-10-20.** After ~6 code requests a
  day, Substack stops sending. Rule: budget codes; park gated work to
  the next day instead of resending. Enforced: PROSE + healing table.
- **L-09 | SESS-WINDOW-STATE | 2026-10-22.** A "signed out" browser
  window is usually a per-window mirage; the shared profile session is
  warm. Rule: fresh window check before any sign-in escalation.
  Enforced: TEMPLATE (healing table remedy).
- **L-10 | VERIF-LI-CHECK | 2026-10-14.** Automated LinkedIn password
  logins loop security captchas from datacenter IPs. Rule: LinkedIn
  sign-in is a human takeover, always; the warm cookie is the session.
  Enforced: PROSE (AGENTS.md) + never-retry rule in the healing table.
- **L-11 | VERIF-X-HV | 2026-10-13.** X showed a human-verification
  challenge at account launch. Rule: any platform warning stops that
  channel immediately; nothing is ever circumvented. Enforced:
  TEMPLATE (engagement cron body) + POLICY.md.
- **L-12 | QUOTA-YT-UPLOAD | RESOLVED 2026-10-22.** YouTube's daily
  upload cap blocked backlog uploads until phone verification.
  Rule: verify platform capability ceilings during onboarding, not at
  first failure. Enforced: PROSE (BOOTSTRAP onboarding checklist
  candidate).

## Production

- **L-13 | TOOL-EMPTY-OUTPUT | 2026-10-19.** `tts speak` without
  --output silently writes empty MP3s. Rule: render scripts always
  pass --output and assert duration > 0 before reporting success.
  Enforced: CODE (render script template) + healing-table re-run.

## Judgment lessons (no code of their own - registered so they are counted)

- **L-14 | SEO fields | 2026-10-22 (Ravi's catch).** Every article
  ships with Substack SEO title (<=60) and description (<=160) set;
  the pipeline had silently never set them. Enforced: CODE (lint
  SEO_LEN) + GATE (ship-gate presence scan).
- **L-15 | Placeholders | 2026-10-22.** Prep files legitimately carry
  [P2 URL] placeholders until ship day; a ship file must carry none.
  Enforced: GATE (socialy_check.py ship scan).
- **L-16 | Stale present-tense figures | 2026-10-22.** Market levels
  stated in present tense go stale between draft and ship (5.15%
  10-year). Rule: refresh at ship in article, thread, and script
  together; a direction flip holds the piece (settled 2026-10-23).
  Enforced: PROSE (prep-file AT SHIP headers) + ack reporting.
- **L-17 | Duplicate re-drop | 2026-10-22/23.** A re-sent batch with
  only metadata changed entered the pipeline twice. Rule: content-
  level dedup (full paragraphs) against the catalogue at intake.
  Enforced: TEMPLATE (intake cron body) + GATE (parity checker).
- **L-18 | Meo-added promise | 2026-10-23 (Meo's error, Stocky's
  catch).** A dated forward promise added in a derivative bound the
  calendar the draft never set. Rule: derivatives introduce no new
  dated promises; exceptions are reported in the ack as Meo-added.
  Enforced: PROSE (operating brief Gate 4, amended) + ack template.
- **L-19 | Ambiguous upload outcome | 2026-10-22.** A Drive upload
  session died silently; the folder was empty. Rule: after any
  ambiguous failure, verify destination state before re-sending.
  Enforced: PROSE.
- **L-20 | Browser file grants | 2026-10-21.** The browser agent
  can't reliably read granted text files but uploads granted media
  fine. Rule: relay text inline in the task; grant files for media
  only. Enforced: TEMPLATE (operator practice).
- **L-21 | Single-take audio | 2026-10-21 (Ravi).** Never patch or
  splice a render; flawed audio is remade whole or lived with; the
  EP15 render is the frozen baseline (spread ~2 dB or less).
  Enforced: CODE (render scripts) + SPEC-studio (frozen).
- **L-22 | Animation is a gate | 2026-10-20/21 (Ravi).** Every video
  passes a frame-change check; a static render fails regardless of
  audio. Enforced: CODE (qa_frames.py) + healing-table re-render.
- **L-23 | Ship-time additions need surface checks | 2026-10-23
  (Meo's error).** The Meta tweet added at ship ran 59 characters over
  X's 280 limit and stopped the thread at 6 of 11. Rule: any text
  added or changed at ship time gets the surface's mechanical checks
  (length, lint, placeholders) before it reaches a composer - the
  prep-time checks no longer cover it. Enforced: CODE (ship gate now
  fails any numbered tweet line over 280 chars) + this entry.
  EXTENDED 2026-10-24 (L-23b): the trap has a second face - the live
  article URL (~64 chars) replaces [ARTICLE LINK] at ship time, so a
  tweet that fits at prep can break at post (caught on the P4 thread:
  291 chars with the URL in). The gate now measures tweet length with
  every placeholder substituted by a 64-char proxy URL. Enforced: CODE
  (socialy_check.py URL_PROXY) + this entry.
  EXTENDED 2026-10-25 (L-23c - the scorecard miss, root-caused): the
  Scorecard W43 thread shipped with tweets 3/4/6 at 294/310/291 by
  X's counter and stopped live after tweet 2 - yet prep had reported
  the pack gate-verified. Root cause: the prep gate ran on the
  article, episode script and metadata ONLY; the thread file was
  never in the gate's file list (its unfilled link placeholder made
  it "not ship-ready", so it was silently excluded). The gate code
  itself was verified correct - run on a reconstruction of the
  original thread it flags all three tweets and exits 1. Fixes:
  (1) CODE - the gate now also enforces a PREP CEILING of 272 raw
  chars per tweet (config defaults.tweet_prep_char_limit), so a
  draft fails early instead of at the platform limit, and regression
  fixtures + tools/test_socialy_check.py pin the behavior (original
  thread fails, corrected scorecard + Week Ahead threads pass);
  (2) TEMPLATE - the ship gate runs on the WHOLE pack (article,
  thread, script, metadata, LinkedIn, community drafts); a
  placeholder failure never excuses skipping the length measurement
  of the same file. Enforced: CODE (socialy_check.py prep ceiling +
  fixtures) + TEMPLATE (publishing skill ship path, RUNBOOK).
- **L-24 | Narration scripts are their own lint kind | 2026-10-23/24
  (Meo).** The ship gate's written-sign-off rule ("- That70s Da.")
  false-positives on episode narration scripts, which must carry the
  sign-off phonetically ("That seventies day") for TTS - the written
  form in a script would be spoken aloud wrongly. Rule: the linter
  takes --kind script (exempt from the written sign-off, requires the
  phonetic one); the ship gate auto-detects script files by filename
  and passes the kind through. Enforced: CODE (socialy_lint.py,
  socialy_check.py) + this entry.

## Weekend of 2026-10-24/25 - industrialized 2026-10-25 (Ravi's directive)

- **L-25 | PREFLIGHT - verify sessions before the run, not during it |
  2026-10-24/25.** LinkedIn's session was expired on both weekend
  mornings and YouTube's EP20 upload died in an open dialog Saturday
  night; every one of these was discovered MID-RUN, after other work
  had already flowed around the dead surface. Rule: every publish
  or engagement run starts with a session preflight - list every
  platform the run will touch, open each in the live browser, confirm
  the signed-in identity from the profile name or handle, and report
  pass/expired BEFORE any posting result; an expired session stops
  that platform only (manual-takeover sign-in ask; never a password
  retry). Enforced: TEMPLATE (publish_session_preflight skill +
  RUNBOOK step 0 + publishing-skill ship path + engagement routine).
- **L-26 | TOOL-BG-OUTPUT | 2026-10-24.** Two backgrounded exec video
  builds "completed" and their mp4s did not exist afterward;
  foreground-completed work persisted. Rule: media builds run as
  STAGED FOREGROUND builds (stage_build.py pattern - one card group
  per invocation), and the output file's existence + duration are
  verified after each stage before the next begins; a build that
  reports success with no file on disk is a failed build. Enforced:
  TEMPLATE (SPEC-studio B3, bumped v1.1 2026-10-25) + build-task
  text.
- **L-27 | GATE-COMMUNITY-LEN | 2026-10-24.** The first P3 community
  text was 288 chars by X's counter (8 over) with the button disabled
  in the composer, and the identical trimmed text posted to a second
  community was rejected by X's duplicate check ("Whoops! You
  already said that"). Rule: derivative texts (community posts,
  Notes, quote-posts) pass the same length measurement as tweets
  before handoff (prep ceiling 272, URL at t.co length in the
  poster's count), and each community gets DISTINCT wording written
  for it - never the same text twice. Enforced: CODE (ship gate
  measures COMMUNITY POST blocks) + TEMPLATE (SPEC-seo-growth,
  config growth comments, engagement routine).
- **L-28 | Site-error backoff | 2026-10-23/24/25.** Substack free
  subscribes failed three straight days and the daily Note four
  times in two days, every time with the platform's "Something went
  wrong" / "Failed to send note" - site errors, with zero warnings,
  limits or CAPTCHAs attached. Daily retries bought nothing and
  burned run time. Rule: a platform site error (distinct from a
  warning) gets a DECAYING retry cadence - skip the next run, then
  retry every other day - logged as a standing site issue until a
  run succeeds; warnings still stop the channel immediately and are
  never retried through. Enforced: TEMPLATE (config.yaml safety
  site_error_backoff + POLICY.md platform safety + healing-table
  row).
- **L-29 | Drive filing rides the intake job's scope | 2026-10-24/25.**
  Filing the Oct 24 Stocky originals (inbox -> consumed) stalled for
  a day: ad-hoc manual `files update` attempts from the operator's
  shell spawned their OWN approval cards (separate from the intake
  job's approved scope), one call hung outright, and a stuck
  equivalent write blocked retries. Rule: Drive filing moves ride
  the stocky-drive-intake job's own approved scope - let the cron
  path move files; do not improvise manual moves from an interactive
  shell. Ravi granted standing permission on 2026-10-25 for Meo to
  reorganize the Stocky handshake folders (inbox/consumed/acks/
  feedback) whenever needed without asking. Enforced: PROSE
  (RUNBOOK note) + the standing permission recorded here.
