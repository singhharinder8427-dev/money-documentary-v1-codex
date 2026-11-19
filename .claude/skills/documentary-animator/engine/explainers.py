"""Timed overlays for the approved Dirty Dollar map and evidence graphics.

Times are in seconds. Callers draw their own background and provide content
callbacks so labels, icons, and geographic data belong to the current story.
"""

import math

import skia

from engine.core import F_LABEL, GOLD, NAVY, PAPER
from engine.kit import K, circ, ease, ease_out, ink, line, linear, poly, rect, sp
from engine import kit, widgets


_OUTLINE = '#0A142A'
PORTRAIT_SIZE = (640, 615)
EMPHASIS_PORTRAIT_SIZE = (420, 380)


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


def _portrait_light(canvas, image, light):
    width, height = PORTRAIT_SIZE
    bounds = skia.Rect(0, 0, width, height)
    dark = skia.Paint()
    dark.setColorFilter(skia.ColorFilters.Matrix([
        .25, 0, 0, 0, .023, 0, .26, 0, 0, .035, 0, 0, .38, 0, .062, 0, 0, 0, 1, 0,
    ]))
    canvas.drawImage(image, 0, 0, skia.SamplingOptions(), dark)
    if light > 0:
        edge = 667 - 790 * light
        canvas.saveLayer(bounds)
        canvas.drawImage(image, 0, 0)
        mask = sp(linear(edge, 255, edge + 108, 246, [skia.ColorTRANSPARENT, skia.ColorWHITE]),
                  blend=skia.BlendMode.kDstIn)
        canvas.drawRect(bounds, mask)
        canvas.restore()


def _portrait_frame(canvas, image, origin, scale, light, label, draw_label):
    canvas.save()
    canvas.translate(*origin)
    canvas.scale(scale, scale)
    rect(canvas, 12, 16, 705, 794, _OUTLINE, 0, r=23)
    rect(canvas, 0, 0, 690, 780, '#263D65', 6, r=20, v=_OUTLINE)
    rect(canvas, 8, 8, 682, 772, None, 3, r=15, v='#9DB0DA')
    rect(canvas, 20, 19, 670, 642, _OUTLINE, 0, r=8)
    canvas.save()
    canvas.translate(25, 24)
    canvas.clipRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, *PORTRAIT_SIZE), 6, 6), doAntiAlias=True)
    _portrait_light(canvas, image, light)
    canvas.restore()
    line(canvas, 678, 32, 678, 47 + 558 * light, 5, GOLD, round(65 + 190 * light))
    if label > 0:
        canvas.saveLayerAlpha(None, round(255 * label))
        draw_label(canvas)
        canvas.restore()
    canvas.restore()


def portrait_reveal(canvas, time, *, image, origin, draw_label, scale=1.0,
                    light_at=.28, light_duration=1.38, label_at=1.64):
    """Light a PORTRAIT_SIZE image, then draw its nameplate in frame-local coordinates."""
    light = _reveal(time, light_at, light_duration)
    label = _reveal(time, label_at, .36)
    _portrait_frame(canvas, image, origin, scale, light, label, draw_label)


def portrait_callback(canvas, time, *, image, origin, draw_label, draw_document, connector,
                      scale=.855, document_at=.30, link_at=.97, highlight_at=1.30):
    """Bring a portrait back beside evidence. Reuse the image and nameplate from its reveal.

    draw_document(canvas, visibility, highlight) draws in shot coordinates.
    The connector runs from the portrait frame to the relevant document field.
    """
    _portrait_frame(canvas, image, origin, scale, 1.0, 1.0, draw_label)
    draw_document(canvas, _reveal(time, document_at, .43), _reveal(time, highlight_at, .43))
    marker = _reveal(time, link_at, .51)
    if marker > 0:
        draw_route(canvas, connector, marker, width=5, arrow=False)
        circ(canvas, *connector[0], 7, GOLD, 3, _OUTLINE)
    if marker >= .99:
        circ(canvas, *connector[-1], 9, GOLD, 3, _OUTLINE)


def muted_portrait_paint():
    """Return the reusable navy treatment for portraits outside the focus."""
    luma = (.2126, .7152, .0722)
    matrix = []
    for tint, lift in ((.53, .043), (.62, .068), (.79, .113)):
        matrix.extend([component * tint for component in luma] + [0, lift])
    paint = skia.Paint()
    paint.setColorFilter(skia.ColorFilters.Matrix(matrix + [0, 0, 0, 1, 0]))
    return paint


def emphasis_portrait_card(canvas, image, name, center, *, emphasis, inactive, muted):
    """Draw the approved card around an EMPHASIS_PORTRAIT_SIZE image."""
    width, height = EMPHASIS_PORTRAIT_SIZE
    canvas.save()
    canvas.translate(*center)
    canvas.scale(1 + .045 * emphasis, 1 + .045 * emphasis)
    kit.rect(canvas, -235, -221, 246, 264, _OUTLINE, 0, r=16)
    kit.rect(canvas, -242, -230, 242, 256, '#22375B', 5, r=15, v='#718BB5')
    canvas.save()
    canvas.translate(-210, -206)
    canvas.clipRRect(skia.RRect.MakeRectXY(skia.Rect(0, 0, width, height), 7, 7),
                     doAntiAlias=True)
    canvas.drawImage(image, 0, 0, skia.SamplingOptions(), muted)
    if emphasis:
        canvas.drawImage(image, 0, 0, skia.SamplingOptions(),
                         skia.Paint(Alphaf=emphasis))
    if inactive:
        canvas.drawRect(skia.Rect(0, 0, width, height), kit.fp(NAVY, round(78 * inactive)))
    canvas.restore()

    kit.rect(canvas, -210, 180, 210, 237, '#9FB3D4' if inactive > .5 else '#D6DEEC', 0, r=6)
    widgets.text(canvas, name, 0, 220, 46, NAVY, F_LABEL, 'center')
    if emphasis:
        edge = skia.RRect.MakeRectXY(skia.Rect(-242, -230, 242, 256), 15, 15)
        canvas.drawRRect(edge, kit.ink(6, GOLD, round(255 * emphasis)))
        canvas.drawRoundRect(skia.Rect(-209, 180, 209, 237), 6, 6,
                             kit.fp(PAPER, round(255 * emphasis)))
        kit.line(canvas, -199, 188, -199, 229, 6, GOLD, round(255 * emphasis))
        widgets.text(canvas, name, 0, 220, 46, NAVY, F_LABEL, 'center', alpha=round(255 * emphasis))
    canvas.restore()


def selective_emphasis(canvas, time, *, items, selected, draw_item, draw_note=None,
                       focus_at=.78, focus_duration=1.15, note_at=2.26):
    """Draw the full group as focus moves to one item, then reveal an optional note.

    draw_item(canvas, index, item, emphasis, inactive) receives two progress values.
    draw_note(canvas) appears after the focus shift.
    """
    focus = _reveal(time, focus_at, focus_duration)
    for index, item in enumerate(items):
        active = index == selected
        draw_item(canvas, index, item, focus if active else 0, 0 if active else focus)

    note = _reveal(time, note_at, .42)
    if draw_note is not None and note > 0:
        canvas.saveLayerAlpha(None, round(255 * note))
        draw_note(canvas)
        canvas.restore()


def object_first_process(canvas, time, *, steps, links, first_pose, last_pose, draw_object,
                         draw_step, move_at=.85, move_duration=.9, step_at=1.67, step_gap=.98,
                         link_at=2.35, link_gap=.98, arrow_width=13):
    """Show the outcome first, move it aside, and reveal the process in order.

    Each pose is (x, y, scale). Each horizontal link is (start_x, end_x, y).
    Callbacks are draw_object(canvas, x, y, scale) and draw_step(canvas, index, item, visibility).
    """
    shift = _reveal(time, move_at, move_duration)
    for index, item in enumerate(steps):
        visibility = _reveal(time, step_at + index * step_gap, .45)
        draw_step(canvas, index, item, visibility)
    for index, (start_x, end_x, y) in enumerate(links):
        widgets.arrow(canvas, start_x, y, end_x, y, K(time, link_at + index * link_gap, .40), wdt=arrow_width)
    position = tuple(kit.lerp(a, b, shift) for a, b in zip(first_pose, last_pose))
    draw_object(canvas, *position)
