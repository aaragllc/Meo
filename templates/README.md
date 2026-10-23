# templates/ - onboarding a new persona or channel

Templates turn the working that70sda instance into a starting point: a
second persona (or a new channel for an existing one) is onboarded by
filling these in, not by copying the live instance and editing out its
identity. Structure comes from practice - every section in these templates
exists because the worked example needed it.

## The templates

- `persona-pack/` - mirrors `../personas/that70sda/`:
  - `directive-template.md` - the governing directive skeleton: identity,
    voice, lanes, sign-off, rules, escalation, rhythm, segments, metrics,
    money path - with the universal non-negotiables (owner anonymity, no
    visible automation, no invented facts, human pacing, the em dash ban)
    stated generically, to be carried over unchanged.
  - `STATE-template.md` - the point-in-time state snapshot.
  - `OPERATING-LESSONS-template.md` - the persona's lessons file, empty
    at birth, filled by production.
  - `files/README.md` - what the pack's `files/` folder is for.
  - `skills/README.md` - where production skills install and what a
    persona needs.
- `channel-adapter.md` - one filled copy per channel surface: identity
  and account, session model, publish flow, engagement actions, pacing,
  verification, known failure modes (by taxonomy code, from
  `../SPEC-run-log.md`), and parity obligations (from
  `../SPEC-parity-audit.md`).

## How onboarding runs

1. **Stand up the environment** per `../BOOTSTRAP.md` (repo placement,
   account reconnection, cron recreation). Templates assume that harness.
2. **Create the pack:** copy `persona-pack/` to `../personas/<slug>/`,
   renaming the `*-template.md` files to the persona's real names
   (`<slug>-directive.md`, `STATE-<date>.md`, `OPERATING-LESSONS.md`).
3. **Fill the directive first.** It is the governing document; policy,
   adapters, and skills all inherit from it. Anything the owner has not
   decided stays as an explicit open question in the Resolutions section -
   never silently defaulted.
4. **Write one adapter per channel** from `channel-adapter.md`, into the
   new pack at `../personas/<slug>/adapters/<channel>.md` (the template's
   relative references are written for that destination), seeded
   from `../SPEC-foundation-adapters.md`'s channel notes where the new
   persona shares a platform with an existing one. Platform mechanics
   transfer; account facts never do.
5. **Install the skills** per `persona-pack/skills/README.md`.
6. **Dry-run before live:** walk a full publish and a full engagement run
   in draft only, verify the QC and logging steps work, then start live
   operation at the young-account volume in `../config.yaml`.

## What "done" looks like - the worked example

`../personas/that70sda/` is a completed template set:

| Template | Filled instance |
|---|---|
| `directive-template.md` | `personas/that70sda/that70sda-meo-directive.md` |
| `STATE-template.md` | `personas/that70sda/STATE-2026-10-22.md` |
| `OPERATING-LESSONS-template.md` | `personas/that70sda/OPERATING-LESSONS-agents.md` |
| `files/README.md` (the folder it describes) | `personas/that70sda/files/` (post template, welcome draft, contributor prompt) |
| `skills/README.md` (the folder it describes) | `personas/that70sda/skills/` (publishing + TTS narration) |
| `channel-adapter.md` (x5 surfaces) | the channel notes in `../SPEC-foundation-adapters.md` (X, LinkedIn page, Substack, YouTube; Spotify as the monitored-only variant) |

Where a filled instance and its template disagree in structure, the
template is the one to fix - it is supposed to be the shape the next
onboarding can trust.
