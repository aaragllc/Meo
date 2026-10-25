# Socialy.INK - Self-learning and self-healing operations (Phase 5, v1)

Status: v1, 2026-10-23. This spec turns the platform's scar tissue into
machinery. Until now, lessons lived in prose (AGENTS.md, TOOLS.md,
MEMORY.md, run-log codes) and enforcement depended on the operator
remembering them at the right moment. Phase 5 gives every lesson a
lifecycle, every known failure a codified remedy, and the whole system
a heartbeat that checks itself.

## 1. The lesson lifecycle (self-learning)

Every operational lesson moves through five states. A lesson that is
not moving is not learned.

1. **Incident.** Something fails, surprises, or is caught by a human
   (Ravi caught the missing SEO fields; Meo caught the duplicate
   re-drop). The run that saw it records it in its run log with a
   taxonomy code from SPEC-run-log.md.
2. **Registration.** The lesson is entered in `LESSONS.md`: id, date,
   source incident, taxonomy code, the rule in one sentence, where it
   is enforced, and its enforcement class (below).
3. **Enforcement.** The rule is pushed as far down this ladder as it
   can go:
   - **Code** - a lint rule, the ship-gate runner, a render script
     assertion. Fires automatically, cannot be forgotten.
   - **Gate** - a check in `tools/socialy_check.py` that must pass
     before a ship or a state change proceeds.
   - **Template** - baked into the standing task text (browser publish
     instructions, cron bodies), so every run inherits it.
   - **Prose** - written guidance only. Acceptable for judgment calls;
     a failure that recurs while prose-only is a signal to promote it.
4. **Verification.** The enforcement is exercised: linter fixtures,
   the gate runner's state mode, the parity audit, or the next live
   occurrence passing clean.
5. **Promotion rule.** The same failure mode three times mints a new
   taxonomy code if none fits (per SPEC-run-log) AND forces the lesson
   one rung down the enforcement ladder. This is the rule already
   promised to Stocky for content gates; it now governs operations too.

The Sunday cycle carries an ops-health section (section 4) that walks
LESSONS.md: new incidents, promotions, lessons still prose-only.

## 2. The healing table (self-healing)

For every known failure: how it is detected, the remedy the operator
executes WITHOUT asking (safe and reversible), how the remedy is
verified, and what escalates instead. Improvisation at failure time is
what this table replaces.

| Code / failure | Detection | Auto-remedy | Verify | Escalate when |
|---|---|---|---|---|
| TOOL-EMPTY-OUTPUT (empty render) | render script asserts duration > 0 | re-run the render once, same recipe | duration + mean volume in range | second failure |
| Audio QC fail (window spread > ~2 dB) | render log windows | ONE fresh single-take re-render (never patch/splice) | new spread in range | second failure - ship decision to Meo/Ravi |
| Video animation fail (frame-change) | qa_frames.py | re-render via the episode build script once | frame-change passes | second failure |
| SESS-WINDOW-STATE (cold session mirage) | sign-in wall in one window | open a FRESH window and re-check before reporting a blocker | session confirmed warm | genuinely signed out - Ravi takeover ask |
| GATE-CODE (Substack publish/edit gate) | browser stops at dialog | if Ravi is present: MANUAL TAKEOVER is primary - he clicks Resend in the live window and enters the fresh code himself (proven P2 2026-10-23, P3 2026-10-24; L-06 extension). Sealed relay (newest code via verification_code) is fallback only - its handoff + approval round trips exceed the ~10-min code life and lost two codes on 2026-10-24 | publish completes | code rejected twice, or throttled (QUOTA-CODE-SEND) - park to next day |
| Site error, no warning (Substack "Something went wrong" / "Failed to send note" on subscribe or Note) | run log outcome on the action | NONE in-run beyond one retry - then the decaying cadence (L-28): skip the next run, retry every other day, logged as a standing site issue | a later run's action succeeds | never escalates as a failure; if the error ever arrives WITH a warning/limit/CAPTCHA it is reclassified as a platform warning (full stop row below) |
| GATE-CODE-STALE | code rejected as invalid | re-read inbox, take the NEWEST code email only, retry once | publish completes | second rejection |
| EDIT-PASTE-DRIFT (listen-line misfire) | full-body verify after edit | restore from Version history, re-insert with the confirmed caret method | full live body verbatim | second misfire on the same post - park it |
| EDIT-SUBTITLE-TRUNC | live subtitle ending check | shorten subtitle to <=200 complete sentence, re-set (edit gate rules apply) | live ending verified | edit gate throttled - next day |
| PLACEHOLDER in a ship file | ship-gate scan (socialy_check.py ship) | fill from the live source (published URL, refreshed figure) before any publish step | scan clean | source does not exist yet - the ship re-sequences |
| Parity gap (catalogue vs live) | parity checker / weekly audit | open a repair entry in the audit gap register; fix records immediately when the gap is clerical | checker exit 0 | gap is on a live surface - schedule the fix ship |
| Intake miss (drop un-acked > 2h) | watchdog poll of inbox + acks | run the intake consumption + ack on the spot | ack present in acks/ | drop malformed - ack says what's missing |
| Backup miss (archive stale > 26h) | watchdog reads the backup state file | re-run archive + Drive upload (standing permission) | byte-size verified in Drive | upload fails twice |
| Major change unbacked | sentinel (2h) polls git log vs backup state, classifying the range by the POLICY backups rule | run the intraday archive + Drive upload (standing permission) | byte-size verified; state file HEAD = repo HEAD | upload fails twice (nightly + watchdog floor remains) |
| VERIF-X-HV / any platform warning | in-run observation | NONE - full stop of that channel, report first | n/a | always escalates; never auto-retried |
| VERIF-LI-CHECK (LinkedIn security check) | login loop observed | NONE - never automated password retry; Ravi manual takeover | warm session persists | always escalates |
| Refresh flips a claim's direction | ship-day verification | hold the piece; ack question to Stocky + same-day flag to Ravi | Stocky's -v2 consumed | n/a - this IS the escalation path |

Rules above the table: a remedy runs at most once autonomously; the
second failure always escalates. No remedy ever touches identity,
money, or a platform warning. Every remedy execution is written into
the run log with its code, so the Sunday ops review can count heals
vs escalations.

## 3. The gate runner - tools/socialy_check.py

One command, two modes:

- `ship FILE [FILE ...]` - the pre-ship gate: lints every file
  (socialy_lint.py), scans for unresolved placeholders ([... URL],
  <URL>, TODO/TBD tokens in body lines), and reports subtitle/SEO
  presence for article prep files. Exit 1 blocks the ship.
- `state` - the platform self-check: parity checker against the live
  catalogue, run-log validation over logs/, and a coverage check that
  every taxonomy code in SPEC-run-log.md is registered in LESSONS.md.
  Exit 1 lists what's unwell.

BOOTSTRAP's daily-operation section gains: gate runner in `ship` mode
before every publish sequence; `state` mode in the Sunday review.

## 4. The watchdog + Sunday ops-health

- **Watchdog cron (daily, morning):** runs `socialy_check.py state`;
  polls the Drive intake for un-acked drops older than 2h and the
  backup state file for staleness; executes the two standing remedies
  in the healing table (intake consumption, backup re-run); reports
  ONLY on a failure or a heal - silence means healthy.
- **Major-backup sentinel (every 2h):** enforces the POLICY.md
  backups rule - an intraday archive for any major commit settled
  more than 45 minutes with no backup at its HEAD (clean tree
  required, 2-hour coalescing window). Silent unless it uploads or
  fails twice.
- **Sunday ops-health (inside the weekly review):** failures by code
  for the week, heals vs escalations, lessons registered/promoted,
  prose-only lessons aging, and the gate runner's state output. This
  is the operational mirror of the Stocky feedback digest: the
  audience loop learns what resonates; the ops loop learns what breaks.

## 5. What v1 does not do

- No remedy touches a live publishing surface autonomously beyond the
  two standing permissions (intake, backup). Publishing fixes still
  flow through the normal ship path.
- No cross-agent auto-edits of Stocky's drafts; content healing stays
  the ack/feedback loop.
- Expansion (persona #2) remains parked; Phase 5 deepens the one
  operation that exists before widening it.
