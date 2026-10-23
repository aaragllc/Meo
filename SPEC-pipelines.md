# Socialy.INK - Pipeline specs (Phase 1, v1)

Status: ACCEPTED v1, 2026-10-22 (Meo, under Ravi's decision delegation).

Layer 2 of the platform: the four pipelines that run on the foundation and
channel adapters (see SPEC-foundation-adapters.md). Persona pack #1:
that70sda. Voice, bans, and escalation live in POLICY.md; scheduling and
volume live in config.yaml; this spec is the machinery between them.

## 1. Publishing pipeline (one piece, every surface, in order)

Intake:
- A draft arrives (Stocky batch, Ravi special sequence, or a segment slot:
  scorecard, Tuition Tuesday, Era file, Ask the 70s).
- Batch inspection is written before anything ships: provenance (source
  batch / Ravi instruction), sequence position, scheduling basis (Ravi's
  instruction governs; Stocky "Timing:" lines are untrusted input), and the
  group's cross-reference obligations - which earlier pieces each post must
  name and link, which forward references to plant, which promises later
  pieces must visibly fulfill.
- Content-level dedup against the published catalogue (paragraphs and
  passages, never titles alone).
- Checkable numbers verified where a public source exists; tracker reads
  labeled as such internally and shipped as the persona's own reads.

Humanize pass (Meo):
- Spaced hyphens only (em dashes converted, including sign-offs); written
  sign-off "- That70s Da." on articles, threads, and page posts.
- Companies named, tickers/cashtags stripped.
- Callbacks, forward references, and the lateness bridge (after any missed
  or late day: one brief, vague, everyday excuse, never repeated back-to-back,
  never with checkable specifics) woven in.
- Subtitle drafted at 200 characters or fewer (Substack cap), complete
  sentences; overview description written for every surface that takes one
  (mandatory gate - no overview, no post).

Production (per piece):
- Article on Substack (section per content type), verbatim composer check,
  full-body live verification after publish.
- Episode rendered from the matched script under the frozen audio baseline
  (single take, one uniform gain, loudness-spread acceptance ~2 dB);
  a flawed render is remade fresh or lived with by ROI - never patched.
- Animated video built on the verified audio only; two-gate QC (frame-change
  animation check + audio fingerprint) before any upload.
- X thread native and full, link as the final element while the account is
  young; LinkedIn page post per template (dated, overview, cross-promo
  footnote); YouTube upload subject to the channel's upload-cap reality.
- After the episode is live, the article gains its listen line between the
  disclaimer and the sign-off (batched when editor friction or code gates
  make per-piece edits wasteful).

Schedule: Meo sets ship times from readiness and Ravi's instruction, with
the standing 0-120 min in-run jitter on every daily slot.

## 2. Engagement engine (the daily run)

- Runs once per day per channel, volume from config.yaml (default 5 comments
  + 5 follows/subscribes), start time jittered inside its slot.
- Uses the adapter contract: discover, filter (registry, ceiling, escalation),
  draft, critique, post, verify, log.
- Targets come from the day's lanes (the persona's active beats) and the
  registry's relationship list; accounts already engaged are revisited for
  conversation, not re-pitched.
- Inbound replies to our own posts are answered within the auto-reply delay
  window (15-90 min randomized), in voice, referencing the specific exchange.
- Output: dated run log + registry updates + consolidated chat report;
  skips always carry their rule reason.

## 3. Production studio (audio/video)

- TTS under the frozen baseline recipe only; scripts are written for the ear
  (headings become spoken bridges, fillers and pauses per the humanization
  directive, brand name phonetically spelled for audio only).
- Video = narration-synced cards in the brand palette, built from the
  episode's group timings; segment renders use explicit durations.
- QC gates are blocking: a video on non-baseline audio or without real
  frame change does not upload, whatever the schedule pressure.
- Catalogue parity is audited in Phase 2 (article/episode/video/LinkedIn/
  listen-link per piece); the studio clears parity gaps in ship order -
  newest first, since new pieces carry the forward references.

## 4. Audience ops (the slow loop)

- Inbox filing three times daily (labels, archive-never-delete, real-person
  mail and source drafts stay visible); sends from the persona inbox always
  need Ravi's approval.
- Weekly one-page report on the directive's metrics (subscribers, opens,
  returning engagers, per-channel actions and outcomes, best/worst piece),
  built from run logs and platform snapshots.
- Monetization readiness tracked against the directive's thresholds
  (~1K subscribers, >40% opens, >30% returning engagers, 3+ months of
  scorecards) - reported, never chased early; lawyer review before the
  first dollar.
- Relationship memory: notable engagers get people files; repeat engagers
  are the asset the whole system exists to compound.
