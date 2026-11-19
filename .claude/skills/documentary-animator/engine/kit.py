import math, random, os
import numpy as np, skia, soundfile as sf

W, H, FPS = 1920, 1080, 30
from engine.core import FONT_DIR as FD
FONT_HAND = skia.Typeface.MakeFromFile(FD + "CaveatBrush-Regular.ttf")
KALAM = skia.Typeface.MakeFromFile(FD + "Kalam-Bold.ttf")
MARKER = skia.Typeface.MakeFromFile(FD + "PermanentMarker-Regular.ttf")
INK = (24, 22, 27); LW = 6.0
GOLD = '#F2C14E'; RED = '#C8242C'; LIME = '#B8F04A'; CREAM = '#FFF6DC'

def C(rgb, a=255): return skia.Color(int(rgb[0]), int(rgb[1]), int(rgb[2]), int(a))
def hx(h, a=255):
    h = h.lstrip('#'); return C((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)), a)
def col(v, a=255): return hx(v, a) if isinstance(v, str) else C(v, a)
def radial(cx, cy, r, colors, pos=None): return skia.GradientShader.MakeRadial(center=(cx, cy), radius=r, colors=colors, positions=pos)
def linear(x0, y0, x1, y1, colors, pos=None): return skia.GradientShader.MakeLinear(points=[(x0, y0), (x1, y1)], colors=colors, positions=pos)
def ease(u): u = min(max(u, 0), 1); return 0.5 - 0.5 * math.cos(math.pi * u)
def ease_out(u): u = min(max(u, 0), 1); return 1 - (1 - u) ** 3
def pop(u):  # 0 -> 1.15 -> 1
    if u <= 0: return 0.0
    if u >= 1: return 1.0
    return 1.15 * ease_out(u / 0.6) if u < 0.6 else 1.15 - 0.15 * ease((u - 0.6) / 0.4)
def back(u, k=1.9):  # snappy overshoot for pose changes
    u = min(max(u, 0.0), 1.0) - 1; return 1 + (k + 1) * u ** 3 + k * u ** 2
def lerp(a, b, k): return a + (b - a) * k
def K(t, t0, d): return min(max((t - t0) / d, 0.0), 1.0)
def blink(t, period=2.7, phase=0.0): return ((t + phase) % period) < 0.1

def mouth_track(wav, hold=3):  # per-frame 'open'/'mid'/'closed' from loudness, held 3 frames
    s, sr = sf.read(wav); s = s.mean(1) if s.ndim > 1 else s
    hop = sr // FPS; n = len(s) // hop + 1
    rms = np.array([np.sqrt(np.mean(s[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    m = rms.max(); out = []; cur = 'closed'; held = hold
    for v in rms:
        tgt = 'open' if v > .45 * m else 'mid' if v > .14 * m else 'closed'
        if tgt != cur and held >= hold: cur = tgt; held = 0
        held += 1; out.append(cur)
    out[-1] = 'closed'; return out

def fp(v, a=255, blur=0, blend=None):
    p = skia.Paint(AntiAlias=True, Color=col(v, a))
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if blend: p.setBlendMode(blend)
    return p
def sp(shader, blend=None, blur=0):
    p = skia.Paint(AntiAlias=True); p.setShader(shader)
    if blend: p.setBlendMode(blend)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p
def ink(w=LW, v=INK, a=255):
    p = skia.Paint(AntiAlias=True, Color=col(v, a)); p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w)
    p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join); return p
def shape(c, path, fill, w=LW, v=INK):
    if fill is not None: c.drawPath(path, fill if isinstance(fill, skia.Paint) else fp(fill))   # fill=None -> outline only
    if w: c.drawPath(path, ink(w, v))
def rect(c, x0, y0, x1, y1, fill, w=LW, r=0, v=INK):
    p = skia.Path()
    if r: p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r))
    else: p.addRect(skia.Rect(x0, y0, x1, y1))
    shape(c, p, fill, w, v); return p
def circ(c, x, y, r, fill, w=LW, v=INK): p = skia.Path(); p.addCircle(x, y, r); shape(c, p, fill, w, v); return p
def oval(c, x0, y0, x1, y1, fill, w=LW, v=INK): p = skia.Path(); p.addOval(skia.Rect(x0, y0, x1, y1)); shape(c, p, fill, w, v); return p
def line(c, x0, y0, x1, y1, w=LW, v=INK, a=255): c.drawLine(x0, y0, x1, y1, ink(w, v, a))
def poly(c, pts, fill, w=LW, v=INK):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); shape(c, p, fill, w, v); return p
def text_w(s, size, font=None): return skia.Font(font or KALAM, size).measureText(s)
def label(c, s, x, y, size, color, font=None, align='left', stroke=0, stroke_col=INK, skew=-0.16, alpha=1.0, rot=0.0):
    f = skia.Font(font or KALAM, size); w = f.measureText(s)
    ox = -w / 2 if align == 'center' else -w if align == 'right' else 0
    c.save(); c.translate(x, y); c.rotate(rot); c.skew(skew, 0)
    if stroke: c.drawString(s, ox, 0, f, ink(stroke, stroke_col, 255 * alpha))
    c.drawString(s, ox, 0, f, fp(color, 255 * alpha)); c.restore(); return w

# ---------------- lighting
def night(c, lights, ambient='#4C5CA0'):
    """Multiply navy darkness over everything drawn so far, with soft holes for lights.
    lights: ('pool',x,y,r,a) | ('oval',x,y,rx,ry,a) | ('path',skia.Path,a,blur)"""
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kMultiply); c.saveLayer(None, p); c.drawPaint(fp(ambient))
    for L in lights:
        if L[0] == 'pool':
            _, x, y, r, a = L
            c.drawCircle(x, y, r, sp(radial(x, y, r, [C((0,0,0), 255*a), C((0,0,0), 255*a*.75), C((0,0,0), 0)], [0, .5, 1]), blend=skia.BlendMode.kDstOut))
        elif L[0] == 'oval':
            _, x, y, rx, ry, a = L; c.save(); c.translate(x, y); c.scale(1, ry / rx)
            c.drawCircle(0, 0, rx, sp(radial(0, 0, rx, [C((0,0,0), 255*a), C((0,0,0), 255*a*.7), C((0,0,0), 0)], [0, .55, 1]), blend=skia.BlendMode.kDstOut)); c.restore()
        else:
            _, path, a, blur = L; c.drawPath(path, fp((0, 0, 0), 255 * a, blur=blur, blend=skia.BlendMode.kDstOut))
    c.restore()
def add_light(c, x, y, r, v, a):
    c.drawCircle(x, y, r, sp(radial(x, y, r, [col(v, a), col(v, a * .4), col(v, 0)], [0, .5, 1]), blend=skia.BlendMode.kPlus))
def cone_path(x, y, top_w, bot_w, length, lean=0):
    p = skia.Path(); p.moveTo(x - top_w/2, y); p.lineTo(x + top_w/2, y); p.lineTo(x + lean + bot_w/2, y + length); p.lineTo(x + lean - bot_w/2, y + length); p.close(); return p
def blur_begin(c, sigma):  # depth blur for everything until c.restore()
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(sigma, sigma)); c.saveLayer(None, p)
def vignette(c, strength=0.64, inner=.42):
    c.drawRect(skia.Rect(0, 0, W, H), sp(radial(W/2, H/2, W*.74, [C((0,0,0), 0), C((0,0,0), 0), C((2,3,12), 255*strength)], [0, inner, 1])))
def _sat(s, contrast, lift):
    lr, lg, lb = 0.2126, 0.7152, 0.0722
    m = [lr*(1-s)+s, lg*(1-s), lb*(1-s), lr*(1-s), lg*(1-s)+s, lb*(1-s), lr*(1-s), lg*(1-s), lb*(1-s)+s]
    out = []
    for r in range(3): out += [m[r*3+i] * contrast for i in range(3)] + [0, lift]
    return out + [0, 0, 0, 1, 0]
GRADE_CF = skia.ColorFilters.Matrix(_sat(0.94, 0.97, 0.012))
THRESH_CF = skia.ColorFilters.Matrix([1.7,0,0,0,-0.78, 0,1.7,0,0,-0.78, 0,0,1.7,0,-0.78, 0,0,0,1,0])
def finish(surf, bloom=0.40, sigma=20):  # grade + bloom; call after drawing a frame
    c = surf.getCanvas(); img = surf.makeImageSnapshot(); c.clear(C((0, 0, 0)))
    p = skia.Paint(); p.setColorFilter(GRADE_CF); c.drawImage(img, 0, 0, skia.SamplingOptions(), p)
    b = skia.Paint(); b.setImageFilter(skia.ImageFilters.Blur(sigma, sigma, skia.TileMode.kClamp, skia.ImageFilters.ColorFilter(THRESH_CF)))
    b.setBlendMode(skia.BlendMode.kScreen); b.setAlphaf(bloom); c.drawImage(img, 0, 0, skia.SamplingOptions(), b)

# ---------------- puppet character
def head_rrect(cx, cy, R):
    """slightly rectangular head: soft top corners, a much rounder chin"""
    rr = skia.RRect(); top, chin = R * .42, R * .86
    rr.setRectRadii(skia.Rect(cx - R * .96, cy - R, cx + R * .96, cy + R),
                    [skia.Point(top, top), skia.Point(top, top), skia.Point(R * .88, chin), skia.Point(R * .88, chin)])
    return rr
BODY_TOP, BODY_BOT, HEAD_R = -345, -128, 100
HEAD_CY = BODY_TOP - 116
SHOULDER = (-56, BODY_TOP + 54)
ARM = {  # left arm: (elbow, hand, show_hand); right arm is mirrored
    'down': ((-90, -235), (-96, -168), True), 'pocket': ((-96, -232), (-70, -176), False),
    'hip': ((-128, -238), (-84, -190), True), 'present': ((-128, -306), (-208, -338), True),
    'gesture': ((-136, -262), (-152, -352), True), 'chin': ((-128, -262), (-62, -322), True),
    'hat': ((-140, -400), (-104, -482), True), 'hold': ((-96, -236), (-44, -214), True),
    'push': ((-120, -270), (-190, -262), True),
    # added for the documentary animator
    'point': ((-150, -300), (-250, -318), True),   # arm straight out, pointing
    'phone': ((-128, -300), (-96, -452), True),    # hand at the ear
    'facepalm': ((-118, -310), (-22, -440), True), # hand over the face
    'cheer': ((-134, -420), (-120, -548), True),   # arm up
    'shrug': ((-134, -258), (-178, -316), True),   # palm out at the side
    'cross': ((-112, -246), (40, -262), True),     # arm across the chest
    'wave': ((-150, -380), (-176, -470), True),    # hand up by the head
    'count': ((-126, -300), (-120, -372), True)}   # hand raised in front (counting / listing)
FRONT_POSES = ('facepalm', 'phone')
HAIR_STYLES = ('bald', 'slick', 'silver', 'bob', 'curly', 'buzz', 'bun', 'long', None)
OUTFITS = ('suit', 'open', 'sweater', 'hoodie')   # suit = jacket+tie (locked default); open = jacket, open collar, no tie

def _arm(spec):  # 'name' or ('from', 'to', k) blended with overshoot
    if isinstance(spec, str): return ARM[spec]
    a, b, k = spec; k = back(k, 1.6); ea, ha, sa = ARM[a]; eb, hb, sb = ARM[b]
    return (lerp(ea[0], eb[0], k), lerp(ea[1], eb[1], k)), (lerp(ha[0], hb[0], k), lerp(ha[1], hb[1], k)), (sb if k > .5 else sa)

def KALAM_DOLLAR():
    from engine.core import F_TITLE
    return F_TITLE

def draw_char(c, x, y, s, spec, face=0.0, eyes='dot', mouth='smile', brow=0.0, brow_tilt=0.0, arms=('down', 'down'),
              tilt=0.0, bob=0.0, squash=0.0, sweat=-1.0, light=-1, rim=None, hat=False, legs=None, pupil=0.0, sparkle=0.0):
    """x,y = feet. s=1 -> head radius 100 px (s=1 wide shot, s~2.15 close-up with feet at y~1390).
    face -1..1 = 3/4 turn. light -1 = key from left. eyes: dot/half/wide/closed. mouth: smile/smirk/flat/o/mid/open."""
    lw = max(5.2, 4.0 / s); R = HEAD_R
    c.save(); c.translate(x, y); c.scale(s, s)
    pants = spec.get('pants', spec['suit_d'])
    for (hx0, fx, lift) in (legs or ((-26, 0, 0), (26, 0, 0))):
        x0, y0, x1, y1 = hx0, BODY_BOT - 14, hx0 + fx, -lift - 16
        lp = skia.Path(); lp.moveTo(x0 - 21, y0); lp.lineTo(x0 + 21, y0); lp.lineTo(x1 + 18, y1); lp.lineTo(x1 - 18, y1); lp.close()
        shape(c, lp, pants, lw)
        side = -1 if hx0 < 0 else 1
        sh = skia.Path(); sh.addRRect(skia.RRect.MakeRectXY(skia.Rect(x1 - 22 + side * 8, y1 - 4, x1 + 22 + side * 8, y1 + 16), 9, 9)); shape(c, sh, spec.get('shoes', '#23201E'), lw)
    c.translate(0, -bob); c.scale(1 + squash * .6, 1 - squash)
    if spec.get('hair') in ('bob', 'long'):   # back of the hair sits behind the neck and body
        c.save(); c.translate(0, HEAD_CY); c.rotate(tilt); bk = skia.Path(); bot = 96 if spec['hair'] == 'bob' else 190
        bk.addRRect(skia.RRect.MakeRectXY(skia.Rect(-R - 16, -R - 6, R + 16, bot), 44, 44)); shape(c, bk, spec.get('hair_col', '#1C1B22'), lw); c.restore()
    nk = skia.Path(); nk.addRRect(skia.RRect.MakeRectXY(skia.Rect(-22, HEAD_CY + 70, 22, BODY_TOP + 16), 8, 8)); shape(c, nk, spec['skin_d'], lw)
    body = skia.Path(); body.addRRect(skia.RRect.MakeRectXY(skia.Rect(-86, BODY_TOP, 86, BODY_BOT), 22, 22))
    c.drawPath(body, fp(spec['suit'])); c.save(); c.clipPath(body, doAntiAlias=True)
    if spec.get('gloss', True): c.drawRect(skia.Rect(-74, BODY_TOP + 10, -50, BODY_BOT - 14), fp((255, 255, 255), 55, blur=8))
    sh = skia.Path(body); sh.offset(light * 16, -5); c.drawPath(skia.Op(body, sh, skia.PathOp.kDifference_PathOp), fp(spec['suit_d']))
    outfit = spec.get('outfit', 'suit')
    if outfit in ('sweater', 'hoodie'):
        if outfit == 'hoodie':
            hd = skia.Path(); hd.addRRect(skia.RRect.MakeRectXY(skia.Rect(-64, BODY_TOP - 12, 64, BODY_TOP + 34), 20, 20)); shape(c, hd, spec['suit_d'], lw * .7)
            for sx in (-1, 1): c.drawLine(sx * 16, BODY_TOP + 20, sx * 18, BODY_TOP + 92, ink(lw * .55)); circ(c, sx * 18, BODY_TOP + 96, 4, spec.get('shirt', '#F4EFE2'), lw * .45)
            pk = skia.Path(); pk.addRRect(skia.RRect.MakeRectXY(skia.Rect(-52, BODY_BOT - 74, 52, BODY_BOT - 26), 12, 12)); c.drawPath(pk, ink(lw * .6))
        else:
            nk2 = skia.Path(); nk2.addArc(skia.Rect(-38, BODY_TOP - 26, 38, BODY_TOP + 24), 20, 140); c.drawPath(nk2, ink(lw * .7))
            if spec.get('shirt'): cl = skia.Path(); cl.moveTo(-24, BODY_TOP + 2); cl.lineTo(0, BODY_TOP + 22); cl.lineTo(24, BODY_TOP + 2); c.drawPath(cl, ink(lw * .5))
            for yy in (BODY_BOT - 22,): c.drawLine(-80, yy, 80, yy, ink(lw * .5))
        c.restore(); c.drawPath(body, ink(lw))
    else:
     if spec.get('wing_collar'):
        for sx in (-1, 1): poly(c, [(sx * 4, BODY_TOP - 10), (sx * 30, BODY_TOP - 14), (sx * 22, BODY_TOP + 10)], '#FFFFFF', lw * .55)
     v = skia.Path(); v.moveTo(-34, BODY_TOP - 4); v.lineTo(0, BODY_TOP + 96 if outfit == 'suit' else BODY_TOP + 64); v.lineTo(34, BODY_TOP - 4); v.close(); c.drawPath(v, fp(spec['shirt']))
     if outfit == 'open' or spec.get('tie') is None:
        for sx in (-1, 1): poly(c, [(sx * 4, BODY_TOP + 2), (sx * 34, BODY_TOP - 4), (sx * 26, BODY_TOP + 22)], spec['shirt'], lw * .6)
     elif spec.get('bowtie'):
        by = BODY_TOP + 40; bt = skia.Path(); bt.moveTo(0, by); bt.lineTo(-24, by - 14); bt.lineTo(-24, by + 14); bt.close()
        bt.moveTo(0, by); bt.lineTo(24, by - 14); bt.lineTo(24, by + 14); bt.close(); shape(c, bt, spec['tie'], lw * .75); circ(c, 0, by, 5, spec['tie'], lw * .7)
     else:
        poly(c, [(-9, BODY_TOP + 24), (9, BODY_TOP + 24), (13, BODY_TOP + 82), (0, BODY_TOP + 98), (-13, BODY_TOP + 82)], spec['tie'], lw * .75)
     for sx in (-1, 1):
        lp = skia.Path(); lp.moveTo(sx * 36, BODY_TOP - 2); lp.lineTo(sx * 2, BODY_TOP + 98); lp.lineTo(sx * 2, BODY_BOT); c.drawPath(lp, ink(lw * .75))
        c.drawLine(sx * 22, BODY_TOP + 58, sx * 40, BODY_TOP + 44, ink(lw * .6))
     if spec.get('hanky'): poly(c, [(30, BODY_TOP+96), (52, BODY_TOP+92), (48, BODY_TOP+76), (40, BODY_TOP+86), (33, BODY_TOP+76)], spec['hanky'], lw * .55)
     c.restore(); c.drawPath(body, ink(lw))
    def _draw_arm(side, a):
        e, h, show = _arm(a); m = 1 if side < 0 else -1
        sx, sy = SHOULDER[0] * m, SHOULDER[1]; ex, ey, hx_, hy_ = e[0] * m, e[1], h[0] * m, h[1]
        ap = skia.Path(); ap.moveTo(sx, sy); ap.quadTo(1.35*ex - .175*(sx+hx_), 1.35*ey - .175*(sy+hy_), hx_, hy_); c.drawPath(ap, ink(lw))
        if show: circ(c, hx_, hy_, 13, spec['skin'], lw * .8)
    front = [(sd, a) for sd, a in ((-1, arms[0]), (1, arms[1])) if (a if isinstance(a, str) else a[1]) in FRONT_POSES]
    for side, a in ((-1, arms[0]), (1, arms[1])):
        if (side, a) not in front: _draw_arm(side, a)
    c.save(); c.translate(0, HEAD_CY); c.rotate(tilt)
    fw, fh = spec.get('face_shape', (1.0, 1.0)); c.scale(fw, fh)   # real people: face cut (wide / long / narrow), e.g. (1.08, .94)
    head = skia.Path(); head.addRRect(head_rrect(0, 0, R)); hair = spec.get('hair')
    if hair == 'bald':
        for sx in (-1, 1):
            tf = skia.Path(); tf.moveTo(sx * 84, -44)
            for (px, py) in ((112, -34), (98, -18), (118, -4), (100, 10), (112, 26), (86, 34)): tf.lineTo(sx * px, py)
            tf.close(); shape(c, tf, spec.get('hair_col', '#8A8A92'), lw * .8)
    hcol = spec.get('hair_col', '#1C1B22')
    if hair == 'bun': circ(c, 0, -R - 22, 40, hcol, lw)
    if hair == 'curly':
        cp = skia.Path()
        for i in range(11):
            a = math.pi * (1.05 + i * 0.09); cp.addCircle(math.cos(a) * (R + 4), math.sin(a) * (R - 6) - 10, 30)
        shape(c, cp, hcol, lw)
    c.drawPath(head, fp(spec['skin'])); c.save(); c.clipPath(head, doAntiAlias=True)
    lit = skia.Path(head); lit.offset(light * 7, -17); c.drawPath(skia.Op(head, lit, skia.PathOp.kDifference_PathOp), fp(spec['skin_d']))
    if rim: rm = skia.Path(head); rm.offset(-light * 11, 4); c.drawPath(skia.Op(head, rm, skia.PathOp.kDifference_PathOp), fp(rim, 215))
    if spec.get('gloss', True):
        c.drawOval(skia.Rect(-72, -86, -8, -48), fp((255, 255, 255), 95, blur=7)); c.drawOval(skia.Rect(-60, -80, -34, -64), fp((255, 255, 255), 150, blur=3))
    c.restore()
    if hair == 'silver':
        fs = face * 10; hc = spec.get('hair_col', '#E9E9EE'); c.save(); c.clipPath(head, doAntiAlias=True)
        hp = skia.Path(); hp.moveTo(-R - 10, -R - 10); hp.lineTo(R + 10, -R - 10); hp.lineTo(R + 10, -34)
        hp.cubicTo(R - 14, -60, 62 + fs, -88, 30 + fs, -80)      # sweep from the right
        hp.lineTo(18 + fs, -66)                                   # the side part
        hp.cubicTo(-10 + fs, -84, -60, -84, -R - 10, -40); hp.close()
        c.drawPath(hp, fp(hc)); c.drawPath(hp, ink(lw))
        for sx in (-1, 1):                                        # silver temples over the ears
            tp = skia.Path(); tp.moveTo(sx * (R + 10), -44); tp.lineTo(sx * 80, -40); tp.lineTo(sx * 74, -10); tp.lineTo(sx * 84, 8); tp.lineTo(sx * (R + 10), 12); tp.close()
            c.drawPath(tp, fp(hc)); c.drawPath(tp, ink(lw * .8))
        st = skia.Path(); st.moveTo(26 + fs, -86); st.cubicTo(50 + fs, -92, 70 + fs, -84, 82, -66); c.drawPath(st, ink(lw * .55, (150, 150, 160)))   # comb lines
        st2 = skia.Path(); st2.moveTo(-20 + fs, -86); st2.cubicTo(-46, -88, -70, -78, -84, -60); c.drawPath(st2, ink(lw * .55, (150, 150, 160)))
        c.restore()
    if hair == 'slick':
        fs = face * 14; c.save(); c.clipPath(head, doAntiAlias=True)
        hp = skia.Path(); hp.moveTo(-R - 10, -R - 10); hp.lineTo(R + 10, -R - 10); hp.lineTo(R + 10, -6)
        hp.cubicTo(R - 20, -46, 56 + fs, -64, 6 + fs, -54); hp.cubicTo(-34 + fs, -50, -72, -40, -R - 10, -2); hp.close()
        c.drawPath(hp, fp(spec.get('hair_col', '#1C1B22'))); c.drawPath(hp, ink(lw))
        if spec.get('hair_part'):   # crisp side parting + comb lines (slicked-back 1920s look)
            for k_ in (0, 1, 2):   # glossy comb lines sweeping back from a left parting
                cl = skia.Path(); cl.moveTo(-40 + fs + k_ * 26, -62 + k_ * 2); cl.quadTo(-10 + fs + k_ * 26, -92, 30 + k_ * 24, -96); c.drawPath(cl, ink(lw * .45, (110, 110, 130)))
        c.restore()
        shn = skia.Path(); shn.moveTo(-50 if light < 0 else 20, -82); shn.lineTo(-14 if light < 0 else 56, -88); c.drawPath(shn, ink(lw * 1.3, (92, 96, 122)))
    if hair in ('bob', 'long'):   # bangs / side-swept fringe
        c.save(); c.clipPath(head, doAntiAlias=True); b = skia.Path()
        if hair == 'bob':
            b.moveTo(-R - 10, -18); b.lineTo(-R - 10, -R - 10); b.lineTo(R + 10, -R - 10); b.lineTo(R + 10, -18)
            for i in range(6): b.lineTo(R + 10 - (i + 0.5) * 36.6, -(44 if i % 2 else 30))
        else:
            fs = face * 12; b.moveTo(-R - 10, -R - 10); b.lineTo(R + 10, -R - 10); b.lineTo(R + 10, 10)
            b.cubicTo(R - 10, -40, 40 + fs, -60, -10 + fs, -66); b.cubicTo(-50, -64, -80, -30, -R - 10, 20)
        b.close(); c.drawPath(b, fp(hcol)); c.drawPath(b, ink(lw * .9)); c.restore()
    if hair in ('bun', 'curly', 'buzz'):
        c.save(); c.clipPath(head, doAntiAlias=True); cap = skia.Path()
        top = {'bun': -52, 'curly': -40, 'buzz': -64}[hair]
        cap.moveTo(-R - 10, -R - 10); cap.lineTo(R + 10, -R - 10); cap.lineTo(R + 10, top + 30); cap.cubicTo(R - 20, top, -R + 20, top, -R - 10, top + 30); cap.close()
        c.drawPath(cap, fp(hcol)); c.drawPath(cap, ink(lw * (0.7 if hair == 'buzz' else 0.9))); c.restore()
    c.drawPath(head, ink(lw))
    if hat and spec.get('hat_style') == 'boater':   # flat straw boater (1920s)
        oval(c, -R - 38, -70, R + 38, -44, spec.get('hat_col', '#E8C77A'), lw)
        cr = skia.Path(); cr.addRRect(skia.RRect.MakeRectXY(skia.Rect(-R + 8, -R - 18, R - 8, -54), 8, 8)); shape(c, cr, spec.get('hat_col', '#E8C77A'), lw)
        c.save(); c.clipPath(cr, doAntiAlias=True); c.drawRect(skia.Rect(-R, -82, R, -60), fp(spec.get('hat_band', '#14213D'))); c.restore(); c.drawPath(cr, ink(lw))
        for k in range(-3, 4): c.drawLine(k * 22, -R - 14, k * 22 + 4, -84, ink(lw * .3, (180, 140, 70)))
    elif hat:
        crown = skia.Path(); crown.moveTo(-R + 6, -56); crown.cubicTo(-R - 2, -R - 82, R + 2, -R - 82, R - 6, -56); crown.close()
        shape(c, crown, spec.get('hat_col', '#2E2E38'), lw); c.save(); c.clipPath(crown, doAntiAlias=True)
        c.drawRect(skia.Rect(-R, -86, R, -56), fp(spec.get('hat_band', '#7E1C24'))); c.drawLine(-R, -86, R, -86, ink(lw * .7)); c.restore()
        c.drawPath(crown, ink(lw)); oval(c, -R - 40, -70, R + 40, -40, spec.get('hat_col', '#2E2E38'), lw)
    fx = face * 40; eyy = -6
    for ex0 in (-30, 30):
        ex = ex0 + fx; far = (face > 0 and ex0 > 0) or (face < 0 and ex0 < 0); sq = 1 - .3 * abs(face) if far else 1.0
        if eyes == 'dollar':   # money-crazy: big white eyes with a gold $ instead of the pupil
            oval(c, ex - 26*sq, eyy - 26, ex + 26*sq, eyy + 26, '#FBFBF7', lw * .7)
            fd = skia.Font(KALAM_DOLLAR(), 48); dw = fd.measureText('$')
            c.save(); c.translate(ex, eyy); c.scale(sq, 1)
            c.drawString('$', -dw / 2, 17, fd, ink(lw * .9)); c.drawString('$', -dw / 2, 17, fd, fp('#FCA311')); c.restore()
        elif eyes == 'wide':
            oval(c, ex - 17*sq, eyy - 17, ex + 17*sq, eyy + 17, '#FBFBF7', lw * .7)
            c.drawOval(skia.Rect(ex - 5.5*sq + pupil*6, eyy - 5.5, ex + 5.5*sq + pupil*6, eyy + 5.5), fp(INK))
        elif eyes == 'closed':
            e = skia.Path(); e.moveTo(ex - 11*sq, eyy); e.quadTo(ex, eyy + 9, ex + 11*sq, eyy); c.drawPath(e, ink(lw * .8))
        elif eyes == 'half':
            c.save(); c.clipRect(skia.Rect(ex - 20, eyy - 3, ex + 20, eyy + 22)); oval(c, ex - 14*sq, eyy - 14, ex + 14*sq, eyy + 14, '#FBFBF7', lw * .65)
            c.drawOval(skia.Rect(ex - 6.5*sq, eyy - 4, ex + 6.5*sq, eyy + 10), fp(INK)); c.restore()
            c.drawLine(ex - 13*sq, eyy - 4, ex + 13*sq, eyy - 4, ink(lw * .8))
        else:
            oval(c, ex - 14*sq, eyy - 16, ex + 14*sq, eyy + 16, '#FBFBF7', lw * .65)
            px = ex + pupil * 5 + (face * 3)
            c.drawOval(skia.Rect(px - 7*sq, eyy - 6, px + 7*sq, eyy + 9), fp(INK)); c.drawCircle(px + 2.5, eyy - 1, 2.6, fp((255, 255, 255), 235))
        inner = 1 if ex0 < 0 else -1; by = eyy - 29 - brow * 9
        c.drawLine(ex - 13*sq, by + (brow_tilt*7 if inner < 0 else -brow_tilt*7), ex + 13*sq, by + (brow_tilt*7 if inner > 0 else -brow_tilt*7), ink(lw * .78))
    if spec.get('glasses'):
        for ex0 in (-30, 30):
            ex = ex0 + fx; far = (face > 0 and ex0 > 0) or (face < 0 and ex0 < 0); sq = 1 - .3 * abs(face) if far else 1.0
            g = skia.Path(); g.addOval(skia.Rect(ex - 24*sq, eyy - 24, ex + 24*sq, eyy + 24)); c.drawPath(g, fp((225, 240, 255), 55)); c.drawPath(g, ink(lw * .7))
        c.drawLine(fx - 7, eyy - 3, fx + 7, eyy - 3, ink(lw * .7))
    mx, my = face * 34, 42
    if spec.get('moustache'):
        my = my + spec.get('moustache_dy', 0)
        mu = skia.Path()
        if spec.get('moustache_style') == 'pencil':   # thin trimmed 1920s moustache (Ponzi)
            mu.moveTo(mx - 26, my - 14); mu.quadTo(mx - 12, my - 22, mx - 2, my - 18); mu.lineTo(mx + 2, my - 18)
            mu.quadTo(mx + 12, my - 22, mx + 26, my - 14); mu.quadTo(mx + 12, my - 13, mx, my - 13); mu.quadTo(mx - 12, my - 13, mx - 26, my - 14); mu.close()
        else:
            mu.moveTo(mx, my - 20)
            mu.cubicTo(mx-12, my-28, mx-30, my-22, mx-40, my-30); mu.cubicTo(mx-30, my-10, mx-12, my-12, mx, my-15)
            mu.cubicTo(mx+12, my-12, mx+30, my-10, mx+40, my-30); mu.cubicTo(mx+30, my-22, mx+12, my-28, mx, my-20); mu.close()
        c.drawPath(mu, fp(spec.get('moustache_col', spec.get('hair_col', '#1C1B22'))))
        if spec.get('moustache_outline'): c.drawPath(mu, ink(lw * .55))
    if mouth == 'grit':
        my = my + 12
        gp = skia.Path(); gp.addRRect(skia.RRect.MakeRectXY(skia.Rect(mx - 34, my - 14, mx + 34, my + 16), 10, 10))
        c.drawPath(gp, fp('#FAFAF4')); c.save(); c.clipPath(gp, doAntiAlias=True)
        for tx in range(-22, 34, 14): c.drawLine(mx + tx, my - 14, mx + tx, my + 16, ink(lw * .45))
        c.drawLine(mx - 34, my + 1, mx + 34, my + 1, ink(lw * .5)); c.restore(); c.drawPath(gp, ink(lw * .8))
    if mouth == 'smile': m = skia.Path(); m.moveTo(mx - 17, my - 2); m.quadTo(mx, my + 13, mx + 17, my - 2); c.drawPath(m, ink(lw * .8))
    elif mouth == 'smirk':
        d = 1 if face >= 0 else -1; m = skia.Path(); m.moveTo(mx - 15*d, my + 3); m.quadTo(mx + 4*d, my + 12, mx + 20*d, my - 6); c.drawPath(m, ink(lw * .8))
    elif mouth == 'flat': c.drawLine(mx - 12, my + 2, mx + 12, my + 2, ink(lw * .8))
    elif mouth == 'o': oval(c, mx - 8, my - 9, mx + 8, my + 11, '#5A1A1E', lw * .7)
    elif mouth == 'mid': oval(c, mx - 12, my - 4, mx + 12, my + 10, '#5A1A1E', lw * .7)
    elif mouth == 'open':
        mp = skia.Path(); mp.moveTo(mx - 20, my - 5); mp.lineTo(mx + 20, my - 5); mp.cubicTo(mx + 19, my + 24, mx - 19, my + 24, mx - 20, my - 5); mp.close()
        c.drawPath(mp, fp('#5A1A1E')); c.save(); c.clipPath(mp, doAntiAlias=True)
        c.drawRect(skia.Rect(mx - 22, my - 6, mx + 22, my + 2), fp('#FAFAF4')); c.drawOval(skia.Rect(mx - 11, my + 9, mx + 11, my + 26), fp('#D05860')); c.restore()
        c.drawPath(mp, ink(lw * .7))
    if sparkle > 0:
        k = pop(sparkle) * (1 if sparkle < 1 else max(0, 2 - sparkle)); sx_, sy_ = mx + 26 * (1 if face >= 0 else -1), my - 8; st = skia.Path()
        for i in range(8):
            r_ = (20 if i % 2 == 0 else 5) * k; a = i * math.pi / 4; (st.moveTo if i == 0 else st.lineTo)(sx_ + r_ * math.cos(a), sy_ + r_ * math.sin(a))
        st.close(); c.drawPath(st, fp('#FFFFFF'))
    c.restore(); c.save()   # back to body space: arms that go in front of the face
    for side, a in front: _draw_arm(side, a)
    c.translate(0, HEAD_CY); c.rotate(tilt)
    if sweat >= 0:
        sx0, sy0 = (-1 if face > 0 else 1) * 62, -66 + 30 * (sweat % 1.0)
        d = skia.Path(); d.moveTo(sx0, sy0 - 19); d.cubicTo(sx0 + 12, sy0 - 3, sx0 + 11, sy0 + 10, sx0, sy0 + 10); d.cubicTo(sx0 - 11, sy0 + 10, sx0 - 12, sy0 - 3, sx0, sy0 - 19); d.close()
        shape(c, d, '#8FC8EE', lw * .7)
    c.restore(); c.restore()

def cane(c, x, y, s, arms, side=1, bob=0.0):
    """Walking cane with a gold handle held in one hand (Ponzi's signature prop). Draw after the character."""
    hx, hy = hand_pos(x, y, s, arms, side, bob)
    c.drawLine(hx, hy + 6 * s, hx + side * 6 * s, y, ink(13 * s, INK)); c.drawLine(hx, hy + 6 * s, hx + side * 6 * s, y, ink(7 * s, (40, 26, 18)))
    p = skia.Path(); p.addArc(skia.Rect(hx - 4 * s, hy - 16 * s, hx + 26 * s * side if side > 0 else hx + 4 * s, hy + 14 * s), 180, 180)
    hd = skia.Path(); hd.moveTo(hx, hy + 8 * s); hd.quadTo(hx, hy - 16 * s, hx + side * 18 * s, hy - 14 * s); hd.quadTo(hx + side * 32 * s, hy - 12 * s, hx + side * 30 * s, hy + 2 * s)
    c.drawPath(hd, ink(15 * s, INK)); c.drawPath(hd, ink(9 * s, '#FCA311'))

def hand_pos(x, y, s, arms, side, bob=0.0):
    """World position of a character's hand (side -1 = screen-left hand, 1 = screen-right) for props held in hand."""
    e, h, _ = _arm(arms[0] if side < 0 else arms[1]); m = 1 if side < 0 else -1
    return x + h[0] * m * s, y + (h[1] - bob) * s

def walk_legs(phase, stride=46, lift=20):  # pass as legs=walk_legs((t-t0)*11) with bob=7*abs(sin(phase))
    a = math.sin(phase)
    return ((-10, a * stride, max(0, math.cos(phase)) * lift), (10, -a * stride, max(0, -math.cos(phase)) * lift))

# example cast (always invent new looks per video: hair, glasses, suit colour, hat)
HERO = dict(skin='#E6BE8E', skin_d='#C99F70', suit='#3B4660', suit_d='#2B3348', shirt='#F4EFE2', tie='#A8232B', hair='slick', moustache=True, hanky='#F4EFE2')
MARK = dict(skin='#EBC79C', skin_d='#CFA677', suit='#7A5A3C', suit_d='#5E432B', shirt='#F4EFE2', tie='#2F6B4E', bowtie=True, hair='bald', glasses=True)
