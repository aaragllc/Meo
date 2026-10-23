# Socialy.INK - build plan (proposed 2026-10-22)

Goal: everything hand-built for that70sda becomes a platform that runs
predictably and repeatably, so a new persona or a new channel is a config
change plus one adapter - not a new pile of one-off sessions.

## Architecture: foundation + layers

### Layer 0 - Platform foundation (common to all channels and personas)

- **Identity & sessions.** Anonymity rules; warm browser sessions per account;
  sign-in playbooks per platform (LinkedIn: manual takeover only, never
  automated passwords); credentials stay in the vault, never in docs or logs.
- **Config.** One config file drives volume and toggles: N comments/day and
  N follows/day per channel (default 5), target freshness window, follower
  ceiling, pacing windows, per-channel enable flags.
- **Policy engine.** Voice rules, hard bans (hype words, buy/sell calls,
  invented numbers, tickers), escalation triggers -> skip + report, QC gates,
  stop-on-any-platform-warning, never circumvent a block.
- **Scheduler.** Daily slots with built-in randomization (0-120 min jitter,
  human-plausible hours), one run per pipeline per day, retries never repeat a
  possibly-completed action.
- **Reporting & memory.** Per-run logs, a consolidated daily report in chat,
  weekly audience one-pager, metrics snapshots, people/relationship files,
  an engaged-target registry (no repeat targets inside a cooldown window).
- **Escalation.** Chat ping with the exact action needed; email to the
  attention address when a blocker sits unresolved ~48h on the critical path.

### Layer 1 - Channel adapters (channel-specific, one contract)

Contract: discover -> draft -> critique -> policy gate -> post -> verify -> log,
plus follows/connects where the channel supports them.

- **X.** Posts/threads, replies, follows. Quirks: young-account daily action
  caps (hit 2026-10-16 and 2026-10-21) - pacing and stop-on-limit are adapter
  rules; replies under 200 chars.
- **LinkedIn (company page).** Posts, feed comments, page follows. Quirks:
  composer identity switcher is per-post (check every time); pages cannot
  comment in Groups or follow people; follows go through Manage following;
  single-Enter paragraph formatting; manual-takeover sign-in only.
- **Substack.** Articles, podcast episodes, comments, follows/subscribes.
  Quirks: email-code verification gates on publishes/edits (one gated session
  with the human present, newest code only, daily code budget); editor accepts
  non-destructive inserts only; sections per content type.
- **YouTube.** Uploads, comments, subscribes. Quirks: daily upload limit
  (verification declined for anonymity; wait for reset); every upload passes
  the two-gate video QC (animation + audio baseline).
- **Spotify.** No direct actions - parity by RSS from Substack; monitored, not
  operated.
- **Future channels** (Instagram, Threads, TikTok, etc.): new adapter doc +
  config block; the engine, policy, and reporting do not change.

### Layer 2 - Automation pipelines (what runs on the foundation)

1. **Publishing pipeline (the posting framework).** Draft intake (Stocky) ->
   content-level dedup -> fact verification -> humanize pass -> continuity
   pass (callbacks, open-loop closes, forward references, lateness bridge) ->
   Substack article -> X thread -> LinkedIn overview post -> podcast episode
   -> YouTube at parity. Standing gates: overview description on every post,
   written sign-off, companies not tickers, schedule decided by the platform,
   not the draft.
2. **Engagement engine (Socialy core).** Daily per channel: N comments +
   N follows/connects from config. In-lane discovery, bot/spam filtering,
   critique pass, escalation skips logged for human calls. This is the
   pipeline that replaces hand-run reply sessions.
3. **Production studio.** Narration scripts (headings become spoken bridges,
   humanization: fillers/pauses per the standing recipe) -> single-take TTS on
   the frozen audio baseline (one voice, one uniform gain, loudness-spread
   acceptance ~2 dB) -> no-editing rule (flawed renders are remade or kept,
   never patched) -> animated video builds (narration-synced cards) ->
   two-gate QC -> metadata with real descriptions and cross-links.
4. **Audience ops.** Inbox filing and triage (labels, archive-never-delete,
   drafts and real people stay in inbox), metrics snapshots, weekly one-pager,
   relationship tracking, monetization-readiness checks against thresholds.

### The that70sda persona system (tenant #1, the reference implementation)

- Governing directive + voice profile + segments (scorecard, Tuition Tuesday,
  Era file, Ask the 70s) + continuity rules live as the persona pack; the
  platform runs any persona pack, that70sda is simply the first.
- Persona pack = directive doc, publishing skill, TTS skill, templates
  (LinkedIn post template, welcome email), brand assets (badge, banner,
  palette). A second persona = a second pack, same platform.

## Phases

- **Phase 0 - today (2026-10-22).** Finish the approved launches under the new
  runbook: X replies/threads/follows (running), EP15+EP16 YouTube uploads,
  the 9-edit listen-link batch (human present for codes), and the first full
  engagement run: LinkedIn 5 comments + 5 page follows, Substack 5 comments +
  5 follows, YouTube 5 comments + 5 subscribes. EP15 ear verdict logged: pass.
- **Phase 1 - this week.** Codify: foundation spec, one adapter spec per
  channel, one spec per pipeline (docs in this workspace, distilled from the
  existing skills and memory). Rework the daily cron from reply-drafts-for-
  approval to the framework engagement run (all channels, config-driven).
  Config becomes the single source for N and toggles.
- **Phase 2 - harden (next 1-2 weeks).** Engaged-target registry with
  cooldowns, run-log schema, failure taxonomy (gate/limit/sign-out/quality
  skip), weekly platform health report folded into the audience one-pager,
  backlog parity checks (every article has episode, video, LinkedIn post,
  listen link) as a standing audit.
- **Phase 3 - scale.** Move the repo to GitHub when Ravi provides details;
  adapter template + persona-pack template so channel #5 or persona #2 is a
  fill-in exercise; only then consider multi-persona runs.
- **Phase 4 - make it code (started 2026-10-22 on Ravi's instruction).**
  Turn the platform's deterministic core into a tested local toolkit in the
  repo (`tools/`): (1) draft linter - the policy gate as code (em dash,
  tickers/cashtags, banned hype words, sign-off, subtitle and SEO limits);
  (2) parity checker - emits the audit table from catalogue records;
  (3) run-log validator - enforces the SPEC-run-log schema and taxonomy
  codes; (4) wire the toolkit into BOOTSTRAP so the offline route can run
  it with no agent account at all. The expansion track (persona #2 or
  channel #5) is Phase 4's second half and waits on Ravi's creative call;
  the onboarding path is already proven by the Phase 3 dry run.

## Decisions needed from Ravi

- GitHub repo details (when ready - Phase 3 only, nothing blocks on it).
- Anything in the phasing he wants reordered; N changes are config edits,
  no approval needed per change.

## Phase 5 - Self-learning and self-healing operations (added 2026-10-23, Ravi's direction)

Spec: SPEC-self-learning.md. Core built same day: LESSONS.md registry (22
lessons, every taxonomy code registered), tools/socialy_check.py gate
runner (ship gate + platform state), healing table (detect -> remedy ->
verify -> escalate per failure code), daily ops watchdog cron with two
standing auto-remedies (intake consumption, backup re-run), ops-health
section in the Sunday review. Engagement cron revised to emit
SPEC-run-log-schema logs (first conforming log: 2026-10-24 run). State
check at build time: HEALTHY (parity 0 new gaps, 13/13 codes covered).
Remaining Phase 5 polish (build when idle): BOOTSTRAP wiring of the gate
runner into the daily-operation section; ops aggregator over run logs
for the Sunday ops-health numbers.

## Phase 6 - Growth industrialization (approved 2026-10-23, Ravi)

The growth audit (goal files/growth-audit-2026-10-23.md) built as platform,
not one-offs: recommendations graph ON with the warm eight; tag taxonomy +
Notes cadence + quote-post + Communities test wired into the engagement
run; Shorts pipeline (build_shorts.py) at 1/episode; YouTube playlists,
search-clause titles, pinned comments, end screens in the upload path;
episode follow line in the metadata template; LinkedIn milestone 150
tracked in the Sunday ledger; Apple Podcasts claim attempted (identity
wall = Ravi's call); welcome email stays Ravi's manual paste. Every lever
measured in the Sunday growth ledger; a lever producing nothing in 4
weeks gets cut.
