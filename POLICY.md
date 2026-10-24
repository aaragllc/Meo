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
- Stop the channel's run on ANY warning, daily-limit message, CAPTCHA, or
  verification challenge. Never circumvent a block, never retry through it.
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
