# Resume the Jensen Huang episode on Windows

Open PowerShell in the root of your existing Dirty Dollar Codex checkout on `main`. Its GitHub remote should end in `money-documentary-v1-codex.git`.

Update the checkout.

```powershell
git pull --ff-only origin main
```

Start the local Codex session with this handoff.

```powershell
& 'D:\npm-global\codex.cmd' 'Read videos/jensen-huang-investigation/POWERSHELL_HANDOFF.md and follow the local Codex handoff on this PC.'
```

## Local Codex handoff

Work in `videos/jensen-huang-investigation/` in this Codex checkout. Read its [README](README.md), [script](script.md), [source notes](sources.md), and [shot plan](shot-plan.md). Read the repository’s `START_HERE.md`, `BRAND.md`, and documentary animator skill. Use this checkout’s animation engine. Treat the separate Claude repository and its assets as read-only.

1. Finish the script pass before making media. Compare the chapter handoffs with `videos/ponzi-full/script.md`. Sharpen Chapter 2 so it ends on the documented route to Malaysia and the question of what happened beyond that. Rewrite the end of Chapter 4 so it naturally leads into the viewer’s possible exposure through an index fund. Keep the final server-rack callback, comment question, and Malaysia tease for Episode 2. Update `script.md`, `script.json`, and `voice_script.md` together. Check the latest primary sources for any changes that affect dated claims. Keep suspected activity attributed and the known route distinct from open questions. Run the plan check and show the revised lines for script approval.
2. After script approval, prepare narration and review stills locally on Windows. Use `D:\pyenv\Scripts\python.exe` and the existing Dirty Dollar models, fonts, and FFmpeg. The episode runner is `run.py`. Use `ready` for environment checks, `voices` for a supplied narration recording or a confirmed temporary Kokoro read, `plan` for measured timing, and `stills` for the review sheets. Use the approved working assets on this PC and configure `DOCANIM_FONTS` and `DOCANIM_MODELS` when needed.
3. Apply the current brand guidance in the review pass. Use a focused cast and give the main beats distinct actions and compositions. Introduce the draft Jensen character for visual approval. Place an original, simplified Nvidia eye mark in white or gold on naturally relevant hardware, signage, or screens. Use the same house treatment for other company logos. Review the start, middle, and end of every shot for captions, framing, prop readability, logo contrast, and repeated setups. Fix issues, open the review sheets, print their full paths, and stop for visual approval.
4. Start the full Windows render after the owner approves the stills. Use the usual render, audio, final, and check stages. After the final render, the thumbnail deliverable is a detailed prompt the owner can paste back for image generation. Take framing and expressive emphasis from the Paper Billions reference and use the Dirty Dollar cast, palette, type, and marks.

Keep generated media local. The project’s current contents are the script and engine code through the updated Episode 2 ending.
