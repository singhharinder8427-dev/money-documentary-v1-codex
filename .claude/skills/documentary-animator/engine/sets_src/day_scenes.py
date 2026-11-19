"""Scene drawings for the daytime sets. Run print_look.py (not this file) to get the locked print style.
Five DAYTIME scenes for money-lesson videos. Same kit, same locked characters and palette as the night sets,
but lit by daylight: bright cream/sky-blue base, gold sunlight shafts, soft cool shade, light vignette.
Paper grain on the background only; characters drawn last, crisp and glossy. No green anywhere."""
import os, math, random
import numpy as np
from PIL import Image as _PI, ImageFilter as _PF
import kit
from engine.core import FONT_DIR as _FD; kit.FD = _FD
from kit import *
def _shape(c, path, fill, w=LW, v=INK):
    if fill is not None: c.drawPath(path, fill if isinstance(fill, skia.Paint) else fp(fill))
    if w: c.drawPath(path, ink(w, v))
kit.shape = _shape; shape = _shape
TF = lambda n: skia.Typeface.MakeFromFile(kit.FD + n)
SLAB, BAR, BARS, TYPE, DSEG = TF('AlfaSlabOne-Regular.ttf'), TF('BarlowCondensed-Bold.ttf'), TF('BarlowCondensed-SemiBold.ttf'), TF('SpecialElite-Regular.ttf'), TF('DSEG7Classic-Bold.ttf')
NAVY, NAVY2, NAVY3, GOLD_, ORNG, WHITE, GREY = '#14213D', '#1E3157', '#2B4A7A', '#FCA311', '#F35B04', '#FFFFFF', '#E5E5E5'
SKY0, SKY1, CREAM, OAK, OAK_D = '#8FAEE0', '#DDE8F8', '#F4ECDF', '#C99A66', '#A87C4E'
RIM = '#FFE3A6'

CEO = dict(skin='#F8E2D2', skin_d='#E6C4AE', suit=NAVY, suit_d='#0C152B', shirt=WHITE, tie=GOLD_, hair='silver', hair_col='#ECECF1', glasses=True,
           moustache=True, moustache_col='#FFFFFF', moustache_outline=True, moustache_dy=10)
ANALYST = dict(skin='#C8875A', skin_d='#A86C43', suit=GREY, suit_d='#BDBDBD', shirt=WHITE, tie=NAVY, hair='slick', hair_col='#1A1414', glasses=True)
WORKER = dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#6B4A2E', suit_d='#4F3520', shirt='#F4EFE2', tie='#2B4A7A', hair='slick', hair_col='#7A4A26', hat_col='#3A3F4A', hat_band=GOLD_)
BANKER = dict(skin='#E2B48C', skin_d='#C49468', suit='#2E2E38', suit_d='#1E1E26', shirt=WHITE, tie=GOLD_, bowtie=True, hair='slick', hair_col='#3A2A20', moustache=True, hanky=GOLD_)
INVESTOR = dict(skin='#8D5A3B', skin_d='#6F4429', suit=GOLD_, suit_d='#D88A06', shirt=WHITE, tie=NAVY, hair=None)

def text(c, s, x, y, size, color, tf=None, align='left', stroke=0, sc=INK, rot=0):
    f = skia.Font(tf or BAR, size); w = f.measureText(s); ox = {'left': 0, 'center': -w / 2, 'right': -w}[align]
    c.save(); c.translate(x, y); c.rotate(rot)
    if stroke: st = ink(stroke, sc); c.drawString(s, ox, 0, f, st)
    c.drawString(s, ox, 0, f, fp(color)); c.restore(); return w
def path(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]
    if close: p.close()
    return p
def cloud(c, x, y, s):
    p = skia.Path()
    for dx, dy, r in ((0, 0, 46), (52, -22, 56), (110, 0, 44), (56, 14, 48)): p.addCircle(x + dx * s, y + dy * s, r * s)
    p = skia.Op(p, skia.Path(), skia.PathOp.kUnion_PathOp) if False else p
    c.drawPath(p, fp(WHITE));
def sky(c, x0, y0, x1, y1, scene='suburb', seed=2, sun=None):
    rnd = random.Random(seed); c.save(); c.clipRect(skia.Rect(x0, y0, x1, y1))
    c.drawRect(skia.Rect(x0, y0, x1, y1), sp(linear(0, y0, 0, y1, [hx(SKY0), hx(SKY1)])))
    if sun: add_light(c, sun[0], sun[1], 260, '#FFE9B0', 180); circ(c, sun[0], sun[1], 54, '#FFF3D0', 0)
    for i in range(3): cloud(c, x0 + 60 + i * (x1 - x0) / 3 + rnd.uniform(-30, 30), y0 + 70 + rnd.uniform(0, 70), rnd.uniform(.7, 1.0))
    base = y1
    if scene == 'suburb':
        x = x0 - 30
        while x < x1:
            w = rnd.randint(150, 230); hgt = rnd.randint(90, 140); col_ = rnd.choice(['#5D77A8', '#7189B5', '#4E6798'])
            rect(c, x, base - hgt, x + w, base, col_, 4); poly(c, [(x - 16, base - hgt), (x + w / 2, base - hgt - 70), (x + w + 16, base - hgt)], '#3A4F7E', 4)
            for k in range(2): rect(c, x + 26 + k * (w - 90), base - hgt + 30, x + 64 + k * (w - 90), base - hgt + 70, '#DDE8F8', 3)
            x += w + rnd.randint(20, 60)
        for tx in (x0 + 120, x1 - 160):   # autumn trees (gold), no green
            line(c, tx, base, tx, base - 120, 10, '#5A3E2A')
            for a in range(7): circ(c, tx + math.cos(a * 0.9) * 50, base - 170 + math.sin(a * 1.3) * 40, 48, '#E9A93A' if a % 2 else GOLD_, 4)
    else:  # city
        x = x0 - 20
        while x < x1:
            w = rnd.randint(70, 140); hgt = rnd.randint(int((y1 - y0) * .3), int((y1 - y0) * .78)); col_ = rnd.choice(['#6F87B4', '#8299C2', '#5C75A6'])
            rect(c, x, base - hgt, x + w, base, col_, 4)
            for wy in range(int(base - hgt + 18), int(base - 10), 30):
                for wx in range(int(x + 12), int(x + w - 18), 24): c.drawRect(skia.Rect(wx, wy, wx + 12, wy + 16), fp('#DDE8F8', 200))
            x += w + rnd.randint(6, 24)
    c.restore()
def window(c, x0, y0, x1, y1, scene='suburb', panes=(2, 2), sun=None, seed=2, frame=WHITE):
    sky(c, x0, y0, x1, y1, scene, seed, sun)
    for i in range(1, panes[0]): x = x0 + (x1 - x0) * i / panes[0]; rect(c, x - 8, y0, x + 8, y1, frame, 4)
    for j in range(1, panes[1]): y = y0 + (y1 - y0) * j / panes[1]; rect(c, x0, y - 8, x1, y + 8, frame, 4)
    # glass shine
    for k in range(2): c.drawPath(path([(x0 + 40 + k * 70, y1), (x0 + 90 + k * 70, y1), (x0 + 260 + k * 70, y0), (x0 + 210 + k * 70, y0)]), fp(WHITE, 40))
    p = skia.Path(); p.addRect(skia.Rect(x0 - 22, y0 - 22, x1 + 22, y1 + 22)); p.addRect(skia.Rect(x0, y0, x1, y1)); p.setFillType(skia.PathFillType.kEvenOdd); shape(c, p, frame, 5)
    rect(c, x0 - 44, y1 + 14, x1 + 44, y1 + 40, frame, 5, r=4)
def sun_shaft(c, pts, a=34): c.drawPath(path(pts), fp('#FFD98A', a, blur=26, blend=skia.BlendMode.kPlus))
def daylight(c, holes, ambient='#CAD3EA'):
    night(c, holes, ambient)
def grain(c):
    r = np.random.default_rng(7); fine = r.normal(0, 1, (H, W))
    soft = np.asarray(_PI.fromarray((r.random((54, 96)) * 255).astype(np.uint8)).resize((W, H), _PI.BICUBIC).filter(_PF.GaussianBlur(18)), dtype=float) / 255 - .5
    g = np.clip(240 + fine * 7 + soft * 26, 0, 255).astype(np.uint8)
    img = skia.Image.fromarray(np.dstack([g, g, g, np.full_like(g, 255)]))
    gp = skia.Paint(); gp.setShader(img.makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp)); gp.setBlendMode(skia.BlendMode.kMultiply); c.drawPaint(gp)
def shadow(c, x, y, w=120, a=90): c.drawOval(skia.Rect(x - w, y - 18, x + w, y + 16), fp((20, 26, 50), a, blur=10))
def finish_bg(surf):
    finish(surf, bloom=0.22, sigma=22); c = surf.getCanvas(); vignette(c, 0.28, .5); grain(c); return c
def save(surf, name): surf.makeImageSnapshot().save(name, skia.kPNG); print('saved', name)

def bill(c, x, y, rot, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(c, -80, -36, 80, 36, '#F4F1E8', 4); rect(c, -70, -27, 70, 27, None, 2.5, v=NAVY); circ(c, 0, 0, 20, GOLD_, 2.5)
    text(c, '$', 0, 11, 30, NAVY, SLAB, 'center'); c.restore()
def coin(c, x, y, r=22): circ(c, x, y, r, GOLD_, 3.5); circ(c, x, y, r * .7, None, 2, v='#B07A0A'); text(c, '$', x, y + r * .4, r * 1.05, '#9A6A08', SLAB, 'center')
def mug(c, x, y, col_=NAVY, steam=True):
    rect(c, x - 30, y - 66, x + 30, y, col_, 4, r=8); oval(c, x + 18, y - 52, x + 52, y - 18, None, 7); oval(c, x + 18, y - 52, x + 52, y - 18, None, 0)
    c.drawArc(skia.Rect(x + 16, y - 54, x + 54, y - 16), -90, 180, False, ink(7, INK)); c.drawArc(skia.Rect(x + 16, y - 54, x + 54, y - 16), -90, 180, False, ink(3, col_))
    rect(c, x - 30, y - 66, x + 30, y - 58, None, 0)
    if steam:
        for k in (-12, 10):
            p = skia.Path(); p.moveTo(x + k, y - 80); p.cubicTo(x + k - 16, y - 100, x + k + 16, y - 116, x + k, y - 140); c.drawPath(p, ink(5, WHITE, 170))
def piggy(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for lx in (-40, -14, 18, 42): rect(c, lx - 10, 20, lx + 10, 52, '#E39A12', 4, r=4)
    oval(c, -80, -60, 80, 40, GOLD_, 5); c.drawOval(skia.Rect(-56, -46, -10, -22), fp(WHITE, 120, blur=6))
    oval(c, 66, -26, 98, 8, '#F2B640', 5); circ(c, 76, -10, 4, INK, 0); circ(c, 88, -10, 4, INK, 0)
    poly(c, [(20, -56), (40, -86), (50, -50)], '#E39A12', 4); circ(c, 44, -26, 6, INK, 0); rect(c, -24, -64, 18, -54, NAVY, 3, r=4); c.restore()
def books(c, x0, y, x1, seed=1):
    rnd = random.Random(seed); x = x0
    while x < x1 - 20:
        w = rnd.randint(18, 30); h = rnd.randint(70, 96); rect(c, x, y - h, x + w, y, rnd.choice([NAVY, NAVY3, GOLD_, '#E5E5E5', '#6B4A2E', '#5D77A8']), 3); x += w + 2
def plant_pampas(c, x, y):   # dried pampas grass in a vase: no green
    for a in range(-3, 4):
        ang = a * 0.16; tx, ty = x + math.sin(ang) * 230, y - math.cos(ang) * 230
        line(c, x, y - 40, tx, ty, 4, '#8A6A44')
        p = skia.Path(); p.addOval(skia.Rect(-20, -70, 20, 70)); m = skia.Matrix(); m.setRotate(math.degrees(ang)); m.postTranslate(tx, ty); p.transform(m); shape(c, p, '#EAD9B8', 4)
    poly(c, [(x - 44, y - 70), (x + 44, y - 70), (x + 34, y + 30), (x - 34, y + 30)], NAVY2, 5)
def wall_clock(c, x, y, r, h=9.2):
    circ(c, x, y, r + 8, NAVY, 5); circ(c, x, y, r, WHITE, 4)
    for i in range(12): a = i * math.pi / 6; line(c, x + math.sin(a) * r * .78, y - math.cos(a) * r * .78, x + math.sin(a) * r * .9, y - math.cos(a) * r * .9, 4)
    line(c, x, y, x + math.sin(h / 12 * 2 * math.pi) * r * .5, y - math.cos(h / 12 * 2 * math.pi) * r * .5, 7); line(c, x, y, x + math.sin(h % 1 * 2 * math.pi) * r * .75, y - math.cos(h % 1 * 2 * math.pi) * r * .75, 4)
    circ(c, x, y, 6, GOLD_, 2)
def calendar(c, x, y, month='MARCH', mark=(3, 2)):
    rect(c, x, y, x + 210, y + 250, '#FBF8F0', 5); rect(c, x, y, x + 210, y + 56, NAVY, 5); text(c, month, x + 105, y + 42, 36, WHITE, BAR, 'center')
    for i in range(20): rect(c, x + 16 + (i % 5) * 38, y + 72 + (i // 5) * 42, x + 48 + (i % 5) * 38, y + 106 + (i // 5) * 42, '#EEE8DA', 2)
    c.drawCircle(x + 32 + mark[0] * 38, y + 89 + mark[1] * 42, 24, ink(5, GOLD_))
def dseg_money(c, value, cx, y, size, color=GOLD_):
    groups = f'{value:,}'.split(','); fd = skia.Font(DSEG, size); fb = skia.Font(BAR, size * 1.15)
    parts = [('$', fb)] + sum([[(g, fd)] + ([(',', fb)] if i < len(groups) - 1 else []) for i, g in enumerate(groups)], [])
    tw = sum(f.measureText(t) for t, f in parts) + 6 * (len(parts) - 1); x = cx - tw / 2
    for t, f in parts: c.drawString(t, x, y, f, fp(color)); x += f.measureText(t) + 6
def bar_chart_screen(c, x0, y0, x1, y1, vals=(.3, .45, .4, .62, .8)):
    rect(c, x0, y0, x1, y1, NAVY, 5, r=8); bw = (x1 - x0 - 40) / len(vals)
    for i, v in enumerate(vals):
        bx = x0 + 20 + i * bw; rect(c, bx + 6, y1 - 16 - (y1 - y0 - 40) * v, bx + bw - 6, y1 - 16, GOLD_, 3)
    c.drawRect(skia.Rect(x0 + 6, y0 + 6, x1 - 6, y0 + 18), fp(WHITE, 30))

# ============ 1. LIVING ROOM (budgeting at home)
def living_room():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, H), fp(CREAM))
    for x in range(0, W, 110): c.drawRect(skia.Rect(x, 0, x + 55, 760), fp('#EFE4D2'))
    rect(c, -10, 740, W + 10, 776, WHITE, 5)
    rect(c, -10, 776, W + 10, H + 10, OAK, 5)
    for y in range(820, H, 64): line(c, -10, y, W + 10, y, 3, OAK_D)
    for i, y in enumerate(range(776, H, 64)):
        for x in range(-200 + (i % 2) * 180, W, 360): line(c, x, y, x, y + 64, 3, OAK_D)
    window(c, 1140, 130, 1720, 620, 'suburb', (2, 2), seed=4)
    for cx, d in ((1080, -1), (1780, 1)):
        cp = skia.Path(); cp.moveTo(cx - 60, 80); cp.lineTo(cx + 60, 80); cp.cubicTo(cx + 60, 380, cx + 40, 560, cx + 50 * d, 730); cp.lineTo(cx - 50 * d, 730); cp.cubicTo(cx - 40, 560, cx - 60, 380, cx - 60, 80); cp.close(); shape(c, cp, NAVY2, 5)
        for k in (-25, 5, 30): line(c, cx + k, 110, cx + k * 1.1, 700, 3, NAVY)
    rect(c, 980, 64, 1880, 86, '#8A6A44', 5, r=8)
    # wall: framed art, shelf with books + piggy bank
    rect(c, 330, 150, 610, 360, '#8A6A44', 6); rect(c, 352, 172, 588, 338, '#FBF8F0', 4)
    poly(c, [(370, 320), (450, 230), (520, 300), (560, 260), (575, 320)], NAVY3, 4); circ(c, 540, 210, 26, GOLD_, 4)
    rect(c, 660, 190, 820, 340, '#8A6A44', 6); rect(c, 680, 210, 800, 320, '#FBF8F0', 4); rect(c, 700, 240, 780, 300, GOLD_, 3)
    rect(c, 60, 300, 280, 316, '#8A6A44', 4); books(c, 70, 300, 200, 3); piggy(c, 240, 278, .42)
    rect(c, 60, 470, 280, 486, '#8A6A44', 4); books(c, 70, 470, 270, 6)
    # floor lamp
    line(c, 940, 760, 940, 360, 8); oval(c, 900, 750, 980, 774, '#2E2E38', 5); poly(c, [(880, 360), (1000, 360), (970, 270), (910, 270)], '#FBF8F0', 5)
    # sofa
    rect(c, 140, 520, 900, 640, NAVY2, 6, r=34)
    rect(c, 110, 600, 930, 760, NAVY2, 6, r=30); rect(c, 180, 620, 520, 700, '#24396A', 5, r=18); rect(c, 520, 620, 860, 700, '#24396A', 5, r=18)
    rect(c, 90, 560, 180, 760, '#1A2A4E', 6, r=30); rect(c, 860, 560, 950, 760, '#1A2A4E', 6, r=30)
    for x0, r_ in ((220, -8), (720, 7)):
        c.save(); c.translate(x0 + 60, 560); c.rotate(r_); rect(c, -64, -50, 64, 50, GOLD_, 5, r=18); c.restore()
    for lx in (150, 890): rect(c, lx - 10, 760, lx + 10, 790, '#5A3E2A', 4)
    # rug + coffee table with laptop chart, mug, papers
    oval(c, 200, 840, 1500, 1060, '#F7F1E6', 6); oval(c, 250, 860, 1450, 1040, None, 5, v=NAVY3)
    rect(c, 980, 820, 1440, 850, '#8A6A44', 6, r=8); rect(c, 1000, 850, 1024, 950, '#6B4A33', 5); rect(c, 1396, 850, 1420, 950, '#6B4A33', 5)
    poly(c, [(1060, 822), (1250, 822), (1270, 806), (1040, 806)], '#BFC5D2', 4); c.save(); c.translate(1150, 806); c.skew(-.12, 0)
    bar_chart_screen(c, -96, -150, 96, -6); c.restore()
    mug(c, 1330, 820, GOLD_)
    c.save(); c.translate(1300, 812); c.rotate(-8); rect(c, -60, -10, 60, 6, '#FBF8F0', 3); c.restore()
    plant_pampas(c, 1830, 740)
    # daylight: shade everywhere but the window and the sun patch
    win = skia.Path(); win.addRect(skia.Rect(1120, 110, 1740, 640))
    patch = path([(1160, 780), (1700, 780), (1460, 1080), (760, 1080)])
    daylight(c, [('path', win, .95, 20), ('path', patch, .8, 60), ('oval', 960, 560, 900, 560, .55), ('oval', 940, 330, 160, 160, .5)])
    sun_shaft(c, [(1140, 140), (1720, 140), (1500, 1080), (720, 1080)], 30); add_light(c, 940, 320, 140, '#FFE6B0', 70)
    c = finish_bg(surf)
    shadow(c, 600, 975, 110); shadow(c, 860, 985, 110)
    draw_char(c, 600, 975, .98, ANALYST, face=.25, eyes='dot', mouth='open', brow=.3, arms=('down', 'present'), light=1, rim=RIM)
    draw_char(c, 860, 985, .98, WORKER, face=-.2, eyes='wide', mouth='smile', brow=.4, arms=('chin', 'down'), light=1, rim=RIM)
    save(surf, 'day1_living.png')

# ============ 2. KITCHEN, MORNING (bills on the table)
def kitchen():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, H), fp('#E9EEF6'))
    for y in range(380, 620, 40):   # subway-tile backsplash
        for x in range(-40 + (y // 40 % 2) * 40, W, 80): rect(c, x, y, x + 80, y + 40, '#F6F8FC', 2, v='#C9D2E3')
    # upper cabinets (white, navy handles) + window between
    for x0 in (60, 340, 1380, 1640):
        rect(c, x0, 60, x0 + 240, 330, WHITE, 5, r=6); rect(c, x0 + 20, 80, x0 + 220, 310, None, 3, v='#C9D2E3'); rect(c, x0 + 110, 270, x0 + 130, 300, NAVY, 3, r=4)
    window(c, 720, 90, 1220, 470, 'suburb', (2, 1), sun=(840, 230), seed=9)
    # counter + lower navy cabinets + sink + coffee maker + fridge
    rect(c, -10, 620, 1600, 660, '#F4F4F2', 5); rect(c, -10, 660, 1600, 900, NAVY2, 5)
    for x0 in range(20, 1580, 260): rect(c, x0, 680, x0 + 240, 880, None, 4, v='#2B4A7A'); rect(c, x0 + 100, 700, x0 + 140, 714, GOLD_, 3, r=4)
    oval(c, 840, 600, 1100, 640, '#C9CFDB', 5); line(c, 970, 600, 970, 540, 8); line(c, 970, 540, 1010, 540, 8)
    rect(c, 300, 480, 420, 620, '#2E2E38', 5, r=10); rect(c, 330, 560, 390, 620, '#BFC5D2', 4); rect(c, 320, 500, 400, 530, '#3E3E4A', 3, r=4)
    # fridge with magnets + budget list
    rect(c, 1620, 140, 1900, 900, '#D6DBE5', 6, r=18); line(c, 1620, 420, 1900, 420, 5); rect(c, 1640, 300, 1660, 400, '#9AA3B5', 3, r=4); rect(c, 1640, 450, 1660, 560, '#9AA3B5', 3, r=4)
    c.save(); c.translate(1770, 560); c.rotate(4); rect(c, -90, -120, 90, 120, '#FBF8F0', 4); text(c, 'BUDGET', 0, -78, 36, NAVY, BAR, 'center')
    for i in range(5): line(c, -66, -40 + i * 30, 30 + (i % 3) * 14, -40 + i * 30, 4, '#9AA3B5'); c.drawCircle(-74, -44 + i * 30, 5, fp(NAVY))
    c.restore(); circ(c, 1770, 440, 14, GOLD_, 4); circ(c, 1690, 220, 16, NAVY3, 4); rect(c, 1790, 200, 1840, 250, '#FBF8F0', 3)
    wall_clock(c, 560, 200, 70, 8.1); calendar(c, 60 if False else 1260, 420, 'APRIL', (1, 2)) if False else None
    # floor
    rect(c, -10, 900, W + 10, H + 10, '#D9CBB4', 5)
    for x in range(0, W, 120): line(c, x, 900, x - 60, H, 3, '#C2B297')
    # foreground table with bills, calculator, envelope, mug
    rect(c, 980, 880, 1880, 930, '#B78656', 6, r=10); rect(c, 1010, 930, 1040, 1090, '#8A6A44', 5); rect(c, 1820, 930, 1850, 1090, '#8A6A44', 5)
    for i, (x, y, r_) in enumerate(((1110, 862, -9), (1300, 850, 5), (1240, 905, -3))):
        c.save(); c.translate(x, y); c.rotate(r_); rect(c, -105, -30, 105, 30, '#FBF8F0', 4); text(c, ['RENT', 'POWER', 'CARD'][i], -90, 9, 26, NAVY, TYPE); text(c, ['$1,450', '$118', '$312'][i], 92, 9, 26, NAVY, TYPE, 'right'); c.restore()
    c.save(); c.translate(1580, 860); c.rotate(-5); rect(c, -70, -40, 70, 30, '#2E2E38', 5, r=10); rect(c, -58, -32, 58, -6, '#C7D3B0' if False else '#DDE8F8', 3)
    text(c, '1716.00', 52, -11, 20, NAVY, DSEG, 'right'); [circ(c, -44 + k * 30, 12, 7, '#5A5A68', 2) for k in range(4)]; c.restore()
    mug(c, 1740, 880, NAVY)
    # daylight: morning sun through the window
    win = skia.Path(); win.addRect(skia.Rect(700, 70, 1240, 490))
    daylight(c, [('path', win, .95, 20), ('path', path([(760, 600), (1200, 600), (1650, 1080), (900, 1080)]), .7, 60), ('oval', 960, 650, 900, 500, .55)], ambient='#D6D8E8')
    sun_shaft(c, [(740, 120), (1200, 120), (1700, 1080), (820, 1080)], 32); add_light(c, 840, 230, 300, '#FFE6B0', 60)
    c = finish_bg(surf)
    shadow(c, 600, 1000, 110)
    draw_char(c, 600, 1000, 1.0, WORKER, face=.3, eyes='half', mouth='flat', brow=.6, brow_tilt=-.4, arms=('chin', 'hip'), light=1, rim=RIM)
    save(surf, 'day2_kitchen.png')

# ============ 3. BANK LOBBY, DAY
def bank():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, H), fp('#F1EADC'))
    for y in range(0, 700, 90): line(c, 0, y, W, y, 2, '#E2D7C2')
    # tall arched windows
    for x0 in (90, 1560):
        p = skia.Path(); p.moveTo(x0, 600); p.lineTo(x0, 220); p.arcTo(skia.Rect(x0, 80, x0 + 270, 360), 180, 180, False); p.lineTo(x0 + 270, 600); p.close()
        c.save(); c.clipPath(p, doAntiAlias=True); sky(c, x0, 80, x0 + 270, 600, 'city', seed=x0); c.restore()
        line(c, x0 + 135, 90, x0 + 135, 600, 10, WHITE); line(c, x0, 340, x0 + 270, 340, 10, WHITE); c.drawPath(p, ink(16, WHITE)); c.drawPath(p, ink(5))
    # columns
    for x in (420, 1440):
        rect(c, x - 60, 120, x + 60, 720, '#F8F3EA', 5); [line(c, x + k, 140, x + k, 700, 3, '#E2D7C2') for k in (-30, 0, 30)]
        rect(c, x - 80, 100, x + 80, 130, '#F8F3EA', 5); rect(c, x - 80, 700, x + 80, 730, '#F8F3EA', 5)
    rect(c, -10, 60, W + 10, 100, '#F8F3EA', 5)
    # emblem + sign
    circ(c, 930, 190, 70, GOLD_, 6); poly(c, [(880, 175), (930, 140), (980, 175)], NAVY, 4); [rect(c, x - 6, 180, x + 6, 225, NAVY, 3) for x in (895, 918, 942, 965)]; rect(c, 880, 228, 980, 238, NAVY, 3)
    text(c, 'SAVINGS  ·  CHECKING  ·  LOANS', 930, 310, 44, NAVY, BAR, 'center')
    wall_clock(c, 1180, 200, 56, 11.4)
    # teller counter with brass grille
    rect(c, 560, 470, 1320, 500, '#6B4A33', 5); rect(c, 540, 500, 1340, 720, '#8A6A44', 6)
    for x0 in range(570, 1310, 190): rect(c, x0, 520, x0 + 170, 700, None, 4, v='#6B4A33')
    for x in range(580, 1310, 26): line(c, x, 360, x, 470, 4, '#C9902A')
    line(c, 560, 360, 1320, 360, 7, '#C9902A'); rect(c, 840, 420, 1040, 470, '#F1EADC', 4); text(c, 'TELLER', 940, 456, 34, NAVY, BAR, 'center')
    # marble floor: big cream slabs in perspective, navy inlay border, gold medallion (our own, no checkerboard)
    rect(c, -10, 720, W + 10, H + 10, '#F4EFE6', 5)
    def X(i_, y): return 960 + (i_ * 260) * (0.55 + 0.45 * (y - 720) / (H - 720))
    for i in range(-8, 9): line(c, X(i, 720), 720, X(i, H), H, 3, '#D9CCB4')
    for j in range(1, 5): y = 720 + (H - 720) * (j / 5) ** 1.3; line(c, -10, y, W + 10, y, 3, '#D9CCB4')
    for k, yy in enumerate((760, 1060)): c.drawRect(skia.Rect(-10, yy - 10, W + 10, yy + 10), fp(NAVY2))
    c.save(); c.translate(960, 905); c.scale(1, 0.32)
    circ(c, 0, 0, 300, NAVY2, 6); circ(c, 0, 0, 250, '#F4EFE6', 5); circ(c, 0, 0, 120, GOLD_, 5)
    for k in range(8):
        a_ = k * math.pi / 4; rr = 240 if k % 2 == 0 else 170
        poly(c, [(math.cos(a_) * rr, math.sin(a_) * rr), (math.cos(a_ + .2) * 70, math.sin(a_ + .2) * 70), (math.cos(a_ - .2) * 70, math.sin(a_ - .2) * 70)], GOLD_ if k % 2 == 0 else NAVY3, 4)
    circ(c, 0, 0, 46, NAVY2, 4); c.restore()
    # rope stands
    for x in (300, 560, 1360, 1620):
        rect(c, x - 30, 1000, x + 30, 1016, '#C9902A', 4, r=6); line(c, x, 1000, x, 880, 9, '#C9902A'); circ(c, x, 872, 14, GOLD_, 4)
    for xa, xb in ((300, 560), (1360, 1620)):
        p = skia.Path(); p.moveTo(xa, 884); p.quadTo((xa + xb) / 2, 950, xb, 884); c.drawPath(p, ink(18, INK)); c.drawPath(p, ink(10, '#7A1328' if False else NAVY3))
    win1 = skia.Path(); win1.addRect(skia.Rect(80, 70, 370, 610)); win2 = skia.Path(); win2.addRect(skia.Rect(1550, 70, 1840, 610))
    daylight(c, [('path', win1, .95, 20), ('path', win2, .95, 20), ('oval', 960, 600, 1000, 560, .6),
                 ('path', path([(100, 620), (380, 620), (820, 1080), (420, 1080)]), .7, 50), ('path', path([(1540, 620), (1820, 620), (1500, 1080), (1100, 1080)]), .7, 50)], ambient='#D0D6EA')
    sun_shaft(c, [(90, 120), (360, 120), (820, 1080), (420, 1080)], 30); sun_shaft(c, [(1560, 120), (1830, 120), (1500, 1080), (1100, 1080)], 30)
    c = finish_bg(surf)
    shadow(c, 760, 1020, 115); shadow(c, 1120, 1025, 115)
    draw_char(c, 760, 1020, 1.0, BANKER, face=.25, eyes='closed', mouth='smile', brow=.2, arms=('present', 'hip'), light=-1, rim=RIM)
    draw_char(c, 1120, 1025, 1.0, ANALYST, face=-.25, eyes='dot', mouth='o', brow=.6, arms=('down', 'chin'), light=1, rim=RIM)
    save(surf, 'day3_bank.png')

# ============ 4. MAIN STREET, DAY (shopping / spending lessons)
def street():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    sky(c, 0, 0, W, 700, 'city', seed=11, sun=(1650, 120))
    # storefront row
    shops = [(0, 470, '#F1EADC', 'COFFEE'), (470, 960, NAVY2, 'SALE'), (960, 1420, '#C8A97E', 'PHARMACY'), (1420, 1940, '#E5E5E5', 'GROCERY')]
    for x0, x1, colr, name in shops:
        rect(c, x0, 220, x1, 760, colr, 6); rect(c, x0, 220, x1, 260, '#3A4F7E' if colr != NAVY2 else '#0F1A33', 5)
        for k in range(3): rect(c, x0 + 40 + k * (x1 - x0 - 80) / 3, 370, x0 + 20 + (k + 1) * (x1 - x0 - 80) / 3, 450, '#BFD0EC', 4)
        sign_col = NAVY if colr != NAVY2 else GOLD_
        rect(c, x0 + 50, 280, x1 - 50, 345, NAVY if colr != NAVY2 else '#0F1A33', 5, r=6); text(c, name, (x0 + x1) / 2, 329, 50, GOLD_ if name != 'SALE' else WHITE, BAR, 'center')
        # awning stripes (navy / white or gold / white)
        stripe = GOLD_ if name in ('COFFEE', 'GROCERY') else NAVY3
        for k in range(int((x1 - x0 - 60) / 46)):
            xa = x0 + 30 + k * 46; poly(c, [(xa, 470), (xa + 46, 470), (xa + 54, 540), (xa - 8, 540)], stripe if k % 2 else WHITE, 4)
        rect(c, x0 + 60, 560, x1 - 220, 760, '#BFD0EC', 5); rect(c, x1 - 190, 580, x1 - 70, 760, '#6B4A33', 5); circ(c, x1 - 90, 680, 7, GOLD_, 2)
        c.drawPath(path([(x0 + 90, 760), (x0 + 150, 760), (x0 + 250, 560), (x0 + 190, 560)]), fp(WHITE, 60))
    text(c, '50% OFF', 640, 680, 64, GOLD_, SLAB, 'center', stroke=10)
    for i in range(3): mug(c, 140 + i * 90, 740, [NAVY, GOLD_, WHITE][i], steam=False)
    # sidewalk, curb, road, crosswalk
    rect(c, -10, 760, W + 10, 920, '#D9DCE3', 5)
    for x in range(0, W, 160): line(c, x, 760, x - 40, 920, 3, '#C2C6D0')
    rect(c, -10, 920, W + 10, 944, '#BFC4CE', 5); rect(c, -10, 944, W + 10, H + 10, '#4A4F5C', 5)
    for x in range(1240, 1760, 90): rect(c, x, 960, x + 54, H + 10, WHITE, 0)
    # street lamp, hydrant (navy/gold), planter tree (gold leaves)
    line(c, 1440, 920, 1440, 200, 12, NAVY); line(c, 1440, 200, 1520, 200, 10, NAVY); poly(c, [(1500, 200), (1550, 200), (1540, 230), (1510, 230)], GOLD_, 4)
    rect(c, 1540, 860, 1580, 920, NAVY3, 4, r=6); rect(c, 1530, 870, 1590, 884, GOLD_, 3, r=4)
    rect(c, 300, 860, 420, 920, '#8A6A44', 5); line(c, 360, 860, 360, 640, 12, '#5A3E2A')
    for a in range(9): circ(c, 360 + math.cos(a * .8) * 70, 590 + math.sin(a * 1.4) * 50, 56, '#E9A93A' if a % 2 else GOLD_, 4)
    # parked car (navy)
    c.save(); c.translate(260, 990)
    rect(c, -200, -70, 220, 30, NAVY2, 6, r=30); poly(c, [(-120, -70), (-70, -140), (110, -140), (160, -70)], NAVY2, 6); poly(c, [(-100, -76), (-62, -128), (20, -128), (20, -76)], '#BFD0EC', 4); poly(c, [(36, -76), (36, -128), (100, -128), (140, -76)], '#BFD0EC', 4)
    for wx in (-110, 130): circ(c, wx, 30, 42, '#23201E', 6); circ(c, wx, 30, 18, '#BFC5D2', 4)
    rect(c, 196, -50, 222, -30, GOLD_, 3, r=4); c.restore()
    daylight(c, [('oval', 960, 300, 1500, 520, .9), ('oval', 960, 840, 1300, 260, .7), ('oval', 1650, 120, 500, 400, .9)], ambient='#D3DAEE')
    for k in range(3): sun_shaft(c, [(1600 - k * 40, 0), (1700 - k * 40, 0), (1000 - k * 300, 1080), (800 - k * 300, 1080)], 16)
    c = finish_bg(surf)
    for x, s in ((880, .95), (1290, .95)): c.drawPath(path([(x - 60, 910), (x + 60, 910), (x - 60, 960), (x - 220, 960)]), fp((20, 26, 50), 70, blur=12))
    draw_char(c, 880, 905, .95, INVESTOR, face=.3, eyes='dot', mouth='smile', brow=.3, arms=('hold', 'gesture'), light=1, rim=RIM)
    draw_char(c, 1290, 905, .95, WORKER, face=-.3, eyes='wide', mouth='o', brow=.8, arms=('down', 'chin'), hat=True, light=1, rim=RIM)
    save(surf, 'day4_street.png')

# ============ 5. LESSON ROOM (whiteboard: compound growth)
def lesson():
    surf = skia.Surface(W, H); c = surf.getCanvas()
    c.drawRect(skia.Rect(0, 0, W, H), fp('#DFE6F1'))
    rect(c, -10, 720, W + 10, 760, WHITE, 5)
    rect(c, -10, 760, W + 10, H + 10, '#BC8E5E', 5)
    for y in range(800, H, 60): line(c, -10, y, W + 10, y, 3, '#A27748')
    window(c, 80, 140, 440, 600, 'city', (2, 2), seed=5)
    # whiteboard with gold growth curve
    rect(c, 600, 110, 1500, 640, '#F8FAFD', 8, r=10); rect(c, 580, 640, 1520, 668, '#BFC5D2', 5, r=6)
    line(c, 680, 580, 1440, 580, 6, NAVY); line(c, 680, 580, 680, 170, 6, NAVY)
    for i, yr in enumerate(('0', '10', '20', '30')): x = 680 + i * 240; line(c, x, 580, x, 596, 5, NAVY); text(c, yr, x, 628, 32, NAVY, BAR, 'center')
    text(c, 'YEARS', 1440, 562, 30, NAVY, BAR, 'right')
    lin = skia.Path(); lin.moveTo(680, 560); lin.lineTo(1400, 440); c.drawPath(lin, ink(6, '#9AA3B5'))
    cv = skia.Path(); cv.moveTo(680, 560); [cv.lineTo(680 + t * 7.2, 560 - 360 * ((1.08 ** (t * .3) - 1) / (1.08 ** 30 - 1))) for t in range(1, 101)]
    c.drawPath(cv, ink(16, INK)); c.drawPath(cv, ink(9, GOLD_))
    text(c, '$100/mo', 760, 230, 44, NAVY, BAR); text(c, 'at 8%', 760, 278, 36, NAVY3, BARS)
    rect(c, 1150, 160, 1460, 250, NAVY, 5, r=8); dseg_money(c, 149036, 1305, 228, 50)
    for x, y, r_ in ((1300, 470, -6), (1400, 520, 5)): c.save(); c.translate(x, y); c.rotate(r_); rect(c, -54, -44, 54, 44, '#FFE6A6', 4); c.restore()
    # bookshelf right, desk with globe + lamp
    rect(c, 1600, 160, 1860, 720, '#8A6A44', 6)
    for sh in range(4): y = 280 + sh * 120; line(c, 1600, y, 1860, y, 6); books(c, 1614, y - 4, 1846, sh + 2)
    # desk in light wood so the print look keeps the drawers readable (owner QC)
    rect(c, 1080, 800, 1600, 830, '#C99A66', 6, r=6); rect(c, 1100, 830, 1300, 1000, '#B9895A', 6); rect(c, 1480, 830, 1580, 1000, '#B9895A', 6)
    for yy in (845, 897, 949): rect(c, 1116, yy, 1284, yy + 40, '#D6AE7E', 4, r=4); circ(c, 1200, yy + 20, 7, GOLD_, 3)
    circ(c, 1200, 730, 50, NAVY3, 5); c.drawArc(skia.Rect(1150, 680, 1250, 780), 200, 140, False, ink(4, GOLD_)); line(c, 1200, 780, 1200, 800, 6); rect(c, 1170, 790, 1230, 802, '#3A3328', 4)
    books(c, 1290, 800, 1400, 9); mug(c, 1470, 800, GOLD_)
    line(c, 1540, 800, 1520, 690, 6); poly(c, [(1490, 690), (1560, 690), (1580, 640), (1500, 640)], NAVY, 4)
    wall_clock(c, 520, 120 if False else 700 - 580, 46, 2.3)
    win = skia.Path(); win.addRect(skia.Rect(60, 120, 460, 620))
    daylight(c, [('path', win, .95, 20), ('oval', 1050, 380, 620, 420, .8), ('path', path([(100, 760), (440, 760), (1100, 1080), (500, 1080)]), .7, 50), ('oval', 960, 900, 900, 260, .45)])
    sun_shaft(c, [(80, 150), (440, 150), (1100, 1080), (500, 1080)], 30)
    c = finish_bg(surf)
    shadow(c, 520, 990, 110); shadow(c, 860, 1000, 110)
    draw_char(c, 520, 990, 1.0, ANALYST, face=.3, eyes='dot', mouth='open', brow=.4, arms=('down', 'gesture'), light=-1, rim=RIM)
    draw_char(c, 860, 1000, 1.0, CEO, face=-.25, eyes='wide', mouth='o', brow=.7, arms=('chin', 'down'), light=-1, rim=RIM)
    save(surf, 'day5_lesson.png')

if __name__ == '__main__':
    import sys
    todo = sys.argv[1:] or ['living_room', 'kitchen', 'bank', 'street', 'lesson']
    for n in todo: globals()[n]()
