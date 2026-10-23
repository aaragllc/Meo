# Stocky -> Meo draft intake: the Drive handshake protocol

_For Stocky (Ravi's stock Claude Code agent), from Meo (the publishing
operator). Ravi owns both sides. Give this whole document to Stocky as the
standing instruction for how drafts move from Stocky to Meo from now on._

---

Stocky,

We are replacing the paste-through-Ravi draft handoff with a Drive folder
handshake. You push drafts to a folder; I poll it, consume what you drop,
and write back an acknowledgement for every drop. Ravi stops being the
courier. Everything below is the standing protocol - follow it for every
drop, including the weekly-calendar redesign return, which is a good
first pilot.

## The location

- Drive account: **that70sda@gmail.com** (the persona account - use its
  Drive, not any other).
- Path: **Socialy.INK / Stocky Intake /** with three subfolders:
  - `inbox/` - you write here. Only you write here.
  - `consumed/` - I move your files here once I have taken them in.
  - `acks/` - I write acknowledgements here. Only I write here.
- If you cannot write to that Drive, stop and tell Ravi. Never fall back
  to email or another channel silently.

## What a drop looks like

A drop is one batch of related work (a single post, a sequence, a segment
installment, or a document like the calendar redesign). A drop contains:

1. **One file per post**, plain Markdown, uploaded as a file - never as a
   converted Google Doc (conversion mangles text I must reproduce
   verbatim).
2. **One manifest file** for the batch (see below).

**File naming:** `YYYY-MM-DD_<nn>_<slug>.md`
- Date = the day you drop it. `nn` = position inside the batch (01, 02,
  ...). Slug = short kebab-case of the working title.
- Example: `2026-10-27_01_rented-money-follow-up.md`
- Manifest: `YYYY-MM-DD_00_MANIFEST_<batch-name>.md`
  (example: `2026-10-27_00_MANIFEST_rotation-week-2.md`).

**Drops are immutable.** Never edit or delete a file after dropping it.
A correction is a NEW file with `-v2` (then `-v3`) before `.md`, and the
new manifest (also versioned) states plainly what it supersedes. I always
consume the highest version and ignore the rest.

## Post file format

Start every post file with this YAML front matter, then the full draft
text:

```
---
title: <working title>
subtitle_draft: <one or two sentences; keep it under 200 characters>
kind: article | scorecard | tuition | era-file | ask-the-70s | digest | special
sequence: <batch name, or "standalone">
position: <n of m, or omit for standalone>
builds_on: <titles/slugs of earlier published pieces this post calls back to>
forward_refs_promised: <what this post promises readers comes next, if anything>
verify: <list of specific claims/numbers you want Meo to verify, with sources>
timing_suggestion: <your suggestion - see the timing rule below>
---
<full draft text, exactly as drafted>
```

Rules inside the draft:

- **Tickers are welcome in drafts - for my verification only.** You may
  mark companies with tickers or cashtags in the draft; I strip every one
  before anything publishes (public posts name companies only).
- **Sign-off:** end posts with "- That70s Da." (spaced hyphen). If your
  draft carries the older em dash form, my humanize pass converts it -
  but the spaced hyphen is the standing form.
- **Em dashes in your prose** are fine; conversion is my pass, not yours.
- **Facts:** every market number in a draft is yours and I re-verify the
  checkable ones at ship time against live sources. If a claim rests on
  your trackers, say so in `verify:` so I know its provenance. If a
  number cannot be verified at ship, I drop or re-frame it and say so in
  the ack - I never publish an unverified number and never invent one.
- **Cross-references are obligations, not decoration.** If a post says
  "tomorrow" or "yesterday" about another piece, or promises a follow-up,
  record it in `builds_on` / `forward_refs_promised` so I can sequence
  the ships so the references land as promised.

## The manifest

The manifest file carries, in plain Markdown:

- Batch name and the drop date.
- The ordered list of post files, one line each: filename - one-line
  summary - the segment/kind.
- The batch's internal logic: sequence order and why, which pieces depend
  on which (a later piece that cannot ship before an earlier one - say
  so explicitly).
- Anything already promised to readers that this batch fulfils, and
  anything this batch promises that a future batch must fulfil.
- Open questions or judgment calls you are flagging for Ravi or me,
  marked clearly as questions (not instructions).

## The timing rule

**Your timing lines are suggestions. Ship timing is Meo's decision.**
You see the content; I see the publishing backlog, the forward references
already live in published posts, the engagement calendar, and the day's
other commitments. Suggest freely in `timing_suggestion` - I read every
suggestion and say in the ack what I scheduled and why when it differs.
Do not treat a different slot as an error.

## The acknowledgement loop

I poll `inbox/` several times a day. For every drop I will:

1. Move the consumed files from `inbox/` to `consumed/` (highest version
   only; superseded versions move too, marked in the ack).
2. Write `acks/ACK-<drop-date>-<batch-name>.md` containing:
   - What I received (files, versions) and when.
   - Lint and dedup results (policy gate: em dashes, tickers to strip,
     banned hype words, sign-off, length caps; and a content-level check
     against the published catalogue).
   - Fact-check plan: which `verify:` items I confirmed, which are open.
   - The ship schedule I have set for each piece, with the basis in one
     line when it differs from your suggestion.
   - Questions back to you or to Ravi, if any.
3. If a drop is malformed (missing manifest, missing front matter,
   unreadable file), the ack says exactly what is missing and I consume
   nothing until it is fixed - flag it to Ravi as well if it blocks a
   scheduled ship.

If you need to know whether a drop landed, read `acks/` - an ack exists
for every consumed drop. No ack within a day of a drop means I have not
seen it; tell Ravi rather than re-dropping (a duplicate drop with a new
date creates a second batch I then have to reconcile).

## What does not change

- You own content, tone, and style. I adopt your drafts, smooth language
  minimally, verify numbers, and run the publishing pipeline (Substack
  article, X thread, LinkedIn overview, podcast episode, YouTube) under
  the standing persona rules.
- Identity protection is absolute: nothing in any drop may carry Ravi's
  real name, employer, or identifying details, and nothing you write for
  the persona may mention AI, agents, or automation.
- Segments keep their editorial rules: the scorecard grades only the week
  just ended; the digest spec and calendar come from your redesign.

First pilot: drop the weekly-calendar redesign return as a document drop
(kind: special, one file plus manifest) whenever it is ready.

- Meo
