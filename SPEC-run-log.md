# Socialy.INK - Run-log schema + failure taxonomy (Phase 2, v1)

Status: v1, 2026-10-22. Every Socialy run writes one log in this schema and
classifies every non-success outcome with a taxonomy code from section 2.
Codes are stable: never rename or reuse one; new failures get new codes
appended here.

## 1. Run-log schema

### Location and retention

- Canonical home: `~/workspace/socialy-ink/logs/`, one file per run,
  named `<kind>-<YYYY-MM-DD>-<seq>.md` (seq = 01, 02... within the day).
  Kinds: `engagement`, `publishing`, `production`.
- Legacy note: day-1 engagement detail logs live in the operating goal's
  `hidden_files/` (`engagement-log-<date>.md`); new runs log here only.
- Retention: run logs are kept indefinitely - they are the audit trail the
  weekly report counts from. Scratch (page dumps, screenshots) is not part
  of the log and is not retained.

### Per-run header (required fields)

```yaml
run_id: 20261022-engagement-01        # YYYYMMDD-<kind>-<seq>
date: 2026-10-22                      # local date of the run
kind: engagement                      # engagement | publishing | production
channels: [x, substack, linkedin_page, youtube]
operator: meo (browser profile: default; windows: <ids or n/a>)
config_ref: config.yaml @ <git hash or mtime> + POLICY.md @ <same>
started_local: 2026-10-22T09:47-07:00
finished_local: 2026-10-22T14:05-07:00
status: completed                     # completed | partial | blocked | aborted
totals: {attempted: 20, succeeded: 17, skipped_policy: 2, failed: 1, parked: 0}
failure_tally: {EDIT-PASTE-DRIFT: 1}  # counts by taxonomy code, section 2
```

### Per-action rows (one per attempted action, in execution order)

| field | content |
|---|---|
| `id` | sequential within the run (A01, A02...) |
| `channel` | x \| substack \| linkedin_page \| youtube \| spotify (monitor) |
| `target` | account/publication/channel name + registry key when one exists |
| `action` | comment \| reply \| follow \| subscribe \| publish_post \| publish_episode \| upload_video \| render_audio \| render_video \| edit_existing \| delete |
| `locator` | live URL / URN / workspace file path proving where it landed |
| `verification` | method + result: `composer_verbatim`, `live_read_full`, `live_read_partial`, `frame_change_qc`, `loudness_spread`, `studio_content_list`, `none` |
| `outcome` | `success` \| `skipped_policy` (name the policy rule) \| `failed:<CODE>` \| `blocked:<CODE>` \| `parked:<CODE>` |
| `notes` | one line: counts verified in-session, restore/QC evidence, hand-off state |

Rules:
- An action is logged when it is attempted, not when it is planned. Targets
  dropped at the filter stage appear once, as `skipped_policy`, not per draft.
- `verification: none` on a `success` is a schema violation - nothing ships
  unverified; if verification was impossible, the outcome is
  `parked:<CODE>` (usually EDIT-DRAG-SHORT or CTRL-DEAD), never success.
- A failure that ends a channel or the run still gets its action row, and the
  run header's `status` and `failure_tally` reflect it.

## 2. Failure taxonomy

Classes: `platform_gate`, `editor_hazard`, `quota`, `session`,
`verification`, `tooling`. Severity: S1 = wrong/harmful content live or account at
risk; S2 = blocks progress until resolved; S3 = degrades or delays, a
workaround or park exists. Scope: what the failure blocks - `run`,
`channel`, or `item`.

### platform_gate

**GATE-CODE** - Substack demands a 6-digit email code ("Check your email")
before a publish or an edit-update completes. Fires on cold-session
publishes AND separately on edits to published posts, even inside a session
already trusted for publishes.
Observed: 2026-10-20 (Post 3 + server-makers publishes gated; both
listen-link edits gated in the warm session); 2026-10-22 (articles 4, 5, 6
of the listen-link batch each gated individually; the code relay + operator
card approval cleared each).
S2 - blocks: item (run continues once the code lands).
Standing response: stop at the dialog; exactly one code request in flight;
only the NEWEST code email is valid; enter it in the window whose dialog is
open, in real time (sealed Gmail relay or operator takeover). Never open a
second dialog, never pre-request a code.

**GATE-CODE-STALE** - a code is rejected because it expired (~10 min) or was
superseded by a newer request before entry.
Observed: 2026-10-20 - two codes expired during the chat-approval
round-trip; the relay once delivered a superseded code and Substack
rejected it as invalid.
S3 - blocks: item.
Standing response: discard the stale code, request ONE fresh code with the
operator already standing at the dialog; if a second staleness occurs in
the same session, park the item for a with-operator session.

### editor_hazard

**EDIT-FILL-REPLACE** - fill/typing entry into the Substack editor body
field REPLACES the entire article body with the inserted text, and the
truncated version can publish.
Observed: 2026-10-21 - the Post 4 listen-link edit published a body
containing only the listen line; caught on live read, repaired from Version
history. (The same day, presence-only verification wrongly reported a
success - the reason `live_read_full` exists in the schema.)
S1 - blocks: item, plus immediate repair duty.
Standing response: fill/typing on the body field is banned absolutely.
Insert only by non-destructive paste/caret. After ANY edit publish, verify
the FULL live body paragraph by paragraph. If it fires: Version history ->
restore last published version -> re-insert -> verify full text in the
editor before Update.

**EDIT-PASTE-DRIFT** - a paste does not honor the verified caret: the text
lands mid-paragraph or mid-word, glues to a paragraph front, or merges
into / appends after the sign-off paragraph.
Observed: 2026-10-22 - rotation P1 article (3 attempts, 3 wrong landings);
yield and Era articles (merged into the sign-off on every method);
Record high, Grading, Reading the dashboard, Friday's alarm (appended
after the sign-off). One article (One green day) succeeded via click
sign-off -> Home -> Enter -> paste. All failures were draft-only and
restored from Version History; no live article was harmed.
S2 - blocks: item.
Standing response: one paste attempt per item per session. On drift:
restore the draft from Version History (Published version), verify the
original in full, park the item for a hand finish in a with-operator
session. Never retry-thrash an editor.

**EDIT-DRAG-SHORT** - the Substack settings (welcome-email) editor defeats
automated text entry: short strings will not drag, the single-line staging
field strips newlines (collapsing a two-paragraph block into one line),
and the editor's visual state can diverge from its DOM, making the result
unverifiable.
Observed: 2026-10-22 - welcome email: paragraphs 1-5 placed by drag; the
13-character sign-off would not drag by any method; the merged-block
workaround lost its line break; final state unverifiable, so all unsaved
changes were discarded and the email left at its default.
S3 - blocks: item.
Standing response: never save an unverifiable state. Discard, leave the
setting at its prior state, and hand the item to the operator for a
30-second manual paste via takeover.

**EDIT-SUBTITLE-TRUNC** - Substack silently truncates post/episode
subtitles at 200 characters at publish, mid-sentence, with no warning.
Observed: 2026-10-22 - rotation Post 1's 264-char subtitle went live ending
"...The first piece in a new".
S3 - blocks: item (degrades live copy until re-edited).
Standing response: draft every subtitle at <=200 characters, complete
sentences only; verify the live subtitle's ending after every publish;
fix by shortening + re-verify (the Post 1 fix shipped clean the same day).

### quota

**QUOTA-YT-UPLOAD** - YouTube daily upload cap on a channel that has not
completed the one-time phone verification.
Observed: 2026-10-21 - the 10-video backlog batch consumed the day's
allowance; 2026-10-22 - the first EP15 attempt hit "Daily upload limit
reached" again. RESOLVED 2026-10-22: the operator completed phone
verification and EP15/16/17 uploaded the same day. Code retained for
history; recurrence would mean a new, different cap - log and escalate.
S2 - blocks: channel (uploads only; comments/subscribes unaffected).
Standing response: queue newest-first under the cap; never split a series
out of order to beat it; the fix is the one-time verification, which is
the operator's action, not a retry strategy.

**QUOTA-CODE-SEND** - Substack stops sending verification-code emails
after roughly 6 code requests in a day; Resend clicks produce no email.
Observed: 2026-10-20 evening - no code email arrived after 15:50 PT
despite repeated attempts.
S2 - blocks: channel (all gated work) for the rest of the day.
Standing response: never spam Resend (it spends the budget and mints
superseding codes). Park gated items, retry next day on a fresh budget;
batch gated edits into one operator-present session by design.

### session

**SESS-WINDOW-STATE** - a single browser window presents as signed out or
broken while the shared profile's session is actually live; the failure is
per-window state, not a dead session.
Observed: 2026-10-22 - LinkedIn, YouTube, and Substack "sign-in blockers"
all turned out to be live warm sessions when checked in a fresh window.
Also 2026-10-22: one Substack session's editors stopped scrolling and its
menus misrouted, while other windows handled the same editors normally.
S3 - blocks: item until re-windowed.
Standing response: open a fresh window and re-check session state BEFORE
escalating any sign-in to the operator. Only a failure that reproduces in
a fresh window is a real session failure.

**CTRL-DEAD** - a platform control renders and accepts clicks but does
nothing: no dialog, no navigation, no error.
Observed: 2026-10-21 and 2026-10-22 (two sessions) - the Delete Post
button (Post Settings > Danger zone) for throwaway draft 221306444 never
responded; the draft is still in Drafts. The drafts-list "..." menu in the
same area navigated to the editor instead of opening a menu.
S3 - blocks: item.
Standing response: two honest attempts maximum, in different sessions if
available; then park the item for the operator (a seconds-long manual
action) - never force a destructive action through a misbehaving UI.

### verification

**VERIF-X-HV** - X presents a human-verification challenge; automation
must not solve or circumvent it.
Observed: at the @That70sDa account launch (2026-10-13/14) - one
challenge shown during early activity.
S2 - blocks: channel.
Standing response: stop ALL X activity immediately, report, and let the
operator resolve it in person if they choose. Any platform warning on X
is treated the same way: full stop, no retry.

**VERIF-LI-CHECK** - LinkedIn's security-check loop triggered by automated
password login from a datacenter IP (standing note, AGENTS.md 2026-10-14).
Observed: the persona's original LinkedIn path died here; the surviving
model is the company page under the operator's real profile.
S2 - blocks: channel.
Standing response: NEVER attempt an automated password login to LinkedIn.
The operator signs in manually via takeover; the warm cookie is reused;
on expiry, repeat the manual login - do not fall back to credentials.

### tooling

**TOOL-EMPTY-OUTPUT** - a local production tool invoked with a missing
required flag silently produces an empty artifact (observed 2026-10-19:
`tts speak` without `--output` wrote empty MP3s; TOOLS.md).
S3 - blocks: item.
Standing response: verify every render's duration and loudness before it
enters the pipeline; the invocation contract for each tool lives in
TOOLS.md and the studio spec - follow it verbatim.

## 3. Referencing the codes in reporting

- Outcome strings carry the code verbatim (`failed:EDIT-PASTE-DRIFT`,
  `parked:GATE-CODE`, ...). A code in a log always means the definition in
  this file - free-text failure descriptions go in `notes`, never instead
  of a code.
- The run header's `failure_tally` counts codes for that run; the weekly
  report (audience one-pager) aggregates tallies across the week's logs
  into: count by code, count by channel, blocked-scope totals (items /
  channel-blocks / run-blocks), first and last seen, and any code whose
  count rose week over week.
- A failure that matches no code is logged as `failed:UNCLASSIFIED` with a
  full description in `notes`; three occurrences of the same unclassified
  failure oblige a new code in this spec before the next weekly report.
- Resolved codes (e.g. QUOTA-YT-UPLOAD) stay in the taxonomy, marked
  RESOLVED with the date; their weekly count should be zero, and any
  recurrence is reported as a regression, not a new code.
