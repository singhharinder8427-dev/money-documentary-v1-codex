---
name: thumbnail-prompt
description: "At the final production stage, writes a detailed, copy-ready YouTube thumbnail prompt for Dirty Dollar. Use the approved character, house palette and typography, a strong expression, and one dominant story prop. The owner returns the prompt to the assistant for image generation."
---

# Thumbnail prompt

After the episode is rendered, read the finished story and select an accurate visual hook. Give the owner one complete prompt they can paste back into the assistant for image generation. Include alternate concepts when the owner asks.

Use Paper Billions as a reference for tight cropping, expressive acting, and a prop that carries the story at phone size. Use an original Dirty Dollar composition and artwork. The approved Ponzi thumbnail in `videos/ponzi-full/thumbnails/make_thumb.py` is a reference for the house type and character treatment.

Write a prompt for a 16:9 composition. Match the approved episode character’s rectangular head, facial traits, wardrobe, and proportions. Specify the person’s expression, gaze, pose, and hand placement. Give the central prop believable materials and a clear silhouette. Tie the setting to the story and keep background detail subordinate to the face and the prop. Use the sourced facts to choose the headline, dates, amounts, and any brand cues.

Include a relevant real-world logo when it helps identify the subject. Ask for a simplified, independently drawn 2D mark with roughly 60% resemblance, keeping the familiar motif and using Dirty Dollar colours. Name its placement on a story object or in the setting. For Nvidia, describe a simplified stepped eye badge in gold or white on navy or black.

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
4. **Story-specific background** with Dirty Dollar’s print texture and a dark navy vignette. Soften background details enough to make the face and prop read at phone size.
5. **Lighting:** use gold or warm white on the prop and on the edges of the face and jacket. Use orange only for a loss or alert.

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
BACKGROUND: [scene] in deep navy #14213D with a dark vignette and subtle paper grain; [story-specific detail]. Keep the face and prop sharp and readable at phone size.
LIGHTING: [direction of the light], warm gold rim light on the character. Use orange #F35B04 only for a loss or alert.
COMPANY MARK: [if relevant, specify the company, recognizable motif, simplified 2D geometry, house colour, and placement on the prop or set].
STYLE: Dirty Dollar 2D cartoon rendering, locked palette, the exact requested headline, story-specific props and marks.
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
STYLE: Dirty Dollar 2D cartoon rendering with the exact headline and the locked palette.
```
