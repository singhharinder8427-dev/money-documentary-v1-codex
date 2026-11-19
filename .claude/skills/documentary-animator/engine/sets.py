"""The 10 LOCKED sets as empty, reusable backgrounds.
   get_set(name) -> Set(base, fg, spots, rim, light, kind)
     base  = skia.Image: the set in its locked look (+ any background extras such as the trading-floor crowd, crisp)
     fg    = skia.Image with alpha, or None: things that stand IN FRONT of actors (desk, table) - draw after actors
     spots = suggested actor places {name: (x_feet, y_feet, scale)}
Night sets use the night print look, day sets the day print look. Results are cached as PNG files."""
import os, sys, hashlib, pathlib
import numpy as np, skia
from PIL import Image as PI
from engine import kit
from engine.core import W, H, REPO
from engine import looks
sys.modules.setdefault('kit', kit)            # the scene sources do `import kit`

# ---------- render modes (patch the kit's paint factories once; passthrough unless a mode is active)
M = {'m': 'off', 'inp': False, 'k': 0, 'plane': None, 'extras': (), 'lights': None, 'glows': [], 'img': None}
_fp, _ink, _sp, _night, _add = kit.fp, kit.ink, kit.sp, kit.night, kit.add_light
def _mod(p, fx):
    m = M['m']
    if m in ('off', 'bg') or M['inp']: return p
    if m == 'unlit':
        if fx: p.setAlphaf(0.0)
        return p
    if fx: p.setAlphaf(0.0)                       # mask modes: glows / soft shadows never cut anything
    else: p.setBlendMode(skia.BlendMode.kClear)   # solid things drawn later hide what is behind them
    return p
def _fx(a, k, bi, li): return bool((len(a) > bi and a[bi]) or k.get('blur')) or bool((len(a) > li and a[li]) or k.get('blend'))
kit.fp = lambda *a, **k: _mod(_fp(*a, **k), _fx(a, k, 2, 3))
kit.ink = lambda *a, **k: _mod(_ink(*a, **k), False)
kit.sp = lambda *a, **k: _mod(_sp(*a, **k), _fx(a, k, 2, 1))
def _night_w(c, lights, ambient='#4C5CA0'):
    if M['m'] == 'unlit': M['lights'] = (lights, ambient)
    elif M['m'] in ('off', 'bg'): _night(c, lights, ambient)
def _add_w(c, x, y, r, v, a):
    if M['m'] == 'unlit': M['glows'].append((x, y, r, v, a))
    elif M['m'] in ('off', 'bg'): _add(c, x, y, r, v, a)
kit.night, kit.add_light = _night_w, _add_w

from engine.sets_src import night_scenes as NS, day_scenes as DS
from engine.core import F_LABEL2, F_TITLE, F_TYPE
NS.KAL, NS.MRK, NS.HAND = F_LABEL2, F_TITLE, F_TYPE
NS.txt = lambda c, s, x, y, size, color, font=None, align='left', stroke=0, rot=0.0, skew=0, sc=kit.INK: kit.label(c, s, x, y, size, color, font=font or NS.KAL, align=align, stroke=stroke, stroke_col=sc, skew=0, rot=rot)
NS.night, NS.add_light = _night_w, _add_w
from engine.cast import LOCKED as _L
_SPEC = {id(NS.CEO): _L['ceo'], id(NS.ANALYST): _L['analyst'], id(NS.WORKER): _L['worker'], id(NS.BANKER): _L['banker'], id(NS.INVESTOR): _L['investor']}
def _person(c, x, y, s, spec, **kw):
    k = M['k']; M['k'] += 1; m = M['m']
    if m == 'extras' and k in M['extras']:
        M['inp'] = True; kw.pop('light', None); rim = kw.pop('rim', '#9FB8F0')
        kit.draw_char(c, x, y, s, _SPEC.get(id(spec), spec), light=-1, rim=rim, **kw); M['inp'] = False
    elif m == 'plane' and k == M['plane']:
        M['inp'] = True; c.drawRect(skia.Rect(-50, -50, W + 50, H + 50), _fp('#FFFFFF')); M['inp'] = False
NS.person = _person
def _frame_out(surf, path): M['img'] = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).copy()
NS.frame_out = _frame_out
# day scenes: no actors, capture after the day print pass
def _day_finish(surf):
    a = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(float)
    out = looks.grain(looks.day_print(a), base=240, fine=7, soft=26, seed=7)
    M['img'] = np.dstack([np.clip(out, 0, 255).astype(np.uint8), np.full((H, W), 255, np.uint8)]); return surf.getCanvas()
DS.finish_bg = _day_finish; DS.draw_char = lambda *a, **k: None; DS.shadow = lambda *a, **k: None; DS.save = lambda *a, **k: None

# ---------- the catalogue
NIGHT_RIM, DAY_RIM = '#9FB8F0', '#FFE3A6'
SETS = {
 'night/office':   dict(fn=NS.office,  plane=0, extras='none', spots={'behind_desk': (930, 950, 1.08), 'front_left': (380, 1070, 1.05), 'front_right': (1500, 1070, 1.05)}),
 'night/trading':  dict(fn=NS.trading, plane=-2, extras='before', spots={'left': (760, 1180, 1.35), 'right': (1260, 1150, 1.25)}),
 'night/desk':     dict(fn=NS.desk,    plane=None, extras='all', spots={}),          # top-down desk: hands + documents, no standing actors
 'night/street':   dict(fn=NS.street,  plane=0, extras='none', spots={'walk': (900, 905, .6), 'bank_door': (220, 880, .52), 'pawn': (540, 880, .52), 'pawn2': (650, 880, .52)}),
 # street1920: people at s .36 so buildings read at the right scale; the line ends at the hero door (x 1020)
 'night/street1920': dict(fn=lambda: (setattr(NS, 'STREET_ERA', '1920'), NS.street(), setattr(NS, 'STREET_ERA', 'modern')), plane=0, extras='none', spots={'door': (1020, 860, .36), 'queue': (930, 864, .36)}),
 'night/kitchen':  dict(fn=NS.kitchen, plane=0, extras='none', spots={'left': (640, 1060, 1.05), 'right': (1180, 1060, 1.05)}),
 'day/living':     dict(fn=DS.living_room, spots={'left': (600, 975, .98), 'right': (860, 985, .98)}),
 'day/kitchen':    dict(fn=DS.kitchen, spots={'center': (600, 1000, 1.0)}),
 'day/bank':       dict(fn=DS.bank, spots={'left': (760, 1020, 1.0), 'right': (1120, 1025, 1.0)}),
 'day/street':     dict(fn=DS.street, spots={'left': (880, 905, .95), 'right': (1290, 905, .95)}),
 'day/lesson':     dict(fn=DS.lesson, spots={'board_left': (520, 990, 1.0), 'board_right': (860, 1000, 1.0)}),
}
CACHE = pathlib.Path(os.environ.get('DOCANIM_CACHE', str(REPO / '.cache' / 'sets')))

class Set:
    def __init__(self, name, base, fg, spots, kind):
        self.name, self.base, self.fg, self.spots, self.kind = name, base, fg, spots, kind
        self.rim = NIGHT_RIM if kind == 'night' else DAY_RIM
        self.light = -1 if kind == 'night' else 1
    def draw(self, c, back=(), front=()):
        """Draw the set with actors: back = callables drawn between base and fg (behind desks/tables),
        front = callables drawn after fg (in front of everything). Each callable takes the canvas."""
        c.drawImage(self.base, 0, 0)
        for f in back: f(c)
        if self.fg is not None: c.drawImage(self.fg, 0, 0)
        for f in front: f(c)

def _run(fn, mode, **kw):
    M.update(m=mode, k=0, glows=[], img=None, **kw); fn(); out = M['img']; M['m'] = 'off'; return out
def _to_img(a): return skia.Image.fromarray(np.ascontiguousarray(a), colorType=skia.kRGBA_8888_ColorType)
def _src_hash():
    h = hashlib.md5()
    for p in ('sets_src/night_scenes.py', 'sets_src/day_scenes.py', 'looks.py', 'kit.py', 'sets.py'): h.update(open(pathlib.Path(__file__).parent / p, 'rb').read())
    return h.hexdigest()[:10]

def _build(name):
    cfg = SETS[name]; kind = name.split('/')[0]
    if kind == 'day':
        return _run(cfg['fn'], 'bg'), None
    fn = cfg['fn']
    _run(fn, 'count'); n_people = M['k']                              # count person() calls
    plane = cfg['plane']; plane = (n_people + plane) if (plane is not None and plane < 0) else plane
    ex = {'none': (), 'all': tuple(range(n_people)), 'before': tuple(range(plane or 0))}[cfg['extras']]
    U = _run(fn, 'unlit')[..., :3].astype(float); lights, amb = M['lights']; glows = list(M['glows'])
    # light map
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.ColorWHITE); _night(c, lights, amb)
    m = s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(float).mean(-1) / 255
    # The approved night look was made with this value at 0 (skia's Color4f(int) returned ~0 on Linux but a real
    # value on Windows, so PC renders came out darker and full of dots). Fixed at 0 so every machine matches.
    ambv = np.mean([int(amb[k:k + 2], 16) for k in (1, 3, 5)]) / 255; m = np.clip((m - ambv) / (1 - ambv), 0, 1)   # real ambient: rooms dark navy, lamp pools lit (owner's night look)
    s2 = skia.Surface(W, H); c2 = s2.getCanvas(); c2.clear(skia.ColorBLACK)
    for g_ in glows: _add(c2, *g_)
    gm = s2.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(float).mean(-1) / 255
    Lm = np.clip(m + gm * 1.6, 0, 1)
    printed = np.clip(looks.grain(looks.night_print(U, Lm)), 0, 255)
    base = printed.copy()
    if ex:
        exl = _run(fn, 'extras', extras=ex); a = exl[..., 3:4].astype(float) / 255; base = base * (1 - a) + exl[..., :3] * a
    fg = None
    if plane is not None:
        pl = _run(fn, 'plane', plane=plane); fa = 255 - pl[..., 3]
        if fa.max() > 0: fg = np.dstack([printed.astype(np.uint8), fa.astype(np.uint8)])
    base = np.dstack([np.clip(base, 0, 255).astype(np.uint8), np.full((H, W), 255, np.uint8)])
    return base, fg

_MEM = {}
def get_set(name):
    if name in _MEM: return _MEM[name]
    CACHE.mkdir(parents=True, exist_ok=True); key = name.replace('/', '_') + '_' + _src_hash()
    bp, fp_ = CACHE / f'{key}_base.png', CACHE / f'{key}_fg.png'
    if bp.exists():
        base = np.asarray(PI.open(bp).convert('RGBA')); fg = np.asarray(PI.open(fp_).convert('RGBA')) if fp_.exists() else None
    else:
        base, fg = _build(name); PI.fromarray(base).save(bp)
        if fg is not None: PI.fromarray(fg).save(fp_)
    st = Set(name, _to_img(base), _to_img(fg) if fg is not None else None, SETS[name]['spots'], name.split('/')[0])
    _MEM[name] = st; return st
