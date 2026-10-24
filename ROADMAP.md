# Socialy.INK - roadmap (approved by Ravi 2026-10-22)

Sequencing rule: daily commitments run first every day; framework work fills
the gaps between them. Nothing in a framework phase may block a day's
publishing or engagement. Anything needing Ravi (relogins, verification codes,
decisions) is surfaced first and specifically, per his priority instruction.

## Daily commitments (every day, in this order)

1. Publishing pipeline: the day's article -> X thread -> LinkedIn overview
   post -> podcast episode -> YouTube at parity, all gates applied.
2. Socialy engagement run: N=5 comments + N=5 follows/connects per enabled
   channel (X, LinkedIn page, Substack, YouTube), config-driven.
3. Inbox filing/triage (3x daily cron), Stocky draft intake in the evening.
4. Blocker surfacing: sign-ins, codes, decisions - exact action + path.

## Phase 0 - today, Thu 2026-10-22 (launch day)

- [running] X: 5 replies live; Tuition/yield/Era threads + 5 follows finishing.
- [blocked on Ravi relogin] LinkedIn engagement run (5 comments incl. Crespo
  + 5 page follows); YouTube engagement run (5 comments + 5 subscribes);
  EP15/EP16 YouTube uploads (daily limit rechecked after sign-in).
- [running] Substack engagement run (5 comments + 5 subscribes).
- Rotation trio Post 1 "The safe places aren't safe either" ships today
  (article + thread + episode EP17; LinkedIn post follows the relogin).
- Listen-link batch (9 edits) + test-draft delete: one session with Ravi
  present for Substack codes.

## Phase 1 - Fri 2026-10-23 to Wed 2026-10-28 (codify)

- Trio Posts 2 (Fri) and 3 (Sat) ship with their cross-references landed.
- Week-2 audience one-pager lands Sun 2026-10-25.
- Write the foundation spec + one adapter spec per channel (X, LinkedIn,
  Substack, YouTube) + one spec per pipeline (publishing, engagement,
  production studio, audience ops), distilled from the live skills/memory.
- Cron rework: that70sda-reply-targets becomes the Socialy daily engagement
  run (all channels, reads config.yaml for N and toggles, escalation skips
  reported not posted). Config.yaml becomes the single source of truth.
- Engaged-target registry v1 (who we commented/followed, when; cooldowns).

## Phase 2 - Thu 2026-10-29 to Sun 2026-11-08 (harden)

- Standing parity audit: every article has episode + video + LinkedIn post +
  listen link; gaps reported weekly, fixed in batches.
- Run-log schema + failure taxonomy (gate / limit / sign-out / quality skip /
  escalation) with per-channel health in the weekly report.
- Production studio spec frozen around the audio baseline + two-gate video QC.

## Phase 3 - scale (starts when Ravi provides GitHub details)

- Move the platform repo to GitHub; docs + config + runbooks versioned there.
- Adapter template + persona-pack template; dry-run onboarding of one new
  channel or persona against the templates before any live run.

## Phase 4 - make it code (started 2026-10-22, Ravi's instruction)

- Toolkit in `tools/`: draft linter first (the policy gate as code), tested
  against the live prep files; then the parity checker and the run-log
  validator; wire all of it into BOOTSTRAP for the offline route.
- Expansion (persona #2 / channel #5) is the second half, gated on Ravi's
  creative direction; the onboarding path is already proven.

- Phase 5 (2026-10-23): self-learning/self-healing layer - see PLAN.md
  and SPEC-self-learning.md. Core live; polish items build when idle.
- Phase 6 addendum (2026-10-23): SEO + growth industrialized as a
  project rule - SPEC-seo-growth.md, the rule in POLICY.md and in the
  channel-onboarding path (adapter template section 10), ship-gate
  SEO/growth checks live; applies to every new channel at onboarding.
