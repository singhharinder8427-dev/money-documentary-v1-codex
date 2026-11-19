"""Dirty Dollar portrait reveal and evidence callback. Drawn with the house Skia kit."""
import argparse
import subprocess
import sys
from pathlib import Path

import skia
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "documentary-animator"))

from engine import explainers, kit, widgets
from engine.cast import CAST
from engine.core import FONT_DIR, F_LABEL, F_LABEL2, F_TYPE, GOLD, H, NAVY, PAPER, W


DARK = '#0A142A'
NAME = 'Morgan Reed'
ROLE = 'Company treasurer'


def portrait_image():
    width, height = explainers.PORTRAIT_SIZE
    surface = skia.Surface(width, height)
    c = surface.getCanvas()
    c.clear(kit.hx(NAVY))
    kit.poly(c, [(254, 0), (640, 0), (640, 615), (23, 615)], '#263D65', 0)
    kit.poly(c, [(459, 0), (640, 0), (640, 615), (225, 615)], '#314B77', 0)
    for y in range(10, height, 11):
        first = max(11, round(width * .76 - y * .42))
        for x in range(first + y % 8, width, 11):
            kit.circ(c, x, y, 1.6, '#263D65', 0)
    kit.draw_char(c, 323, 1130, 1.87, CAST['banker'], face=.20, eyes='dot',
                  mouth='smirk', brow=.13, light=1, rim='#FFE3A6')
    return surface.makeImageSnapshot()


def nameplate(c):
    kit.rect(c, 24, 653, 666, 756, PAPER, 0, r=7)
    kit.rect(c, 25, 654, 34, 755, GOLD, 0, r=3)
    widgets.text(c, NAME, 345, 708, 62, NAVY, F_LABEL, 'center')
    widgets.text(c, ROLE, 345, 744, 34, NAVY, F_LABEL2, 'center')


def filing(c, shown, highlighted):
    if shown <= 0:
        return
    left, top, right, bottom = 916, 175, 1710, 864
    c.saveLayerAlpha(None, round(255 * shown))
    c.translate(14 * (1 - shown), 10 * (1 - shown))
    kit.rect(c, left + 14, top + 18, right + 14, bottom + 18, DARK, 0, r=8)
    kit.rect(c, left + 6, top + 8, right + 6, bottom + 8, '#D9CEB6', 3, r=6, v=DARK)
    kit.rect(c, left, top, right, bottom, PAPER, 4, r=7, v=DARK)
    widgets.text(c, 'ILLUSTRATIVE COMPANY FILING', 984, 253, 39, NAVY, F_LABEL)
    kit.line(c, 984, 278, 1643, 278, 4, GOLD)
    widgets.text(c, 'Annual filing', 984, 369, 84, NAVY, F_TYPE)
    widgets.text(c, 'Merrow & Vale Holdings', 984, 435, 45, NAVY, F_TYPE)
    kit.line(c, 984, 476, 1643, 476, 2, '#A89D87')
    if highlighted:
        c.drawRoundRect(skia.Rect(984, 555, 984 + 660 * highlighted, 685), 6, 6, kit.fp(GOLD, 80))
    widgets.text(c, 'SIGNED BY', 1004, 600, 40, NAVY, F_LABEL)
    widgets.text(c, NAME, 1004, 662, 61, NAVY, F_TYPE)
    kit.line(c, 984, 736, 1643, 736, 2, '#A89D87')
    widgets.text(c, ROLE, 984, 793, 43, NAVY, F_LABEL2)
    c.restore()


def sequences(image):
    def reveal(c, time):
        widgets.framed_bg(c)
        explainers.portrait_reveal(c, time, image=image, origin=(615, 148), draw_label=nameplate)

    def callback(c, time):
        widgets.framed_bg(c)
        connector = ((787, 792), (820, 792), (820, 624), (956, 624))
        explainers.portrait_callback(c, time, image=image, origin=(189, 186), draw_label=nameplate,
                                     draw_document=filing, connector=connector)

    return (
        ('12a-portrait-reveal', 'Portrait reveal', reveal,
         ((0.0, 'Edge in shadow'), (.99, 'Light crosses the portrait'), (2.25, 'Name and role'))),
        ('12b-portrait-callback', 'Portrait callback', callback,
         ((0.0, 'The portrait returns'), (.80, 'The filing appears'), (1.96, 'The filing names the treasurer'))),
    )


def save_previews(root):
    title_font = ImageFont.truetype(str(Path(FONT_DIR) / 'BarlowCondensed-Bold.ttf'), 45)
    label_font = ImageFont.truetype(str(Path(FONT_DIR) / 'BarlowCondensed-Bold.ttf'), 29)
    mobile_size = (1000, 1125)
    overview = Image.new('RGB', (1024, 1250), DARK)
    overview_text = ImageDraw.Draw(overview)
    for number, (slug, title, draw, cues) in enumerate(sequences(portrait_image())):
        folder = root / slug
        folder.mkdir(parents=True, exist_ok=True)
        sheet = Image.new('RGB', mobile_size, DARK)
        sheet_text = ImageDraw.Draw(sheet)
        sheet_text.text((12, 4), title, fill=PAPER, font=title_font)
        for index, (time, label) in enumerate(cues, 1):
            surface = skia.Surface(W, H)
            draw(surface.getCanvas(), time)
            target = folder / f'{index:02d}.png'
            surface.makeImageSnapshot().save(str(target), skia.kPNG)
            with Image.open(target) as rendered:
                still = rendered.convert('RGB')
            if index < 3:
                x, y = 10 + (index - 1) * 494, 66
                sheet.paste(still.resize((486, 273), Image.Resampling.LANCZOS), (x, y))
                sheet_text.text((x + 5, y + 280), label, fill=PAPER, font=label_font)
            else:
                final = still.resize((980, 551), Image.Resampling.LANCZOS)
                sheet.paste(final, (10, 405))
                sheet_text.text((15, 970), label, fill=PAPER, font=label_font)
                sheet = sheet.crop((0, 0, 1000, 1014))
                overview_y = 11 + number * 622
                overview_text.text((22, overview_y), title, fill=PAPER, font=title_font)
                overview.paste(final, (22, overview_y + 55))
        sheet.save(folder / 'contact-sheet.jpg', quality=91, subsampling=0)
    overview.save(root / 'portrait-phone-preview.jpg', quality=91, subsampling=0)


def save_motion(path):
    width, height, fps = 960, 540, 30
    surface = skia.Surface(width, height)
    canvas = surface.getCanvas()
    canvas.scale(width / W, height / H)
    args = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{width}x{height}',
            '-r', str(fps), '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(path)]
    with subprocess.Popen(args, stdin=subprocess.PIPE) as encoder:
        for _, _, draw, _ in sequences(portrait_image()):
            for frame in range(96):
                draw(canvas, frame / fps)
                encoded = surface.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType)
                encoder.stdin.write(encoded.tobytes())
        encoder.stdin.close()
        if encoder.wait() != 0:
            raise RuntimeError(f'ffmpeg failed to encode {path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_folder', type=Path)
    parser.add_argument('--motion', action='store_true')
    args = parser.parse_args()
    save_previews(args.output_folder)
    if args.motion:
        save_motion(args.output_folder / 'portrait-motion-small.mp4')
