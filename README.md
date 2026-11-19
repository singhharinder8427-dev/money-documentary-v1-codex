**New session? Read `START_HERE.md` first.**

# money-documentary-v1

Style toolkit for a US money documentary channel (long-form 16:9, max 10 min). **Start with [BRAND.md](BRAND.md)**: the locked decisions.

| Folder | What |
|---|---|
| `characters/` | Final character style: `kit.py` (drawing kit), `draw_cast.py` (the 5-person cast), `cast_final.jpg` |
| `daytime/` | **Locked daytime look** (printed illustration): reference scenes (`day*.jpg`) and the [approved boardroom set](daytime/boardroom/README.md) |
| `environments/` | **Locked night look** (night print): reference scenes (`night*.jpg`) and the [approved sales floor set](environments/sales-floor/README.md) |
| [Approved sets and paper-trail props](graphics/approved-sets-and-props/README.md) | Suburban home, hotel seminar stage, investigation room, daytime courtroom and illustrated financial records |
| [Story asset library](graphics/story-assets/README.md) | Finance, law, everyday life, wealth and media settings, plus props, screens and supporting cast |
| `branding/` | **Dirty Dollar** profile photo + banner (`make_branding.py`) |
| `type/` | Font system specimen (`type_system.jpg`, `specimen.py`) |
| `palette/` | Locked colour palette |
| `.claude/skills/documentary-animator/` | **Animation skill**: turns a script into the rendered video in the locked style (engine, sets, cast, graphics, music/SFX, voices, render runner) |
| `videos/ponzi-test/` | First test video (script, sources, shot list). Owner feedback: `.claude/skills/documentary-animator/FIXES.md` |
| `.claude/skills/thumbnail-prompt/` | **Thumbnail skill**: detailed AI-image prompts in the locked style, written after each video is rendered |
| `.claude/skills/documentary-script/` | **Script skill** (Template A): researched, fact-checked documentary scripts for money stories, corruption, scams, rackets |

## Re-run
```bash
pip install skia-python numpy pillow    # on Linux also: apt-get install libegl1
./fetch_fonts.sh                        # free fonts into ./fonts
cd characters && python3 draw_cast.py   # writes the cast image
```
Scripts expect `../fonts/` (environments, daytime) and the Inter font for name tags; adjust paths if needed.

Credit: the character/lighting kit is based on the "Claude 2D Animation Long Form" skill **made by aivxer**.
