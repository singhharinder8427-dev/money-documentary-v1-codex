---
name: documentary-animator
description: "Turns a finished documentary script (from the documentary-script skill) into the rendered long-form 16:9 animated video for the money documentary channel, in the LOCKED house style: rectangular-head glossy cast, night-print sets for story parts, day-print sets for lessons and courtroom scenes, locked fonts and navy/gold/orange palette, code-made music and SFX, ElevenLabs narrator + Kokoro character voices, 1920x1080 30 fps 24 Mbps. Use when the owner asks to animate / render / make the video for a script, make a test video, or names this skill. Always asks the owner whether to render on their PC or in the cloud before rendering."
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
   - Story parts (hook, Ch1-Ch4, twist, ending) default to **night-print** sets. The lesson part (Ch5 "your wallet")
     and all courtroom scenes use **day-print** sets.
   - Colours: gold `#FCA311` = money / brand; orange `#F35B04` = losses only, always with a minus sign or a down
     arrow; gains in navy/white with an up arrow; **no green anywhere** (only exception: real national flags,
     e.g. in `anim.map_route(flag_a=..., flag_b=...)`, keep their true colours); gold and orange never touch.
   - Fonts: DSEG7 counters, Alfa Slab titles / chapter names / stamps, Special Elite text cards + documents (typed
     word by word, gold cursor), Barlow Condensed labels / name tags / sticky notes / place tags.
4. **Characters come first (owner's rule):** at the start of EVERY new video, ask the owner: *"Do we need a new
   character, or use an existing one?"* A new character is made BEFORE the video work starts: the owner researches
   the person and sends reference images -> Claude designs the character in our 2D style from them -> show it ->
   adjust until the owner is satisfied -> only then lock it into `REAL` (or the cast) in `engine/cast.py`. Locked
   characters are reused every time (video + thumbnail + later videos); never redesign one without asking.
   **Places + props come first too (owner's rule):** also ask *"New places and props for this story, or reuse existing
   ones?"* Each new story gets its OWN story-specific sets (e.g. Madoff's 17th-floor Manhattan office) and props
   (e.g. fake statements), built in our style in `engine/sets_src/` + `engine/sets.py` / `engine/anim.py`, shown to the
   owner, adjusted until approved, then locked and ADDED to the library (the library keeps growing; never let every
   story reuse the same office/street).
   **Signature parts always stay the same:** the night/day print looks, palette, fonts, vignette, captions, character
   drawing style, title/chapter/text cards + typewriter, counters, stamps, the red-flags board, outro + end screen,
   and the animation tools (filled with each story's own content).
   **Real people:** design each real person's character from their real traits - face cut
   (`face_shape=(width, height)`), hair style + colour (`hair`, `hair_part`), facial hair (`moustache_style`), glasses,
   build/height (scale), signature outfit and props (e.g. Ponzi's boater + gold cane via `kit.cane`) - add it to
   `REAL` in `engine/cast.py`, and use the SAME character in the video and on the thumbnail. Always our 2D style,
   never photo-real.
5. **Truth:** the picture must not show anything the script doesn't support. Real people are drawn in our style with
   only their signature traits (hair, glasses, outfit) and identified with a name tag - never a likeness of a photo.
   Private people are not named.
6. Never copy another channel's characters, frames, titles or thumbnails.
7. Output is always **1920x1080, 30 fps, H.264 24 Mbps, AAC 256 kbps**, max 10 minutes.

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

0. **Characters, places + props** - ask the owner: (a) new character(s) or existing ones? (b) new places and props
   for this story, or reuse existing ones? For new ones: references from the owner -> design -> iterate until approved
   -> lock (cast in `engine/cast.py`, sets in `engine/sets_src/` + `engine/sets.py`, props in `engine/anim.py`).
   Show the current library of sets so the owner can choose what to reuse.
1. **Script** - from the `documentary-script` skill: `script.json` (beats, speakers, `card`, `counter`,
   `dramatised`, `sources`, `shot_hint`) + `voice_script.md`. Add `"title_after": "<last hook line id>"`.
2. **Narration** - the owner records the narrator lines with ElevenLabs (one file, narrator lines only, in script
   order) and puts it in the video folder as `narration.mp3` / `.wav`.
3. **Voices** - `python <skill>/make_video.py voices`: cuts the narration into one clip per line (speech-to-text
   word timings) and makes every character line with that character's fixed Kokoro voice (`engine/voices.py`
   `CHARACTER_VOICES`). Without a narration file, narrator lines get a temporary Kokoro voice so work can start.
   Watch the log for `NOT MATCHED` lines and Kokoro OOV warnings (add the word to `lex_extra.txt`).
4. **Shot list** - copy `template/shots.py` to the video folder. Give each story beat a clear visual and let one scene carry several lines when the action develops naturally (rules below).
5. **Creative quality check (mandatory, by Claude)** - render 3 frames per shot (start / middle / end) into ONE
   compact sheet and review every shot against this checklist; fix everything before the owner renders:
   - **Mistakes:** cut-off text or props, overlaps, empty first frames, characters hidden or too small, tables/props
     not readable, wrong colours (orange only for losses, no green), facts on screen that the script doesn't support.
   - **Variation:** review neighboring shots as a sequence. Look for repeated actions, staging, and runs of
     similar cards or graphics, including repeats disguised by a new character, prop, or location.
   - **Look:** dots subtle (not dominant), vignette on scene shots, framed stage for diagrams/documents.
   - **Clarity:** check what each character, prop, and graphic contributes. Keep the cast focused and simplify
     any crowded shot. Let an effective scene hold while the action develops.
   - Keep usage low: one compact sheet per round; after fixes re-check only the changed shots.
   Then tell the owner what was found and changed.
6. **Ask PC or cloud**, then **render** - `make_video.py render` (one MP4 per shot, all CPU cores).
   On the PC the owner runs the same commands; give them the exact commands in separate `bash` blocks.
7. **Audio** - `make_video.py audio`: cleaned voices (narrator vs character chain, character level-matched to the
   narrator), code music from the mood map, SFX, ducking, two-pass loudnorm to -14 LUFS.
8. **Final** - `make_video.py final` -> `out/final.mp4` + `out/frames.jpg` (one frame every 7 s). Check the sheet.
9. **Check** - `make_video.py check`: transcript of the mix vs the script (aim > 0.9). Claude cannot hear or watch:
   tell the owner to watch once for timing.
10. **Thumbnail** - Claude draws it with the engine and the video's own character (`thumbnail-prompt` skill).
11. **Credits** - the typewriter key sounds are a real recording (CC BY 4.0): put the line from
   `assets/typewriter/ATTRIBUTION.md` in every video's description.
12. **Thumbnail prompts (optional backup)** - write 2-3 prompts with the `thumbnail-prompt` skill.
13. **Deliver** - send the MP4 (or the PC commands), with: length, what is in it, facts not checked, dramatised
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

- **Build around story beats.** Vary what the viewer sees and what happens on screen. Choose from a wide
  establishing shot, a close reaction, an action in progress, a story-specific prop, or a graphic according to
  what the beat needs. Let an action or reaction carry the scene across narration lines when it reads well.
- **Keep the cast focused.** Reuse established characters and introduce a new person when their role clarifies
  the story. A single character or a prop can carry a beat. Use a group when the group itself matters.
- **Use graphics and cards selectively.** Give them screen time when they clarify a relationship, comparison,
  or key figure, or provide a meaningful structural pause. When a scene, action, or readable prop already
  communicates the point, let it carry the explanation.
- Every shot moves: push-in 5-10% (`zoom=(1.0, 1.07)`), small rotate on desk shots, whip on place jumps, shake on
  stamp hits. Never a frozen frame.
- **Hook:** start in the middle of the action on a night set, a counter or stamp in the first 5 s, title card after
  the hook (sound logo plays automatically).
- **Script line flags:** `card: true` marks a candidate for a typed text card. Choose it when the words deserve
  their own frame. Use `widgets.counter` for figures that benefit from a count-up (orange + minus + down arrow
  for losses; ticks + ding / low tone are added automatically). Chapter changes use a `chapter:N` shot
  (navy, Alfa Slab, gold rule).
- **Dialogue moments:** two characters, close-ups or a wide two-shot; the speaker's mouth follows its voice clip
  (`Actor.say(tl, line_id, mouths)` with `mouths = tl.mouths()`).
- **Midpoint twist:** stage the reveal in whichever format makes it land. The music cuts to silence with a
  low boom (automatic from the `TWIST` beat).
- **Ch5 "your wallet":** use day sets (`day/...`) and show the practical takeaway clearly. A chart, counter,
  sticky note, or card can help when the takeaway calls for it.
- **Ending:** return to the opening set for the callback. Hold on the final question through a scene or text card,
  then `anim.outro` (sound logo) and
  `anim.end_screen` (~18 s). The timeline adds these automatically (`'outro'`, `'endscreen'` markers); the music
  resolves on a final chord and a soft bed plays under the end screen.
- **Lesson part:** use a step-by-step red-flags board when the viewer needs to see the points build or compare.
- **Story animations** (`anim`) are available for beats that call for a specific action, such as a hand slam or a stamp.
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
| `sets` | `get_set(name)` -> `.draw(c, back=[...], front=[...])`, `.spots`, `.rim`, `.light`. Night: `night/office` `night/trading` `night/sales_floor` `night/investigation_room` `night/desk` `night/street` `night/kitchen`. Day: `day/living` `day/kitchen` `day/bank` `day/boardroom` `day/courtroom` `day/suburban_home` `day/hotel_ballroom` `day/street` `day/lesson`. Where a set has a furniture layer, actors in `back` stand behind it. Cached in `.cache/sets/` |

See the [approved sales floor](../../../environments/sales-floor/README.md) for the staging example and reusable workstation props.

The [approved sets and paper-trail props](../../../graphics/approved-sets-and-props/README.md) include full-size references, actor spots, and the Ponzi courtroom staging example.

The [story asset library](../../../graphics/story-assets/README.md) lists 22 additional set keys, paper and screen props, furnishings, and seven supporting characters.

See the [approved daytime boardroom](../../../daytime/boardroom/README.md) for the table layer and actor placement.
| `actor` | `Actor(who, x, y, s, face=, light=, rim=)` with `.pose(t, arms)`, `.expression(t, ...)`, `.walk_to(t0, t1, x1)`, `.say(tl, id, mouths)`; idle bob, blink, squash, overshoot built in |
| `widgets` | `framed_bg` (owner's framed stage), `paper_card`, `big_label`, `arrow`, `text_card`, `chapter_card`, `title_card`, `counter`, `stamp` (returns shake), `pop_label`, `lower_third`, `place_tag`, `sticky`, `document`, `bar_chart`, `line_chart`, `bill`, `coin`, `cash_stack`, `gold_bar`, `falling_money`, `polaroid` |
| `anim` | story animations: `hand_slam` (cash / paper / sticky, returns shake), `pyramid` (Ponzi diagram), `calendar` (tear-off countdown), `map_route`, `handcuffs`, `newspaper` (spin-in), `phone_ring`, `ledger`, `envelope`, `prison_bars`, `sleeve`, `police_car`, `phone_screen`, `coin_rain`, `queue` (line of people waiting at a door; `worried=`, `phones=`, `cast=`), `held` (cash / glowing phone in the queue's hands, as overlay), `stamp_shake(hit)` (camera shake for a stamp hit), `outro`, `end_screen` |
| `explainers` | Timed evidence inset, border highlight, port pulses with grouped movement, goods-to-routes reveal, masked place label, portrait reveal and callback, selective emphasis, and object-first process |
| `shots` | `wide(set, back, front, overlay, t0)`, `closeup(set, actor, focus)` (actor s~2.15, feet y~1390), `card(kind, dur, ...)`, `desk(overlay)`, `plain(overlay)` (framed stage by default) |
| `render` | `render_shot` (24 Mbps), `still`, `contact_sheet`, `join`, `mux`, `frame_sheet` |
| `audio` | mood music (`suspense`, `twist`, `lesson`, `ending`), SFX set (`SFX`), `sound_logo`, `voice_chain`, `mix` (-14 LUFS). Real tracks can replace a mood: put `music_<mood>.wav` in the video folder |
| `voices` | Kokoro character lines (`CHARACTER_VOICES`, picked in the first test render, then fixed), narration splitting, transcript check |
| `timeline` | `build(lines, clips, ...)`, `tl.at(marker)`, `tl.dur(a, b)`, `tl.mood_segments()`, `tl.voice_track()`, `tl.mouths()` |

Character scale guide: wide shot s 0.9-1.1 (feet y 950-1070), street s 0.5-0.6, close-up s 2.15 (feet y 1390).
Use the set's `rim` and `light` for its actors (night: blue rim, key from the left; day: warm rim, key from the right).

## Approved explainer overlays (styles 7–14)

In a shot's `draw(canvas, time)` function, draw the story's background first and pass the shot-local time in
seconds to the overlay. Use `widgets.framed_bg` for diagrams and the matching daytime or night-print set for
place labels. The drawing callbacks supply story-specific labels, locations, icons, and evidence.

| Style | Engine call | Use |
|---|---|---|
| 7 · Evidence inset | `explainers.evidence_inset` | Pass the connector points, the inset's pivot, and a document callback. Use its `highlight` progress to emphasize the relevant line. Keep the parent graphic readable while the inset opens. |
| 8 · Animated border highlight | `explainers.border_highlight` | Pass a projected outline and a label callback. Repeat the first point at the end when the outline is closed. |
| 9 · Port pulses and grouped movement | `explainers.port_pulses` | Pass a route, timed port markers, and drawing callbacks for ports and vessels. Adjust `group_size` and `spacing` for the shot. |
| 10 · Goods-to-routes reveal | `explainers.goods_to_routes` | Pass the opening goods, route paths, and callbacks for goods and destinations. Draw the common hub at the same position through the transition. |
| 11 · Masked place label | `explainers.masked_place_label` | Draw the complete place label in a callback. Supply its bounds and set when it opens, holds, and retracts. |

The approved examples and four review frames per style can be regenerated with the installed Skia kit and fonts.
From the repo root in PowerShell, use `D:\pyenv\Scripts\python.exe -B graphics/style-review/render_additional_previews.py "$env:TEMP\dirty-dollar-styles-07-to-11"`.
See the example functions for complete map, inset, and label layouts. [Preview script](../../../graphics/style-review/render_additional_previews.py)

**12 · Portrait reveal and callback.** Draw the approved character as a crisp `explainers.PORTRAIT_SIZE` image and
pass it to `explainers.portrait_reveal`, with a callback for the name and role in the frame's local coordinates.
Reuse the same image and nameplate in `explainers.portrait_callback` later in the story. Give it a document
callback and a connector that ends next to the relevant field. The document callback receives separate progress
values for the page reveal and the field highlight. Use the person's verified name, role, and evidence in a real story.

From the repo root in PowerShell, regenerate the Style 12 stills with
`D:\pyenv\Scripts\python.exe -B graphics/style-review/render_portrait_preview.py "$env:TEMP\dirty-dollar-portrait"`.
Add `--motion` for the silent preview with FFmpeg on `PATH`. [Portrait preview script](../../../graphics/style-review/render_portrait_preview.py)

**13 · Selective emphasis.** Give `explainers.selective_emphasis` the full group and the index of the item to
highlight. Its drawing callback receives separate emphasis and inactive values. Keep every label readable while
the active subject gains the gold accent. For a portrait group, use `muted_portrait_paint` and `emphasis_portrait_card`
with `EMPHASIS_PORTRAIT_SIZE` images. Use the optional note to explain why the selected item matters.

**14 · Object-first process.** Give `explainers.object_first_process` the completed object, its opening and final
poses `(x, y, scale)`, the ordered steps, and the arrow positions. Let the viewer see the completed object before
it moves aside. Keep the same object visible at the end of the flow while its steps appear in order.

From the repo root in PowerShell, regenerate the Style 13 and 14 stills with
`D:\pyenv\Scripts\python.exe -B graphics/style-review/render_emphasis_and_process.py "$env:TEMP\dirty-dollar-styles-13-and-14"`.
Add `--motion` for the silent preview with FFmpeg on `PATH`. [Styles 13–14 preview script](../../../graphics/style-review/render_emphasis_and_process.py)

## Speed

About 8 frames per second per process at 1080p on a laptop-class CPU; shots render in parallel on all cores.
Backgrounds are drawn once per set and cached; only actors and graphics are drawn per frame.
