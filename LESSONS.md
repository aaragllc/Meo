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
- **L-03 | EDIT-PASTE-DRIFT | 2026-10-22/23.** Pasted lines drift to
  the wrong paragraph in the Substack editor. Rule: the listen-line
  method is click sign-off, Home, Enter, verified caret in the new
  empty paragraph, then paste (confirmed clean 2026-10-23 on P2).
  Enforced: TEMPLATE (edit tasks carry the method verbatim).
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
- **L-24 | Narration scripts are their own lint kind | 2026-10-23/24
  (Meo).** The ship gate's written-sign-off rule ("- That70s Da.")
  false-positives on episode narration scripts, which must carry the
  sign-off phonetically ("That seventies day") for TTS - the written
  form in a script would be spoken aloud wrongly. Rule: the linter
  takes --kind script (exempt from the written sign-off, requires the
  phonetic one); the ship gate auto-detects script files by filename
  and passes the kind through. Enforced: CODE (socialy_lint.py,
  socialy_check.py) + this entry.
