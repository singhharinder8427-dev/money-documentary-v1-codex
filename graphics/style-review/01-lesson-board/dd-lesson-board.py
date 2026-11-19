import argparse
from pathlib import Path

import skia

from engine import kit, widgets
from engine.actor import Actor
from engine.core import F_LABEL, F_TITLE, GOLD, NAVY, PAPER, WHITE
from engine.render import contact_sheet, render_shot, still
from engine.sets import get_set


DURATION = 7.2
CAMERA_FOCUS = (965, 520)
CAMERA_ZOOM = (1.10, 1.16)
CARD_LEFTS = (605, 930, 1255)
CARD_WIDTH = 257
CARD_TOP = 266
CARD_BOTTOM = 519
LINK_Y = 388


def deposit_icon(canvas):
    for x, y, angle in ((-20, -9, -10), (10, -1, 9), (0, 22, 0)):
        widgets.bill(canvas, x, y, angle, .81)


def account_icon(canvas):
    kit.rect(canvas, -61, -48, 66, 51, PAPER, 5, r=8, v=NAVY)
    kit.rect(canvas, -67, -53, 60, 45, NAVY, 5, r=8, v=NAVY)
    kit.rect(canvas, -55, -43, -46, 35, '#29416C', 0, r=4)
    kit.rect(canvas, -30, -25, 35, 20, PAPER, 3, r=5, v=NAVY)
    widgets.text(canvas, '$', 2, 11, 31, NAVY, F_TITLE, 'center')
    kit.rect(canvas, 46, -11, 67, 17, GOLD, 3, r=4, v=NAVY)


def investor_icon(canvas):
    for x, y, scale in ((37, -5, .86), (-33, 0, 1.0)):
        canvas.save()
        canvas.translate(x, y)
        canvas.scale(scale, scale)
        kit.rect(canvas, -30, -7, 30, 42, '#29416C', 4, r=16, v=NAVY)
        kit.circ(canvas, 0, -22, 23, PAPER, 4, v=NAVY)
        canvas.restore()
    widgets.bill(canvas, 25, 31, -10, .51)


def draw_card(canvas, x, label, icon, progress, accent):
    if progress == 0:
        return
    canvas.saveLayerAlpha(None, round(255 * min(1, progress * 2.5)))
    canvas.translate(0, 22 * (1 - kit.ease_out(progress)))
    center = x + CARD_WIDTH / 2
    kit.rect(canvas, x + 5, CARD_TOP + 8, x + CARD_WIDTH + 5, CARD_BOTTOM + 8,
             '#D1D9E7', 0, r=16)
    kit.rect(canvas, x, CARD_TOP, x + CARD_WIDTH, CARD_BOTTOM,
             WHITE, 4.5, r=16, v=NAVY)
    if accent > 0:
        kit.line(canvas, x + 19, CARD_TOP + 3.5, x + CARD_WIDTH - 19,
                 CARD_TOP + 3.5, 5.5, GOLD, round(255 * accent))

    canvas.save()
    canvas.translate(center, CARD_TOP + 96)
    scale = .94 + .06 * kit.pop(progress)
    canvas.scale(scale, scale)
    icon(canvas)
    canvas.restore()

    face = skia.Font(F_LABEL, 42)
    size = min(42, 222 / face.measureText(label) * 42)
    widgets.text(canvas, label, center, CARD_TOP + 201, size, NAVY, F_LABEL, 'center')
    canvas.restore()


def make_scene():
    room = get_set('day/lesson')
    analyst = Actor('analyst', 385, 948, 1.17, face=.44, light=1, rim=room.rim)
    analyst.pose(0, ('down', 'present')).pose(.91, ('down', 'point'))
    analyst.pose(2.31, ('hip', 'present')).pose(3.15, ('hip', 'point'))
    analyst.pose(4.63, ('down', 'present')).pose(5.67, ('down', 'down'))

    def draw(canvas, time):
        room.draw(canvas)
        kit.rect(canvas, 583, 110, 1552, 644, '#F8FAFD', 8, r=12, v=NAVY)
        kit.rect(canvas, 574, 641, 1539, 668, '#BFC5D2', 4, r=5, v=NAVY)
        widgets.text(canvas, 'HOW A PONZI SCHEME PAYS', 1060, 207, 54,
                     NAVY, F_TITLE, 'center')
        kit.line(canvas, 823, 226, 1297, 226, 8, GOLD)

        steps = zip(CARD_LEFTS, ('NEW DEPOSITS', 'SCHEME ACCOUNT', 'EARLY INVESTORS'),
                    (deposit_icon, account_icon, investor_icon), (-.5, 1.78, 3.89))
        for x, label, icon, start in steps:
            progress = kit.K(time, start, .37)
            accent = kit.ease(kit.K(time, start + .17, .22)) * (1 - kit.K(time, start + 1.35, .40))
            draw_card(canvas, x, label, icon, progress, accent)

        for i, start in enumerate((1.13, 3.24)):
            widgets.arrow(canvas, CARD_LEFTS[i] + CARD_WIDTH + 12, LINK_Y,
                          CARD_LEFTS[i + 1] - 11, LINK_Y, kit.K(time, start, .47), wdt=13)

        takeaway = kit.ease_out(kit.K(time, 5.12, .36))
        if takeaway:
            canvas.saveLayerAlpha(None, round(255 * takeaway))
            kit.rect(canvas, 605, 553, 1512, 608, NAVY, 0, r=8)
            kit.rect(canvas, 605, 553, 615, 608, GOLD, 0, r=4)
            widgets.text(canvas, 'The scheme depends on new money coming in.',
                         1058, 592, 39, WHITE, F_LABEL, 'center')
            canvas.restore()

        analyst.draw(canvas, time)

    draw.vignette = .78
    return draw


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', type=Path)
    parser.add_argument('--stills-only', action='store_true')
    args = parser.parse_args()
    scene = make_scene()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.stills_only:
        times = (0, 1.4, 2.4, 3.55, 4.7, 6.7)
        panels = []
        for index, time in enumerate(times):
            zoom = kit.lerp(*CAMERA_ZOOM, kit.ease(time / DURATION))
            panels.append(still(scene, time, str(args.output_dir / f'frame-{index}.png'),
                                zoom=zoom, focus=CAMERA_FOCUS))
        contact_sheet(panels, args.output_dir / 'review.jpg')
    else:
        still(scene, 6.7, str(args.output_dir / 'lesson-board-still.png'),
              zoom=CAMERA_ZOOM[1], focus=CAMERA_FOCUS)
        render_shot(str(args.output_dir / 'lesson-board-flow.mp4'), DURATION, scene,
                    zoom=CAMERA_ZOOM, focus=CAMERA_FOCUS)
