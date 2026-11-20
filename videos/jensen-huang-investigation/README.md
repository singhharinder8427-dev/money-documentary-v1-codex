# The Investigation That Reached Nvidia’s CEO

A separate Dirty Dollar episode project. The draft opens on the June 2025 Megaspeed inspection, follows the hardware and sales records, and returns to the rack after the Nvidia board takes up a different question.

## Ready for script review

| File | Purpose |
| --- | --- |
| [script.md](script.md) | Full narration draft with five chapters, the midpoint reveal, and the callback. |
| [voice_script.md](voice_script.md) | Clean narrator copy in recording order with a pronunciation guide. |
| [sources.md](sources.md) | Dated sources and open questions. Recheck the inquiries before release. |
| [shot-plan.md](shot-plan.md) | Scene coverage and the visual action for each beat. |
| [youtube.md](youtube.md) | Draft description and estimated chapters. |
| `script.json`, `shots.py`, `run.py` | Engine-ready script, episode drawing code, and runner. |

The draft has 1,219 words and 76 voice cues. The dry timeline covers 44 picture shots and 16,286 frames at 30 fps, about 9:03 including the title, chapter transitions, outro, and 18-second Watch Next screen. Final timing comes from the recorded voices. All 44 drawing functions passed an in-memory start, middle, and end smoke check. Full-size stills are the visual approval step.

## Engine and assets

Use the shared Dirty Dollar documentary animator. The cloud copy has Skia, FFmpeg, FFprobe, the house fonts and sound assets, Kokoro, and Parakeet. The verified local engine revision is `9b7d769`. The newer Codex `main` contained documentation changes only and its guidance on shot variety was used here.

The episode uses a draft Jensen caricature in the house rig, an existing saver for the fund scene, and anonymous hands on the equipment and records. The server rack, moving equipment, and case props are drawn in this episode’s Python code. The working spec adds silver hair, rectangular glasses, and a black jacket to the house rig. The board and company graphics use sourced summaries marked as illustrations.

## Run the project

| Command | Result |
| --- | --- |
| `python -B run.py ready` | Verify the environment and dry timeline. |
| `python -B run.py voices` | Split the supplied narration into cues. Without a narration recording, the house runner uses local Kokoro. |
| `python -B run.py plan` | Check coverage and durations. Uses actual clip lengths when voices exist. |
| `python -B run.py stills` | Write start, middle, and end review frames for every shot in `out/review/`. |
| `python -B run.py render` | Encode individual shots after the visual review. |
| `python -B run.py audio` | Mix the voice, music, and timed effects through the house pipeline. |
| `python -B run.py final` | Assemble the video and export the SRT. |
| `python -B run.py check` | Check the final audio transcript against the script. |

The runner finds the skill when this folder is inside the Codex checkout. For a standalone folder on Windows, point `DOCANIM_SKILL` at the Codex checkout’s `.claude/skills/documentary-animator` folder. Set `DOCANIM_FONTS` and `DOCANIM_MODELS` if the house resources are stored separately. For a recorded narration, place `narration.wav` or `narration.mp3` beside `script.json` before the voices stage.

The current cloud volume has about 0.27 GiB free. A complete cloud render will need more space for the shot files, audio mix, and final MP4. The existing Windows engine installation can use the standalone project folder.
