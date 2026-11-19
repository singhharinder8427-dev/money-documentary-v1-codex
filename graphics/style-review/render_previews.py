"""Dirty Dollar styles 4–6. Skia drawing kit based on aivxer's Claude 2D Animation Long Form."""
import math
from pathlib import Path
import sys

import skia
from PIL import Image

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT.parents[1] / ".claude" / "skills" / "documentary-animator"))

from engine.core import F_TITLE, F_LABEL, F_LABEL2, GOLD, H, NAVY, PAPER, W
from engine.kit import circ, fp, ink, line, poly, rect
from engine.widgets import framed_bg, text

DARK = "#0A142A"
WATER = "#1C3053"
LAND = "#354E77"
RIM = "#718BB5"
MUTED = "#ADC0DF"
LIGHT = "#D6DEEC"

FILES = {
    "04-hub-and-spoke": ("01-hub.png", "02-one-route.png", "03-two-routes.png", "final.png"),
    "05-locator-zoom": ("01-wide.png", "02-locator.png", "03-mid-zoom.png", "final.png"),
    "06-layered-build": ("01-base-site.png", "02-storage.png", "03-inventory.png", "final.png"),
}


def stage(c, title, description):
    framed_bg(c)
    text(c, title, 960, 171, 80, PAPER, F_TITLE, "center")
    line(c, 921, 206, 999, 206, 5, GOLD)
    text(c, description, 960, 264, 43, LIGHT, F_LABEL2, "center")


def panel(c):
    rect(c, 108, 300, 1812, 967, WATER, 3, 16, RIM)
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect(111, 303, 1809, 964), 13, 13))


def paper(c, title, x, y, size=64, secondary=None):
    width = skia.Font(F_LABEL, size).measureText(title) + 66
    height = size + (60 if secondary else 23)
    left, right = x - width / 2, x + width / 2
    rect(c, left + 4, y + 8, right + 4, y + height + 8, DARK, 0, 9)
    rect(c, left, y, right, y + height, PAPER, 2, 9, DARK)
    line(c, left + 18, y + 11, right - 18, y + 11, 4, GOLD)
    text(c, title, x, y + size * .94, size, NAVY, F_LABEL, "center")
    if secondary:
        text(c, secondary, x, y + height - 16, 38, NAVY, F_LABEL2, "center")


def pathline(c, points, width, color, alpha=255):
    path = skia.Path()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    c.drawPath(path, ink(width, color, alpha))


def grid(c, step):
    for x in range(144, 1810, step):
        line(c, x, 304, x, 964, 1, MUTED, 38)
    for y in range(321, 964, step):
        line(c, 111, y, 1809, y, 1, MUTED, 38)


def compass(c):
    text(c, "N", 1732, 370, 44, LIGHT, F_LABEL, "center")
    poly(c, [(1732, 382), (1718, 419), (1732, 411), (1746, 419)], LIGHT, 0)


US = [
    (-124.7,48.4),(-123,48.1),(-122.6,49),(-95,49),(-94.6,48.7),(-92,48.2),
    (-89.5,48),(-87.1,46.9),(-84.6,46.6),(-83,45.7),(-82.5,43.2),(-79,43.8),
    (-76.8,44.8),(-74.8,45),(-71.4,45),(-70.7,47.3),(-67.1,47),(-67,44.8),
    (-70.1,43.1),(-70.7,41.7),(-74,40.5),(-75.2,38.6),(-75.8,36.7),(-76,35.4),
    (-78,33.8),(-80.7,32.2),(-81.4,30.7),(-80.4,27.1),(-80.2,25.5),(-81.3,25),
    (-82.7,27.7),(-83,29),(-84.4,29.8),(-85.4,29.7),(-88,30.4),(-89.8,30),
    (-89.3,29.1),(-91.8,29.5),(-93.8,29.8),(-96.5,28.4),(-97.4,25.9),(-99.3,26.5),
    (-100.3,28.4),(-102.6,29.8),(-104.4,29.5),(-106.5,31.8),(-108.2,31.3),
    (-111,31.3),(-114.7,32.5),(-117.1,32.5),(-118.4,34),(-120.5,34.5),(-121,35.5),
    (-122.5,37.8),(-123.1,39),(-124.4,40.4),(-124.2,42.2),(-124.5,43.1),(-124,45.8),
]
LAKES = [
    [(-92.1,46.8),(-90.9,47.8),(-89.1,47.9),(-87.4,47.1),(-85,46.6),(-87.5,46.5),(-89,46.7)],
    [(-87.1,45.8),(-85.7,46),(-85.6,44.5),(-86.1,42.2),(-87.2,41.7),(-87.6,42.7)],
    [(-84.9,45.9),(-83.5,46.3),(-82.1,45.6),(-81.7,44.5),(-82.5,43.2),(-83.4,44.1)],
    [(-83.3,41.8),(-81.4,42.4),(-78.8,42.9),(-79.9,41.9),(-82.2,41.4)],
    [(-79.8,43.3),(-78.6,43.7),(-76.1,44.1),(-76.6,43.4),(-78.4,43.1)],
]


def us_point(lon, lat):
    return 268 + (lon + 125) * 24.7, 378 + (49 - lat) * 21.6


def route(c, source, control1, control2, target):
    dx, dy = target[0] - control2[0], target[1] - control2[1]
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    tx, ty = target[0] - 17 * ux, target[1] - 17 * uy
    ax, ay = tx - 33 * ux, ty - 33 * uy
    path = skia.Path()
    path.moveTo(*source)
    path.cubicTo(*control1, *control2, ax + 5 * ux, ay + 5 * uy)
    c.drawPath(path, ink(16, DARK))
    c.drawPath(path, ink(8, GOLD))
    poly(c, [(tx, ty), (ax - 15 * uy, ay + 15 * ux), (ax + 15 * uy, ay - 15 * ux)],
         GOLD, 3, DARK)
    circ(c, *target, 9, GOLD, 3, DARK)


def hubs(c, count):
    stage(c, "Distribution routes", "Illustrative U.S. network")
    panel(c)
    grid(c, 91)
    poly(c, [us_point(*point) for point in US], LAND, 3, RIM)
    for lake in LAKES:
        poly(c, [us_point(*point) for point in lake], WATER, 2, RIM)
    for lon, bottom in [(-120,42),(-114,37),(-109,32),(-102,37),(-95,36)]:
        if lon != -120:
            pathline(c, [us_point(lon, bottom), us_point(lon, 48.7)], 1, MUTED, 55)
    for lat, start, end in [(46,-123,-104),(42,-120,-104),(37,-114,-102)]:
        pathline(c, [us_point(start,lat), us_point(end,lat)], 1, MUTED, 55)
    compass(c)
    hub = us_point(-87.63, 41.88)
    destinations = [
        ("Seattle", (-122.33,47.61), (930,434), (610,347), (-3,38)),
        ("Dallas", (-96.8,32.78), (1155,628), (1055,699), (-16,32)),
        ("Atlanta", (-84.39,33.75), (1265,563), (1330,625), (70,37)),
    ]
    for name, coord, control1, control2, (ox, oy) in destinations[:count]:
        target = us_point(*coord)
        route(c, hub, control1, control2, target)
        paper(c, name, target[0] + ox, target[1] + oy, 65)
    circ(c, *hub, 39, DARK, 4, GOLD)
    circ(c, *hub, 25, GOLD, 0)
    circ(c, *hub, 8, DARK, 0)
    line(c, hub[0], hub[1]-38, hub[0], hub[1]-58, 4, GOLD)
    paper(c, "Chicago", hub[0], hub[1]-195, 81, "Distribution hub")
    c.restore()


# A single coastline and port point drive every view. Terminal details use the same
# longitude/latitude space as the regional shore and become legible during the push.
PORT = (-118.217, 33.757)
COAST = [
    (-121.0,35.25),(-120.85,35),(-120.65,34.57),(-120.47,34.45),(-120.07,34.47),
    (-119.71,34.39),(-119.43,34.35),(-119.28,34.27),(-119.24,34.15),(-118.95,34.04),
    (-118.79,34.00),(-118.56,34.04),(-118.50,34.01),(-118.43,33.91),(-118.41,33.84),
    (-118.40,33.79),(-118.42,33.76),(-118.36,33.74),(-118.30,33.71),(-118.28,33.72),
    (-118.272,33.734),(-118.277,33.760),(-118.262,33.773),(-118.258,33.790),
    (-118.239,33.795),(-118.232,33.781),(-118.220,33.787),(-118.202,33.782),
    (-118.193,33.769),(-118.181,33.765),(-118.157,33.762),(-118.143,33.754),
    (-118.12,33.738),(-118.09,33.723),(-118.02,33.675),(-117.88,33.607),
    (-117.74,33.53),(-117.59,33.46),(-117.38,33.24),(-117.29,33.1),
    (-117.26,32.85),(-117.21,32.73),(-117.13,32.54),(-116.93,32.24),
]
TERMINALS = [
    [(-118.251,33.773),(-118.228,33.767),(-118.236,33.756),(-118.235,33.746),
     (-118.259,33.744),(-118.262,33.757)],
    [(-118.224,33.780),(-118.219,33.762),(-118.205,33.762),(-118.201,33.750),
     (-118.228,33.748),(-118.233,33.765),(-118.231,33.785)],
    [(-118.205,33.781),(-118.202,33.765),(-118.187,33.765),(-118.18,33.751),
     (-118.188,33.744),(-118.196,33.750),(-118.201,33.760),(-118.212,33.765)],
    [(-118.261,33.740),(-118.240,33.742),(-118.222,33.731),(-118.231,33.722),
     (-118.258,33.725)],
]
ISLANDS = [
    [(-120.5,34.02),(-120.36,34.07),(-120.28,34.03),(-120.39,33.97)],
    [(-120.26,34.01),(-120.15,34.03),(-120.04,33.97),(-120.15,33.92)],
    [(-119.95,34.05),(-119.76,34.08),(-119.53,34.03),(-119.7,33.97),(-119.89,34)],
    [(-118.61,33.45),(-118.49,33.47),(-118.33,33.34),(-118.43,33.31)],
    [(-118.63,33.03),(-118.53,33.01),(-118.34,32.82),(-118.43,32.82)],
]
BREAKWATERS = [
    [(-118.296,33.706),(-118.249,33.709)],
    [(-118.245,33.710),(-118.210,33.714),(-118.185,33.723)],
    [(-118.176,33.725),(-118.143,33.738),(-118.106,33.741)],
]


def locator(c, frame):
    stage(c, "Southern California", "Pacific coast" if frame < 2 else "San Pedro Bay")
    panel(c)
    grid(c, 90)
    scale = (259, 259, 1300, 6100)[frame]
    anchor_x, anchor_y = ((1015,555), (1015,555), (1000,574), (980,585))[frame]

    def project(lon, lat):
        return anchor_x + (lon - PORT[0]) * scale, anchor_y - (lat - PORT[1]) * scale / .83

    coast = [(-124,38)] + COAST + [(-115,30),(-110,43),(-124,43)]
    poly(c, [project(*point) for point in coast], LAND, 2, RIM)
    for island in ISLANDS + TERMINALS:
        poly(c, [project(*point) for point in island], LAND, 2, RIM)
    for wall in BREAKWATERS:
        pathline(c, [project(*point) for point in wall], 5 if frame == 3 else 2, RIM)
    if frame < 2:
        for name, coord, offset in [
            ("Santa Barbara", (-119.70,34.42), (-94, 53)),
            ("Los Angeles", (-118.24,34.05), (0, -21)),
            ("San Diego", (-117.16,32.72), (110, 15)),
        ]:
            x, y = project(*coord)
            circ(c, x, y, 5, LIGHT, 0)
            text(c, name, x + offset[0], y + offset[1], 46, LIGHT, F_LABEL2, "center")
        text(c, "PACIFIC OCEAN", 570, 797, 48, MUTED, F_LABEL2, "center")
    elif frame == 2:
        text(c, "SAN PEDRO BAY", 746, 818, 48, MUTED, F_LABEL2, "center")
    else:
        text(c, "MIDDLE HARBOR", 717, 767, 49, LIGHT, F_LABEL2, "center")
        text(c, "OUTER HARBOR", 1467, 895, 46, MUTED, F_LABEL2, "center")
        for row in range(3):
            for col in range(5):
                x, y = project(-118.224 + .0027 * col, 33.755 - .0016 * row)
                rect(c, x-6, y-4, x+6, y+4, RIM, 0, 1)
    compass(c)
    if frame:
        x, y = project(*PORT)
        rings = (28,49,72) if frame == 1 else (30,)
        for radius in rings:
            c.drawCircle(x, y, radius, ink(3, GOLD, 230 - radius))
        pathline(c, [(x+20,y),(x+90,y),(x+133,y-44),(x+157,y-44)], 4, GOLD)
        circ(c, x, y, 19, GOLD, 5, DARK)
        circ(c, x, y, 5, DARK, 0)
        paper(c, "Port of Long Beach", x+402, y-88, 64)
    c.restore()


def zone(c, x, width):
    rect(c, x, 381, x+width, 754, "#253C60", 2, 13, RIM)
    for yy in range(402, 749, 18):
        for xx in range(x+16, x+width-9, 18):
            circ(c, xx, yy, 1.4, RIM, 0)
    for yy, turn in [(401,1),(733,-1)]:
        for xx, direction in [(x+18,1),(x+width-18,-1)]:
            pathline(c, [(xx, yy+turn*19),(xx,yy),(xx+direction*23,yy)], 3, MUTED)


def building(c, x, y, scale):
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    poly(c, [(5,85),(212,57),(252,91),(208,140),(33,144)], DARK, 0)
    poly(c, [(0,14),(166,14),(166,115),(0,115)], PAPER, 4, DARK)
    poly(c, [(166,14),(222,-20),(222,79),(166,115)], RIM, 4, DARK)
    poly(c, [(0,14),(34,-31),(200,-31),(166,14)], LIGHT, 4, DARK)
    poly(c, [(34,-31),(91,-68),(252,-68),(200,-31)], PAPER, 4, DARK)
    poly(c, [(166,14),(200,-31),(252,-68),(222,-20)], "#A5B8D7", 4, DARK)
    line(c, 32, 35, 134, 35, 5, GOLD)
    for xx in (17, 65, 113):
        rect(c, xx, 54, xx+34, 110, WATER, 3, 2, DARK)
        for yy in (64,74,84,94):
            line(c, xx+3, yy, xx+31, yy, 2, RIM)
    c.restore()


def crate(c, x, y, scale):
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    poly(c, [(-12,60),(65,60),(112,39),(102,55),(66,74),(-12,74)], DARK, 0)
    poly(c, [(0,0),(66,0),(66,62),(0,62)], "#E1B673", 4, DARK)
    poly(c, [(66,0),(104,-21),(104,40),(66,62)], "#A67D4D", 4, DARK)
    poly(c, [(0,0),(38,-21),(104,-21),(66,0)], PAPER, 4, DARK)
    poly(c, [(25,0),(63,-21),(77,-21),(39,0),(39,20),(25,20)], GOLD, 0)
    line(c, 8,48,23,48,3,DARK)
    c.restore()


def truck(c, x, y, scale):
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    rect(c, 0, 58, 210, 80, DARK, 0, 8)
    rect(c, 0, 0, 137, 66, PAPER, 4, 5, DARK)
    poly(c, [(0,0),(25,-18),(158,-18),(137,0)], LIGHT, 4, DARK)
    poly(c, [(137,20),(176,20),(200,44),(211,48),(211,70),(137,70)], GOLD, 4, DARK)
    poly(c, [(155,27),(174,27),(190,45),(155,45)], WATER, 3, DARK)
    line(c, 16, 20, 117, 20, 4, RIM)
    line(c, 16, 52, 117, 52, 3, RIM)
    for xx in (40, 168):
        circ(c, xx, 69, 17, DARK, 2, NAVY)
        circ(c, xx, 69, 7, LIGHT, 0)
    c.restore()


def site(c, frame):
    stage(c, "Warehouse operation", "Illustrative site plan")
    panel(c)
    rect(c, 134, 338, 1786, 924, "#1E3457", 2, 16, RIM)
    for x in (166, 700, 1234):
        zone(c, x, 520)
    rect(c, 146, 788, 1774, 900, DARK, 2, 10, RIM)
    for x in range(174, 1750, 96):
        line(c, x, 844, x+53, 844, 3, RIM)
    for x in (424, 958, 1492):
        for xx in (x-47, x+47):
            line(c, xx, 756, xx, 786, 3, RIM)
    if frame >= 1:
        building(c, 211, 544, .98)
        building(c, 422, 510, .93)
        paper(c, "Storage buildings", 426, 652, 61)
    if frame >= 2:
        for x, y, scale in [(779,518,.99),(895,494,.97),(1012,473,1.00),
                            (850,570,1.07),(978,553,1.12)]:
            crate(c, x, y, scale)
        paper(c, "Inventory", 960, 652, 61)
    if frame >= 3:
        truck(c, 1304, 471, 1.03)
        truck(c, 1454, 557, 1.03)
        paper(c, "Delivery vehicles", 1494, 652, 61)
    c.restore()


def render():
    for (folder, names), draw in zip(FILES.items(), (hubs, locator, site)):
        output = ROOT / folder
        output.mkdir(exist_ok=True)
        for step, name in enumerate(names):
            surface = skia.Surface(W, H)
            draw(surface.getCanvas(), step)
            surface.makeImageSnapshot().save(str(output / name), skia.kPNG)


def sheets():
    for folder, names in FILES.items():
        output = ROOT / folder
        sheet = Image.new("RGB", (1956, 1116), DARK)
        for index, name in enumerate(names):
            with Image.open(output / name) as still:
                assert still.size == (W, H)
                panel_image = still.convert("RGB").resize((960, 540), Image.Resampling.LANCZOS)
                sheet.paste(panel_image, (12 + 972 * (index % 2), 12 + 552 * (index // 2)))
        sheet.save(output / "contact-sheet.jpg", quality=95, subsampling=0)


if __name__ == "__main__":
    if sys.argv[1:] == ["--sheets"]:
        sheets()
    else:
        render()
