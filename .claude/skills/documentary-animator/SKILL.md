---
name: documentary-animator
description: "Turns a finished documentary script (from the documentary-script skill) into the rendered long-form 16:9 animated video for the money documentary channel, in the LOCKED house style: rectangular-head glossy cast, night-print sets for story parts, day-print sets for the lesson part, locked fonts and navy/gold/orange palette, code-made music and SFX, ElevenLabs narrator + Kokoro character voices, 1920x1080 30 fps 24 Mbps. Use when the owner asks to animate / render / make the video for a script, make a test video, or names this skill. Always asks the owner whether to render on their PC or in the cloud before rendering."
---

# Documentary animator (house style, locked)

Makes the finished video from a script. Everything is drawn in code (skia-python), rendered with ffmpeg, music and
sound effects are generated in code. The look is LOCKED in `BRAND.md` (repo root): never change colours, cast,
fonts, sets or looks without the owner's say-so.

Built on the drawing kit and pipeline of the **"Claude 2D Animation Long Form" skill, made by aivxer** (keep this
credit), heavily modified for this channel.

## Before anything else: read `FIXES.md`
`FIXES.md` (in this folder) holds the owner's feedback from the first test render. Until every item there is done
and the owner has approved the result, apply those instructions on every video. Standing rules from it:
**music level stays as it is; sound effects quieter; typed text always uses a real typewriter sound.**

## Hard rules

1. **Ask before every render:** for each new video ask the owner: *render on your Windows PC or in the cloud?*
   Never assume, never reuse the last answer.
2. **Never save, commit or push** anything without the owner's explicit permission. After every change, **ask the owner: "save now or later?"**
3. **Locked style only** (BRAND.md):
   - Cast: rectangular head with curved chin, neck, rectangle body, trouser legs + shoes, ball hands, pupil eyes,
     glossy, drawn crisp on top of the backgrounds (never through the print pass, never grained).
   - Story parts (hook, Ch1-Ch4, twist, ending) use **night-print** sets; the lesson part (Ch5 "your wallet") uses
     **day-print** sets.
   - Colours: gold `#FCA311` = money / brand; orange `#F35B04` = losses only, always with a minus sign or a down
     arrow; gains in navy/white with an up arrow; **no green anywhere** (only exception: real national flags,
     e.g. in `anim.map_route(flag_a=..., flag_b=...)`, keep their true colours); gold and orange never touch.
   - Fonts: DSEG7 counters, Alfa Slab titles / chapter names / stamps, Special Elite text cards + documents (typed
     word by word, gold cursor), Barlow Condensed labels / name tags / sticky notes / place tags.
4. **Truth:** the picture must not show anything the script doesn't support. Real people are drawn in our style with
   only their signature traits (hair, glasses, outfit) and identified with a name tag - never a likeness of a photo.
   Private people are not named.
5. Never copy another channel's characters, frames, titles or thumbnails.
6. Output is always **1920x1080, 30 fps, H.264 24 Mbps, AAC 256 kbps**, max 10 minutes.

## Setup (once per machine)

```bash
pip install skia-python numpy scipy soundfile pillow sherpa-onnx
bash fetch_fonts.sh                      # in the repo root -> ./fonts (or set DOCANIM_FONTS)
mkdir -p ~/models && cd ~/models         # or set DOCANIM_MODELS
R=https://github.com/k2-fsa/sherpa-onnx/releases/download
curl -L -O $R/tts-models/kokoro-multi-lang-v1_0.tar.bz2 && tar xjf kokoro-multi-lang-v1_0.tar.bz2
curl -L -O $R/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2 && tar xjf sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2
```
- **Windows PC:** install Python 3.11+, ffmpeg (`winget install Gyan.FFmpeg`) and Git for Windows; run the commands
  above in Git Bash. With an NVIDIA card set `DOCANIM_ENCODER=h264_nvenc` (still 24 Mbps) for faster encoding.
- **Linux cloud:** skia may need `apt-get install -y libegl1`. Hugging Face is often blocked; the GitHub URLs work.

## Workflow (one video)

Work in `videos/<slug>/` (the video folder). The runner is `make_video.py` in this skill folder.

1. **Script** - from the `documentary-script` skill: `script.json` (beats, speakers, `card`, `counter`,
   `dramatised`, `sources`, `shot_hint`) + `voice_script.md`. Add `"title_after": "<last hook line id>"`.
2. **Narration** - the owner records the narrator lines with ElevenLabs (one file, narrator lines only, in script
   order) and puts it in the video folder as `narration.mp3` / `.wav`.
3. **Voices** - `python <skill>/make_video.py voices`: cuts the narration into one clip per line (speech-to-text
   word timings) and makes every character line with that character's fixed Kokoro voice (`engine/voices.py`
   `CHARACTER_VOICES`). Without a narration file, narrator lines get a temporary Kokoro voice so work can start.
   Watch the log for `NOT MATCHED` lines and Kokoro OOV warnings (add the word to `lex_extra.txt`).
4. **Shot list** - copy `template/shots.py` to the video folder and write **one picture per sentence** (rules below).
5. **Creative quality check (mandatory, by Claude)** - render 3 frames per shot (start / middle / end) into ONE
   compact sheet and review every shot against this checklist; fix everything before the owner renders:
   - **Mistakes:** cut-off text or props, overlaps, empty first frames, characters hidden or too small, tables/props
     not readable, wrong colours (orange only for losses, no green), facts on screen that the script doesn't support.
   - **Repetition:** no two shots in a row with the same composition; a new picture every 2-3 s (hook especially).
   - **Look:** dots subtle (not dominant), vignette on scene shots, framed stage for diagrams/documents.
   - **Creativity:** for every shot ask "would adding something make this more interesting, immersive or
     eye-catching?" (a story-specific prop, a light sweep, a hand action, a detail close-up, a camera move) - add it.
   - Keep usage low: one compact sheet per round; after fixes re-check only the changed shots.
   Then tell the owner what was found and changed.
6. **Ask PC or cloud**, then **render** - `make_video.py render` (one MP4 per shot, all CPU cores).
   On the PC the owner runs the same commands; give them the exact commands in separate `bash` blocks.
7. **Audio** - `make_video.py audio`: cleaned voices (narrator vs character chain, character level-matched to the
   narrator), code music from the mood map, SFX, ducking, two-pass loudnorm to -14 LUFS.
8. **Final** - `make_video.py final` -> `out/final.mp4` + `out/frames.jpg` (one frame every 7 s). Check the sheet.
9. **Check** - `make_video.py check`: transcript of the mix vs the script (aim > 0.9). Claude cannot hear or watch:
   tell the owner to watch once for timing.
10. **Credits** - the typewriter key sounds are a real recording (CC BY 4.0): put the line from
   `assets/typewriter/ATTRIBUTION.md` in every video's description.
11. **Thumbnails** - write 2-3 prompts with the `thumbnail-prompt` skill.
12. **Deliver** - send the MP4 (or the PC commands), with: length, what is in it, facts not checked, dramatised
    lines, and anything to watch for.

## Publishing checklist (every video)
1. **Thumbnail** from the `thumbnail-prompt` skill (biggest factor for clicks).
2. **`videos/<slug>/youtube.md`**: 3 title options, description with chapters (start at 0:00, at least 3), SEC/FBI
   facts as relevant, sources, "Not financial advice", the typewriter credit line, 3 hashtags, 15-20 tags.
3. Upload **`out/captions.srt`** under Subtitles; add the end screen (2 videos + subscribe) over the end-screen section.
4. **Schedule** for the US audience: weekdays 12-4 pm Eastern (Thu/Fri/Sat strongest), weekends 9 am-12 pm Eastern;
   keep the same day/time every week (owner is in India: 12-4 pm ET = about 10:30 pm-2:30 am IST - use Schedule).
5. **Shorts as trailers:** cut 2-3 Shorts from the best moments and link the full video ("Related video").
6. **Playlists** (e.g. "Famous Scams", "Money Lessons"); reply to comments in the first hours.
7. **Length:** aim for 8-10 min on future videos (mid-roll ads need 8+ min once monetised).

## Shot rules (retention)

- **One picture per sentence**; something new every 20-30 s (card, counter, stamp, chart, dialogue, place jump).
- Every shot moves: push-in 5-10% (`zoom=(1.0, 1.07)`), small rotate on desk shots, whip on place jumps, shake on
  stamp hits. Never a frozen frame.
- **Hook:** start in the middle of the action on a night set, a counter or stamp in the first 5 s, title card after
  the hook (sound logo plays automatically).
- **Script line flags:** `card: true` -> full-screen typed text card (`shots.card('text', ...)`, gold for the key
  word); `counter` -> `widgets.counter` (orange + minus + down arrow for losses; ticks + ding / low tone are added
  automatically). Chapter changes -> chapter card (navy, Alfa Slab, gold rule) - add a `chapter:N` shot.
- **Dialogue moments:** two characters, close-ups or a wide two-shot; the speaker's mouth follows its voice clip
  (`Actor.say(tl, line_id, mouths)` with `mouths = tl.mouths()`).
- **Midpoint twist:** text card; the music cuts to silence with a low boom (automatic from the `TWIST` beat).
- **Ch5 "your wallet":** day sets (`day/...`), charts (`widgets.bar_chart`, `line_chart`), counters per American,
  one practical takeaway on a sticky note or card.
- **Ending:** return to the opening set (callback); final-question text card held, then `anim.outro` (sound logo) and
  `anim.end_screen` (~18 s). The timeline adds these automatically (`'outro'`, `'endscreen'` markers); the music
  resolves on a final chord and a soft bed plays under the end screen.
- **Lesson part:** always a red-flags / how-to-spot-it board where the points pop in one by one with the narrator.
- **Use the story animations** (`anim`) often: a hand slam, a stamp, a chart or a prop every 20-30 s.
- **Captions:** small burned-in captions are added to every shot automatically (`engine/captions.py`; bottom centre,
  current word in gold; skipped on typed text cards). `final` also writes `out/captions.srt` for YouTube CC.
  `CAPTIONS=0` turns them off.
- Name tags, place tags and labels go in the shot's `hud` (screen space) so camera moves never crop them.
- Real people: `widgets.lower_third(name, role)` the first time they appear. Places / dates: `widgets.place_tag`.

## Engine reference (`engine/`)

| Module | What it gives |
|---|---|
| `core` | `W, H, FPS`, palette constants, locked fonts (`F_COUNTER`, `F_TITLE`, `F_TYPE`, `F_LABEL`) |
| `kit` | `draw_char` (locked character) + poses `down pocket hip present gesture chin hat hold push point phone facepalm cheer shrug cross wave count`, hair `bald slick silver bob curly buzz bun long`, outfits `suit open sweater hoodie`, eyes `dot half wide closed`, mouths `smile smirk flat o mid open grit`, `walk_legs`, `hand_pos` |
| `cast` | `CAST` (locked: ceo, analyst, worker, banker, investor; archetypes: saver, grad, scammer, agent, reporter, retiree), `person(base, **changes)` for new people |
| `sets` | `get_set(name)` -> `.draw(c, back=[...], front=[...])`, `.spots`, `.rim`, `.light`. Night: `night/office` `night/trading` `night/desk` `night/street` `night/kitchen`. Day: `day/living` `day/kitchen` `day/bank` `day/street` `day/lesson`. Desks/tables are a front layer: actors in `back` stand behind them. Cached in `.cache/sets/` |
| `actor` | `Actor(who, x, y, s, face=, light=, rim=)` with `.pose(t, arms)`, `.expression(t, ...)`, `.walk_to(t0, t1, x1)`, `.say(tl, id, mouths)`; idle bob, blink, squash, overshoot built in |
| `widgets` | `framed_bg` (owner's framed stage), `paper_card`, `big_label`, `arrow`, `text_card`, `chapter_card`, `title_card`, `counter`, `stamp` (returns shake), `pop_label`, `lower_third`, `place_tag`, `sticky`, `document`, `bar_chart`, `line_chart`, `bill`, `coin`, `cash_stack`, `gold_bar`, `falling_money`, `polaroid` |
| `anim` | story animations: `hand_slam` (cash / paper / sticky, returns shake), `pyramid` (Ponzi diagram), `calendar` (tear-off countdown), `map_route`, `handcuffs`, `newspaper` (spin-in), `phone_ring`, `ledger`, `envelope`, `prison_bars`, `sleeve`, `outro`, `end_screen` |
| `shots` | `wide(set, back, front, overlay, t0)`, `closeup(set, actor, focus)` (actor s~2.15, feet y~1390), `card(kind, dur, ...)`, `desk(overlay)`, `plain(overlay)` (framed stage by default) |
| `render` | `render_shot` (24 Mbps), `still`, `contact_sheet`, `join`, `mux`, `frame_sheet` |
| `audio` | mood music (`suspense`, `twist`, `lesson`, `ending`), SFX set (`SFX`), `sound_logo`, `voice_chain`, `mix` (-14 LUFS). Real tracks can replace a mood: put `music_<mood>.wav` in the video folder |
| `voices` | Kokoro character lines (`CHARACTER_VOICES`, picked in the first test render, then fixed), narration splitting, transcript check |
| `timeline` | `build(lines, clips, ...)`, `tl.at(marker)`, `tl.dur(a, b)`, `tl.mood_segments()`, `tl.voice_track()`, `tl.mouths()` |

Character scale guide: wide shot s 0.9-1.1 (feet y 950-1070), street s 0.5-0.6, close-up s 2.15 (feet y 1390).
Use the set's `rim` and `light` for its actors (night: blue rim, key from the left; day: warm rim, key from the right).

## Speed

About 8 frames per second per process at 1080p on a laptop-class CPU; shots render in parallel on all cores.
Backgrounds are drawn once per set and cached; only actors and graphics are drawn per frame.
