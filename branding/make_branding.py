"""Dirty Dollar - channel branding: profile photo (800x800) + banner (2560x1440, safe area 1546x423).
Locked style: navy + gold, Alfa Slab / Barlow, ink outlines, dotted print vignette, our cast."""
import sys, os, math, pathlib, numpy as np, skia
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '.claude' / 'skills' / 'documentary-animator'))
from engine import kit, widgets as Wd
from engine.cast import CAST
from engine.core import NAVY, GOLD, GOLD_D, ORANGE, WHITE, PAPER, F_TITLE, F_LABEL, F_LABEL2
from engine.kit import fp, ink, circ, rect, poly, draw_char

def dotted_bg(w, h, centre=(66, 92, 150), edge=(12, 20, 46), P=9.0):
    yy, xx = np.mgrid[0:h, 0:w].astype(float); d = np.sqrt(((xx - w / 2) / (w * .55)) ** 2 + ((yy - h / 2) / (h * .6)) ** 2)
    a = np.radians(45); u = (xx * np.cos(a) + yy * np.sin(a)) * 2 * np.pi / P; v = (-xx * np.sin(a) + yy * np.cos(a)) * 2 * np.pi / P
    scr = (np.cos(u) + np.cos(v) + 2) / 4; t = np.clip((d - .4) / .6, 0, 1); k = np.clip(d / 1.1, 0, 1)[..., None]
    base = np.array(centre) * (1 - k) + np.array(edge) * k; out = np.where((t > (1 - scr))[..., None], np.array(edge, float), base)
    return skia.Image.fromarray(np.dstack([np.clip(out, 0, 255).astype(np.uint8), np.full((h, w), 255, np.uint8)]), colorType=skia.kRGBA_8888_ColorType)

def coin(c, x, y, r):
    """Big gold coin with a $ and a dirty smudge + crack (the 'dirty dollar')."""
    c.drawCircle(x + r * .06, y + r * .08, r * 1.02, fp((0, 0, 0), 110, blur=r * .08))
    circ(c, x, y, r, GOLD, r * .07); circ(c, x, y, r * .8, None, r * .035, v='#B07A0A')
    for i in range(40): a = i / 40 * 2 * math.pi; c.drawLine(x + math.cos(a) * r * .88, y + math.sin(a) * r * .88, x + math.cos(a) * r * .95, y + math.sin(a) * r * .95, ink(r * .02, '#B07A0A'))
    c.drawOval(skia.Rect(x - r * .62, y - r * .7, x - r * .1, y - r * .38), fp(WHITE, 120, blur=r * .05))      # gloss
    f = skia.Font(F_TITLE, r * 1.25); w = f.measureText('$')
    c.drawString('$', x - w / 2 + r * .04, y + r * .44 + r * .04, f, fp('#8A5A06')); c.drawString('$', x - w / 2, y + r * .44, f, fp(NAVY))
    sm = skia.Path(); sm.moveTo(x + r * .1, y + r * .25)                                                       # dirt smudge
    for k in range(9): a = k / 9 * 2 * math.pi; rr = r * (.3 + .12 * math.sin(k * 2.7)); sm.lineTo(x + r * .32 + math.cos(a) * rr, y + r * .42 + math.sin(a) * rr * .7)
    sm.close(); c.save(); p = skia.Path(); p.addCircle(x, y, r * .97); c.clipPath(p, doAntiAlias=True)
    c.drawPath(sm, fp('#3A2A12', 150, blur=r * .05)); [c.drawCircle(x + r * (.1 + .09 * k), y + r * (.15 + .07 * (k % 3)), r * .03, fp('#3A2A12', 170)) for k in range(7)]
    cr = skia.Path(); cr.moveTo(x - r * .95, y + r * .1)
    for px, py in ((-.6, .02), (-.45, .2), (-.25, .08), (-.08, .3)): cr.lineTo(x + r * px, y + r * py)
    c.drawPath(cr, ink(r * .035, NAVY)); c.restore()

def profile(path, size=800):
    s = skia.Surface(size, size); c = s.getCanvas(); c.drawImage(dotted_bg(size, size), 0, 0)
    R = size / 2
    for inset, wd in ((size * .03, size * .025), (size * .075, size * .01)): c.drawCircle(R, R, R - inset, ink(wd, '#9DB0DA'))
    coin(c, R, R * .9, size * .3)
    f = skia.Font(F_TITLE, size * .088); t = 'DIRTY DOLLAR'; w = f.measureText(t)
    yb = size * .82; rect(c, R - w / 2 - size * .04, yb - size * .1, R + w / 2 + size * .04, yb + size * .035, NAVY, size * .012, r=size * .02)
    c.drawString(t, R - w / 2, yb, f, fp(WHITE)); fw = skia.Font(F_TITLE, size * .088).measureText('DIRTY ')
    c.drawString('DOLLAR', R - w / 2 + fw, yb, f, fp(GOLD))
    s.makeImageSnapshot().save(path, skia.kPNG)

def banner(path, W=2560, H=1440):
    s = skia.Surface(W, H); c = s.getCanvas(); c.drawImage(dotted_bg(W, H, P=10.0), 0, 0)
    # safe area (visible on every device): 1546 x 423 centred -> x 507-2053, y 508-931
    cy = H / 2
    # cast on the sides (TV/desktop show them; phones show only the centre)
    for (x, who, arms, kw) in ((170, 'ponzi', ('present', 'hip'), dict(hat=True, mouth='smirk', eyes='half')), (385, 'scammer', ('cross', 'cross'), dict(mouth='smirk', eyes='half')),
                               (2175, 'ceo', ('pocket', 'hip'), dict(mouth='grit', eyes='wide', brow=.8)), (2390, 'investor', ('chin', 'down'), dict(mouth='o', eyes='wide', brow=.7))):
        draw_char(c, x, 1180, 1.12, CAST[who], face=(.3 if x < W / 2 else -.3), arms=arms, light=-1, rim='#9FB8F0', **kw)
    for i in range(14): Wd.bill(c, 700 + (i * 137) % 1200, 180 + (i * 89) % 260, -30 + (i * 23) % 60, 1.2)       # money flying (top band)
    f = skia.Font(F_TITLE, 150); t1, t2 = 'DIRTY ', 'DOLLAR'; w1 = f.measureText(t1); w = w1 + f.measureText(t2)
    cr = 125; gap = 40; total = 2 * cr + gap + w; xc = (W - total) / 2                      # coin + title fit the safe area (507-2053)
    coin(c, xc + cr, cy - 10, cr); x0 = xc + 2 * cr + gap
    for tx, col in ((t1, WHITE), (t2, GOLD)):
        xx = x0 if tx == t1 else x0 + w1
        c.drawString(tx, xx + 8, cy + 30 + 10, f, fp((0, 0, 0), 140, blur=6)); c.drawString(tx, xx, cy + 30, f, ink(18, '#0A1124')); c.drawString(tx, xx, cy + 30, f, fp(col))
    tag = 'MONEY STORIES  ·  SCAMS  ·  FRAUD  ·  LESSONS'; ft = skia.Font(F_LABEL, 50); tw = ft.measureText(tag)
    rect(c, x0, cy + 60, x0 + w, cy + 130, NAVY, 6, r=12); c.drawRect(skia.Rect(x0 + 4, cy + 64, x0 + 20, cy + 126), fp(GOLD))
    c.drawString(tag, x0 + 36 + (w - 36 - tw) / 2, cy + 112, ft, fp(WHITE))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(24, 24, W - 24, H - 24), 40, 40), ink(14, '#9DB0DA'))
    s.makeImageSnapshot().save(path, skia.kPNG)

def banner_mobile(path, W=2560, H=1440):
    """Mobile-optimised: EVERYTHING (cast + name + tagline) inside the 1546x423 safe area that phones show
    (x 507-2053, y 508-931). Characters are big busts whose heads + bodies sit in the strip."""
    s = skia.Surface(W, H); c = s.getCanvas(); c.drawImage(dotted_bg(W, H, P=10.0), 0, 0)
    for i in range(10): Wd.bill(c, 620 + (i * 151) % 1320, 300 + (i * 67) % 150, -30 + (i * 23) % 60, 1.0)      # money above (desktop/TV bonus)
    S = 0.95; FEET = 1085                                                                                       # head top ~530, body inside the strip
    for (x, who, arms, kw) in ((655, 'ponzi', ('pocket', 'hip'), dict(hat=True, mouth='smirk', eyes='half')), (835, 'scammer', ('cross', 'cross'), dict(mouth='smirk', eyes='half')),
                               (1725, 'ceo', ('pocket', 'hip'), dict(mouth='grit', eyes='wide', brow=.8)), (1920, 'investor', ('chin', 'down'), dict(mouth='o', eyes='wide', brow=.7))):
        draw_char(c, x, FEET, S, CAST[who], face=(.35 if x < W / 2 else -.35), arms=arms, light=-1, rim='#9FB8F0', **kw)
    cx = W / 2; f = skia.Font(F_TITLE, 132)
    for word, col, y in (('DIRTY', WHITE, 690), ('DOLLAR', GOLD, 830)):
        w = f.measureText(word); c.drawString(word, cx - w / 2 + 7, y + 9, f, fp((0, 0, 0), 140, blur=6)); c.drawString(word, cx - w / 2, y, f, ink(16, '#0A1124')); c.drawString(word, cx - w / 2, y, f, fp(col))
    coin(c, cx, 575, 46)
    tag = 'MONEY STORIES  ·  SCAMS  ·  FRAUD'; ft = skia.Font(F_LABEL, 40); tw = ft.measureText(tag)
    rect(c, cx - tw / 2 - 30, 856, cx + tw / 2 + 30, 914, NAVY, 5, r=10); c.drawString(tag, cx - tw / 2, 899, ft, fp(WHITE))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(24, 24, W - 24, H - 24), 40, 40), ink(14, '#9DB0DA'))
    s.makeImageSnapshot().save(path, skia.kPNG)

def profile_face(path, who='ceo', size=800, over_mouth='open', name_band=False, **over):
    """Profile photo: one character close-up with gold dollar signs in his eyes, name band below."""
    from engine.cast import person
    s = skia.Surface(size, size); c = s.getCanvas(); c.drawImage(dotted_bg(size, size), 0, 0)
    R = size / 2
    for i in range(16):                                                                     # gold rays behind the head
        a = i / 16 * 2 * math.pi; p = skia.Path(); p.moveTo(R, R * .82)
        p.lineTo(R + math.cos(a - .09) * size, R * .82 + math.sin(a - .09) * size); p.lineTo(R + math.cos(a + .09) * size, R * .82 + math.sin(a + .09) * size); p.close()
        c.drawPath(p, fp(GOLD, 38))
    c.drawCircle(R, R * .8, size * .34, fp(GOLD, 70, blur=size * .08))
    spec = person(who, glasses=False, **over)
    sc = size / 330; draw_char(c, R, size * .5 + sc * 461, sc, spec, face=0.0, eyes='dollar', mouth=over_mouth, brow=-.5, brow_tilt=.5, arms=('down', 'down'), light=-1, rim='#9FB8F0', sparkle=0)
    for inset, wd in ((size * .03, size * .025), (size * .075, size * .01)): c.drawCircle(R, R, R - inset, ink(wd, '#9DB0DA'))
    if not name_band: s.makeImageSnapshot().save(path, skia.kPNG); return   # owner: no text on the profile photo
    f = skia.Font(F_TITLE, size * .074); t = 'DIRTY DOLLAR'; w = f.measureText(t); yb = size * .83
    rect(c, R - w / 2 - size * .04, yb - size * .1, R + w / 2 + size * .04, yb + size * .035, NAVY, size * .012, r=size * .02)
    fw = f.measureText('DIRTY '); c.drawString('DIRTY ', R - w / 2, yb, f, fp(WHITE)); c.drawString('DOLLAR', R - w / 2 + fw, yb, f, fp(GOLD))
    s.makeImageSnapshot().save(path, skia.kPNG)

if __name__ == '__main__':
    profile_face(str(HERE / 'profile_800.png'), 'ceo', moustache_dy=10, over_mouth='open'); profile(str(HERE / 'profile_coin_800.png')); banner(str(HERE / 'banner_2560x1440.png')); banner_mobile(str(HERE / 'banner_mobile_2560x1440.png')); print('saved')
