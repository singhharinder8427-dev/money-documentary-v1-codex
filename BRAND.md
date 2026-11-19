# Money Documentary v1: locked brand decisions

Owner-approved, 18 Nov 2026. Change only with the owner's say-so.

**Working rule:** never save / commit / push without the owner's OK - after every change, ask: "save now or later?"

## Channel
- Long-form 16:9 money videos for a **US audience**: money lessons + real money stories. Max **10 minutes**.
- Delivery: **1920x1080, 30 fps, 24 Mbps**; render on PC or in the cloud - ask the owner for every video.

## Colours (locked)
| Colour | Hex | Job |
|---|---|---|
| Navy | `#14213D` | Main background, ink for text on paper |
| Black | `#000000` | Data walls, dark story scenes |
| White | `#FFFFFF` | Paper |
| Light grey | `#E5E5E5` | Cards, desks |
| **Gold** | `#FCA311` | **Brand**: key words, chapter stamps, dollar amounts, highlights |
| **Orange** | `#F35B04` | **Losses and alerts only** |

Exception (owner-approved): **real national flags keep their true colours** (e.g. Italy's green) - flags only, nothing else.

Rules: gold = money / brand, orange = danger / loss, never swapped; they never touch; orange always with a minus sign
or down arrow; gains in navy ink with an up arrow (no green); small handwriting on white paper is navy, not gold.

## Characters (locked) - `characters/`
- **Head:** slightly rectangular, soft top corners, a well-curved rounded chin. **Short neck.**
- **Body:** rectangle with small rounded corners: jacket, lapels, shirt V, tie or bow tie, pocket square.
- **Legs:** trouser legs in the outfit colour + dark rounded shoes. **Arms:** thin ink-line arms, **round ball hands** (no paper hands).
- **Eyes:** white with a dark pupil + highlight (also half-lidded, closed, wide).
- One thick near-black ink outline. **Crisp, bright, glossy** (jacket + head sheen, blue rim light). **No grain on characters.**
- Outfits in navy / gold / grey / brown / black. Cast so far: CEO (fair skin, side-parted silver hair, white outlined
  moustache, glasses, navy suit, gold tie), Analyst, Worker, Banker, Investor.
- Built on the drawing kit of the "Claude 2D Animation Long Form" skill **made by aivxer** (keep this credit), modified.

## Night scenes (locked: "night print") - `environments/`
- Used for the **story / drama parts**; the night twin of the daytime print look, so the whole channel shares one style.
- **Dark areas:** navy paper in 4 shades by each object's brightness (`#0D1630` `#1B2A52` `#2B3F70` `#3E5689`),
  so floors, desks and walls stay separate, with light-navy ink outlines `#9FB3DE`.
- **Lamp / window light:** reveals the day print (cream `#F8EDD3`, warm grey, small soft navy dots), with only outlines
  in dark navy; the light fades out through a **dotted halftone edge**. Gold `#FCA311` stays the spot colour; orange
  only for losses. No smooth glow, no bloom (that is the reference channel's signature).
- **Paper grain on the background only**; locked cast drawn crisp on top with correct occlusion (desks/tables in front
  still hide them). Locked fonts (Alfa Slab / Barlow / Special Elite).
- Sample sets: CEO office, trading floor, desk top-down, street (bank / cash advance / pawn / mortgages), kitchen.

## Daytime scenes (locked: style A "printed illustration") - `daytime/`
- Used for **lessons / "your money" parts**; night scenes stay for the story and drama parts.
- The world is a **2-colour print**: navy ink outlines on cream paper `#F6EFE2`, light navy tint `#D6DEEC` under
  shade, **small soft navy halftone dots** `#465C8C` for shading (lightened on the owner's request), solid mid-navy
  for navy objects, **gold `#FCA311` as the only spot colour**. No smooth gradients, no bloom, no green.
- Sunlight = clean cream areas cutting through the dotted shade.
- **Characters stay full-colour and glossy** on top (drawn after the print pass), with a soft contact shadow.
- Our own details instead of the reference channel's: no checkerboard floors (bank = cream marble + gold medallion),
  autumn-gold trees and dried pampas grass instead of green plants.
- Sample sets: living room, kitchen (morning), bank lobby, Main Street, lesson room (whiteboard + counter).
- Animation tip: render each shot's background once as a still, animate characters/props over it.

## Fonts (locked) - `type/`
| Use | Font |
|---|---|
| Number counters | **DSEG7 Classic** (digital); gold for money, orange for losses |
| Titles + chapter names | **Alfa Slab One** |
| Text cards, documents, quotes | **Special Elite** (typewriter, typed word by word, gold cursor) |
| Labels, name tags, sticky notes, place tags | **Barlow Condensed** |

## Script structure (locked) - `.claude/skills/documentary-script/`
- **Template A** for every documentary (money stories, corruption, scams, rackets, fraud): hook (<= 45 s, title at
  ~0:45) -> Ch 1 origin -> Ch 2 the opening -> Ch 3 the plan -> midpoint twist -> Ch 4 the fallout -> Ch 5 your
  wallet -> callback ending. 10 min default, ~1,500 words at 155 wpm.

## Real people + thumbnails (owner's rule)
- **Characters come first:** before each video Claude asks "new character or existing one?". For a new one the owner
  researches and sends reference images; Claude designs it in our style; we iterate until the owner is satisfied; then
  it is locked and reused every time.
- **Places + props per story:** before each video Claude also asks "new places and props, or reuse existing ones?".
  Each story gets its own story-specific sets and props in our style (approved first), added to a growing library.
  **Signature parts never change:** looks, palette, fonts, vignette, captions, character style, title/chapter/text
  cards + typewriter, counters, stamps, red-flags board, outro + end screen.
- Every real person a video is about gets a character built from their **real traits** (face cut, hair, facial hair,
  glasses, build, signature outfit and props) in our 2D style, and **the same character appears in the video and on
  the thumbnail**. Claude draws the thumbnail in code with the channel engine.

## Thumbnails (locked) - `.claude/skills/thumbnail-prompt/`
- **Locked style (owner-approved "$20 MILLION GONE" v3):** the channel's own night-print set as a sharp background, a
  huge emotional main character with shock lines and a glow, the whole story packed around him (crowd, police car +
  spotlight, newspaper headline, key prop, flying cash, coins, crash arrow), a big Alfa Slab headline (white + one
  orange/gold accent). Drawn by Claude in code with the engine.
- Made by the owner in an AI image tool from **detailed prompts written at the end of every video** (after render),
  2-3 options per video.
- Every prompt names the locked palette (hex + jobs, no green) and describes **our character style**; real people
  drawn in our style with their signature traits.
- Formula: top text band (white + one gold/orange word), one big expressive face, one glowing story object,
  dark blurred story background, dramatic rim light.

## Voices (locked) - test in the first short render
- **Narrator:** ElevenLabs (owner makes it from `voice_script.md`).
- **Characters:** a free local voice model (**Kokoro**, runs on the owner's PC), one fixed voice per recurring
  character so they sound the same in every video; clips made automatically from the speaker labels in `script.json`.
- Character clips get a light loudness/tone match to the ElevenLabs narration so the switch sounds smooth.
- Lip-sync: mouths move from each clip's loudness (same for both voice sources).
- Voice picks per character are chosen during the first short test render, not before.

## Music + sound (locked: option D, made in code) - test in the first short render
- **All music and sound effects are generated in code.** The render reads the beat marks in `script.json`
  (hook, chapters, midpoint twist, wallet lesson, ending, cards, counters, stamps) and places everything itself.
- **Swappable:** music is chosen by mood tag, so licensed / ElevenLabs tracks can replace the code music later
  without changing anything else (decide after the first test render).
- **Mood map:**
  | Part | Mood |
  |---|---|
  | Night story parts (hook, Ch1-Ch4) | dark true-crime suspense: low synth pulse, ticking clock, tense plucked strings |
  | Midpoint twist | music cuts to silence, then a deep low boom as the card lands |
  | Day lesson part (Ch5 "your wallet") | lighter and warmer: soft piano, marimba, light percussion |
  | Callback ending | opening theme returns softer, ends on silence over the final question card |
  | Title card | 2-second **sound logo**, same every video: typewriter clack + coin ring |
- **Sound effects (fixed set):** typewriter keys (text cards, matches Special Elite), stamp thud, counter ticks that
  speed up and end in a gold "ding" (money) or a low tone (loss), paper slides + whooshes (props, scene changes),
  cash / coin sounds (money), falling tone (orange loss moments).
- **Mix:** music well under the voice with automatic ducking whenever someone speaks; the final mix is levelled to
  YouTube's standard loudness (about -14 LUFS).

## Rendering pipeline (locked) - based on the aivxer "Claude 2D Animation Long Form" skill (made by aivxer)
- **Ask every time:** for each new video, ask the owner whether to render on their **Windows PC** or **in the cloud**.
  Never assume.
- **Output:** 1920x1080, 30 fps, H.264 at **24 Mbps** (`-b:v 24M -maxrate 24M -bufsize 48M`), AAC 256 kbps,
  videos up to 10 minutes.
- **Steps:**
  1. Script (`documentary-script` skill, Template A) -> `script.json` with beats, speakers, cards, counters.
  2. Shot list: one picture per sentence, using the locked night sets (story parts) and day sets (lesson parts).
  3. Voices: narrator = owner's ElevenLabs file; characters = Kokoro clips, one fixed voice per character.
  4. Timeline: every shot and line timed from the measured voice lengths.
  5. Test stills: 6-9 of the busiest frames on one contact sheet, fixed before the long render.
  6. Render: every frame drawn in Python (skia) with the locked kit, piped into ffmpeg, one MP4 per shot, joined
     without re-encoding. Static backgrounds are drawn once (night/day print pass) and reused; characters and
     props animate on top.
  7. Audio: voice clean-up, code-made music + SFX from the mood map, ducking, -14 LUFS, muxed onto the video.
  8. Check: transcribe the final audio with a free speech-to-text model against the script; one frame per shot
     on a contact sheet; the owner watches once for timing.
  9. Thumbnail prompts (`thumbnail-prompt` skill) after the render.
- **Changes from the uploaded skill:** our cast, fonts, night/day print looks and text cards instead of its round
  heads, handwritten fonts, glow and white handwriting cards; 24 Mbps instead of its quality setting; our mood map
  instead of its single jazzy track; ElevenLabs narration + Kokoro characters handled as separate files.

## Channel name (locked)
- **DIRTY DOLLAR** (owner's final choice). Written "DIRTY" in white + "DOLLAR" in gold, Alfa Slab One.
- Branding in `branding/`: `profile_800.png` (**official profile photo**: the CEO close-up with gold dollar-sign eyes
  and a greedy grin, gold rays, no text; `profile_coin_800.png` = spare coin version), `banner_2560x1440.png`
  (text inside YouTube's safe area; cast on the sides - desktop/TV), `banner_mobile_2560x1440.png` (**the official banner** - owner's choice: cast +
  name + tagline all inside the phone-visible strip), made by `make_branding.py`.
- "Paper Trillions" was only a working placeholder - never use it publicly.


## YouTube channel profile (locked)
- **Name:** Dirty Dollar · **Handle:** @DirtyDollarFile
- **Description:**
  > Dirty Dollar tells the true stories behind money — the scams, frauds, cons and corruption that took fortunes,
  > and the lessons that protect yours.
  >
  > Every video is a fact-checked, animated documentary: real people, real numbers, real consequences. Then we show
  > you how the same trick shows up in your wallet today — and how to spot it before it costs you.
  >
  > 🎬 Scams & con artists · Fraud & corruption · Business scandals · Money lessons
  >
  > Subscribe so you never fall for the next one.
  >
  > Educational content only — not financial advice. Sources are listed in every video description.
- **Keywords** (Studio → Settings → Channel → Basic info):
  `dirty dollar, money stories, scams explained, scam awareness, fraud documentary, financial fraud, true crime money,
  ponzi scheme, con artists, white collar crime, corruption stories, investment scams, how scams work, money lessons,
  personal finance, financial literacy, business scandals, money history, animated documentary, wall street scandals`

## Not decided yet
- nothing - all brand decisions are locked.
