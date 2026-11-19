"""Dirty Dollar style previews for selective emphasis and object-first processes."""
import argparse
from functools import lru_cache
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
import skia

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "documentary-animator"))

from engine import explainers, kit, widgets
from engine.cast import CAST
from engine.core import FONT_DIR, F_LABEL, F_TITLE, F_TYPE, GOLD, H, NAVY, PAPER, W
from render_previews import DARK, LIGHT, RIM, stage


PORTRAIT_W, PORTRAIT_H = explainers.EMPHASIS_PORTRAIT_SIZE
ROLE_CARDS = (('ceo', 'Promoter'), ('banker', 'Account operator'), ('investor', 'Investor'))
STEP_POSITIONS = (339, 686, 1033)
STEP_LABELS = ('Send invoice', 'Approve invoice', 'Send payment')


def portrait(who):
    surface = skia.Surface(PORTRAIT_W, PORTRAIT_H)
    canvas = surface.getCanvas()
    canvas.clear(kit.hx('#263D65'))
    kit.poly(canvas, [(244, 0), (420, 0), (420, 380), (106, 380)], '#334E7C', 0)
    for y in range(8, PORTRAIT_H, 12):
        for x in range(284 + y % 7 - y // 4, PORTRAIT_W, 12):
            kit.circ(canvas, x, y, 1.3, '#263D65', 0)
    kit.draw_char(canvas, 210, 723, 1.20, CAST[who], face=.12, eyes='dot',
                  mouth='flat', brow=.14, light=1, rim='#FFE3A6')
    return surface.makeImageSnapshot()


def selective_scene():
    muted = explainers.muted_portrait_paint()
    portraits = [(portrait(who), name) for who, name in ROLE_CARDS]

    def item(canvas, index, item, emphasis, inactive):
        image, name = item
        explainers.emphasis_portrait_card(canvas, image, name, (398 + index * 562, 552),
                                          emphasis=emphasis, inactive=inactive, muted=muted)

    def note(canvas):
        kit.line(canvas, 960, 824, 960, 856, 5, GOLD)
        kit.circ(canvas, 960, 854, 6, GOLD, 0)
        kit.rect(canvas, 600, 870, 1320, 954, DARK, 2, r=8, v=GOLD)
        widgets.text(canvas, 'Can move funds out of the account', 960, 926, 49,
                     PAPER, F_LABEL, 'center')

    def draw(canvas, time):
        stage(canvas, 'Who controls the account?', 'Illustrative account access')
        explainers.selective_emphasis(canvas, time, items=portraits, selected=1,
                                      draw_item=item, draw_note=note)

    return draw


def paid_invoice(canvas, x, y, scale):
    canvas.save()
    canvas.translate(x, y)
    canvas.scale(scale, scale)
    kit.rect(canvas, -241, -262, 267, 283, DARK, 0, r=11)
    kit.rect(canvas, -247, -269, 259, 275, '#D9CEB6', 3, r=8, v=DARK)
    kit.rect(canvas, -253, -276, 253, 268, PAPER, 4, r=7, v=DARK)
    kit.poly(canvas, [(180, -276), (253, -203), (180, -203)], '#D9CEB6', 3, DARK)
    widgets.text(canvas, 'SAMPLE INVOICE', -203, -205, 41, NAVY, F_LABEL)
    kit.line(canvas, -203, -182, 166, -182, 4, GOLD)
    widgets.text(canvas, 'Invoice', -202, -83, 84, NAVY, F_TYPE)
    kit.line(canvas, -203, -45, 202, -45, 2, '#B6A991')
    widgets.text(canvas, 'TOTAL', -202, 22, 49, NAVY, F_LABEL)
    widgets.text(canvas, '$240', 203, 22, 58, NAVY, F_LABEL, 'right')
    kit.line(canvas, -203, 51, 202, 51, 2, '#B6A991')
    canvas.save()
    canvas.translate(5, 157)
    canvas.rotate(-8)
    kit.rect(canvas, -146, -51, 146, 53, None, 7, r=8, v=NAVY)
    kit.rect(canvas, -142, -47, 142, 49, GOLD, 0, r=6)
    widgets.text(canvas, 'PAID', 0, 27, 78, NAVY, F_TITLE, 'center')
    canvas.restore()
    canvas.restore()


def step_icon(canvas, index):
    if index == 0:
        kit.rect(canvas, -61, -62, 40, 62, PAPER, 4, r=7, v=DARK)
        kit.poly(canvas, [(12, -62), (40, -34), (12, -34)], '#BCCBE5', 3, DARK)
        for y in (-24, -3, 18):
            kit.line(canvas, -43, y, 14, y, 4, NAVY)
        kit.poly(canvas, [(-9, 42), (78, 14), (47, 81), (24, 59)], GOLD, 4, DARK)
        kit.line(canvas, 25, 57, 65, 25, 3, NAVY)
    elif index == 1:
        kit.rect(canvas, -62, -54, 64, 70, PAPER, 4, r=9, v=DARK)
        kit.rect(canvas, -31, -70, 32, -47, '#ACBEDD', 3, r=5, v=DARK)
        for y in (-18, 8, 34):
            kit.line(canvas, -42, y, 23, y, 4, NAVY)
        kit.circ(canvas, 44, 36, 33, GOLD, 5, DARK)
        path = skia.Path()
        path.moveTo(27, 36)
        path.lineTo(39, 48)
        path.lineTo(59, 23)
        canvas.drawPath(path, kit.ink(6, NAVY))
    else:
        kit.poly(canvas, [(-76, -21), (0, -63), (76, -21)], PAPER, 4, DARK)
        kit.rect(canvas, -67, -21, 67, 52, '#334E7C', 4, r=4, v=DARK)
        for x in (-48, -8, 32):
            kit.rect(canvas, x, -12, x + 16, 42, LIGHT, 0, r=3)
        kit.rect(canvas, -79, 40, 80, 57, PAPER, 3, r=4, v=DARK)
        widgets.bill(canvas, 28, 49, -10, .61)


def step_card(canvas, index, label, shown):
    if shown <= 0:
        return
    x = STEP_POSITIONS[index]
    y = 617 + 24 * (1 - shown)
    canvas.saveLayerAlpha(None, round(255 * shown))
    kit.rect(canvas, x - 136, y - 159, x + 151, y + 177, DARK, 0, r=13)
    kit.rect(canvas, x - 143, y - 169, x + 143, y + 167, '#273E65', 3, r=13, v=RIM)
    kit.line(canvas, x - 51, y - 141, x + 51, y - 141, 5, GOLD)
    canvas.save()
    canvas.translate(x, y - 34)
    step_icon(canvas, index)
    canvas.restore()
    kit.rect(canvas, x - 126, y + 90, x + 126, y + 145, PAPER, 0, r=6)
    widgets.text(canvas, label, x, y + 128, 40, NAVY, F_LABEL, 'center')
    canvas.restore()


@lru_cache(maxsize=1)
def invoice_stage():
    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()
    stage(canvas, 'How an invoice gets paid', 'Illustrative payment workflow')
    kit.rect(canvas, 109, 301, 1810, 967, '#192D4E', 3, r=16, v=RIM)
    for y in range(344, 936, 22):
        for x in range(135 + y % 13, 1788, 22):
            kit.circ(canvas, x, y, 1.4, '#283F66', 0)
    return surface.makeImageSnapshot()


def object_first(canvas, time):
    canvas.drawImage(invoice_stage(), 0, 0)
    explainers.object_first_process(
        canvas, time, steps=STEP_LABELS, links=((490, 535, 619), (837, 882, 619), (1185, 1325, 619)),
        first_pose=(960, 626, 1.02), last_pose=(1547, 619, .83), draw_object=paid_invoice, draw_step=step_card,
    )


def examples():
    return (
        ('13-selective-emphasis', 'Selective emphasis', selective_scene(), 114,
         ((0, 'All roles shown'), (1.30, 'Attention shifts'), (2.03, 'Operator in focus'), (3.14, 'Role explained'))),
        ('14-object-first', 'Object-first process', object_first, 171,
         ((0, 'Start with the paid invoice'), (2.16, 'First step appears'), (3.16, 'Approval appears'),
          (5.22, 'The full process'))),
    )


def save_stills(output, scenes):
    font_path = str(Path(FONT_DIR) / 'BarlowCondensed-Bold.ttf')
    font = ImageFont.truetype(font_path, 31)
    heading = ImageFont.truetype(font_path, 47)
    overview = Image.new('RGB', (1024, 1260), DARK)
    titles = ImageDraw.Draw(overview)
    for style_index, (slug, title, draw, _, keys) in enumerate(scenes):
        folder = output / slug
        folder.mkdir(parents=True, exist_ok=True)
        sheet = Image.new('RGB', (1464, 920), DARK)
        notes = ImageDraw.Draw(sheet)
        for index, (time, label) in enumerate(keys):
            surface = skia.Surface(W, H)
            draw(surface.getCanvas(), time)
            still_path = folder / f'{index + 1:02d}.png'
            surface.makeImageSnapshot().save(str(still_path), skia.kPNG)
            with Image.open(still_path) as image:
                still = image.convert('RGB')
            x, y = 8 + index % 2 * 728, 8 + index // 2 * 456
            sheet.paste(still.resize((720, 405), Image.Resampling.LANCZOS), (x, y))
            notes.text((x + 13, y + 412), label, fill=PAPER, font=font)
            if index == len(keys) - 1:
                row = 8 + style_index * 625
                titles.text((22, row), title, fill=PAPER, font=heading)
                overview.paste(still.resize((980, 551), Image.Resampling.LANCZOS), (22, row + 57))
        sheet.save(folder / 'contact-sheet.jpg', quality=90, subsampling=0)
    overview.save(output / 'phone-review.jpg', quality=90, subsampling=0)


def save_motion(path, scenes):
    width, height, fps = 960, 540, 30
    surface = skia.Surface(width, height)
    canvas = surface.getCanvas()
    canvas.scale(width / W, height / H)
    args = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra',
            '-s', f'{width}x{height}', '-r', str(fps), '-i', '-', '-an', '-c:v', 'libx264',
            '-preset', 'fast', '-crf', '23', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(path)]
    with subprocess.Popen(args, stdin=subprocess.PIPE) as encoder:
        for _, _, draw, duration, _ in scenes:
            for frame in range(duration):
                draw(canvas, frame / fps)
                pixels = surface.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType)
                encoder.stdin.write(pixels.tobytes())
        encoder.stdin.close()
        if encoder.wait() != 0:
            raise RuntimeError(f'ffmpeg failed to encode {path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_folder', type=Path)
    parser.add_argument('--motion', action='store_true')
    args = parser.parse_args()
    scenes = examples()
    save_stills(args.output_folder, scenes)
    if args.motion:
        save_motion(args.output_folder / 'styles-13-and-14-small.mp4', scenes)
