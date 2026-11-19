"""On-screen graphics in the locked style. Every function draws onto a skia canvas at time u.
Colour rules: gold = money / brand, orange = losses ONLY and always with a minus sign or a down arrow,
gains in navy (on paper) or white (on dark) with an up arrow, never green. Fonts: DSEG counters, Alfa Slab
titles/stamps, Special Elite typed text, Barlow labels."""
import math, random
import skia
from engine.core import W, H, NAVY, NAVY2, NAVY3, BLACK, WHITE, GREY, GOLD, GOLD_D, ORANGE, PAPER, F_COUNTER, F_TITLE, F_TYPE, F_LABEL, F_LABEL2
from engine.kit import fp, ink, hx, rect, circ, poly, shape, pop, back, ease, ease_out, lerp, K, INK

def _font(tf, size): return skia.Font(tf, size)
def text(c, s, x, y, size, color, tf=F_LABEL, align='left', stroke=0, stroke_col=INK, alpha=255):
    f = _font(tf, size); w = f.measureText(s); ox = {'left': 0, 'center': -w / 2, 'right': -w}[align]
    if stroke: c.drawString(s, x + ox, y, f, ink(stroke, stroke_col, alpha))
    c.drawString(s, x + ox, y, f, fp(color, alpha)); return w
def wrap(words, tf, size, maxw):
    f = _font(tf, size); lines, cur = [], []
    for w in words:
        if cur and f.measureText(' '.join(cur + [w])) > maxw: lines.append(cur); cur = [w]
        else: cur.append(w)
    if cur: lines.append(cur)
    return lines

# ---------------- framed stage (owner's reference for diagram / document / newspaper shots)
_FRAME = None
def framed_bg(c):
    """Navy stage with a soft dotted vignette and a double rounded light-navy border around the whole frame."""
    global _FRAME
    if _FRAME is None:
        import numpy as np
        yy, xx = np.mgrid[0:H, 0:W].astype(float); d = np.sqrt(((xx - W / 2) / (W * .55)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2)
        a = np.radians(45); P = 8.0; u = (xx * np.cos(a) + yy * np.sin(a)) * 2 * np.pi / P; v = (-xx * np.sin(a) + yy * np.cos(a)) * 2 * np.pi / P
        scr = (np.cos(u) + np.cos(v) + 2) / 4; t = np.clip((d - .45) / .55, 0, 1)
        centre = np.array([66, 92, 150], float); edge = np.array([14, 24, 52], float)
        base = centre * (1 - np.clip(d / 1.1, 0, 1))[..., None] + edge * np.clip(d / 1.1, 0, 1)[..., None]
        out = np.where((t > (1 - scr) * 1.05)[..., None], edge, base)
        img = np.dstack([np.clip(out, 0, 255).astype(np.uint8), np.full((H, W), 255, np.uint8)])
        s = skia.Surface(W, H); cc = s.getCanvas(); cc.drawImage(skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType), 0, 0)
        for inset, wdt, col_ in ((26, 12, '#9DB0DA'), (60, 5, '#9DB0DA')):
            cc.drawRRect(skia.RRect.MakeRectXY(skia.Rect(inset, inset, W - inset, H - inset), 34, 34), ink(wdt + 6, '#0A1124'))
            cc.drawRRect(skia.RRect.MakeRectXY(skia.Rect(inset, inset, W - inset, H - inset), 34, 34), ink(wdt, col_))
        _FRAME = s.makeImageSnapshot()
    c.drawImage(_FRAME, 0, 0)

def paper_card(c, x, y, title, lines, u, w=760, h=560, rot=3, slam=False):
    """Big paper card (owner's coupon reference): Barlow heading + rule, Special Elite lines.
    Default: flutters in from below (swaying, shadow lifting off the table) and settles with a small bounce.
    slam=True: drops from above, shadow shrinks to contact, lands with a bounce (pair with a 'stamp' SFX)."""
    k = min(max(u / .45, 0), 1)
    if slam:
        kk = k ** 2.2; sc = lerp(1.4, 1.0, kk); dy = 0; sway = 0
        land = max(0, u - .45); bump = math.exp(-land * 10) * math.sin(land * 34) * .025 if land > 0 else 0; sc += bump
        lift = (1 - kk) * 60
    else:
        e = back(k, 1.3); dy = (1 - e) * 640; sway = math.sin(k * math.pi * 3) * (1 - k) * 9; sc = 1.0; lift = (1 - k) * 50
    c.save(); c.translate(x, y + dy); c.rotate(rot + sway); c.scale(sc, sc)
    c.drawRect(skia.Rect(-w / 2 + 14 + lift, -h / 2 + 18 + lift, w / 2 + 14 + lift, h / 2 + 18 + lift), fp((0, 0, 0), int(90 - lift * .6), blur=14 + lift * .3))
    rect(c, -w / 2, -h / 2, w / 2, h / 2, PAPER, 6)
    c.drawRect(skia.Rect(w / 2 - 70, -h / 2, w / 2, -h / 2 + 70), fp('#E9DFC8'))                  # folded corner
    poly(c, [(w / 2 - 70, -h / 2), (w / 2, -h / 2 + 70), (w / 2 - 70, -h / 2 + 70)], '#D9CDB2', 4)
    text(c, title.upper(), -w / 2 + 50, -h / 2 + 100, 76, NAVY, F_LABEL); c.drawRect(skia.Rect(-w / 2 + 50, -h / 2 + 128, w / 2 - 90, -h / 2 + 136), fp(NAVY))
    for i_, ln in enumerate(lines): text(c, ln, -w / 2 + 50, -h / 2 + 220 + i_ * 72, 52, NAVY, F_TYPE)
    c.restore()

def big_label(c, s, x, y, u, color=WHITE, size=110, maxw=760):
    """Large Alfa Slab label with ink stroke (EUROPE / UNITED STATES style); shrinks to fit maxw."""
    size = min(size, size * maxw / max(_font(F_TITLE, size).measureText(s.upper()), 1))
    k = .85 + .15 * pop(u); c.save(); c.translate(x, y); c.scale(k, k); text(c, s.upper(), 0, 0, size, color, F_TITLE, 'center', stroke=14); c.restore()

def arrow(c, x0, y0, x1, y1, u, color=GOLD, wdt=60):
    """Big flat arrow that grows from x0 to x1."""
    k = ease_out(min(max(u, 0), 1)); xe = lerp(x0, x1, k); hd = wdt * 1.1
    if xe - x0 < hd: return
    poly(c, [(x0, y0 - wdt / 2), (xe - hd, y0 - wdt / 2), (xe - hd, y0 - wdt), (xe, y0), (xe - hd, y0 + wdt), (xe - hd, y0 + wdt / 2), (x0, y0 + wdt / 2)], color, 7)

# ---------------- cards (full screen)
TYPE_CPS = (9.0, 16.0)   # typing speed range (characters per second): believable, but finishes inside the voice line
def type_times(s, dur):
    """Reveal time of every character of a typed card (same times drive the typewriter sound)."""
    n = max(len(s), 1); cps = min(max(n / max(dur * .85, .1), TYPE_CPS[0]), TYPE_CPS[1])
    return [i / cps for i in range(len(s))]
def text_card(c, s, t, gold_words=(), bg=BLACK, size=78, color=WHITE, dur=3.0):
    """Typed text card: Special Elite, revealed LETTER BY LETTER at a typewriter pace (type_times), gold block cursor.
    t = seconds into the card, dur = the voice line length. First letter visible on frame 1. Max ~12 words."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(bg)); words = s.split(); lines = wrap(words, F_TYPE, size, 1500)
    times = type_times(s, dur); shown = max(1, sum(1 for x in times if x <= t)); f = _font(F_TYPE, size); lh = size * 1.35
    y0 = H / 2 - (len(lines) - 1) * lh / 2 + size * .3; k = 0; cx = cy = None
    gw = {g.lower().strip('.,!?') for g in gold_words}
    for i, ln in enumerate(lines):
        x = W / 2 - f.measureText(' '.join(ln)) / 2; y = y0 + i * lh
        for wd in ln:
            col_ = GOLD if wd.lower().strip('.,!?') in gw else color
            vis = wd[:max(0, min(len(wd), shown - k))]
            if vis: c.drawString(vis, x, y, f, fp(col_)); cx, cy = x + f.measureText(vis) + 8, y
            x += f.measureText(wd + ' '); k += len(wd) + 1
    if cx is None: cx, cy = W / 2 - f.measureText(' '.join(lines[0])) / 2, y0
    if shown < len(s) or int(t * 2.5) % 2 == 0: c.drawRect(skia.Rect(cx, cy - size * .78, cx + size * .45, cy + size * .08), fp(GOLD))

def chapter_card(c, n, title, u):
    """Navy chapter card: 'CHAPTER n' in gold Barlow, title in Alfa Slab popping in, gold rule growing."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(NAVY))
    a = .45 + .55 * ease(K(u, 0, .25)); text(c, f'CHAPTER {n}', W / 2, 420, 52, GOLD, F_LABEL, 'center', alpha=int(255 * a))
    ts = min(120, 120 * 1640 / max(_font(F_TITLE, 120).measureText(title.upper()), 1))
    k = .8 + .2 * pop(K(u, 0, .35)); c.save(); c.translate(W / 2, 560); c.scale(k, k); text(c, title.upper(), 0, 0, ts, WHITE, F_TITLE, 'center', stroke=0); c.restore()
    wl = 520 * (.25 + .75 * ease_out(K(u, .1, .4))); c.drawRect(skia.Rect(W / 2 - wl, 618, W / 2 + wl, 628), fp(GOLD))

def title_card(c, title, u, gold_word=None, sub=None):
    """Black title card after the hook: Alfa Slab title, one gold word, optional Barlow subtitle."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(BLACK)); k = .82 + .18 * pop(K(u, 0, .4)); f = _font(F_TITLE, 130)
    words = title.upper().split(); tw = f.measureText(' '.join(words)); c.save(); c.translate(W / 2, H / 2 + 30); c.scale(k, k); x = -tw / 2
    for w in words:
        c.drawString(w, x, 0, f, fp(GOLD if gold_word and w.strip('.,!?') == gold_word.upper() else WHITE)); x += f.measureText(w + ' ')
    c.restore()
    if sub: text(c, sub.upper(), W / 2, H / 2 + 120, 44, GREY, F_LABEL2, 'center', alpha=int(255 * ease(K(u, .3, .3))))

# ---------------- counters
def money_str(v, unit='$', decimals=0):
    s = f'{abs(v):,.{decimals}f}'; return s
def counter(c, x, y, v0, v1, u, unit='$', loss=False, size=96, label=None, panel=True, suffix='', decimals=0):
    """Digital counter (DSEG digits, Barlow $ , and commas). Gold for money; loss=True -> orange with a minus and
    a down arrow. (x, y) = centre of the panel. u 0..1 counts with ease-out."""
    v = lerp(v0, v1, ease_out(min(max(u, 0), 1))); col = ORANGE if loss else GOLD
    groups = money_str(v, unit, decimals).split(','); fd = _font(F_COUNTER, size); fb = _font(F_LABEL, size * 1.12)
    parts = ([('-', fb)] if loss else []) + ([(unit, fb)] if unit else [])
    for i, g in enumerate(groups): parts += [(g, fd)] + ([(',', fb)] if i < len(groups) - 1 else [])
    if suffix: parts.append((suffix, fb))
    gap = size * .06; tw = sum(f.measureText(t) for t, f in parts) + gap * (len(parts) - 1); aw = size * .7 if loss else 0
    if panel:
        pw, ph = tw + aw + size * .9, size * 1.45
        rect(c, x - pw / 2, y - ph / 2, x + pw / 2, y + ph / 2, NAVY, 6, r=14); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x - pw / 2 + 8, y - ph / 2 + 8, x + pw / 2 - 8, y + ph / 2 - 8), 10, 10), ink(3, col))
    xx = x - (tw + aw) / 2; yy = y + size * .38
    for t, f in parts: c.drawString(t, xx, yy, f, fp(col)); xx += f.measureText(t) + gap
    if loss: ax = xx + aw * .45; poly(c, [(ax - aw * .35, y - size * .2), (ax + aw * .35, y - size * .2), (ax, y + size * .32)], ORANGE, 0)
    if label: text(c, label.upper(), x, y + size * 1.3, size * .5, WHITE, F_LABEL, 'center', stroke=8)

# ---------------- stamps, labels, tags
def stamp(c, s, x, y, t, color=GOLD, rot=-8, size=110):
    """Stamp slam: t = seconds since the hit. Scale 2.6 -> 1 in 0.2 s. Returns camera shake (dx, dy)."""
    if t < 0: return (0, 0)
    k = lerp(2.6, 1.0, ease_out(min(t / .2, 1))); a = min(t / .08, 1)
    f = _font(F_TITLE, size); tw = f.measureText(s.upper())
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    for inset, w in ((0, 12), (22, 5)):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-tw / 2 - 46 + inset, -size * .78 + inset, tw / 2 + 46 - inset, size * .52 - inset), 18, 18), ink(w, color, int(255 * a)))
    c.drawString(s.upper(), -tw / 2, size * .3, f, fp(color, int(255 * a))); c.restore()
    if t < .35: r = random.Random(int(t * 100)); amp = 14 * (1 - t / .35); return (r.uniform(-amp, amp), r.uniform(-amp, amp))
    return (0, 0)

def pop_label(c, s, x, y, u, color=WHITE, size=84, rot=-4, stroke=16):
    """Barlow label with a thick ink stroke that pops in with overshoot."""
    k = pop(u)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); text(c, s.upper(), 0, 0, size, color, F_LABEL, 'center', stroke=stroke); c.restore()

def lower_third(c, name, role, u, x=80, y=830):   # clear of the captions
    """Name tag: navy box, gold bar, Barlow name + gold role. Scales in with back()."""
    k = back(min(max(u / .4, 0), 1)); fn, fr = _font(F_LABEL, 84), _font(F_LABEL2, 48)
    w = max(fn.measureText(name.upper()), fr.measureText(role.upper())) + 90
    c.save(); c.translate(x, y); c.scale(k, 1)
    rect(c, 0, -40, w, 130, NAVY, 5, r=8); c.drawRect(skia.Rect(4, -36, 24, 126), fp(GOLD))
    c.drawString(name.upper(), 48, 44, fn, fp(WHITE)); c.drawString(role.upper(), 48, 104, fr, fp(GOLD)); c.restore()

def place_tag(c, place, u, sub=None):
    """Location tag top-left: gold pin + Barlow place name (+ date)."""
    a = int(255 * ease(K(u, 0, .3))); x, y = 80, 120
    circ(c, x, y - 40, 20, GOLD, 4); poly(c, [(x - 15, y - 30), (x + 15, y - 30), (x, y)], GOLD, 0)
    text(c, place.upper(), x + 42, y - 14, 66, WHITE, F_LABEL, stroke=10, alpha=a)
    if sub: text(c, sub.upper(), x + 42, y + 36, 44, GOLD, F_LABEL2, stroke=8, alpha=a)

def sticky(c, s, x, y, u, rot=-5, w=220):
    """Gold-paper sticky note with navy Barlow text."""
    k = pop(u)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    c.drawRect(skia.Rect(-w / 2 + 8, -w / 2 + 12, w / 2 + 8, w / 2 + 12), fp((0, 0, 0), 70, blur=8)); rect(c, -w / 2, -w / 2, w / 2, w / 2, '#FFE2A0', 4)
    lines = wrap(s.upper().split(), F_LABEL, 44, w - 30)
    for i, ln in enumerate(lines): text(c, ' '.join(ln), 0, -len(lines) * 24 + 40 + i * 48, 44, NAVY, F_LABEL, 'center')
    c.restore()

def document(c, x, y, title, lines, u, w=560, h=700, rot=-3, stamp_txt=None, stamp_t=-1):
    """Paper document sliding in; title in Barlow, lines typed in Special Elite (navy on paper)."""
    k = back(min(max(u / .35, 0), 1)); c.save(); c.translate(x, y + (1 - k) * 500); c.rotate(rot)
    c.drawRect(skia.Rect(-w / 2 + 14, -h / 2 + 18, w / 2 + 14, h / 2 + 18), fp((0, 0, 0), 80, blur=12)); rect(c, -w / 2, -h / 2, w / 2, h / 2, PAPER, 5)
    text(c, title.upper(), -w / 2 + 36, -h / 2 + 70, 48, NAVY, F_LABEL); c.drawRect(skia.Rect(-w / 2 + 36, -h / 2 + 92, w / 2 - 36, -h / 2 + 97), fp(NAVY))
    total = sum(len(l) for l in lines); shown = int(max(u - .2, 0) / .8 * total); k2 = 0
    for i, ln in enumerate(lines):
        vis = ln[:max(0, min(len(ln), shown - k2))]; k2 += len(ln)
        text(c, vis, -w / 2 + 36, -h / 2 + 160 + i * 56, 34, NAVY, F_TYPE)
    if stamp_txt and stamp_t >= 0: stamp(c, stamp_txt, w * .12, h * .22, stamp_t, ORANGE if stamp_txt.upper() in ('FRAUD', 'DENIED', 'GUILTY', 'LOSS', 'SCAM') else GOLD, rot=-12, size=80)
    c.restore()

# ---------------- charts
def bar_chart(c, x0, y0, x1, y1, values, labels, u, colors=None, fmt=lambda v: f'${v:,.0f}', dark=True, title=None):
    """Bars grow in one after another. colors: list of GOLD / ORANGE (loss) / NAVY3. Axis + labels in white (dark bg) or navy."""
    tc = WHITE if dark else NAVY; n = len(values); vmax = max(values) or 1; bw = (x1 - x0) / n
    c.drawLine(x0, y1, x1, y1, ink(6, tc))
    if title: text(c, title.upper(), x0, y0 - 30, 50, tc, F_LABEL)
    for i, (v, lb) in enumerate(zip(values, labels)):
        g = ease_out(K(u, i * .12, .45)); h = (y1 - y0 - 70) * v / vmax * g; bx = x0 + i * bw + bw * .18; col = (colors or [GOLD] * n)[i]
        if h > 1: rect(c, bx, y1 - h, bx + bw * .64, y1, col, 5, r=6); c.drawRect(skia.Rect(bx + 10, y1 - h + 10, bx + 22, y1 - 10), fp(WHITE, 60))
        if g > .9: text(c, fmt(v), bx + bw * .32, y1 - h - 18, 40, col if col != NAVY3 else tc, F_LABEL, 'center')
        text(c, lb.upper(), bx + bw * .32, y1 + 48, 36, tc, F_LABEL2, 'center')

def line_chart(c, x0, y0, x1, y1, values, u, color=GOLD, dark=True, labels=None, area=True):
    """Line draws on left to right with a glowing dot at the head. Use ORANGE only for a falling (loss) line."""
    tc = WHITE if dark else NAVY; c.drawLine(x0, y1, x1, y1, ink(5, tc)); c.drawLine(x0, y1, x0, y0, ink(5, tc))
    lo, hi = min(values), max(values); rng = (hi - lo) or 1; n = len(values)
    pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - 30 - (y1 - y0 - 60) * (v - lo) / rng) for i, v in enumerate(values)]
    m = (n - 1) * min(max(u, 0), 1); k = int(m); fr = m - k; vis = pts[:k + 1] + ([(lerp(pts[k][0], pts[k + 1][0], fr), lerp(pts[k][1], pts[k + 1][1], fr))] if k + 1 < n else [])
    if len(vis) < 2: return
    p = skia.Path(); p.moveTo(*vis[0]); [p.lineTo(*q) for q in vis[1:]]
    if area:
        a = skia.Path(p); a.lineTo(vis[-1][0], y1); a.lineTo(vis[0][0], y1); a.close(); c.drawPath(a, fp(NAVY3 if dark else '#D6DEEC', 150))
    c.drawPath(p, ink(16, INK)); c.drawPath(p, ink(9, color)); hx_, hy_ = vis[-1]
    c.drawCircle(hx_, hy_, 26, fp(color, 70, blur=10)); circ(c, hx_, hy_, 11, color, 4)
    if labels:
        for i, lb in enumerate(labels):
            if lb: text(c, lb, pts[i][0], y1 + 44, 34, tc, F_LABEL2, 'center')

# ---------------- money props
def bill(c, x, y, rot=0, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(c, -80, -36, 80, 36, '#F4F1E8', 4); rect(c, -70, -27, 70, 27, None, 2.5, v=NAVY); circ(c, 0, 0, 20, GOLD, 2.5); text(c, '$', 0, 11, 30, NAVY, F_TITLE, 'center'); c.restore()
def coin(c, x, y, r=22): circ(c, x, y, r, GOLD, 3.5); circ(c, x, y, r * .7, None, 2, v='#B07A0A'); text(c, '$', x, y + r * .4, r * 1.05, '#9A6A08', F_TITLE, 'center')
def cash_stack(c, x, y, n=6, s=1.0):
    for i in range(n): bill(c, x + (i % 2) * 4, y - i * 10 * s, 0, s)
def gold_bar(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); poly(c, [(-90, 30), (90, 30), (64, -30), (-64, -30)], GOLD, 5); poly(c, [(-64, -30), (64, -30), (52, -44), (-52, -44)], '#FFD266', 4); c.restore()
def falling_money(c, t, seed=3, n=18, area=(0, 0, W, H)):
    r = random.Random(seed)
    for _ in range(n):
        x0, sp, ph, rot = r.uniform(area[0], area[2]), r.uniform(120, 260), r.uniform(0, 10), r.uniform(-40, 40)
        y = area[1] - 80 + ((t + ph) * sp) % (area[3] - area[1] + 160); x = x0 + math.sin((t + ph) * 2) * 40
        bill(c, x, y, rot + math.sin(t * 3 + ph) * 25, .8)

# ---------------- ending
def polaroid(c, frame, u, caption=None, ring=None):
    """Freeze-frame polaroid ending. frame = skia.Image of the last frame. ring = (x, y, r) in frame coords to circle in gold."""
    c.drawRect(skia.Rect(0, 0, W, H), fp(NAVY)); k = ease_out(K(u, 0, .3)); s = lerp(1.0, .67, k); rot = lerp(0, -4, k)
    c.save(); c.translate(W / 2, H / 2 - 20 * k); c.rotate(rot); c.scale(s, s)
    rect(c, -W / 2 - 40, -H / 2 - 40, W / 2 + 40, H / 2 + 200, '#FBF8F0', 6 / s); c.drawImageRect(frame, skia.Rect(-W / 2, -H / 2, W / 2, H / 2), skia.SamplingOptions())
    if ring and u > .35:
        rx, ry, rr = ring; sw = 360 * ease_out(K(u, .35, .5)); p = skia.Path(); p.addArc(skia.Rect(rx - W / 2 - rr, ry - H / 2 - rr, rx - W / 2 + rr, ry - H / 2 + rr), -100, sw); c.drawPath(p, ink(16 / s, GOLD))
    if caption and u > .5: text(c, caption, 0, H / 2 + 130, 80, NAVY, F_TYPE, 'center')
    c.restore()
    if u < .12: c.drawRect(skia.Rect(0, 0, W, H), fp(WHITE, int(255 * (1 - u / .12))))
