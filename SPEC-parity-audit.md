# Socialy.INK - Standing parity audit spec (Phase 2, v1)

Status: v1, 2026-10-22. Persona pack #1: that70sda. Companion docs: SPEC-foundation-adapters.md,
SPEC-pipelines.md, POLICY.md, config.yaml. First audit: parity-audit-2026-10-22.md.

## What parity means

The Substack article is the source of truth for every piece. A piece is AT PARITY when every
applicable surface exists, is publicly reachable, and points back into the system:

| Surface | Expected for | Notes |
|---|---|---|
| Substack article | every piece | The source of truth; carries subtitle (200 chars or fewer), overview, sign-off |
| Podcast episode (Substack, Podcast section) | every article except the intro | Episode-specific subtitle + full description; description links the article |
| Spotify episode | every episode | Arrives by RSS pull from Substack; presence is verified, never assumed |
| YouTube video | every episode (+ trailer) | Animated version only, two-gate QC (animation + audio baseline); description carries the overview, article + episode links, and the original publish date for backlog uploads |
| X thread | every article | Full native thread while the account is young; Substack link as the final tweet |
| LinkedIn overview post | every article | Dated, crisp overview, cross-promo footnote (Substack, YouTube, Spotify, X), listen/watch line where a video or episode verifiably exists |
| Article -> episode listen link | every article with an episode | "Prefer to listen? The audio version is here: <episode URL>" between the disclaimer and the sign-off |
| Episode -> article link | every episode | Inside the episode description |

Non-article audio (the trailer) is audited on its own surfaces: Substack, Spotify, YouTube.

## How the audit runs

- Cadence: weekly, compiled as part of the Sunday review spine, alongside the internal audience
  one-pager. The one-pager reports audience numbers; the audit reports surface completeness.
  They share the week's piece list and nothing else.
- Method: records-first. The auditor works from the catalogue records (MEMORY.md, goal
  hidden_files, run logs, prior audits) and marks each surface Present / Missing / No record.
  "No record" is a finding, not an assumption: it means the records cannot prove the surface
  exists, and the next live check either confirms it (record updated) or converts it to Missing.
- Scope: every piece published since the last audit, plus a rolling re-check of any surface
  previously marked Missing or No record. New pieces are audited the Sunday after they ship.
- Output: one audit file per week, `parity-audit-YYYY-MM-DD.md` in this workspace, in the
  report format below. The audit never edits live content; fixes are separate, dispositioned work.

## Gaps vs accepted exceptions

- GAP: an applicable surface is Missing or unverifiable (No record) and no standing decision
  covers it. Every gap gets a named disposition in the audit: fix (with the route), verify
  (what check, by when), or escalate.
- ACCEPTED EXCEPTION: a surface is absent or substituted under an explicit, dated decision by
  Ravi or a standing rule. The audit records the exception WITH its provenance (who decided,
  when, why) and does not re-flag it as a defect in later audits; it is carried in the
  exceptions register inside each audit until the underlying decision changes.
  Examples of standing exceptions: a LinkedIn listen line may point to the Substack episode
  instead of YouTube where that was the verified link at post time; work explicitly parked by
  Ravi stays parked until he reopens it.
- NOT APPLICABLE: the surface does not apply to the piece (e.g., no episode exists for the
  intro article). Marked N/A with the reason; never counted as a gap.

## Report format

One file per audit, containing:
1. Header: audit date, period covered, auditor's sources.
2. Headline counts: pieces checked; surfaces checked; present; gaps; accepted exceptions.
3. The parity table: one row per piece, one column per applicable surface
  (Present / Missing / No record / N/A / Exception), evidence noted per non-Present cell.
4. Gap register: every gap with evidence, severity (reader-facing vs records-only), and its
  disposition.
5. Exceptions register: every accepted exception with its provenance (decision, date).
6. Carry-forward: items the next audit must re-check.
