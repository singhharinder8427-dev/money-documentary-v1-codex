---
name: thumbnail-prompt
description: "Writes detailed AI-image prompts for the money documentary channel's YouTube thumbnails in the locked style (our character style, navy/gold/orange palette, big-face + story-object + top text band composition). Use at the END of every video, after it is rendered, or when the owner asks for thumbnail prompts. The owner generates the images in their own AI image tool; this skill never generates images itself."
---

# Thumbnails (locked style)

**When:** at the end of every video, **after the video is rendered**, so the thumbnail matches the finished story.
**Who makes the image (owner's rule, updated):** **Claude draws the thumbnail itself in code** with the channel engine
(`.claude/skills/documentary-animator/engine`), using **the exact same character as in the video** - see
`videos/ponzi-full/thumbnails/make_thumb.py` for the pattern (blurred set background, big character close-up with an
expression, story props from `anim`, Alfa Slab headline with outline + shadow, 1280x720 + 1920 PNG).
**LOCKED THUMBNAIL STYLE (owner-approved: "$20 MILLION GONE" v3 - `videos/ponzi-full/thumbnails/make_thumb.py`, `thumb()`):**
1. **Background = the channel's own night-print set** of the story (e.g. the 1920s street), only very slightly softened
   (blur ~1.5) - never a heavy blur. Dark navy + dotted print look, the story's place signs readable.
2. **Huge main character** (the locked character of the video) left/centre, ~45-55% of the frame, a strong emotion
   (gritted teeth / wide eyes / sweat drops / hat knocked sideways) + comic shock lines; an orange or gold glow behind
   the head; a spotlight or rim light on the face.
3. **The whole story packed around him** (owner: "add more elements so people can't resist"): 5-8 story elements the
   video really shows - e.g. the crowd/victims, police car + spotlight, the newspaper headline that exposed it, the
   key prop (coupons), cash flying away, coins falling, handcuffs + sparks, an orange crash arrow for a loss.
4. **Headline:** 2-4 huge words across the top, Alfa Slab, thick dark outline + shadow, white + ONE accent
   (orange = loss, gold = money), auto-fit to the width, never covering the face.
5. Make it in code with the engine (1280x720 jpg + 1920 png), 2-3 variants, the owner picks; use YouTube Test & Compare.
6. Everything must be truthful to the video; locked palette; no green (only real flags).

**Real people:** the character is the one locked before the video (from the owner's reference images, approved by the
owner - see the animator skill, hard rule 4); it is designed from the real person's traits (face cut via `face_shape`, hair style/colour,
facial hair, glasses, build, signature clothes + props), always in our 2D style, and the SAME character is used in the
video and on the thumbnail. The text prompts below remain as an optional backup for an AI image tool.
**Deliver:** **2-3 prompt options** per video (different concepts, e.g. big-face shock / story object / evidence
board), each with the exact headline text, plus a one-line note on which to test first and why.

## 1. Every prompt must contain - the locked palette (names, hex codes and jobs)
- Background: deep navy **#14213D** fading to black **#000000**; white **#FFFFFF** and light grey **#E5E5E5** for paper and highlights.
- **Gold #FCA311**: the brand / money colour - key headline word, money objects, positive emphasis.
- **Orange #F35B04**: ONLY losses, crash arrows, fire, danger.
- **No green anywhere** (no green tickers, charts, money or glow). Screens and tickers in the background use navy, gold and orange.

## 2. Every prompt must describe our character style (never the reference channel's round heads)
"Flat 2D cartoon character with one thick dark ink outline; a **slightly rectangular head with soft rounded top
corners and a well-curved rounded chin**; a **short visible neck**; a **rectangular body** wearing a jacket with
lapels; trouser legs and simple rounded shoes; **thin ink-line arms with round ball hands**; **white eyes with dark
pupils and a small highlight**; crisp, bright, glossy colours with a soft sheen and a rim light; no paper texture on
the character."
- **Real people** are drawn in this same style with only their signature traits (hairstyle and colour, glasses,
  signature outfit), never photo-real and never in the reference channel's style. The image must be truthful to
  the video (no events, objects or claims the video doesn't support).
- The channel's recurring cast keeps its looks (see `characters/` and BRAND.md), e.g. the CEO: fair skin,
  side-parted silver hair, white moustache, round glasses, navy suit, gold tie.

## 3. Composition (the formula)
1. **Top text band:** 2-4 huge words across the top, heavy bold font, white + ONE accent word or number in gold
   (money) or orange (loss), thick dark outline, drop shadow. Text sits above the face, never over it.
2. **One big expressive face**, 40-60 % of the frame, usually left or centre: gritted teeth, wide eyes, sweat drops,
   worried or angry brows.
3. **One glowing story object** in the hands or right beside the face that tells the story (a giant gold chess
   king tipping over, a cracking gold bar, a gold 401(k) nest egg, a zipper, a phone, handcuffs, burning cash).
4. **Dark, detailed, blurred background** tied to the story (trading floor, boardroom, courtroom, city at night)
   with bokeh lights; motion cues (sparks, falling coins, an orange crash arrow).
5. **Dramatic lighting:** gold/orange glow from the object, rim light on the character, high contrast, 16:9, sharp.

## 4. Prompt template (fill every bracket)
```
YouTube thumbnail, 16:9, bold flat 2D cartoon illustration, high contrast, eye-catching.
TEXT across the top in huge heavy bold letters with a thick dark navy outline and drop shadow: "[WORD WORD]" in white
and "[ACCENT]" in gold #FCA311 [or orange #F35B04 for a loss].
CHARACTER: [who, e.g. a caricature of <person> with <signature hair/glasses/outfit>] drawn as a flat 2D cartoon with
one thick dark ink outline, a slightly rectangular head with soft rounded top corners and a well-curved rounded chin,
a short visible neck, a rectangular body in a [outfit + colour], thin ink-line arms with round ball hands, white eyes
with dark pupils; expression: [gritted teeth / wide eyes / sweat drops / brows]; crisp, glossy, rim-lit.
STORY OBJECT: [object], glowing gold #FCA311 [with orange #F35B04 sparks/cracks if it's a loss], [what the hands do].
BACKGROUND: [scene] in deep navy #14213D fading to black, blurred, with bokeh lights; screens and tickers only in navy,
gold and orange; [orange #F35B04 crash arrow / falling coins / sparks].
LIGHTING: dramatic gold and orange glow from the object, rim light on the character.
STYLE RULES: no green anywhere, no photorealism, no round-headed characters, no extra text, no logos, no watermarks.
```

## 5. Example (concept the owner liked: "The $1 Trillion Bet")
```
YouTube thumbnail, 16:9, bold flat 2D cartoon illustration, high contrast, eye-catching.
TEXT across the top in huge heavy bold letters with a thick dark navy outline and drop shadow: "THE" and "BET" in
white and "$1 TRILLION" in gold #FCA311.
CHARACTER: an older tech CEO with swept silver-grey hair, rectangular black glasses and a black jacket, drawn as a
flat 2D cartoon with one thick dark ink outline, a slightly rectangular head with soft rounded top corners and a
well-curved rounded chin, a short visible neck, a rectangular body, thin ink-line arms with round ball hands, white
eyes with dark pupils; expression: gritted teeth, one angry brow, wide eyes, a sweat drop; crisp, glossy, rim-lit.
STORY OBJECT: a giant glossy gold #FCA311 chess king piece tipping over, gripped in both ball hands, gold sparks
scraping on a chessboard, a bright star sparkle on the crown.
BACKGROUND: a trading floor in deep navy #14213D fading to black, blurred, with bokeh lights; screens and tickers only
in navy, gold and orange; a bold orange #F35B04 crash arrow zig-zagging down on the right.
LIGHTING: dramatic gold glow from the chess piece, orange rim light on the character.
STYLE RULES: no green anywhere, no photorealism, no round-headed characters, no extra text, no logos, no watermarks.
```
