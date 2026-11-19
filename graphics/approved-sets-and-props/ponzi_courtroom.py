"""A staged preview of the 1920 plea scene from the Dirty Dollar Ponzi script."""
from pathlib import Path

import skia

from engine import render as renderer, shots
from engine.sets_src.courtroom import court_bench_camera, judge_at_bench
from engine import kit, widgets
from engine.cast import CAST, person
from engine.core import F_LABEL, H, NAVY, W

PROSECUTOR = person('agent', suit='#34415D', suit_d='#222B42', tie='#95713F', hair='slick', hair_part=True)
DEFENSE_COUNSEL = person('analyst', suit='#505A70', suit_d='#354058', skin='#D2A17B',
                         skin_d='#AB795B', glasses=False, hair='slick', hair_col='#433733', tie='#263B63')
PAPER = '#F6EDD7'
INK = '#152038'


def exhibit_in_hand(canvas, x, y, scale):
    canvas.save()
    canvas.translate(x + scale*21, y - scale*39)
    canvas.rotate(8)
    canvas.scale(scale, scale)
    kit.rect(canvas, -46, -55, 48, 49, PAPER, 3, r=3, v=INK)
    widgets.text(canvas, 'EXHIBIT', 0, -23, 22, NAVY, F_LABEL, 'center')
    for line_y, length in ((-9, 60), (3, 55), (15, 64), (27, 39)):
        kit.line(canvas, -32, line_y, -32+length, line_y, 1.7, '#6880A2')
    canvas.restore()


def at_counsel_table(canvas, camera, spec, position, table_back, *, face, brow, eyes, mouth, arms, exhibit=False):
    x, y = camera.point((position[0], 0, position[1]))
    scale = camera.scale(position[1])*.00462
    _, desk_edge = camera.point((0, .88, table_back))
    canvas.save()
    canvas.clipRect(skia.Rect(0, 0, W, desk_edge), doAntiAlias=True)
    if exhibit:
        hand_x, hand_y = kit.hand_pos(x, y, scale, arms, side=1)
        exhibit_in_hand(canvas, hand_x, hand_y, scale)
    kit.draw_char(canvas, x, y, scale, spec, face=face, brow=brow, eyes=eyes, mouth=mouth, arms=arms, rim='#FFE3A6')
    canvas.restore()


def ponzi_hat(canvas, camera):
    x, y = camera.point((2.90, .88, 6.36))
    canvas.save()
    canvas.translate(x, y-3)
    kit.oval(canvas, -52, -10, 53, 9, '#E8C77A', 3.5, INK)
    kit.rect(canvas, -36, -32, 36, -4, '#E8C77A', 3.5, r=5, v=INK)
    for stripe in (-23, -10, 3, 16, 29):
        kit.line(canvas, stripe-4, -28, stripe+2, -12, 1.3, '#B99455')
    kit.rect(canvas, -36, -14, 36, -5, NAVY, 1.8, r=2, v=INK)
    canvas.restore()


def gallery_spectator(canvas, x, y, scale, hair, coat, collar, bob=False):
    """Seat backs frame the view, with spectators seen from behind."""
    canvas.save()
    canvas.translate(x, y)
    canvas.scale(scale, scale)
    kit.rect(canvas, -77, 54, 77, 174, coat, 6, r=23, v=INK)
    kit.poly(canvas, [(-35, 49), (0, 69), (35, 49), (23, 83), (-23, 83)], collar, 2.5, INK)
    kit.rect(canvas, -57, -63, 57, 56 if bob else 45, hair, 5, r=26, v=INK)
    kit.line(canvas, -26, -40, 7, -47, 5.2, '#69748B')
    kit.line(canvas, 22, 35, 43, 22, 2.6, '#434352')
    canvas.restore()


def render(output):
    camera = court_bench_camera()

    def cast(canvas, t):
        judge_at_bench(canvas, camera)
        at_counsel_table(canvas, camera, PROSECUTOR, (-2.87, 6.92), 6.63, face=.47, brow=.13,
                         eyes='dot', mouth='mid', arms=('down', 'present'), exhibit=True)
        at_counsel_table(canvas, camera, DEFENSE_COUNSEL, (3.37, 7.31), 6.96, face=-.38, brow=.21,
                         eyes='dot', mouth='flat', arms=('down', 'down'))
        at_counsel_table(canvas, camera, CAST['ponzi'], (2.03, 7.17), 6.96, face=-.36, brow=.36,
                         eyes='half', mouth='flat', arms=('down', 'hold'))
        ponzi_hat(canvas, camera)
        gallery_spectator(canvas, 164, 1002, 1.02, '#3D3031', '#4F5F7C', '#DFCAB6', bob=True)
        gallery_spectator(canvas, 388, 1022, .89, '#554535', '#6B5648', '#DBD0B7')
        gallery_spectator(canvas, 1657, 1009, 1.03, '#28272F', '#4E556A', '#D6C3AD')
        gallery_spectator(canvas, 1846, 1035, .91, '#615B59', '#635343', '#E4D7BB', bob=True)

    def caption(canvas, t):
        canvas.save()
        canvas.translate(750, H-112)
        canvas.scale(.68, .68)
        widgets.lower_third(canvas, 'Charles Ponzi', 'Courtroom reenactment', 1, x=0, y=0)
        canvas.restore()

    renderer.still(shots.wide('day/courtroom', overlay=cast), 0, str(output), hud=caption)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='Output PNG path')
    render(parser.parse_args().output)
