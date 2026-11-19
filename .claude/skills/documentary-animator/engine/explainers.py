"""Timed overlays for the approved Dirty Dollar map and evidence graphics.

Times are in seconds. Callers draw their own background and provide content
callbacks so labels, icons, and geographic data belong to the current story.
"""

import math

import skia

from engine.core import GOLD
from engine.kit import K, ease, ease_out, ink, poly


_OUTLINE = '#0A142A'


def _reveal(time, start, duration):
    return ease(K(time, start, duration))


def _point_along(points, fraction):
    spans = [(i, a, b, math.dist(a, b)) for i, (a, b) in enumerate(zip(points, points[1:])) if a != b]
    remaining = sum(span[3] for span in spans) * max(0.0, min(1.0, fraction))
    for offset, (index, a, b, distance) in enumerate(spans):
        if remaining <= distance or offset == len(spans) - 1:
            u = min(1.0, remaining / distance)
            point = (a[0] + u * (b[0] - a[0]), a[1] + u * (b[1] - a[1]))
            direction = ((b[0] - a[0]) / distance, (b[1] - a[1]) / distance)
            return index, point, direction
        remaining -= distance
    raise ValueError('a route requires two distinct points')


def draw_route(canvas, points, progress=1.0, *, width=7, arrow=True):
    """Draw a gold path by distance, with an optional advancing arrowhead."""
    if progress <= 0:
        return
    index, (x, y), (dx, dy) = _point_along(points, progress)
    path = skia.Path()
    path.moveTo(*points[0])
    for point in (*points[1:index + 1], (x, y)):
        path.lineTo(*point)
    canvas.drawPath(path, ink(width + 6, _OUTLINE))
    canvas.drawPath(path, ink(width, GOLD))
    if arrow and progress > .075:
        length, half = width * 3.5, width * 1.6
        poly(canvas, [(x, y), (x - dx * length - dy * half, y - dy * length + dx * half),
                      (x - dx * length + dy * half, y - dy * length - dx * half)], GOLD, 3, _OUTLINE)


def evidence_inset(canvas, time, *, connector, pivot, draw_document,
                   connect_at=.60, open_at=1.00, highlight_at=3.70):
    """Open evidence beside a graphic. draw_document(canvas, highlight) draws the paper."""
    draw_route(canvas, connector, _reveal(time, connect_at, .72), width=5, arrow=False)
    opening = _reveal(time, open_at, .68)
    if opening <= 0:
        return
    canvas.saveLayerAlpha(None, round(255 * min(1, 1.4 * opening)))
    canvas.translate(*pivot)
    scale = .82 + .18 * ease_out(opening)
    canvas.scale(scale, scale)
    canvas.translate(-pivot[0], -pivot[1])
    draw_document(canvas, _reveal(time, highlight_at, .6))
    canvas.restore()


def border_highlight(canvas, time, *, outline, draw_label,
                     trace_at=.72, trace_duration=2.05, label_at=3.10):
    """Trace a supplied outline before fading in draw_label(canvas)."""
    draw_route(canvas, outline, _reveal(time, trace_at, trace_duration), width=8, arrow=False)
    label = _reveal(time, label_at, .45)
    if label > 0:
        canvas.saveLayerAlpha(None, round(255 * label))
        draw_label(canvas)
        canvas.restore()


def port_pulses(canvas, time, *, voyage, ports, draw_port, draw_ship,
                route_at=1.85, depart_at=2.70, voyage_duration=3.0, group_size=3, spacing=.115):
    """Animate grouped travel and timed pulses. Ports are ((x, y), pulse_time) pairs.

    Callbacks are draw_port(canvas, index, point, active) and
    draw_ship(canvas, x, y, direction). Group spacing is a fraction of route length.
    """
    draw_route(canvas, voyage, _reveal(time, route_at, .88), width=6)
    moving = K(time, depart_at, voyage_duration)
    if moving:
        leading = (1 + (group_size - 1) * spacing) * ease_out(moving)
        for ship_index in range(group_size):
            fraction = leading - ship_index * spacing
            if 0 < fraction < 1:
                _, (x, y), direction = _point_along(voyage, fraction)
                draw_ship(canvas, x, y, direction)

    for index, ((x, y), pulse_at) in enumerate(ports):
        pulse = K(time, pulse_at, .67)
        if 0 < pulse < 1:
            for radius in (16 + 40 * pulse, 28 + 63 * pulse):
                canvas.drawCircle(x, y, radius, ink(4, GOLD, round(230 * (1 - pulse))))
        draw_port(canvas, index, (x, y), time >= pulse_at)


def goods_to_routes(canvas, time, *, goods, routes, draw_good, draw_destination,
                    goods_at=.51, switch_at=2.42, goods_gap=.31, route_gap=.22):
    """Show goods before links. Callbacks draw_good(canvas, index, item, shift)
    and draw_destination(canvas, index) provide the story-specific graphics.
    """
    switch = _reveal(time, switch_at, .94)
    for index, route in enumerate(routes):
        delay = index * route_gap
        progress = _reveal(time, switch_at + .16 + delay, .93)
        draw_route(canvas, route, progress)
        if progress >= .88:
            alpha = _reveal(time, switch_at + 1.03 + delay, .25)
            canvas.saveLayerAlpha(None, round(255 * alpha))
            draw_destination(canvas, index)
            canvas.restore()

    for index, good in enumerate(goods):
        shown = _reveal(time, goods_at + index * goods_gap, .35) * (1 - switch)
        if shown:
            canvas.saveLayerAlpha(None, round(255 * shown))
            draw_good(canvas, index, good, 16 * switch)
            canvas.restore()


def masked_place_label(canvas, time, *, bounds, draw_label, enter_at=.68, hold_until=3.20,
                       enter_duration=.80, exit_duration=.75):
    """Wipe a fixed paper label on and off. draw_label(canvas) draws its complete state."""
    visible = min(_reveal(time, enter_at, enter_duration), 1 - _reveal(time, hold_until, exit_duration))
    if visible <= 0:
        return
    left, top, right, bottom = bounds
    canvas.save()
    canvas.clipRect(skia.Rect(left - 3, top - 4, left + (right - left + 8) * visible, bottom + 18))
    draw_label(canvas)
    canvas.restore()
