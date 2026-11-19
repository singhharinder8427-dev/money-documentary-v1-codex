"""Story animations (owner: "more relevant animation - hands slamming notes on the table, charts..."):
hand slams, pyramid diagram, tear-off calendar, map route, handcuffs, newspaper spin-in, ringing phone, ledger,
envelope, prison bars, outro + end screen. All in the locked style. Each takes the canvas and local time t (s).
Functions that hit something return a camera shake (dx, dy) to pass to render_shot(shake=...)."""
import math, random
import skia
from engine.core import W, H, NAVY, NAVY2, NAVY3, GOLD, GOLD_D, ORANGE, WHITE, GREY, PAPER, F_TITLE, F_TYPE, F_LABEL, F_LABEL2, F_COUNTER
from engine.kit import fp, sp, ink, rect, circ, oval, poly, shape, ease, ease_out, back, pop, lerp, K, INK
from engine import widgets as Wd

def _shake(t, hit, amp=16, dur=.3):
    d = t - hit
    if 0 <= d < dur: r = random.Random(int(d * 200)); a = amp * (1 - d / dur); return (r.uniform(-a, a), r.uniform(-a, a))
    return (0, 0)

def sleeve(c, x0, y0, x1, y1, col=NAVY2, cuff=WHITE, skin='#E9C09A', w=110):
    """An arm coming in from the frame edge (x0,y0) to the hand at (x1,y1), seen from above."""
    a = math.atan2(y1 - y0, x1 - x0); L = math.hypot(x1 - x0, y1 - y0)
    c.save(); c.translate(x0, y0); c.rotate(math.degrees(a))
    rect(c, -40, -w / 2, L - 70, w / 2, col, 6, r=20); rect(c, L - 92, -w / 2 - 4, L - 56, w / 2 + 4, cuff, 5, r=8)
    circ(c, L - 10, 0, w * .48, skin, 6)
    for k in (-1, 0, 1): c.drawLine(L + 10, k * 20, L + 36, k * 22, ink(5))
    c.restore()

def _cash(c, s=1.0):
    for i in range(5): Wd.bill(c, (i % 2) * 5, -i * 9, 0, s)
def _paper(c, title, lines, w=520, h=380):
    rect(c, -w / 2, -h / 2, w / 2, h / 2, PAPER, 5); Wd.text(c, title.upper(), -w / 2 + 30, -h / 2 + 64, 48, NAVY, F_LABEL)
    c.drawRect(skia.Rect(-w / 2 + 30, -h / 2 + 84, w / 2 - 30, -h / 2 + 90), fp(NAVY))
    for i, ln in enumerate(lines): Wd.text(c, ln, -w / 2 + 30, -h / 2 + 150 + i * 52, 38, NAVY, F_TYPE)

def hand_slam(c, x, y, t, item='cash', title='', lines=(), hit=0.25, side='right', rot=-6, sleeve_col=NAVY2):
    """A hand slams cash / a paper / a sticky note onto the table at (x, y). Impact at t = hit. Returns shake."""
    k = min(max(t / hit, 0), 1); kk = k ** 2.2                 # accelerating drop
    lift = (1 - kk) * 260; sc = 1 + (1 - kk) * .35
    after = t - hit; bounce = (math.exp(-after * 9) * math.sin(after * 30) * 10) if after > 0 else 0
    sx0 = W + 120 if side == 'right' else -120; sy0 = H + 160
    c.save(); c.translate(x, y - lift + bounce); c.rotate(rot); c.scale(sc, sc)
    c.drawOval(skia.Rect(-280, -40 + lift * .8, 280, 60 + lift * .8), fp((0, 0, 0), int(70 * kk), blur=18))
    if item == 'cash': c.scale(3.0, 3.0); _cash(c)
    elif item == 'sticky': Wd.sticky(c, title, 0, 0, 1.0, rot=0, w=340)
    else: _paper(c, title, lines)
    c.restore()
    if after > 0:                                               # dust puffs
        for i in range(8):
            a = i / 8 * 2 * math.pi; r = 120 + after * 500; al = max(0, 1 - after * 3)
            c.drawCircle(x + math.cos(a) * r * 1.6, y + 60 + math.sin(a) * r * .35, 26 + after * 40, fp('#E9E0CC', int(110 * al), blur=8))
    if after < .6:                                              # the arm (leaves after the hit)
        out = ease(min(max((after - .25) / .35, 0), 1)) if after > 0 else 0
        hx, hy = x + 140, y - lift + 40 + out * 500
        sleeve(c, sx0, sy0, hx, hy, sleeve_col)
    return _shake(t, hit, 18)

def pyramid(c, cx, base_y, t, levels=5, labels=('EARLY INVESTORS', 'NEW MONEY'), wobble=0.0, step=.35):
    """Ponzi pyramid: rows of people build up from the top (early investors) to a wide base (new money);
    gold arrows show new money flowing up. wobble > 0 tilts it (about to fall)."""
    c.save(); c.translate(cx, base_y); c.rotate(math.sin(t * 3) * wobble * 4)
    rowh = 92
    for r in range(levels):
        k = ease_out(K(t, r * step, .3))
        if k <= 0: continue
        n = 1 + r * 2; y = -(levels - r) * rowh; wrow = n * 70
        for i in range(n):
            px = -wrow / 2 + 35 + i * 70; s = .9 * k
            c.save(); c.translate(px, y + 30); c.scale(s, s); circ(c, 0, -26, 18, '#E9C09A', 4); rect(c, -20, -8, 20, 34, GOLD if r == 0 else (NAVY3 if r < levels - 1 else GREY), 4, r=8); c.restore()
    if t > levels * step:
        for side in (-1, 1):
            p = skia.Path(); p.moveTo(side * levels * 70 * .55, -40); p.quadTo(side * levels * 70 * .7, -levels * rowh * .6, side * 60, -levels * rowh + 20)
            c.drawPath(p, ink(16, INK)); c.drawPath(p, ink(9, GOLD)); poly(c, [(side * 60 - 18, -levels * rowh + 46), (side * 60 + 18, -levels * rowh + 40), (side * 50, -levels * rowh + 6)], GOLD, 4)
    c.restore()
    if t > .2: Wd.pop_label(c, labels[0], cx, base_y - levels * rowh - 50, (t - .2) / .4, GOLD, 60, rot=0)
    if t > levels * step: Wd.pop_label(c, labels[1], cx, base_y + 70, (t - levels * step) / .4, WHITE, 60, rot=0)

def calendar(c, x, y, t, days_from=45, days_to=0, dur=2.0, label='DAYS LEFT', s=1.5):
    """Tear-off calendar: pages fly off while the number counts down."""
    k = min(max(t / dur, 0), 1); d = int(round(lerp(days_from, days_to, ease(k))))
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -180, -200, 180, 220, PAPER, 6, r=10); rect(c, -180, -200, 180, -110, ORANGE if d < 10 else NAVY, 6, r=10)
    Wd.text(c, label, 0, -140, 42, WHITE, F_LABEL, 'center'); Wd.text(c, str(d), 0, 130, 200, NAVY, F_TITLE, 'center')
    for i in range(2): circ(c, -90 + i * 180, -200, 14, GREY, 4)
    ph = (t * 6) % 1.0
    if 0 < k < 1 and ph > .08:                                   # a page flying away (after it has left the pad)
        c.save(); c.translate(ph * 520, -60 - ph * 380); c.rotate(ph * 60); rect(c, -150, -120, 150, 150, PAPER, 4); c.restore()
    c.restore()

FLAG_STYLE = 'true'   # 'true' = real flag colours (Italy has green: owner-approved exception) | 'brand' = navy/gold/white tint
def _flag_cols(style):
    if style == 'brand': return {'green': '#2B4A7A', 'red': GOLD, 'white': '#F6EFE2', 'blue': NAVY}
    return {'green': '#2E8B57', 'red': '#C8242C', 'white': '#F6EFE2', 'blue': '#1E3A78'}
def flag(c, kind, cx, cy, w, h, t=0.0, style=None):
    """Waving flag (Italy / USA) drawn as vertical strips with a sine wave."""
    col = _flag_cols(style or FLAG_STYLE); n = 36; sw = w / n
    for i in range(n):
        x0 = cx - w / 2 + i * sw; u = i / n; dy = math.sin(u * 6 + t * 4) * h * .04 * u; shade = 1 - .12 * (math.sin(u * 6 + t * 4) * .5 + .5) * u
        def P(hexc):
            r_, g_, b_ = (int(hexc[k:k + 2], 16) for k in (1, 3, 5)); return (r_ * shade, g_ * shade, b_ * shade)
        if kind == 'italy':
            cc = col['green'] if u < 1 / 3 else col['white'] if u < 2 / 3 else col['red']
            c.drawRect(skia.Rect(x0, cy - h / 2 + dy, x0 + sw + .8, cy + h / 2 + dy), fp(P(cc)))
        else:
            for k in range(13):
                y0 = cy - h / 2 + k * h / 13 + dy; cc = col['red'] if k % 2 == 0 else col['white']
                c.drawRect(skia.Rect(x0, y0, x0 + sw + .8, y0 + h / 13 + .8), fp(P(cc)))
            if u < .42:
                c.drawRect(skia.Rect(x0, cy - h / 2 + dy, x0 + sw + .8, cy - h / 2 + dy + h * 7 / 13), fp(P(col['blue'])))
    if kind == 'usa':
        for r_ in range(4):
            for k in range(5): c.drawCircle(cx - w / 2 + w * .05 + k * w * .075 + (r_ % 2) * w * .035, cy - h / 2 + h * .07 + r_ * h * .12, w * .012, fp(col['white']))

def map_route(c, t, dur=2.2, a=(470, 470), b=(1450, 520), label_a='EUROPE', label_b='UNITED STATES', icon='coupon', flag_a=None, flag_b=None):
    """Stylized map: two land circles (optionally showing a waving flag inside), a dotted route that draws itself,
    an icon travelling along it. flag_a / flag_b: 'italy' | 'usa' | None."""
    Wd.framed_bg(c)
    for (mx, my), w_, h_, fl in ((a, 420, 300, flag_a), (b, 520, 330, flag_b)):
        p = skia.Path(); p.addOval(skia.Rect(mx - w_ / 2, my - h_ / 2, mx + w_ / 2, my + h_ / 2))
        c.drawPath(p, fp('#2B3F70'))
        if fl:
            c.save(); c.clipPath(p, doAntiAlias=True); flag(c, fl, mx, my, w_ * 1.05, h_ * 1.05, t)
            c.drawPath(p, sp(Wd_radial(mx, my, max(w_, h_) * .6))); c.restore()
        c.drawPath(p, ink(8)); c.drawPath(p, ink(3, '#9DB0DA'))
    Wd.big_label(c, label_a, a[0], a[1] + 250, 1, WHITE, 80); Wd.big_label(c, label_b, b[0], b[1] + 270, 1, GOLD, 80)
    k = ease(min(max(t / dur, 0), 1)); n = 40
    pts = [(lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n) - math.sin(math.pi * i / n) * 260) for i in range(n + 1)]
    for i in range(int(n * k)):
        if i % 2 == 0: c.drawLine(*pts[i], *pts[i + 1], ink(10, GOLD))
    ix, iy = pts[int(n * k)]
    c.save(); c.translate(ix, iy); rect(c, -60, -40, 60, 40, PAPER, 4); Wd.text(c, 'IRC' if icon == 'coupon' else icon, 0, 14, 36, NAVY, F_LABEL, 'center'); c.restore()

def Wd_radial(x, y, r):
    """Soft inner shadow for the land circles (flags read as a round badge)."""
    from engine.kit import radial
    return radial(x, y, r, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(8, 14, 34, 150)], [0, .7, 1])

def handcuffs(c, x, y, t, close_at=.3):
    """Handcuffs swing in and snap shut at t = close_at. Returns shake."""
    k = ease_out(min(max(t / close_at, 0), 1)); gap = (1 - k) * 60
    c.save(); c.translate(x, y); c.rotate((1 - k) * -25)
    c.drawLine(-60, 0, 60, 0, ink(16, '#9AA3B5')); [circ(c, sx * 40, 0, 10, '#9AA3B5', 4) for sx in (-1, 1)]
    for sx in (-1, 1):
        p = skia.Path(); p.addArc(skia.Rect(sx * 150 - 80, -80, sx * 150 + 80, 80), 0, 360 - gap * 3); c.drawPath(p, ink(28, INK)); c.drawPath(p, ink(18, '#C9CFDB'))
    c.restore(); return _shake(t, close_at, 10, .2)

def newspaper(c, x, y, t, masthead, headline, sub=None, dur=.7):
    """Newspaper spins in and lands (classic film headline). Use the framed stage behind it."""
    k = ease_out(min(max(t / dur, 0), 1)); sc = lerp(.05, 1, k); rot = lerp(720, -3, k)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    rect(c, -560, -380, 560, 380, PAPER, 6); Wd.text(c, masthead.upper(), 0, -280, 90, NAVY, F_TITLE, 'center')
    c.drawRect(skia.Rect(-520, -250, 520, -244), fp(NAVY)); c.drawRect(skia.Rect(-520, -236, 520, -232), fp(NAVY))
    for i, ln in enumerate(Wd.wrap(headline.upper().split(), F_LABEL, 96, 1000)): Wd.text(c, ' '.join(ln), 0, -130 + i * 100, 96, NAVY, F_LABEL, 'center')
    if sub: Wd.text(c, sub, 0, 240, 40, NAVY, F_TYPE, 'center')
    for i in range(3): c.drawRect(skia.Rect(-520 + i * 360, 280, -200 + i * 360, 288), fp('#B8B0A0'))
    c.restore()

def phone_ring(c, x, y, t, s=1.0):
    """Old desk phone shaking with ring lines."""
    sh = math.sin(t * 60) * 6 * (int(t * 2) % 2 == 0)
    c.save(); c.translate(x + sh, y); c.scale(s, s)
    rect(c, -110, -10, 110, 80, '#2E2E38', 6, r=24); oval(c, -150, -80, 150, -10, '#2E2E38', 6); circ(c, 0, 35, 30, GREY, 4)
    if int(t * 2) % 2 == 0:
        for k_ in (1, 2): [c.drawArc(skia.Rect(-150 - k_ * 40, -150 - k_ * 30, 150 + k_ * 40, 60 + k_ * 30), a0, 30, False, ink(8, GOLD)) for a0 in (200, 310)]
    c.restore()

def ledger(c, x, y, t, rows, title='LEDGER', flip_every=.25, flips=4):
    """Open ledger: pages flip, then the rows write in (Special Elite)."""
    rect(c, x - 600, y - 340, x, y + 340, PAPER, 6); rect(c, x, y - 340, x + 600, y + 340, PAPER, 6); c.drawLine(x, y - 340, x, y + 340, ink(8))
    Wd.text(c, title.upper(), x + 60, y - 260, 54, NAVY, F_LABEL)
    for i, (a, b) in enumerate(rows):
        if t > flips * flip_every + i * .3:
            Wd.text(c, a, x + 60, y - 170 + i * 70, 40, NAVY, F_TYPE); Wd.text(c, b, x + 560, y - 170 + i * 70, 40, ORANGE if b.startswith('-') else NAVY, F_TYPE, 'right')
    if t < flips * flip_every:
        ph = (t / flip_every) % 1; wpg = 600 * math.cos(ph * math.pi)
        p = skia.Path(); p.addRect(skia.Rect(min(x, x + wpg), y - 330, max(x, x + wpg), y + 330)); shape(c, p, '#FBF8F0', 5)

def envelope(c, x, y, t, card_title='', card_lines=()):
    """Envelope: flap opens, a card slides up out of it."""
    rect(c, x - 320, y - 200, x + 320, y + 200, '#E9DFC8', 6)
    k = ease(min(max(t / .4, 0), 1)); fy = lerp(y, y - 330, k)
    if t > .4:
        u = ease_out(min((t - .4) / .5, 1)); c.save(); c.translate(x, y - 40 - u * 330); _paper(c, card_title, card_lines, w=520, h=360); c.restore()
    poly(c, [(x - 320, y - 200), (x + 320, y - 200), (x, fy)], '#DDD1B6', 6); poly(c, [(x - 320, y + 200), (x, y + 10), (x + 320, y + 200)], '#E2D7BE', 5)

def prison_bars(c, t, drop=.35):
    """Prison bars slam down over the frame. Returns shake."""
    k = ease_out(min(max(t / drop, 0), 1)); off = (1 - k) * -H
    for i in range(9): x = 120 + i * 210; rect(c, x - 18, off - 20, x + 18, off + H + 20, '#3A3F4A', 6, r=10)
    rect(c, -10, off + 140, W + 10, off + 180, '#3A3F4A', 6); return _shake(t, drop, 14, .25)

def outro(c, t, channel='DIRTY DOLLAR'):
    """Outro card after the final question: the channel name in the locked style (white + gold)."""
    Wd.framed_bg(c); k = .85 + .15 * pop(K(t, 0, .4))
    f = Wd._font(F_TITLE, 130); words = channel.split(' ', 1); w0 = f.measureText(words[0] + ' '); tw = f.measureText(channel)
    c.save(); c.translate(W / 2, H / 2); c.scale(k, k)
    Wd.text(c, words[0] + ' ', -tw / 2, 20, 130, WHITE, F_TITLE, stroke=14)
    if len(words) > 1: Wd.text(c, words[1], -tw / 2 + w0, 20, 130, GOLD, F_TITLE, stroke=14)
    c.restore()
    wl = 420 * ease_out(K(t, .2, .5)); c.drawRect(skia.Rect(W / 2 - wl, H / 2 + 70, W / 2 + wl, H / 2 + 80), fp(GOLD))

def end_screen(c, t):
    """End-screen layout (~15-20 s): two 'watch next' slots + a subscribe circle, placed where YouTube's end-screen
    elements go (the owner adds the real elements in YouTube Studio)."""
    Wd.framed_bg(c)
    Wd.text(c, 'WATCH NEXT', W / 2, 190, 70, GOLD, F_LABEL, 'center')
    for i, x0 in enumerate((180, 1000)):
        k = ease_out(K(t, .2 + i * .15, .4)); y0 = 300 + (1 - k) * 60
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x0 + 740, y0 + 416), 22, 22), ink(10, '#9DB0DA', int(255 * k)))
    k = pop(K(t, .6, .4))
    if k > 0: c.save(); c.translate(W / 2, 880); c.scale(k, k); circ(c, 0, 0, 90, None, 10, v='#9DB0DA'); c.restore()

def police_car(c, x, y, t, s=1.0, spot_target=None, siren=True):
    """1920s police car (boxy, running boards, roof spotlight). spot_target=(x, y): the roof spotlight sweeps onto
    that point (e.g. Ponzi at the arrest). Siren lamp blinks navy-blue / orange (no green)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for wx in (-200, 190): circ(c, wx, 0, 62, '#1E1F2A', 7); circ(c, wx, 0, 26, '#9AA3B5', 5)
    rect(c, -300, -120, 300, -10, '#1B1D26', 7, r=18); rect(c, -330, -30, 330, -6, '#2E2E38', 5, r=6)          # body + running board
    rect(c, -190, -270, 170, -118, '#1B1D26', 7, r=14); rect(c, -160, -245, -20, -140, '#9FB8F0', 5, r=6); rect(c, 10, -245, 140, -140, '#9FB8F0', 5, r=6)
    rect(c, 190, -100, 300, -40, '#1B1D26', 6, r=10); circ(c, 300, -70, 22, '#FFF6DC', 4)                     # bonnet + headlamp
    rect(c, -120, -110, 80, -60, '#E5E5E5', 4, r=6); Wd.text(c, 'POLICE', -20, -72, 38, NAVY, F_LABEL, 'center')
    rect(c, -40, -300, 20, -270, '#2E2E38', 5, r=6)                                                              # spotlight on the roof
    if siren:
        on = int(t * 4) % 2 == 0; col = '#6F8FE0' if on else ORANGE
        circ(c, 120, -282, 18, col, 4); c.drawCircle(120, -282, 70, fp(col, 90, blur=26))
    c.restore()
    if spot_target is not None:                                                                                 # sweeping beam
        sx, sy = x - 10 * s, y - 290 * s; k = ease(min(max(t / 1.2, 0), 1))
        tx = lerp(spot_target[0] + 600, spot_target[0], k); ty = spot_target[1]
        p = skia.Path(); ang = math.atan2(ty - sy, tx - sx); L = math.hypot(tx - sx, ty - sy); wid = 150
        p.moveTo(sx, sy); p.lineTo(tx + math.cos(ang + math.pi / 2) * wid, ty + math.sin(ang + math.pi / 2) * wid)
        p.lineTo(tx - math.cos(ang + math.pi / 2) * wid, ty - math.sin(ang + math.pi / 2) * wid); p.close()
        c.drawPath(p, fp('#FFF2C8', 70, blur=18, blend=skia.BlendMode.kPlus)); c.drawCircle(tx, ty, wid * 1.1, fp('#FFF2C8', 80, blur=30, blend=skia.BlendMode.kPlus))

def phone_screen(c, x, y, t, messages, s=1.0, every=.7, title='Investments'):
    """Big modern phone with chat bubbles popping in one by one (navy / gold bubbles - never green).
    messages: list of (text, side) with side 'in' (left, navy) or 'out' (right, gold)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-250, -470, 270, 490), 60, 60), fp((0, 0, 0), 90, blur=20))
    rect(c, -260, -480, 260, 480, '#1B1D26', 8, r=56); rect(c, -232, -420, 232, 420, '#EEF1F7', 4, r=20)
    rect(c, -232, -420, 232, -330, NAVY, 0, r=20); Wd.text(c, title.upper(), 0, -362, 40, WHITE, F_LABEL, 'center'); rect(c, -60, -455, 60, -440, '#2E2E38', 0, r=6)
    y0 = -290
    for i, (msg, side) in enumerate(messages):
        k = pop(K(t, .2 + i * every, .3))
        if k <= 0: break
        lines = Wd.wrap(msg.split(), F_LABEL2, 40, 300); hgt = 30 + 46 * len(lines); wdt = max(Wd._font(F_LABEL2, 40).measureText(' '.join(l)) for l in lines) + 44
        bx = -210 if side == 'in' else 210 - wdt; col = NAVY3 if side == 'in' else GOLD; tc = WHITE if side == 'in' else NAVY
        c.save(); c.translate(bx + (0 if side == 'in' else wdt), y0); c.scale(k, k); c.translate(-(0 if side == 'in' else wdt), 0)
        rect(c, 0, 0, wdt, hgt, col, 4, r=22)
        for j, l in enumerate(lines): Wd.text(c, ' '.join(l), 22, 50 + j * 46, 40, tc, F_LABEL2)
        c.restore(); y0 += hgt + 26
    c.restore()

def coin_rain(c, t, n=26, area=(300, -100, 1620, 1100), seed=5):
    """Gold coins tumbling down (money disappearing)."""
    r = random.Random(seed)
    for _ in range(n):
        x0, sp, ph = r.uniform(area[0], area[2]), r.uniform(300, 600), r.uniform(0, 3)
        y = area[1] + ((t + ph) * sp) % (area[3] - area[1]); x = x0 + math.sin((t + ph) * 3) * 30
        c.save(); c.translate(x, y); c.scale(abs(math.cos((t + ph) * 4)) * .8 + .2, 1); Wd.coin(c, 0, 0, 34); c.restore()

# ---------------- crowd queue + held props (from the Ponzi video, now in the library)
QUEUE_CAST = ['worker', 'saver', 'retiree', 'grad', 'reporter', 'agent', 'banker', 'analyst', 'saver', 'worker', 'retiree', 'grad', 'agent', 'reporter']
def queue(phones=False, worried=False, n=14, x0=930, step=62, s=.36, y=864, cast=None, rim='#9FB8F0', hats=('worker',)):
    """A line of people waiting at a door (e.g. Ponzi's office on night/street1920: door x 1020, so x0=930).
    The front person stands at x0, the rest step back to the left by `step`. phones/every 3rd person hold something
    (draw it with held()); worried=True gives wide eyes, open mouths and sweat drops. Returns the actors for wide(back=...)."""
    from engine.actor import Actor
    cast = cast or QUEUE_CAST; acts = []
    for i in range(n):
        k = cast[i % len(cast)]; a = Actor(k, x0 - i * step, y + (i % 2) * 4, s, face=.7, light=-1, rim=rim, hat=(k in hats))
        a.pose(0, ('down', 'hold') if (phones or i % 3 == 0) else ('pocket', 'down'))
        if worried: a.expression(0, eyes='wide', mouth='o', brow=.7, sweat=0 if i % 2 else -1)
        acts.append(a)
    return acts

def held(c, acts, what='cash', t=0):
    """Draw the prop in every 'hold' hand of these actors: what='cash' (a bill) or 'phone' (a glowing phone).
    Use as the shot overlay: overlay=lambda c, t: held(c, q, 'cash', t)."""
    from engine import kit
    for a in acts:
        if a._arms(t)[1] != 'hold': continue
        hx, hy = kit.hand_pos(a.x, a.y, a.s, ('down', 'hold'), 1)
        if what == 'cash': Wd.bill(c, hx + 4, hy - 4, -10, .32)
        else:
            c.drawCircle(hx, hy - 10, 30, fp(GOLD, 70, blur=12)); rect(c, hx - 11, hy - 30, hx + 11, hy + 6, '#1B2A52', 3, r=4); c.drawRect(skia.Rect(hx - 8, hy - 27, hx + 8, hy + 2), fp('#FFE2A0'))

_SHAKE_CANVAS = None
def stamp_shake(hit):
    """Camera shake for a stamp hit at `hit` seconds into the shot (same shake as widgets.stamp).
    Use: render_shot(..., shake=stamp_shake(1.0), sfx=[(1.0, 'stamp')])."""
    global _SHAKE_CANVAS
    if _SHAKE_CANVAS is None: _SHAKE_CANVAS = skia.Surface(4, 4)
    return lambda t: Wd.stamp(_SHAKE_CANVAS.getCanvas(), 'x', 0, 0, t - hit)
