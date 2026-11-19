"""Thumbnail B - "$20 MILLION GONE" - drawn with the channel engine (same Ponzi as the video)."""
import sys, os, math, random, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / '.claude' / 'skills' / 'documentary-animator'))
import skia
from engine.core import W, H, NAVY, GOLD, ORANGE, WHITE, PAPER, F_TITLE, F_LABEL, F_TYPE
from engine import kit, widgets as Wd, anim as A
from engine.kit import fp, ink, draw_char, hand_pos, poly, rect, circ, vignette
from engine.cast import CAST
from engine.sets import get_set

def thumb(path):
    """B - "$20 MILLION GONE" v3: channel night-print street (sharp), the whole story around a huge panicked Ponzi:
    the line of investors at SECURITIES EXCHANGE CO., police car + spotlight, Boston Post headline, reply coupons,
    cash flying, coins falling, handcuffs, orange crash arrow."""
    s = skia.Surface(W, H); c = s.getCanvas()
    st = get_set('night/street1920'); p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(1.5, 1.5))
    c.save(); c.translate(W / 2, H / 2); c.scale(1.35, 1.35); c.translate(-880, -560); c.drawImage(st.base, 0, 0, skia.SamplingOptions(), p)
    from engine.actor import Actor                                                     # the line of investors (sharp, in world space)
    q = ['worker', 'saver', 'retiree', 'grad', 'reporter', 'agent', 'banker', 'analyst', 'saver', 'worker']
    for k in range(10):
        a = Actor(q[k], 1000 + k * 62, 864 + (k % 2) * 4, .36, face=-.7, light=-1, rim='#9FB8F0', hat=(q[k] == 'worker'))
        a.expression(0, eyes='wide', mouth='o', brow=.7); a.pose(0, ('down', 'hold') if k % 2 else ('pocket', 'chin')); a.draw(c, .5)
    c.restore()
    c.drawRect(skia.Rect(0, 0, W, H), fp((4, 8, 22), 70)); vignette(c, .8, .45)
    # police car (clear) bottom-right + siren + spotlight beam onto Ponzi
    A.police_car(c, 1560, 1000, 2.0, .75)
    for x, y, col in ((1650, 760, '#5F86F0'), (1580, 760, ORANGE)): c.drawCircle(x, y, 200, fp(col, 80, blur=60, blend=skia.BlendMode.kPlus))
    beam = skia.Path(); beam.moveTo(1555, 780); beam.lineTo(300, 130); beam.lineTo(380, 860); beam.close()
    c.drawPath(beam, fp('#FFF2C8', 105, blur=22, blend=skia.BlendMode.kPlus))
    c.drawCircle(620, 470, 450, fp(ORANGE, 95, blur=110, blend=skia.BlendMode.kPlus))
    # Boston Post headline flying in (upper right)
    c.save(); c.translate(1500, 395); c.rotate(9); c.drawRect(skia.Rect(-250, -150, 260, 165), fp((0, 0, 0), 120, blur=12))
    rect(c, -250, -160, 250, 160, PAPER, 6); Wd.text(c, 'THE BOSTON POST', 0, -100, 46, NAVY, F_TITLE, 'center')
    c.drawRect(skia.Rect(-220, -82, 220, -76), fp(NAVY)); Wd.text(c, 'PONZI', 0, -10, 70, NAVY, F_LABEL, 'center'); Wd.text(c, 'HOPELESSLY INSOLVENT', 0, 50, 44, NAVY, F_LABEL, 'center')
    Wd.text(c, 'AUG. 2, 1920', 0, 112, 30, NAVY, F_TYPE, 'center'); c.restore()
    # cash + reply coupons flying away from him
    r = random.Random(21)
    for k in range(8):
        x0, y0, rot = r.uniform(960, 1280), r.uniform(560, 820), r.uniform(-50, 50)
        c.save(); c.translate(x0, y0); c.rotate(rot); c.scale(1.2, 1.2); Wd.bill(c, 0, 0, 0, 1.0); c.restore()
    for k, (x0, y0, rot) in enumerate(((1110, 560, -18), (1260, 690, 14))): coupon_card(c, x0, y0, rot, .8)
    # huge panicked Ponzi
    X, FEET, S = 600, 1690, 2.45
    draw_char(c, X, FEET, S, dict(CAST['ponzi']), face=.12, eyes='wide', mouth='grit', brow=1.1, brow_tilt=-.9, arms=('chin', 'chin'), tilt=-9,
              sweat=.3, light=1, rim='#FFB070', hat=True)
    hcx, hcy = X, FEET + S * kit.HEAD_CY
    for dx, dy, sc_ in ((-235, -60, 1.3), (240, 10, 1.0)):
        d = skia.Path(); x_, y_ = hcx + dx, hcy + dy; d.moveTo(x_, y_ - 34 * sc_); d.cubicTo(x_ + 22 * sc_, y_ - 6 * sc_, x_ + 20 * sc_, y_ + 18 * sc_, x_, y_ + 18 * sc_)
        d.cubicTo(x_ - 20 * sc_, y_ + 18 * sc_, x_ - 22 * sc_, y_ - 6 * sc_, x_, y_ - 34 * sc_); d.close(); kit.shape(c, d, '#8FC8EE', 6)
    for k in range(12):
        a = -math.pi * ((.02 + .2 * (k % 6) / 5) if k < 6 else (.78 + .2 * (k % 6) / 5)); r0, r1 = 290, 360 + (k % 2) * 40
        p0 = (hcx + math.cos(a) * r0, hcy + math.sin(a) * r0 * .95); p1 = (hcx + math.cos(a) * r1, hcy + math.sin(a) * r1 * .95)
        c.drawLine(*p0, *p1, ink(14, (10, 17, 36))); c.drawLine(*p0, *p1, ink(7, WHITE))
    lx, ly = hand_pos(X, FEET, S, ('chin', 'chin'), -1); rx, ry = hand_pos(X, FEET, S, ('chin', 'chin'), 1); cy = (ly + ry) / 2 + 45
    for hx in (lx, rx):
        c.drawCircle(hx, cy, 50, ink(30, (10, 17, 36))); c.drawCircle(hx, cy, 50, ink(18, '#DCE1EA')); c.drawArc(skia.Rect(hx - 50, cy - 50, hx + 50, cy + 50), 200, 70, False, ink(7, WHITE))
    for k in range(4):
        x_ = lx + 50 + (rx - lx - 100) * (k + .5) / 4; c.drawOval(skia.Rect(x_ - 18, cy - 4, x_ + 18, cy + 18), ink(14, (10, 17, 36))); c.drawOval(skia.Rect(x_ - 18, cy - 4, x_ + 18, cy + 18), ink(7, '#9AA3B5'))
    for k in range(26):
        a = r.uniform(0, 2 * math.pi); d_ = r.uniform(60, 220); x0, y0 = (lx + rx) / 2 + math.cos(a) * d_, cy + math.sin(a) * d_ * .6
        c.drawLine(x0, y0, x0 + math.cos(a) * 26, y0 + math.sin(a) * 16, ink(6, '#FFC27A')); c.drawCircle(x0, y0, 20, fp(ORANGE, 70, blur=10))
    for k in range(12):                                                               # coins falling at the sides
        x0 = r.choice([r.uniform(40, 220), r.uniform(1000, 1300)]); y0 = r.uniform(820, 1060)
        c.save(); c.translate(x0, y0); c.scale(abs(math.cos(k * 1.3)) * .7 + .3, 1); Wd.coin(c, 0, 0, r.uniform(34, 50)); c.restore()
    # orange crash arrow down the middle-right
    pts = [(1020, 250), (1130, 380), (1080, 420), (1250, 600)]
    pa = skia.Path(); pa.moveTo(*pts[0]); [pa.lineTo(*q_) for q_ in pts[1:]]
    c.drawPath(pa, ink(60, (10, 17, 36))); c.drawPath(pa, ink(40, ORANGE)); poly(c, [(1190, 660), (1320, 560), (1325, 680)], ORANGE, 9)
    _headline(c, [('$20 MILLION ', ORANGE), ('GONE', WHITE)], size=190, y0=205)
    _save(s, path)

def _bg(c, zoom=1.6, focus=(1100, 560), dark=120, blur=10):
    st = get_set('night/street1920'); p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
    c.save(); c.translate(W / 2, H / 2); c.scale(zoom, zoom); c.translate(-focus[0], -focus[1]); c.drawImage(st.base, 0, 0, skia.SamplingOptions(), p); c.restore()
    c.drawRect(skia.Rect(0, 0, W, H), fp((6, 10, 28), dark)); vignette(c, .75, .45)

def _headline(c, parts, size=168, y0=190):
    f = skia.Font(F_TITLE, size); wt = sum(f.measureText(t) for t, _ in parts)
    if wt > 1780: size = size * 1780 / wt; f = skia.Font(F_TITLE, size); wt = sum(f.measureText(t) for t, _ in parts)   # auto-fit
    x = (W - wt) / 2
    for txt, col in parts:
        c.drawString(txt, x + 12, y0 + 14, f, fp((0, 0, 0), 170, blur=8)); c.drawString(txt, x, y0, f, ink(30, (10, 17, 36))); c.drawString(txt, x, y0, f, fp(col)); x += f.measureText(txt)

def _save(s, path):
    s.makeImageSnapshot().save(str(path).replace('.jpg', '_1920.png'), skia.kPNG)
    from PIL import Image
    Image.open(str(path).replace('.jpg', '_1920.png')).convert('RGB').resize((1280, 720), Image.LANCZOS).save(path, quality=92)

def coupon_card(c, x, y, rot, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect(-120, -80, 140, 100), fp((0, 0, 0), 90, blur=10)); rect(c, -130, -90, 130, 90, '#FFE9B0', 6)
    rect(c, -114, -74, 114, 74, None, 4, v=(150, 100, 20)); Wd.text(c, 'REPLY', 0, -18, 46, NAVY, F_TITLE, 'center')
    Wd.text(c, 'COUPON', 0, 34, 40, NAVY, F_TITLE, 'center'); circ(c, 0, 62, 10, GOLD, 3); c.restore()

def thumb_a(path):
    """A - "50% IN 45 DAYS": smirking Ponzi holding a fan of glowing coupons, the line queueing behind."""
    s = skia.Surface(W, H); c = s.getCanvas(); _bg(c, 1.7, (760, 640))
    c.drawCircle(1250, 640, 420, fp(GOLD, 70, blur=90, blend=skia.BlendMode.kPlus))
    X, FEET, S = 640, 1440, 2.05
    draw_char(c, X, FEET, S, dict(CAST['ponzi']), face=.25, eyes='half', mouth='smirk', brow=-.35, brow_tilt=.4, arms=('down', 'present'),
              light=1, rim='#FFD27A', hat=True, sparkle=1.0)
    hx, hy = hand_pos(X, FEET, S, ('down', 'present'), 1)
    for k, (dx, rot) in enumerate(((-130, -26), (-45, -10), (45, 6), (130, 22))): coupon_card(c, hx + 190 + dx, hy - 40 - abs(dx) * .25, rot, 1.45)
    r = random.Random(9)
    for k in range(22):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(220, 420); x0, y0 = hx + 120 + math.cos(a) * d, hy + math.sin(a) * d * .7
        c.drawCircle(x0, y0, r.uniform(4, 9), fp('#FFE6A0')); c.drawCircle(x0, y0, 20, fp(GOLD, 70, blur=10))
    _headline(c, [('50% ', GOLD), ('IN 45 DAYS', WHITE)])
    _save(s, path)

def thumb_c(path):
    """C - "THE FIRST PONZI SCHEME": Ponzi on top of a cracking pyramid of investors."""
    s = skia.Surface(W, H); c = s.getCanvas(); _bg(c, 1.4, (900, 400), dark=150)
    cx, base = 1240, 1060; rows = 6; rowh = 125
    for rr in range(rows):
        n = 1 + rr * 2; y = base - (rows - rr) * rowh
        for i in range(n):
            px = cx - n * 92 / 2 + 46 + i * 92
            c.save(); c.translate(px, y + 60); c.scale(1.15, 1.15); circ(c, 0, -34, 22, '#E9C09A', 5); rect(c, -26, -12, 26, 44, NAVY if rr < rows - 1 else '#3E5689', 5, r=10)
            Wd.coin(c, 0, -74, 16); c.restore()
    for side in (-1, 1):
        p = skia.Path(); p.moveTo(cx + side * 470, base - 60); p.quadTo(cx + side * 520, base - 420, cx + side * 90, base - rows * rowh - 20)
        c.drawPath(p, ink(22, (10, 17, 36))); c.drawPath(p, ink(13, GOLD))
    crk = skia.Path(); crk.moveTo(cx - 520, base - 30)
    for px, py in ((-380, -70), (-260, -20), (-120, -90), (0, -40), (140, -100), (300, -30), (520, -80)): crk.lineTo(cx + px, base + py)
    c.drawPath(crk, ink(30, (10, 17, 36))); c.drawPath(crk, ink(16, ORANGE)); c.drawPath(crk, fp(ORANGE, 0)); c.drawPath(crk, ink(40, ORANGE, 70))
    c.drawCircle(470, 560, 380, fp(GOLD, 60, blur=80, blend=skia.BlendMode.kPlus))
    draw_char(c, 470, 1330, 1.85, dict(CAST['ponzi']), face=.35, eyes='closed', mouth='open', arms=('cheer', 'hip'), light=1, rim='#FFD27A', hat=True)
    _headline(c, [('THE FIRST ', WHITE), ('PONZI ', GOLD), ('SCHEME', WHITE)], size=140)
    _save(s, path)

if __name__ == '__main__':
    thumb(HERE / 'thumb_B_20M_gone.jpg'); thumb_a(HERE / 'thumb_A_50pct_45days.jpg'); thumb_c(HERE / 'thumb_C_first_ponzi.jpg')
    thumb(HERE / 'thumb_B_20M_gone.jpg'); print('saved')
