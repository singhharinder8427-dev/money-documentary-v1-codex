"""Reusable staging and reframing from the approved glass-divider conversation."""
from functools import lru_cache

import skia
from PIL import Image

from engine import shots
from engine.core import H, W
from engine.cast import person
from .drawing import BLUE, INK, NAVY, kit, rect

VIEWS = {
    'two_shot': (0, 0, W, H),
    'visitor': (246, 287, 1094, 764),
    'detainee': (834, 287, 1682, 764),
}

visitor=person('saver',suit='#657A9B',suit_d='#405475',hair='bob')
detainee=person('worker',suit='#8E9BAE',suit_d='#626C7D',outfit='sweater')


def conversation(c, t=0):
    """Place both characters behind the counter and retain the glass between faces."""
    for x,spec,face,arms in [(313,visitor,.60,('down','phone')),(651,detainee,-.60,('phone','down'))]:
        y=440
        scale=.46
        c.save()
        c.clipRect(kit.skia.Rect(x-107,134,x+107,326))
        kit.draw_char(c,x,y,scale,spec,face=face,arms=arms,eyes='half',
                      brow=.22,mouth='flat',rim='#AEC5E2')
        hx=x+(44 if face>0 else -44)
        hy=y-452*scale
        c.save()
        c.translate(hx,hy)
        c.rotate(14 if face>0 else -14)
        rect(c,-5,-19,5,18,NAVY,1.6,4)
        for yy in (-22,14):
            rect(c,-6,yy,7,yy+9,INK,1.5,3)
        c.restore()
        tether=kit.skia.Path()
        tether.moveTo(hx,hy+17)
        cradle=408 if face>0 else 551
        tether.cubicTo(hx,hy+68,cradle,326,cradle,297)
        c.drawPath(tether,kit.ink(2,BLUE))
        c.restore()



def _two_shot():
    def overlay(canvas, t):
        canvas.save()
        canvas.scale(2, 2)
        conversation(canvas, t)
        canvas.restore()

    return shots.wide('day/visiting_room_call', overlay=overlay)


@lru_cache(maxsize=2)
def _closeup(view):
    draw = _two_shot()
    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()
    draw(canvas, 0)
    kit.vignette(canvas, draw.vignette, draw.vignette_inner)
    colors = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
    crop = Image.fromarray(colors).convert('RGB').crop(VIEWS[view])
    frame = crop.resize((W, H), Image.Resampling.LANCZOS).convert('RGBA')
    return skia.Image.frombytes(frame.tobytes(), (W, H), skia.kRGBA_8888_ColorType)


def shot(view='two_shot'):
    """Return a normal engine shot of the pair, visitor, or detainee."""
    if view == 'two_shot':
        return _two_shot()
    image = _closeup(view)

    def draw(canvas, t):
        canvas.drawImage(image, 0, 0)

    return draw
