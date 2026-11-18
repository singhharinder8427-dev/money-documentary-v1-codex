# 50% in 45 Days | Windows preview

This is the full Ponzi cut. It uses the project's locked Skia kit, a period night-print story, and a day-print lesson. The working channel name is omitted from the end card. The end screen is part of the five-minute limit.

## Files

- [Script](script.md), [spoken lines](voice_script.md), and [sources](sources.md).
- `script.json` is the engine input. `shots.py` gives every line its own shot, with additional title, chapter, outro, and end-screen shots.
- `preview.py` checks that every voice clip exists and matches its declared duration, then checks the measured length against the five-minute limit. It writes the first, middle, and last frame of each shot, labeled contact sheets, and a CSV in `out/review/`. An image-file pass does not certify visual quality. A local agent must open the previews, inspect composition, lettering, occlusion and continuity, and recheck any corrected shots.

## Working on the PC

Run from a local checkout of the Codex repo. Reuse the installed interpreter `D:\pyenv\Scripts\python.exe`, FFmpeg, Kokoro and Parakeet models. Point `DOCANIM_FONTS` to `D:\money-documentary-v1\fonts` if that is where the installed fonts live. Point `DOCANIM_MODELS` to the existing model directory if it differs from the engine default. All generated files stay under this checkout. Place the recorded narrator lines in `videos/ponzi-full/narration.wav` for the ElevenLabs pass. The voices step uses Kokoro as a placeholder when no narrator recording is present.

```powershell
Set-Location videos\ponzi-full
if (-not $env:DOCANIM_FONTS) { $env:DOCANIM_FONTS = 'D:\money-documentary-v1\fonts' }
& 'D:\pyenv\Scripts\python.exe' preview.py --voices
```

For corrections that leave voice timings untouched, rerun `preview.py` without `--voices`. Keep a fresh output folder when the script, voice recording, or timing changes so old shot clips are not reused.

After visual review and explicit approval to render, run the house runner in the same video folder, in this order: `render`, `audio`, `final`, `check`. Verify `out/final.mp4` has both streams, starts cleanly, and remains under five minutes with the end screen. Use the actual render timeline for chapter timestamps and write the thumbnail prompts after the cut is approved.
