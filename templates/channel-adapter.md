# Channel adapter spec - <Channel name> (<persona-slug>)

*(One filled-in copy of this template per channel surface per persona.
The foundation rules every adapter inherits - warm sessions, policy gate,
verbatim QC, run logging - are in `../../../SPEC-foundation-adapters.md`; this
document defines only what is specific to this channel. The seven-step
adapter contract every adapter implements: DISCOVER, FILTER, DRAFT,
CRITIQUE, POST, VERIFY, LOG, plus the channel's follow/subscribe
primitive where the platform has one.)*

## 1. Identity and account

- Persona identity acted as: <display name and handle, with URL>.
- Account kind: <personal profile / company page / publication / channel -
  and, if a page or publication, the admin model: whose profile administers
  it, and the hard rule about what that admin identity may never do
  publicly (e.g. never comment or follow as the admin when acting for the
  page)>.
- Account identifiers worth recording: <IDs a future operator would have
  to look up twice>.
- Account state at onboarding: <verification status, any one-time checks
  completed or outstanding, follower/subscriber count and date>.

## 2. Session model

- Session lives in: <the shared browser profile / connector / API - and
  how readiness is checked (visit the channel home; never assumed)>.
- Credential entry rule: automation never types credentials on this
  channel: <yes/no; if a service family forbids scripted login, say so
  and name the manual path - operator signs in by takeover, warm cookie
  reused>.
- Dead-session behaviour: <the run pauses this channel and surfaces the
  exact re-sign-in action; never a retry loop>.
- Fresh-window check: <whether per-window state on this platform can
  masquerade as a dead session, and the check to run before escalating>.

## 3. Publish flow

- Surfaces produced, in order: <what this channel publishes for a piece -
  e.g. article, then thread, then episode - and where it sits in the
  blog-first sequence>.
- Proven text-entry method: <the method that works in this channel's
  editor - paste/caret vs typing - and the methods known to mangle or
  destroy content here. If untested, say "untested - first publish is a
  supervised probe with a full live read-back".>
- Format rules: <character caps and silent truncations; paragraph/line-
  break behaviour of the editor; subtitle/description limits; sign-off
  placement; dated-overview or cross-promo requirements; media format
  gates (e.g. animated only)>.
- Gates that can interrupt a publish: <verification codes, reviews, caps -
  each with its taxonomy code from section 7 and the standing response>.

## 4. Engagement actions supported

- Comment/reply: <yes/no; where (feed, own posts, groups) and any identity
  mechanics - e.g. a per-post identity switcher that must be checked every
  time>.
- Follow/subscribe primitive: <what it is called, what it can target
  (people, pages, publications), and its limits>.
- Like/react: <yes/no, and the policy position for this persona>.
- Hard non-actions: <what this channel must never be used for - e.g.
  paying to unlock commenting, commenting somewhere the persona's identity
  cannot be selected>.
- Per-target restrictions: <paid-only or disabled comments and the like
  are a skip of that target, never a run stop>.

## 5. Pacing limits

- Volume keys in `../../../config.yaml` this adapter reads: <comments_per_day,
  follows_per_day for this channel; the author ceiling>.
- Intra-run gaps: <the configured randomized gap (default 2-6 min) and
  any channel-specific burst rule - e.g. thread posts minutes apart,
  never in one burst>.
- Start jitter: <the in-slot random delay (default 0-120 min)>.
- Young-account posture: <any reduced volume while the account is new,
  and what lifts it>.

## 6. Verification method

- Post-publish: <verbatim read-back of the live surface - full body for
  long-form, not just the edited region; visual inspection where the
  channel renders>.
- Per-action: <an action counts only when verified live; the URL/locator
  recorded in the run log and the target registry the same day>.
- Production QC gates, where this channel carries produced media:
  <the gates from the studio spec that apply, e.g. two-gate video QC>.

## 7. Known failure modes

Drawn from the taxonomy in `../../../SPEC-run-log.md`. List each mode this
channel has actually hit (or is known to hit), as: code - the channel-
specific trigger - the standing response. Vocabulary in force:

`GATE-CODE`, `GATE-CODE-STALE` (verification-code gates, incl. ~6/day
send throttle `QUOTA-CODE-SEND`); `EDIT-FILL-REPLACE`, `EDIT-PASTE-DRIFT`,
`EDIT-DRAG-SHORT`, `EDIT-SUBTITLE-TRUNC` (editor hazards);
`QUOTA-YT-UPLOAD` (upload caps); `SESS-WINDOW-STATE`, `CTRL-DEAD`
(session/UI); `VERIF-X-HV`, `VERIF-LI-CHECK` (platform verification);
`TOOL-EMPTY-OUTPUT` (local tooling).

- <CODE> - <trigger on this channel> - <standing response>.
- <A new failure gets logged under its code the day it is observed; a
  mode with no code yet is the trigger to extend the taxonomy, not to
  improvise.>

## 8. Parity obligations

From `../../../SPEC-parity-audit.md` - the surfaces this adapter owes for every
piece, and what each must carry:

- <Surface (e.g. article / episode / thread / overview post)>: <expected
  for which pieces; the required contents - links back into the system,
  overview, sign-off, dates for backlog>.
- <Cross-links this channel owns: e.g. article -> episode listen link,
  episode description -> article link.>
- Monitored-only variant: <if this channel is verified rather than
  posted to (the RSS pattern), say so here - the obligation is presence
  and correctness checks on the audit cadence, never assumed.>

## 9. Stop conditions

- Stop this channel's run immediately on: <any warning, limit message,
  CAPTCHA, or verification challenge on this platform - named as it
  actually appears>. Never circumvent, never retry through it. Record the
  stop in the run log with its taxonomy code and surface it in the run
  report, warnings first.
