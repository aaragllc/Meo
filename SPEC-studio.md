# Socialy.INK - Production Studio Spec

**Status: v1.1, 2026-10-25** (bump from FROZEN v1, 2026-10-22, under
Ravi's 2026-10-25 industrialize directive: B3 gains the staged-
foreground build rule from the 2026-10-24 output-loss incidents
(L-26), and the C6 editor caution is updated to the key-press
insert method verified 2026-10-24 (L-03). No other rule changed.)
**Change rule: this spec changes only by Ravi's direct instruction or a deliberate version bump (v2, v3...) recorded at the top of this file with its date and reason. No run, worker, or adapter may silently deviate from a numbered rule; if production reality contradicts a rule, stop, flag it, and let the version bump settle it.**

Scope: turning a published (or publishing) article into its podcast episode and its YouTube video - audio rendering, video building, episode metadata, and same-day parity. Persona pack #1: that70sda. Article and thread production live in the publishing pipeline spec; this spec governs the studio.

Reference files: `~/workspace/custom-skills/tts_narration_humanization/SKILL.md` (narration recipes), `~/workspace/custom-skills/that70sda-publishing/SKILL.md` (publishing + video QC), `~/TOOLS.md` (Substack editor notes). Where this spec and a skill disagree, this frozen spec governs studio work until the version bump reconciles them.

Canonical palette (all video cards): espresso #371C15, burnt orange #C7701F, gold #DF9729.

---

## A. Audio rules

**A1. Host voice.** One host voice, locked: `avocado_v2:TruthTeller` (masculine American, calm/wise), labeled host "That70sDa" on every episode. No other voice narrates an episode. A new voice is sampled on a short test script before any full render (skill guidance), and adopting one is a spec version bump, not a run-time choice.

**A2. Render command shape.** `/opt/hatch/bin/tts speak --voice avocado_v2:TruthTeller --speed 95 --text-stdin --output <file>.mp3 < <script>.txt`. The `--output` flag is mandatory (`--stream` / `--buffered-stdout` are the only alternatives); a bare stdout redirect fails and writes empty MP3s.

**A3. Script preparation.** The script is the article rewritten for the ear, never the article read raw:
- Titles, headlines, and section headers are NEVER read aloud; every header becomes a spoken bridge ("So what does market breadth tell us", not "Section three: market breadth").
- Lists are spoken as sequences ("First... Second... Third..."), never read like a ticker.
- Punctuation directs the pauses: commas for short beats, ellipses and line breaks for longer ones, spaced hyphens for mid-sentence turns (the em dash character is banned in all persona text, scripts included).
- The finished script is read once as a listener before rendering; any line that sounds like reading rather than talking is rewritten.

**A4. Humanization (standing directive, Ravi 2026-10-21).**
- Fillers ("hmm", "well", "ah") at genuine thinking beats - section openings, transitions, weighing-two-sides moments - roughly one per 30-45 seconds of narration, with varied gaps. A metronome-regular filler is itself a tell; placement must feel hesitant, not scheduled.
- Pauses: ~900ms-1s of real silence between sections; ~500-600ms between tighter sections; breaths at least every ~30 seconds and at clause clusters where a speaker would gather a thought. When in doubt, add the pause - the standing direction is MORE pauses, not fewer.

**A5. Brand name in audio.** The brand is fed to TTS ONLY in its phonetic spelling: **"That seventies day"** - in every script, every render, every re-render, including the sign-off. One missed instance brings the misread back and reads as synthetic. This spelling is AUDIO-ONLY: it never appears in written text (see D6).

**A6. The frozen audio baseline (Ravi, 2026-10-21; reference renders: the EP15 single-take remake, judged "near perfect" on Ravi's full listen 2026-10-22, and the EP16 remake).** Every episode render MUST be:
1. **One single `tts speak` call for the entire script** - voice per A1, speed 95, script verbatim per A3-A5.
2. Finished with **one uniform whole-file gain** to catalogue level, **-29.2 to -29.6 dBFS RMS**, plus a **0.35s tail fade** and **~0.8s trailing silence** as cut-off insurance. Uniform gain + tail finishing is finishing, not editing (see A7).
3. The sign-off sits **inside the single take**, with the closing lines, at the same speed 95 - no separate chunk, no time-stretch, no inserted gap.
4. **Acceptance (measured, not impressionistic):** RMS per consecutive 30s window across the narration body spreads **~2 dB or less** (references: EP15 remake 1.99 dB, EP16 remake 1.41 dB; rejected chunk assemblies measured 4.7-8.2 dB), and the tail envelope ramps smoothly to pure silence with no voice energy at the file edge. A render outside these numbers does not ship as-is.

**A7. NO-AUDIO-EDITING rule (Ravi, 2026-10-21; absolute).** Never patch, splice-fix, seam-repair, or chunk-stitch a rendered episode. A flawed render has exactly two dispositions: (a) **remake it fresh** as one consistent render under A6, or (b) **live with it** - decided by ROI: current/flagship episodes earn the remake, deep catalogue does not. There is no third option. (Historical note: the baseline's one-call rule in A6.1 supersedes the older "fewest possible chunks" fallback in the narration skill; chunks are how EP16's audible cuts happened.)

**A8. Listen check.** Before an episode ships, listen to a full 60-second sample: the brand name sounds right, no titles are read aloud, the pauses feel human, and loudness/cadence are consistent from the first section to the last. Episodes ship on measurement (A6.4) plus this sample; Ravi's ear is the final court for flagship episodes (EP15 precedent).

## B. Video rules

**B1. Animated only.** Every new episode's video is an **animated, narration-synced card video** in the 70s palette (header): data/visual cards timed to the narration, in the EP1 pilot format. A static badge-image render is NEVER a shippable video for a new episode; static renders exist only as a launch/backfill expedient for the old catalogue and are not produced anymore.

**B2. Two-gate QC (Ravi, 2026-10-20/21; both gates, every upload, no exceptions).** A video uploads only if BOTH pass:
- **Gate 1 - Animation:** a frame-change check samples frames across the runtime (`qa_frames.py`); the video must show real changing boundaries between samples (a static video scores ~zero changing boundaries and fails).
- **Gate 2 - Audio:** the narration track must itself satisfy A6-A7 (single consistent render, baseline measurements, no patched or chunk-spliced cuts or loudness jumps), verified with per-section loudness measurements. A video built on flawed audio fails QC regardless of its animation: remake the audio fresh (A7), rebuild the video, re-check both gates.

**B3. Build method.** Builder: `build_video.py` (per-episode card groups in `groups.json`). When rebuilding against a remade audio track: scale the group durations to the new audio length, snap card boundaries to the midpoints of detected silences (-40 dB silencedetect), and render segments with an explicit `-t <duration>` - never `-shortest`, which truncates cards against the audio.
**B3a. Staged foreground builds (2026-10-25, L-26).** Media builds NEVER run as one backgrounded whole build: on 2026-10-24 two backgrounded builds reported completion and their mp4s did not exist afterward. Builds run in foreground-sized stages (the `stage_build.py` pattern - one card group per invocation, then concat), and after EACH stage the operator verifies the output file exists on disk with the expected duration before starting the next. A build whose process reports success but leaves no file is a FAILED build, full stop - it is re-run in stages, never trusted.

**B4. YouTube metadata.** Title = the episode title. Description = the episode's overview description (see D3-D4), composed for YouTube: "Originally published <date>." line first for backlog uploads (D4), the overview, the article link, the episode link, the Spotify show link, and "Not financial advice." Settings: Public, not made for kids, Category Education.

## C. Text and metadata rules

**C1. Subtitle cap (hard).** Every article AND episode subtitle is drafted at **200 characters or fewer, complete sentences only** - Substack silently truncates longer subtitles mid-sentence at publish (learned 2026-10-22). After publishing, verify the live subtitle's ending character-for-character; a truncated subtitle is a failed ship until fixed.

**C2. Episode-specific metadata.** Every episode gets its OWN subtitle and a real description: what it covers, its key points, the article link, and links to related earlier posts. The fixed one-liner "This is the audio version of the article." is retired and never used as a full description.

**C3. Overview-description gate (Ravi, 2026-10-21; mandatory).** Every post on every channel that supports an overview/description carries its post overview description before it goes out. No description means no post - the ship waits, it does not go out bare.

**C4. Backlog dates.** Any backlog/old upload (video or post) carries its original publish date: on YouTube, a dated line at the top of the description ("Originally published October 21, 2026."); the same dating discipline applies to LinkedIn overview posts of older pieces.

**C5. Sections.** Substack filing is fixed: **articles under the "that70sda" section; podcast episodes under the "Podcast" section.** No episode in the article section, no article in Podcast, no "no section" ships.

**C6. Cross-linking (both directions, every episode).** The episode description links its article. Once the episode is live, the article is edited to carry, between the disclaimer and the sign-off: "Prefer to listen? The audio version is here: <episode URL>". (Editor caution from `~/TOOLS.md`, updated 2026-10-24 (L-02/L-03): never use fill/typing entry on the Substack editor body field - it can replace the whole body - and paste proved unsafe for body inserts too (merged lines, replaced text). The verified insert method is: click the "- That70s Da." sign-off paragraph, Home, Enter to create a new empty paragraph above it, verify the caret sits in that new empty paragraph, then enter the line with individual key presses. Verify the FULL live body after any edit publish. Note: per Ravi's 2026-10-22 direction, back-catalogue listen-link fixes are deprioritized - C6 binds new ships; the parked backlog list lives in the goal's `hidden_files/listen-link-batch-status.md`.)

**C7. Written sign-off and separators.** In ALL written text - articles, threads, episode descriptions, metadata - the signature is exactly **"- That70s Da."** and the separator is a spaced hyphen " - "; the em dash character never appears in persona writing. The audio spelling in A5 never leaks into text.

## D. Parity rules

**D1. Same-day parity (Ravi, 2026-10-20).** Every new episode ships to **Substack and YouTube the same day** - YouTube stays at par with Substack, no lagging catalogue. Spotify receives the episode automatically by RSS pull from the Substack podcast feed; no separate Spotify action exists or is taken. Apple Podcasts remains on hold (not a parity surface) until Ravi reopens it.

**D2. Parity is gated, not rushed.** Same-day means same calendar day with BOTH video gates (B2) passed and the audio at baseline (A6.4). A parity ship never trades QC for speed: if the audio fails baseline late in the day, the episode's YouTube upload waits for the fresh remake rather than shipping flawed - and the slip is bridged in the next post per the publishing skill's lateness rule.

**D3. Channel identity on upload.** Uploads go to the That70s Da channel (@That70sDa) only, from the channel's own signed-in session. The channel's one-time phone verification was completed 2026-10-22, so no daily upload cap applies; if YouTube ever presents a limit or verification demand anyway, stop and report - never re-verify or work around it in-run.
