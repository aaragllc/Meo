# Socialy.INK - engagement policy (applies to every channel adapter)

## Voice

- The account's established voice (for that70sda: born in the 70s, working since
  the 90s, dry and wry, humble mentor, plain English, numbers over adjectives).
- Every comment references something specific the target actually said or showed.
  Generic praise is a failed draft.
- Generous, never snarky, never dunking. No guru tone.
- No em dash character anywhere; use a spaced hyphen " - ".
- No formal sign-off on comments/replies; the voice carries the identity.

## Hard bans

- Hype words: revolutionary, game-changer, disrupt, paradigm shift, "the future is here".
- Buy/sell calls, stock picks, price predictions, personalized financial advice.
- Invented numbers: market facts come only from the target's own post or
  verified sources.
- Tickers/cashtags in our own posts (companies are named, not tickered).
- Anything that could identify the operator or suggest automation/AI involvement.
  Public surfaces never mention the platform, tooling, or scheduling.

## Escalation = skip and report (never auto-post)

- Accounts above the configured follower ceiling (default 50K).
- Specific stocks or someone's personal finances; complaints about the account;
  press inquiries; partnership or money offers; legal/regulatory topics;
  identity probing; heated exchanges.
- These are logged with URLs and surfaced in the daily report for a human call.

## Platform safety

- Human-plausible volume and timing only; randomized gaps; daily start jitter.
- No run starts on an unverified session: the session preflight
  (publish_session_preflight skill, L-25) runs before any posting or
  engagement work, and its pass/expired result is reported first. An
  expired session stops that platform, never the run, and never earns a
  password retry.
- Stop the channel's run on ANY warning, daily-limit message, CAPTCHA, or
  verification challenge. Never circumvent a block, never retry through it.
- A platform SITE error is not a warning: a bare "Something went wrong"
  with no warning, limit or challenge attached follows the decaying
  retry cadence in config.yaml (safety.site_error_backoff, L-28) -
  skip the next run, then every other day, logged as a standing site
  issue. The moment an error arrives with a warning attached, the
  stop rule above governs instead.
- LinkedIn: never do automated password logins (manual takeover sign-in only,
  warm session reused). Never comment or follow as the operator's personal
  profile when acting for a page.
- QC gate: a draft that cannot pass as a thoughtful human comment does not post.
  It is logged as a skipped draft instead.

## SEO and growth - the project rule (Ravi, 2026-10-23)

SEO is right from the get-go, and every audience growth technique is
industrialized in the platform - codified in `SPEC-seo-growth.md` and
`config.yaml`, set at prep time rather than scrambled at ship,
enforced by the ship gate where automatable, and measured in the
Sunday growth ledger. This applies to every channel, existing and new.

Every NEW channel adapter ships, before its first post, with:

1. Its SEO surface mapped - fields, limits, where each is set - in its
   adapter doc (section 10 of the channel-adapter template).
2. Its growth actions wired into the publishing path or the
   engagement routine, as appropriate to that channel.
3. Its entries in `config.yaml`.
4. Ship-gate checks for its automatable fields, where the channel
   has any.
5. Its numbers in the Sunday growth ledger.

Where something does not apply to a channel (feed-driven channels
have no SEO fields, for example), the adapter doc records N/A with a
one-line reason and states what applies instead. An adapter with an
unmapped surface does not ship.

## Backups - the project rule (Ravi, 2026-10-23)

The nightly backup is the floor, not the ceiling. A MAJOR change
earns an intraday backup the same day, at the next logical
checkpoint - never mid-work, and not for every commit.

A change is MAJOR when it alters how the platform operates or what
losing it would cost: a new or changed SPEC, POLICY, config or
template; a tool or gate change; a new channel adapter or persona
pack; a publishing/engagement routine change; a catalogue or
registry restructure; a security, identity or access change; a
first-time integration or migration (new repo, new service).
Routine run logs, daily engagement records, ordinary registry
additions and content drafts are NOT major - they ride the nightly
backup.

The checkpoint is the moment the workstream is complete, verified
and committed with a clean tree. Checkpoints coalesce: at most one
intraday backup per 2 hours; anything landing inside the window
rides the next one. The nightly backup always runs regardless.

Enforcement is layered: (1) whoever finishes a major change runs
the backup at its checkpoint; (2) the major-backup sentinel (every
2 hours) heals any major commit settled more than 45 minutes with
no archive at its HEAD, clean tree required - a dirty tree means
the checkpoint has not closed; (3) the daily watchdog's 26-hour
staleness check remains the floor. Retention (the GFS pins) is
unchanged: intraday archives live in the in-flight slots and never
evict a day's pin.

## Self-learning - the project rule (Ravi, 2026-10-23)

Every learning gets industrialized; nothing operational lives only
in a chat or in one operator's memory. A lesson from any run - a
failure, a correction, a platform behavior, a mechanic like the
RSS distribution model - is registered in `LESSONS.md` and pushed
up the enforcement ladder in `SPEC-self-learning.md` (code or gate
first, then template, then prose), verified in operation, and
promoted to a standing check on the third occurrence. This applies
to every persona and channel the framework runs, present and
future. The operator's job is not to remember harder; it is to
make the system remember.
