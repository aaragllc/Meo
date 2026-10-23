# skills/ - production skills for this persona

A persona pack carries its production skills with it so the pack is
self-contained, but the skills are **inert inside the pack**: they only
take effect once installed into the operating environment's custom-skills
folder (`~/workspace/custom-skills/` in the reference environment; see
`../../../BOOTSTRAP.md`, stand-up step 2). When a pack moves to a new
environment, copy each folder here into that folder unchanged.

## Layout

Each skill is a folder named for the skill, containing:

- `SKILL.md` - the playbook itself (required).
- `skill.yaml` - the skill's catalog metadata, where the environment
  uses one.

## What a persona needs

At minimum, a **publishing skill**: the end-to-end workflow that takes
this persona's approved content and ships it across its channels with the
persona's QC rules (verbatim composer check, live inspection, sign-off,
cross-promotion, continuity). Add further skills per production surface
the persona actually uses.

Worked example - that70sda ships two:

- `that70sda-publishing/` - Stocky draft to Substack article, X thread,
  podcast episode, YouTube upload, LinkedIn post, at parity.
- `tts_narration_humanization/` - how narration scripts are written and
  rendered so the synthetic host voice sounds human (shared shape; any
  audio persona needs its own voice/baseline decisions inside it).

## Rules

- Skills are persona property like everything else in the pack; a shared
  technique gets copied and adapted, not linked.
- When production teaches a new rule, update the installed skill AND the
  copy in this pack in the same pass, so the pack never drifts from the
  live skill.
