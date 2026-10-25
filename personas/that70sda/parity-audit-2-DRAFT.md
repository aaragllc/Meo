# Parity audit #2 - DRAFT (2026-10-25)

Status: DRAFT. Verification legwork done 2026-10-25 against the audit #1
gap register (SPEC-parity-audit.md). Not finalized: the Sun 2026-10-25
ship records (Week Ahead, P4) are still landing - both publishes are
paused at the Substack code gate at draft time - and the catalogue
append for P3 + Scorecard W43 lands with this audit. Finalize after
those records close.

## Item 1 - X-thread records for the 5 earliest articles - UNVERIFIABLE

Pieces: intro, record-high, fridays-alarm, grading, dashboard
(catalogue value: no-record for all five).

- Public fetch of x.com is blocked to the audit tooling (policy
  denial on the profile URL), and general web search does not index
  the early threads - no first-tweet URL could be confirmed or
  refuted for any of the five.
- "No record" is not "absent" (SPEC-parity-audit.md): nothing here
  proves the threads do not exist. The early-October manual posting
  period predates the run-log schema, so no in-repo record exists.
- Disposition: all five stay NR with a VERIFY disposition. Closing
  this item needs an in-session X check (signed-in profile scan),
  which is a browser task, not a public-web check.

## Item 2 - LinkedIn listen lines absent on backlog posts 2-5, 12 - ACCEPTED (unchanged)

Accepted exception under Ravi's 2026-10-22 parking decision (the
listen-link workstream is closed; old posts are not reworked).
Carried into audit #2 unchanged; not a defect.

## Item 3 - Trailer + EP1-EP9 episode description links - VERIFIED

Spot checks via the public Substack API (post body = the episode
description that RSS carries), 2026-10-25:

- Trailer (that70s-da-trailer): description carries "Read the
  long-form writing: https://that70sda.substack.com" plus the Spotify
  show link. The trailer has no companion article; the publication
  link is the correct target. VERIFIED.
- EP2 (record-high-thin-crowd-a-test-before-b32): description carries
  "Read the article:
  https://that70sda.substack.com/p/record-high-thin-crowd-a-test-before".
  VERIFIED.
- EP9 (one-green-day-after-eight-red-ones-ab5): description carries
  "Read the article:
  https://that70sda.substack.com/p/one-green-day-after-eight-red-ones".
  VERIFIED.

The 2026-10-20 retro-pass claim holds on all three spot checks.
Item closed.

## Item 4 - Spotify EP15/EP16/EP17/EP18 unconfirmed - VERIFIED (all six open episodes listed)

Public Spotify show page (open.spotify.com/show/2g1VEsoRFdXiZEBWA2xPy4),
read 2026-10-25. The page lists episodes newest-first with full
descriptions and durations; identifications below are by description
content plus duration against the frozen render durations:

- EP20 (Scorecard): listed "Today", 3:47 (render 227.2s). VERIFIED.
- EP19 (Rented money): listed Oct 24, 3:57 (render 237.8s). VERIFIED.
- EP18 (Late in the second inning): listed Oct 23, 4:08 (render
  248.0s). VERIFIED.
- EP17 (The safe places): listed Oct 22, 3:48 (render ~3:49).
  VERIFIED.
- EP16 (Era file): listed Oct 22, 4:49 (render 290s). VERIFIED.
- EP15 (yield): listed Oct 22, 5:09 (render 310s). VERIFIED.

All four audit-register episodes (EP15-EP18) plus EP19 and EP20 are
live on Spotify via the RSS pull. Catalogue update made with this
audit: spotify flipped to "confirmed" for yield, era-file,
rotation-p1, rotation-p2, and the new rotation-p3 and scorecard-w43
records enter as "confirmed". Four baseline gaps close; no new gap
opens.

## Item 5 (new surface) - Apple Podcasts - VERIFIED

Show claimed and live 2026-10-23
(podcasts.apple.com/us/podcast/that70s-da/id6826468869). Checked
2026-10-25 via Apple's lookup API: trackCount 21 (trailer + EP1-EP20);
latest episode is EP20 "Four sessions graded, and the one that
humbled both readers" (released 2026-10-25T03:15:09Z), preceded by
EP19 "Rented money" (2026-10-24T23:35:52Z) and EP18. The show serves
every episode through EP20 by RSS pull. Note: the rendered web page's
top-listed episode lags the API (it showed EP16) - the API is the
reliable read. No gap.

## New records entering with audit #2 (from the catalogue append)

- rotation-p3 (Rented money / EP19): article, episode, Spotify,
  YouTube video + Short, X thread, both X community posts, LinkedIn
  (urn:li:share:7519950604887314432), listen link - all confirmed
  live. The Substack Note for P3 failed on a site error and is
  parked on the backoff cadence; Notes are not a catalogue surface.
- scorecard-w43 (EP20): article, episode, Spotify, YouTube video +
  Short, X thread, listen link - confirmed live. LinkedIn: NR - the
  post is held pending the page session restore (manual sign-in);
  it enters the catalogue as n/a with an NR note because the
  catalogue vocabulary has no NR value for LinkedIn. It is a known
  pending surface, not a silent absence - flagged here so the final
  audit closes it when the post lands.

## Open at draft time

- Week Ahead (EP22) and P4 (EP21) ships: paused at the Substack code
  gate, 2026-10-25. Their records enter the catalogue in the follow-up
  pass once every surface is live.
- Item 1 (earliest X threads) remains NR/VERIFY - needs an in-session
  check.
- Scorecard LinkedIn post remains NR pending the session restore.
