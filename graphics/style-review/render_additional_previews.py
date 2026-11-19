"""Dirty Dollar graphics review, using the drawing kit based on aivxer's Claude 2D Animation Long Form."""
import argparse
import math
import sys
from pathlib import Path

import skia
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "documentary-animator"))

from engine import explainers
from engine.core import FONT_DIR, F_LABEL, F_LABEL2, F_TYPE, GOLD, H, NAVY, PAPER, W
from engine.kit import circ, fp, ink, line, poly, rect
from engine.sets import get_set
from engine.widgets import framed_bg, text
from render_previews import DARK, LAND, LIGHT, MUTED, RIM, US, WATER, compass, grid, panel, paper, pathline, stage, us_point


CALIFORNIA = (
    (-124.21, 42), (-120, 42), (-120, 39), (-114.63, 35), (-114.46, 34.25),
    (-114.72, 33.43), (-114.72, 32.72), (-117.13, 32.54), (-117.31, 33.16),
    (-117.87, 33.61), (-118.27, 33.73), (-118.42, 33.77), (-118.5, 34.03),
    (-119.68, 34.41), (-120.49, 34.45), (-120.62, 34.99), (-121.09, 35.6),
    (-121.91, 36.31), (-121.94, 36.98), (-122.48, 37.8), (-122.96, 38.3),
    (-123.68, 38.94), (-123.75, 39.72), (-124.34, 40.44), (-124.15, 41.05),
    (-124.21, 42),
)
PACIFIC_COAST = (
    (-123.0, 49.4), (-122.72, 48.69), (-122.44, 47.6), (-123.09, 47.0),
    (-124.08, 46.95), (-124.18, 46.23), (-124.09, 45.58), (-124.02, 44.68),
    (-124.35, 43.39), (-124.21, 42),
) + tuple(reversed(CALIFORNIA[7:-1])) + ((-117.13, 32.54), (-116.78, 31.95))


def curved_points(a, b, c, d):
    points = []
    for index in range(33):
        t = index / 32
        q = 1 - t
        points.append(tuple(q ** 3 * a[i] + 3 * q * q * t * b[i] + 3 * q * t * t * c[i] + t ** 3 * d[i]
                            for i in range(2)))
    return points


def dot(canvas, point, *, active=True, radius=12):
    circ(canvas, *point, radius, GOLD if active else LIGHT, 4, DARK)
    if active and radius >= 12:
        circ(canvas, *point, radius / 3, DARK, 0)


def coast(canvas, project):
    outline = (*PACIFIC_COAST, (-115, 30.9), (-106, 30.9), (-106, 51), (-123, 51))
    poly(canvas, [project(*point) for point in outline], LAND, 3, RIM)


def invoice(canvas, highlight):
    x, y, width, height = 1080, 395, 633, 449
    rect(canvas, x + 8, y + 11, x + width, y + height + 10, DARK, 0, 12)
    rect(canvas, x + 3, y + 5, x + width - 3, y + height + 4, '#D7CDB7', 2, 7, DARK)
    rect(canvas, x, y, x + width - 12, y + height, PAPER, 3, 8, DARK)
    text(canvas, 'ILLUSTRATIVE INVOICE', x + 41, y + 62, 41, NAVY, F_LABEL)
    line(canvas, x + 42, y + 83, x + width - 54, y + 83, 4, GOLD)
    text(canvas, 'Freight invoice', x + 41, y + 155, 66, NAVY, F_TYPE)
    text(canvas, 'PORT HANDLING AND DELIVERY', x + 42, y + 217, 35, NAVY, F_LABEL2)
    line(canvas, x + 42, y + 239, x + width - 54, y + 239, 2, NAVY)
    if highlight:
        canvas.drawRoundRect(skia.Rect(x + 35, y + 267, x + 35 + 535 * highlight, y + 361),
                             8, 8, fp(GOLD, 82))
    text(canvas, 'Freight charge', x + 48, y + 328, 47, NAVY, F_TYPE)
    text(canvas, '$240', x + width - 67, y + 332, 62, NAVY, F_LABEL, 'right')
    line(canvas, x + 42, y + 384, x + width - 54, y + 384, 2, '#ABA08E')


def evidence_inset(canvas, time):
    stage(canvas, 'The cost of shipping', 'Illustrative freight charge')
    panel(canvas)
    grid(canvas, 91)

    def project(lon, lat):
        return 560 + (lon + 123) * 85, 495 + (38 - lat) * 76

    coast(canvas, project)
    oakland = project(-122.319, 37.795)
    long_beach = project(-118.217, 33.757)
    route = curved_points(oakland, (410, 638), (620, 832), (long_beach[0] - 18, long_beach[1] + 12))
    explainers.draw_route(canvas, route)
    dot(canvas, oakland)
    dot(canvas, long_beach, radius=15)
    paper(canvas, 'Oakland', oakland[0] - 38, oakland[1] - 97, 58)
    paper(canvas, 'Long Beach', long_beach[0] - 68, long_beach[1] + 29, 58)

    connector = (long_beach, (1014, long_beach[1]), (1048, 622), (1080, 622))
    explainers.evidence_inset(canvas, time, connector=connector, pivot=(1080, 622), draw_document=invoice)
    canvas.restore()


def border_highlight(canvas, time):
    stage(canvas, 'Western United States', 'Regional boundary')
    panel(canvas)
    grid(canvas, 91)

    def project(lon, lat):
        return 235 + (lon + 130) * 65, 345 + (43 - lat) * 50

    coast(canvas, project)
    for boundary in (
        ((-124.21, 42), (-117.04, 42)),
        ((-117.04, 42), (-114.05, 42), (-114.05, 36.1), (-114.70, 35.85), (-114.63, 35)),
        ((-114.05, 37), (-109.05, 37)),
        ((-117.13, 32.54), (-114.72, 32.72), (-111.07, 31.33)),
    ):
        pathline(canvas, [project(*p) for p in boundary], 3, RIM)
    border = [project(*p) for p in CALIFORNIA]
    poly(canvas, border, '#45618D' if time >= 2.85 else LAND, 3, RIM)
    for name, lon, lat in (('OREGON', -121.7, 42.65), ('NEVADA', -116.9, 39.2),
                           ('ARIZONA', -111.65, 34.3), ('PACIFIC OCEAN', -126, 35.5)):
        x, y = project(lon, lat)
        text(canvas, name, x, y, 43, LIGHT if name != 'PACIFIC OCEAN' else MUTED, F_LABEL2, 'center')
    compass(canvas)
    def label(c):
        x, y = project(-120.0, 36.3)
        connector = ((x, y), (x - 58, y), (x - 100, y - 61), (x - 191, y - 61))
        explainers.draw_route(c, connector, width=4, arrow=False)
        dot(c, (x, y), radius=10)
        paper(c, 'California', x - 329, y - 102, 60)

    explainers.border_highlight(canvas, time, outline=border, draw_label=label)
    canvas.restore()


def ship(canvas, x, y, direction, scale=1.0):
    canvas.save()
    canvas.translate(x, y)
    canvas.rotate(math.degrees(math.atan2(direction[1], direction[0])))
    canvas.scale(scale, scale)
    poly(canvas, [(-47, -21), (22, -21), (54, 0), (22, 21), (-47, 21), (-57, 0)], DARK, 5, DARK)
    poly(canvas, [(-41, -14), (20, -14), (42, 0), (20, 14), (-41, 14), (-49, 0)], PAPER, 0)
    for x0 in (-25, -8, 9):
        rect(canvas, x0, -11, x0 + 13, -1, GOLD, 2, 2, NAVY)
        rect(canvas, x0, 2, x0 + 13, 12, '#A5B8D7', 2, 2, NAVY)
    rect(canvas, -39, -10, -29, 10, NAVY, 0, 2)
    canvas.restore()


def fleet_routes(canvas, time):
    stage(canvas, 'Pacific coast shipping', 'Illustrative port sequence')
    panel(canvas)
    grid(canvas, 91)

    def project(lon, lat):
        return 835 + (lon + 124) * 93, 380 + (48.6 - lat) * 28.5

    coast(canvas, project)
    text(canvas, 'PACIFIC OCEAN', 405, 720, 56, MUTED, F_LABEL2, 'center')
    compass(canvas)
    lb = project(-118.217, 33.757)
    oak = project(-122.32, 37.795)
    sea = project(-122.34, 47.60)
    lower = curved_points(lb, (1160, 872), (696, 810), oak)
    upper = curved_points(oak, (493, 626), (630, 446), (sea[0] - 19, sea[1] + 4))
    voyage = lower + upper[1:]
    port_labels = (('Long Beach', 214, 1), ('Oakland', 158, -45), ('Seattle', 150, -44))

    def port(c, index, point, active):
        name, dx, dy = port_labels[index]
        x, y = point
        line(c, x + 12, y, x + dx - 91, y + dy + 31, 3, GOLD if active else RIM)
        dot(c, point, active=active)
        paper(c, name, x + dx, y + dy, 56)

    def vessel(c, x, y, direction):
        ship(c, x, y, direction, .89)

    explainers.port_pulses(canvas, time, voyage=voyage, ports=((lb, .55), (oak, 1.17), (sea, 5.45)),
                          draw_port=port, draw_ship=vessel)
    canvas.restore()


def goods_icon(canvas, name, x, y):
    canvas.save()
    canvas.translate(x, y)
    if name == 'Produce':
        poly(canvas, [(-66, 3), (-51, 57), (52, 57), (67, 3)], '#D7AD6E', 5, NAVY)
        for dx, dy in ((-34, -9), (-4, -24), (33, -10)):
            circ(canvas, dx, dy, 23, GOLD, 4, NAVY)
            line(canvas, dx, dy - 17, dx + 7, dy - 30, 4, NAVY)
        rect(canvas, -65, -1, 66, 20, PAPER, 4, 4, NAVY)
        for xx in (-28, 0, 28):
            line(canvas, xx, 26, xx, 46, 4, NAVY)
    elif name == 'Textiles':
        for yy, color in ((26, '#A5B8D7'), (0, PAPER), (-27, GOLD)):
            poly(canvas, [(-60, yy), (42, yy), (63, yy - 16), (-37, yy - 16)], color, 4, NAVY)
            poly(canvas, [(-60, yy), (42, yy), (42, yy + 20), (-60, yy + 20)], color, 4, NAVY)
            poly(canvas, [(42, yy), (63, yy - 16), (63, yy + 5), (42, yy + 20)], '#8098BE', 4, NAVY)
    else:
        for i in range(10):
            angle = i * 36
            canvas.save()
            canvas.rotate(angle)
            rect(canvas, -10, -57, 10, -32, GOLD, 4, 3, NAVY)
            canvas.restore()
        circ(canvas, 0, 0, 47, GOLD, 5, NAVY)
        circ(canvas, 0, 0, 21, PAPER, 5, NAVY)
    canvas.restore()


def goods_to_routes(canvas, time):
    stage(canvas, 'What moves where?', 'Illustrative trade network')
    panel(canvas)
    grid(canvas, 91)
    poly(canvas, [us_point(*p) for p in US], LAND, 3, RIM)
    compass(canvas)
    hub = us_point(-119.78, 36.74)
    routes = (
        ('Dallas', (-96.8, 32.78), (598, 751), (835, 723), (3, 36)),
        ('Chicago', (-87.63, 41.88), (727, 495), (946, 456), (9, -120)),
        ('Atlanta', (-84.39, 33.75), (709, 605), (995, 661), (98, 38)),
    )
    route_paths = []
    for _, coords, control1, control2, _ in routes:
        x, y = us_point(*coords)
        route_paths.append(curved_points(hub, control1, control2, (x - 15, y)))

    def destination(c, index):
        name, coords, _, _, (dx, dy) = routes[index]
        x, y = us_point(*coords)
        dot(c, (x, y), radius=10)
        paper(c, name, x + dx, y + dy, 60)

    def good(c, index, name, shift):
        x, y = 775 + index * 340, 545 + shift
        rect(c, x - 133, y - 75, x + 133, y + 139, WATER, 3, 12, RIM)
        goods_icon(c, name, x, y + 4)
        paper(c, name, x, y + 70, 54)

    explainers.goods_to_routes(canvas, time, goods=('Produce', 'Textiles', 'Auto parts'),
                              routes=route_paths, draw_good=good, draw_destination=destination)
    dot(canvas, hub, radius=21)
    canvas.drawCircle(*hub, 35, ink(5, GOLD))
    paper(canvas, 'Central Valley', hub[0] + 28, hub[1] + 49, 60)
    canvas.restore()


def masked_place_label(canvas, time):
    framed_bg(canvas)
    x0, y0, x1, y1 = 107, 107, 1813, 973
    shape = skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), 18, 18)
    canvas.save()
    canvas.clipRRect(shape, doAntiAlias=True)
    street = get_set('day/street').base
    cinema_crop = skia.Rect(85, 88, 1835, 976)
    canvas.drawImageRect(street, cinema_crop, skia.Rect(x0, y0, x1, y1), skia.SamplingOptions())

    left, top, right, bottom = 1166, 743, 1722, 863

    def label(c):
        rect(c, left + 6, top + 9, right + 6, bottom + 9, DARK, 0, 13)
        rect(c, left, top, right, bottom, PAPER, 3, 12, DARK)
        rect(c, left + 8, top + 13, left + 18, bottom - 13, GOLD, 0, 4)
        cx, cy = left + 65, top + 56
        poly(c, [(cx - 18, cy + 5), (cx, cy + 31), (cx + 18, cy + 5)], NAVY, 0)
        circ(c, cx, cy - 4, 20, NAVY, 0)
        circ(c, cx, cy - 4, 7, PAPER, 0)
        text(c, 'Market Street', left + 112, top + 80, 73, NAVY, F_LABEL)

    explainers.masked_place_label(canvas, time, bounds=(left, top, right, bottom), draw_label=label)
    canvas.restore()
    canvas.drawRRect(shape, ink(3.5, RIM))


STYLES = (
    ('07-evidence-inset', 'Evidence inset', evidence_inset,
     ((0, 'Map alone'), (1.27, 'Inset opening'), (2.50, 'Invoice visible'), (4.52, 'Charge highlighted'))),
    ('08-border-highlight', 'Animated border highlight', border_highlight,
     ((0, 'Regional map'), (1.70, 'Partial trace'), (2.97, 'Complete outline'), (3.65, 'Final label'))),
    ('09-port-pulses', 'Port pulses and grouped movement', fleet_routes,
     ((0, 'Map alone'), (1.42, 'Origins highlighted'), (3.53, 'Ships in transit'), (5.75, 'Arrival'))),
    ('10-goods-to-routes', 'Goods-to-routes reveal', goods_to_routes,
     ((0, 'Hub alone'), (1.80, 'Goods visible'), (3.04, 'Transition'), (4.40, 'Completed routes'))),
    ('11-masked-place-label', 'Masked place label', masked_place_label,
     ((0, 'Scene alone'), (1.08, 'Label entering'), (2.60, 'Full label'), (3.64, 'Label retracting'))),
)


def gallery(root):
    finals = []
    font_path = str(Path(FONT_DIR) / 'BarlowCondensed-Bold.ttf')
    label_font = ImageFont.truetype(font_path, 30)
    for slug, title, draw, cues in STYLES:
        folder = root / slug
        folder.mkdir(parents=True, exist_ok=True)
        frames = []
        for index, (time, label) in enumerate(cues, 1):
            surface = skia.Surface(W, H)
            draw(surface.getCanvas(), time)
            path = folder / f'{index:02d}.png'
            surface.makeImageSnapshot().save(str(path), skia.kPNG)
            with Image.open(path) as original:
                original.load()
                if original.size != (W, H):
                    raise RuntimeError(f'unexpected frame size in {path}')
                frames.append((original.convert('RGB'), label))

        sheet = Image.new('RGB', (1464, 920), DARK)
        caption = ImageDraw.Draw(sheet)
        for index, (frame, label) in enumerate(frames):
            x, y = 8 + (index % 2) * 728, 8 + (index // 2) * 456
            sheet.paste(frame.resize((720, 405), Image.Resampling.LANCZOS), (x, y))
            caption.text((x + 12, y + 411), label, font=label_font, fill=PAPER)
        sheet.save(folder / 'contact-sheet.jpg', quality=90, subsampling=0)

        final = frames[2 if slug.startswith('11') else 3][0]
        final.resize((1024, 576), Image.Resampling.LANCZOS).save(folder / 'final.jpg', quality=91, subsampling=0)
        representative = frames[2][0] if slug.startswith('09') else final
        mobile = representative.resize((1024, 576), Image.Resampling.LANCZOS)
        finals.append((slug[:2] + '  ' + title, mobile))

    title_font = ImageFont.truetype(font_path, 43)
    all_stills = Image.new('RGB', (1048, 12 + len(finals) * 649), DARK)
    headings = ImageDraw.Draw(all_stills)
    for index, (title, frame) in enumerate(finals):
        y = 12 + index * 649
        headings.text((23, y + 3), title, font=title_font, fill=PAPER)
        all_stills.paste(frame, (12, y + 59))
    all_stills.save(root / 'phone-review.jpg', quality=90, subsampling=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_folder', type=Path)
    gallery(parser.parse_args().output_folder)
