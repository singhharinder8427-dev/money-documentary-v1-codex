"""Light pools for the approved finance and night print assets."""
import numpy as np
import skia

from engine import kit, looks
from engine.core import H, W


def projected_light_map(pools):
    yy, xx = np.ogrid[:H, :W]
    lighting = np.full((H, W), .12)
    for (x, y), rx, ry, power in pools:
        np.maximum(lighting, .12 + power*np.exp(-((xx-x)/rx)**2-((yy-y)/ry)**2), out=lighting)
    return lighting


def office_light_map(pools):
    """Measure the same fixture mask used by the night office set."""
    ambient = '#4C5CA0'
    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()
    canvas.clear(skia.ColorWHITE)
    kit.night(canvas, [('oval', x, y, rx, ry, power) for (x, y), rx, ry, power in pools], ambient)
    pixels = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
    ambient_level = looks.C(ambient).mean() / 255
    return np.clip((pixels[..., :3].mean(-1) / 255 - ambient_level) / (1 - ambient_level), 0, 1)
