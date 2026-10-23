# Humanize TTS narration

## Spell names the way they sound

- Write every brand name and proper noun in the script phonetically, exactly the way the host should say it. When a TTS voice misreads or inconsistently renders a name (one render says that70sday, the next says that70sda), spell it out in full, such as "that seventies day".

- Current default spelling (Ravi, 2026-10-21): "That seventies day" - the word "day". It replaces "that seventies daaa" (three a's), whose ending clipped at full volume and sounded synthetic. "Day" ends on a clean diphthong and the render's tail decays to silence on its own. Test clips: hidden_files/podcast/signoff-tests/. This is an audio-only phonetic spelling: the written post signature stays "- That70s Da." in all text.

- Apply phonetic spelling in every script and every chunk, including re-renders. One missed chunk brings the misread back, and an inconsistent brand name is a dead giveaway of synthetic speech.

## Pace the narration like a human

- Pad real silence between sections, around 900 milliseconds to a full second (raised 2026-10-21), and insert breaths more often than feels necessary: anywhere a stretch runs longer than about 30 seconds without one, plus at clause clusters where a speaker would gather a thought. A shorter pad of around 500-600 milliseconds between tighter sections keeps the rhythm natural. When in doubt, add the pause - Ravi's standing direction is MORE pauses, not fewer.

- DEFAULT sign-off treatment (Ravi, 2026-10-21, supersedes the speed-88 + atempo-stretch treated master and the 1s-gap recipe - both retired, do not use the treated master chunk): render the sign-off inside the single take, with the closing lines, at normal body speed (95), spelling the brand "That seventies day". No separate render, no time-stretch, no 1s gap. Keep only the tail fade-out (~0.35s) and ~0.8s of trailing silence as cut-off insurance, and verify the tail RMS envelope (smooth ramp to zero, no voice energy at the file edge - the "day" render passes this natively). Applies to new productions only - never re-render the existing catalogue.

- Use punctuation to direct pauses: commas for short beats, ellipses and line breaks for longer ones, dashes for mid-sentence turns. Rewrite lists as spoken sequences such as "First... Second..." instead of reading them like a ticker.

- Add natural fillers ("hmm", "well", "ah") at thinking beats throughout the episode - section openings, transitions, moments of weighing two sides - roughly one every 30 to 45 seconds of narration. (Ravi, 2026-10-21, supersedes the earlier "sparse" rule: MORE fillers and MORE pauses, going forward for all audio.) Keep them placed where a person would genuinely hesitate; a metronome-regular filler every paragraph is still a tell, so vary the gaps.

## Verify before shipping

- Rewrite every headline, title and section header as a spoken bridge. A listener should never hear "Section three: market breadth"; they should hear "So what does market breadth tell us". Read the finished script once as a listener would, and cut any line that sounds like reading rather than talking.

- NO EDITING, EVER (Ravi, 2026-10-21): never patch, splice, or seam-repair a rendered episode - chunk-patching is exactly what produced EP16's audible cuts and loudness jumps between sections. Render each episode as ONE take in a single tts call (the frozen baseline below governs); there is no chunk fallback. If a finished render still sounds flawed, the options are a fresh full remake or living with it, decided by ROI (current/flagship episodes earn the remake; deep catalogue does not) - never a patch.
- FROZEN BASELINE (Ravi, 2026-10-21 - the EP15 single-take remake, judged "near perfect" by Ravi's ear; he first said EP16 and corrected the attribution to EP15 the same evening. The standard for all future episodes and video builds): (1) the ENTIRE narration in ONE `tts speak` call, voice avocado_v2:TruthTeller, speed 95, script verbatim (fillers and pauses per the humanization directive); (2) finishing = ONE uniform whole-file gain to catalogue level (~-29.2 to -29.6 dBFS RMS) + 0.35s tail fade + 0.8s trailing silence; (3) acceptance numbers: RMS per consecutive 30s window across the narration body, spread ~2 dB or less (EP16 remake 1.41 dB; EP15 remake 1.99 dB; rejected chunk assemblies measured 4.7-8.2 dB), tail clean to pure silence. A render outside these numbers does not ship as-is.
- Render the episode and listen to a full 60-second sample before it ships. Check the must-haves: the brand name sounds right, no titles are read aloud, the pauses feel human, and loudness/cadence stay consistent from the first section to the last.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- For multi-host conversational episodes, use the two-host format in the Podcast Production skill rather than forcing one narrator to carry dialogue.

- Sample a new voice on a short test script before re-rendering a full episode with it. A voice that sounds right in a catalog clip can still sound synthetic in long narration.