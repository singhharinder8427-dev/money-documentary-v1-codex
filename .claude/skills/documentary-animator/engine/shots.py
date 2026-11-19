"""Standard shot types built from sets, actors and widgets. Each returns draw(c, t) for render.render_shot.
Shot grammar (one picture per sentence): wide set | close-up | top-down desk | text card | chapter card |
title card | chart | counter over a set | polaroid ending."""
import skia
from engine.core import W, H
from engine.sets import get_set
from engine import widgets as Wd

VIGNETTE = 0.78   # owner: cinematic vignette on every scene shot (framed stage + cards have their own look)
def _v(f, k=VIGNETTE, inner=.42):
    f.vignette = k
    f.vignette_inner = inner
    return f

def wide(set_name, back_actors=(), front_actors=(), overlay=None, t0=0.0):
    """Set + actors (back = behind desks/tables, front = in front). overlay(c, t) draws graphics on top. t0 = shot start (absolute)."""
    st = get_set(set_name)
    def draw(c, t):
        st.draw(c, [lambda c, a=a: a.draw(c, t, t0 + t) for a in back_actors], [lambda c, a=a: a.draw(c, t, t0 + t) for a in front_actors])
        if overlay: overlay(c, t)
    return _v(draw, *st.vignette) if st.vignette else _v(draw)

_BLUR = {}
def closeup(set_name, actor, focus=(960, 540), overlay=None, t0=0.0, blur=13, zoom=1.5):
    """Close-up: the set blurred and zoomed behind a big character (actor.s ~2.15, feet y ~1390)."""
    key = (set_name, focus, blur, zoom)
    if key not in _BLUR:
        st = get_set(set_name); s = skia.Surface(W, H); c = s.getCanvas(); p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(blur, blur))
        c.save(); c.translate(W / 2, H / 2); c.scale(zoom, zoom); c.translate(-focus[0], -focus[1]); c.drawImage(st.base, 0, 0, skia.SamplingOptions(), p); c.restore()
        c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color=skia.Color(10, 16, 36, 70))); _BLUR[key] = s.makeImageSnapshot()
    img = _BLUR[key]
    def draw(c, t):
        c.drawImage(img, 0, 0); actor.draw(c, t, t0 + t)
        if overlay: overlay(c, t)
    return _v(draw, .85)

def card(kind, dur, **kw):
    """kind: 'text' (text=, gold_words=), 'chapter' (n=, title=), 'title' (title=, gold_word=, sub=)."""
    def draw(c, t):
        u = t / max(dur, 1e-3)
        if kind == 'text': Wd.text_card(c, kw['text'], max(t - kw.get('lead', 0.3), 0), kw.get('gold_words', ()), dur=dur)   # typing starts with the voice (0.3 s lead)
        elif kind == 'chapter': Wd.chapter_card(c, kw.get('n'), kw['title'], u)
        else: Wd.title_card(c, kw['title'], u, kw.get('gold_word'), kw.get('sub'))
    return draw

def desk(overlay, set_name='night/desk'):
    """Top-down desk (documents, cash, hands). overlay(c, t) slides documents / stamps in."""
    st = get_set(set_name)
    def draw(c, t): c.drawImage(st.base, 0, 0); overlay(c, t)
    return _v(draw)

def plain(overlay, bg='#14213D', framed=True):
    """Stage for diagrams, documents, newspapers, charts, counters. framed=True (default, owner's reference):
    navy with a soft dotted vignette and a double rounded border."""
    def draw(c, t):
        if framed: Wd.framed_bg(c)
        else: c.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color=skia.Color4f.FromColor(int('FF' + bg.lstrip('#'), 16))))
        overlay(c, t)
    return _v(draw, .5)
