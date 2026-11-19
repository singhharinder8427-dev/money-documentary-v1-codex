# START HERE - handover for a new Claude Code session (Dirty Dollar channel)

Read this first, then `BRAND.md`, then the skills in `.claude/skills/`. Everything below is the owner's decision.

## The project
- **Channel:** **Dirty Dollar** (@DirtyDollarFile) - long-form 16:9 animated money documentaries for a **US audience**:
  scams, fraud, corruption, con artists, business scandals + a money lesson ("your wallet"). Videos 4-10 min
  (aim 8-10 min from now on: mid-roll ads need 8+).
- **Repo:** github.com/singhharinder8427-dev/money-documentary-v1 (branch `main`). The `-codex` repo is only a copy.
- **Owner's PC:** Windows, PowerShell, **everything on D:** - project `D:\money-documentary-v1`, Python venv
  `D:\pyenv` (Python 3.12), voice models `D:\models` (`DOCANIM_MODELS`), ffmpeg `D:\ffmpeg`. The owner is in India (IST).

## Working rules (always)
1. **Never save / commit / push without the owner's OK.** After every change ask: **"save now or later?"**
2. **Never render or generate anything the owner didn't ask for.** Ask **PC or cloud** before every render.
3. **Listen first** when the owner gives feedback: collect the full list, don't start changing things mid-list.
4. Give PowerShell commands **one per code block**, step by step, short and clear (the owner is not a developer).
5. **Before every new video ask:** (a) new character(s) or existing? (b) new places + props or reuse existing?
   New ones: owner sends references -> design in our style -> iterate until approved -> lock -> add to the library.
6. **Mandatory Claude creative quality check** before the owner renders: 3 frames per shot on one compact sheet;
   fix mistakes, repetition (new picture every 2-3 s), readability, and ask per shot "would adding something make it
   more interesting / immersive / eye-catching?" (`.claude/skills/documentary-animator/SKILL.md`, step 5).
7. Keep usage low: one compact review sheet per round, re-check only changed shots.

## Pipeline (skills)
1. `documentary-script` - researched, sourced script (Template A), `script.json`, voice script, sources.
2. `documentary-animator` - the engine (`engine/`), runner `make_video.py` (`voices`, `stills`, `render`, `audio`,
   `final`, `check`), per-video `videos/<slug>/shots.py`. Read its `SKILL.md` and `FIXES.md` (owner feedback 1-26).
3. `thumbnail-prompt` - **Claude draws the thumbnail in code** in the LOCKED style ("$20 MILLION GONE" v3:
   sharp night-print set, huge emotional character, whole story packed in, big Alfa Slab headline).
4. Publishing checklist + `videos/<slug>/youtube.md` (titles, description with chapters + sources, tags).

## Locked look (details in BRAND.md)
Navy #14213D + gold #FCA311 (money) + orange #F35B04 (losses only), **no green** (only exception: real flags).
Night print (dark navy, dotted light falloff) for the story; day print for the lesson. Rectangular-head glossy
cast; fonts DSEG7 / Alfa Slab One / Special Elite / Barlow Condensed. Vignette, small burned-in captions (+ .srt),
real typewriter keys (CC BY 4.0 - credit line in every description), code-made music + quiet SFX, outro "DIRTY
DOLLAR" + end screen. Branding: `branding/profile_800.png` (CEO with dollar-sign eyes), `banner_mobile_2560x1440.png`.

## Status (19 Nov 2026)
- Video 1 **"50% in 45 Days" (Charles Ponzi)** - rendered on the owner's PC with captions; **scheduled on YouTube**
  for Thu 19 Nov, 10:00 am ET (8:30 pm IST). Files in `videos/ponzi-full/` (script, sources, shots, thumbnails A/B/C,
  youtube.md). Ponzi's character (real look: pencil moustache, slicked hair, boater, gold cane) is locked in `engine/cast.py`.
- Upload settings used: category **Education**, academic fields left empty, comments on, `captions.srt` uploaded,
  Test & Compare thumbnails (B = owner's favourite).
- Temporary Kokoro narrator so far; the owner may record ElevenLabs narration later (re-run voices/audio/final only).

## Next
- The owner picks the next story. Start by asking the two questions in rule 5, then research + script
  (8-10 min), then characters/places/props approval, shot list, Claude quality check, owner renders on PC,
  thumbnail, youtube.md.
- Ideas not done yet: Shorts cut from each video as trailers; playlists ("Famous Scams", "Money Lessons").
