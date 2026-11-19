"""Daylight courtroom, close framing on the federal judge's bench."""
import numpy as np
import skia

from engine import kit
from engine.cast import person
from engine.core import GOLD, H, W
from engine.sets_src.night_scenes import lamp
from engine.sets_src.sales_floor import Camera, box, face, horizontal, polygon, segment, side_wall

INK = '#161820'
WOOD = '#987E65'
WOOD_DARK = '#68564F'
BRASS = '#E1B162'
PAPER = '#F8EDD3'


def gallery_bench(canvas, cam, left, z):
    x0, x1 = (-6.8, -1.25) if left else (1.25, 6.8)
    for x in (x0+.08, x1-.22):
        box(canvas, cam, x, .035, z-.04, x+.15, .79, z+.58,
            '#A68464', WOOD, WOOD_DARK, 3.5)
    box(canvas, cam, x0, .38, z+.02, x1, .48, z+.57, '#B69575', WOOD, WOOD_DARK, 3)
    box(canvas, cam, x0, .53, z, x1, .88, z+.095, '#B89777', '#8B705D', WOOD_DARK, 4)
    for x in np.linspace(x0+.17, x1-.17, 5)[:-1]:
        face(canvas, cam, x, .584, x+(x1-x0)*.20, .819, z-.013,
             '#A18674', '#6A554C', 1.7)
    segment(canvas, cam, (x0, .875, z-.015), (x1, .875, z-.015), 2, '#C4A680')


def sash_window(canvas, cam, x, z, width):
    side_wall(canvas, cam, x, 1.00, z, 4.43, z+width, '#91827A', INK, 4)
    side_wall(canvas, cam, x+.015, 1.20, z+.12, 4.23, z+width-.12, '#546A94', '#C0AD90', 2.8)
    for y in (2.00, 2.75, 3.50):
        segment(canvas, cam, (x+.023, y, z+.12), (x+.023, y, z+width-.12), 3, '#BEAD9B')
    for d in (.34, .66):
        dz = z+width*d
        segment(canvas, cam, (x+.026, 1.19, dz), (x+.026, 4.24, dz), 3.2, '#A99181')
    for d in (.03, .82):
        side_wall(canvas, cam, x+.03, 1.19, z+width*d, 4.29, z+width*(d+.14),
                  '#3B4157', INK, 2.6)
    polygon(canvas, cam, [(x+.04, 4.27, z), (x+.04, 3.85, z+width*.29),
                          (x+.04, 3.84, z+width*.68), (x+.04, 4.27, z+width)], '#978168')


def panel_front(canvas, cam, x0, x1, y0, y1, z, panels, daylight=False):
    face(canvas, cam, x0, y0, x1, y1, z, '#BDAD95' if daylight else WOOD, INK, 4)
    span = (x1-x0)/panels
    for k in range(panels):
        x = x0+k*span
        face(canvas, cam, x+.12, y0+.10, x+span-.12, y1-.10, z-.024,
             '#E2D7C1' if daylight else '#AD9174', INK, 2.5)
        face(canvas, cam, x+.21, y0+.18, x+span-.21, y1-.18, z-.032,
             '#A6ACB8' if daylight else '#987C65', '#B2987F', 1.45)
    segment(canvas, cam, (x0, y1, z-.028), (x1, y1, z-.028), 3, '#D1B38A')


def scales_medallion(canvas, cam, z, height=3.61):
    x, y = cam.point((0, height, z))
    r = cam.scale(z)*.70
    kit.circ(canvas, x, y, r, '#8B714D', 5, INK)
    kit.circ(canvas, x, y, r*.84, '#C4A370', 2.5, '#684D3E')
    kit.line(canvas, x, y-r*.45, x, y+r*.48, 3.2, INK)
    kit.line(canvas, x-r*.51, y-r*.18, x+r*.51, y-r*.18, 2.6, INK)
    kit.line(canvas, x-r*.26, y+r*.47, x+r*.26, y+r*.47, 3.2, INK)
    for side in (-1, 1):
        bx = x+side*r*.43
        kit.poly(canvas, [(bx, y-r*.16), (bx-r*.18, y+r*.20),
                          (bx+r*.18, y+r*.20)], None, 1.65, INK)
        kit.poly(canvas, [(bx-r*.23, y+r*.20), (bx+r*.23, y+r*.20),
                          (bx+r*.13, y+r*.35), (bx-r*.13, y+r*.35)], '#665040', 1, INK)


def counsel_table(canvas, cam, x0, x1, z):
    box(canvas, cam, x0+.15, .02, z+.10, x1-.15, .81, z+.91,
        '#A0907B', WOOD_DARK, '#7B6454', 3)
    panel_front(canvas, cam, x0+.11, x1-.11, .18, .75, z+.07, 2)
    box(canvas, cam, x0, .79, z, x1, .88, z+1.01, '#C4AA8D', WOOD, WOOD_DARK, 3.8)
    x = (x0+x1)*.5
    horizontal(canvas, cam, x-.54, z+.21, x+.18, z+.70, .899, '#D3BD8D', INK, 2.5)
    horizontal(canvas, cam, x-.44, z+.27, x+.22, z+.69, .915, '#E1D1B1', INK, 2)
    px, py = cam.point((x1-.38, .90, z+.60))
    kit.oval(canvas, px-9, py-3, px+9, py+4, '#202333', 1)
    segment(canvas, cam, (x1-.38, .91, z+.60), (x1-.50, 1.21, z+.60), 3, '#262636')
    kit.oval(canvas, px-22, py-32, px-10, py-24, '#222637', 0)


COURT_WIDE = Camera(center=960, horizon=318, eye_x=.02, eye_y=3.05, focal=1030, offset=3.93)


def bench_props(canvas, cam):
    """Case file, microphone, and gavel sit on the front bench."""
    face(canvas, cam, -.97, 1.52, .03, 1.59, 10.69, '#B29260', INK, 2.1)
    for top, dz, color in ((1.577, 0, '#AE8A55'), (1.605, .045, '#DDCFAD'), (1.626, .08, PAPER)):
        horizontal(canvas, cam, -.97, 10.69+dz, .03, 11.35+dz, top, color, INK, 2.4)
    for z in (10.88, 11.03, 11.17):
        segment(canvas, cam, (-.84, 1.628, z), (-.18, 1.628, z), 1.9, '#6B5948')

    x, y = cam.point((.90, 1.52, 11.21))
    unit = cam.scale(11.21)
    kit.oval(canvas, x-unit*.12, y-3, x+unit*.12, y+5, '#26364F', 2.8, INK)
    mic = skia.Path()
    mic.moveTo(x, y)
    mic.cubicTo(x, y-unit*.22, x-unit*.09, y-unit*.43, x-unit*.20, y-unit*.45)
    canvas.drawPath(mic, kit.ink(4.8, INK))
    kit.oval(canvas, x-unit*.28, y-unit*.49, x-unit*.15, y-unit*.42, '#49546B', 2.5, INK)

    x, y = cam.point((1.82, 1.51, 10.92))
    canvas.save()
    canvas.translate(x, y)
    marker_scale = unit / 150
    canvas.scale(marker_scale, marker_scale)
    kit.oval(canvas, -40, -8, 43, 10, '#685244', 3.1, INK)
    kit.oval(canvas, -38, -13, 41, 5, '#A4835C', 2.5, INK)
    canvas.translate(-11, -19)
    canvas.rotate(16)
    kit.rect(canvas, -2, -5, 77, 5, '#755340', 3, r=4, v=INK)
    kit.rect(canvas, -18, -15, 19, 14, '#907154', 3, r=6, v=INK)
    kit.rect(canvas, -7, -15, 7, 14, GOLD, 1.6, r=2, v='#473829')
    canvas.restore()


def courtroom(canvas, cam):
    back = 12.95
    horizontal(canvas, cam, -7.9, -.7, 7.9, back, 0, '#B0ACAA')
    for z in (4.25, 6.77, 9.27):
        polygon(canvas, cam, [(-7.88, .005, z), (-7.88, .005, z+.85),
                              (1.20, .005, z+1.80), (1.20, .005, z+.95)], '#FFF7E5')
    for x in np.arange(-7.7, 8, .40):
        segment(canvas, cam, (x, .008, -.7), (x, .008, back), 1.3,
                '#A5A5AB')
    horizontal(canvas, cam, -1.06, -.7, 1.06, 9.5, .012, '#364567', INK, 3)
    for x in (-.93, .93):
        segment(canvas, cam, (x, .016, -.7), (x, .016, 9.46), 1.7, '#B49B7A')
    side_wall(canvas, cam, -7.9, 0, -.7, 5.16, back, '#D4CAB8')
    side_wall(canvas, cam, 7.9, 0, -.7, 5.16, back, '#BBB6AC')
    for z in (3.4, 7.2, 10.80):
        sash_window(canvas, cam, -7.89, z, 1.9)
        side_wall(canvas, cam, 7.89, .83, z+.08, 3.52, z+1.92,
                  '#CEC4B3', '#4D5A75', 3.5)
    for x in (-7.87, 7.87):
        side_wall(canvas, cam, x, .15, -.7, .93, back, '#A9A4A0', INK, 2.5)
        segment(canvas, cam, (x, .92, -.7), (x, .92, back), 4, '#B59674')
        segment(canvas, cam, (x, 4.82, -.7), (x, 4.82, back), 4, '#A58B73')
    face(canvas, cam, -7.90, 0, 7.90, 5.16, back, '#DED5C3', INK, 4)
    for x in (-7.2, -5.6, -4.0):
        polygon(canvas, cam, [(x, 5.16, back-.01), (x+1.18, 5.16, back-.01),
                              (x+3.21, 2.06, back-.01), (x+2.03, 2.06, back-.01)], '#FFF7E5')
    face(canvas, cam, -7.84, .34, 7.84, 2.09, back-.044, '#AAA69D', '#485C85', 3)
    face(canvas, cam, -3.16, 1.91, 3.16, 4.64, back-.067,
         '#EEE1C7', INK, 3)
    for x in (-7.36, -4.64, 4.64, 7.36):
        face(canvas, cam, x-.28, .43, x+.28, 4.82, back-.082,
             '#E9DCC5', INK, 3)
        for offset in (-.14, 0, .14):
            segment(canvas, cam, (x+offset, .74, back-.092), (x+offset, 4.60, back-.092), 2, '#B8A182')
    for x in (-6.01, 6.01):
        face(canvas, cam, x-.94, .12, x+.94, 3.29, back-.05, '#80654F', INK, 3)
        face(canvas, cam, x-.78, .31, x+.78, 3.16, back-.08,
             '#BCAD98', '#645045', 2)
        segment(canvas, cam, (x+.5, 1.43, back-.11), (x+.65, 1.43, back-.11), 4, BRASS)
    scales_medallion(canvas, cam, back-.10, height=3.83)
    horizontal(canvas, cam, -7.9, -.7, 7.9, back, 5.16, '#2C3B57')
    for z in (1.6, 4.2, 6.8, 9.4, 12.2):
        horizontal(canvas, cam, -7.86, z, 7.86, z+.15, 5.11, '#344363', '#465675', 2)

    box(canvas, cam, -4.24, 0, 9.82, 4.06, .18, back-.15, '#A29078', WOOD, WOOD_DARK, 4)
    box(canvas, cam, -3.61, .18, 10.54, 3.42, .36, back-.17, '#B1997C', WOOD, WOOD_DARK, 4)
    chair_left, chair_bottom = cam.point((-.56, 1.38, 11.77))
    chair_right, chair_top = cam.point((.56, 2.38, 11.77))
    kit.rect(canvas, chair_left, chair_top, chair_right, chair_bottom,
             '#5E6F8D', 4, r=12, v=INK)
    kit.rect(canvas, chair_left+7, chair_top+7, chair_right-7, chair_bottom-3,
             '#455371', 2, r=8, v='#8391AE')
    for offset in (23, 34):
        kit.line(canvas, chair_left+13, chair_top+offset, chair_right-13, chair_top+offset,
                 1.8, '#647996')
    draw_furniture(canvas, cam)


def draw_furniture(canvas, cam=None):
    if cam is None:
        cam = court_bench_camera()
    zoom = cam.focal / COURT_WIDE.focal
    box(canvas, cam, -3.00, .36, 10.59, 2.97, 1.48, 11.63, '#CCAD88', WOOD, WOOD_DARK, 4)
    panel_front(canvas, cam, -3.02, 3.00, .39, 1.41, 10.563, 3, True)
    horizontal(canvas, cam, -3.08, 10.52, 3.09, 11.65, 1.51,
               '#F1E1C5', INK, 4)
    bench_props(canvas, cam)
    lamp_x, lamp_y = cam.point((-1.90, 1.51, 10.99))
    canvas.save()
    canvas.translate(lamp_x, lamp_y)
    canvas.scale(.33*zoom, .33*zoom)
    lamp(canvas, 0, 0)
    canvas.restore()

    box(canvas, cam, -4.98, .14, 9.59, -3.46, 1.21, 10.75, '#BC9D79', WOOD, WOOD_DARK, 3)
    panel_front(canvas, cam, -5.00, -3.43, .22, 1.14, 9.56, 1, True)

    for z in reversed((6.13, 6.9, 7.67, 8.44, 9.21)):
        for x in (4.50, 5.45, 6.41):
            face(canvas, cam, x-.33, .54, x+.33, 1.30, z+.18, '#685D63', INK, 2.7)
    box(canvas, cam, 3.91, .01, 5.84, 6.96, .91, 6.15, '#B3926D', WOOD, WOOD_DARK, 3)
    panel_front(canvas, cam, 3.91, 6.96, .10, .86, 5.81, 3, True)
    side_wall(canvas, cam, 3.91, .13, 5.85, .91, 9.97, '#9B795F', INK, 3.4)
    segment(canvas, cam, (3.89, .92, 5.85), (3.89, .92, 9.97), 3, '#BD9B74')

    counsel_table(canvas, cam, -4.73, -1.91, 5.62)
    counsel_table(canvas, cam, 1.33, 3.67, 5.95)
    for x, z in ((-3.95, 5.14), (-2.69, 5.14), (1.93, 5.47), (2.96, 5.47)):
        box(canvas, cam, x-.28, .35, z, x+.28, .97, z+.15, '#806854', '#6D574A', '#4E443E', 3)
        face(canvas, cam, x-.20, .51, x+.20, .88, z-.012, '#8B7360', INK, 2)
    for x0, x1 in ((-7.75, -1.17), (1.17, 7.75)):
        panel_front(canvas, cam, x0, x1, .08, .60, 3.55, 5)
        horizontal(canvas, cam, x0-.04, 3.47, x1+.04, 3.66, .64, '#B0957A', INK, 3.1)
    for z in (2.47, 1.53, .54):
        gallery_bench(canvas, cam, True, z)
        gallery_bench(canvas, cam, False, z)

def judge_at_bench(canvas, cam):
    x, y = cam.point((0, .36, 11.76))
    scale = cam.scale(11.76)*.00455
    spec = person('retiree', hair='silver', hair_col='#A9ADBC', suit='#202B40',
                  suit_d='#101727', outfit='sweater', face_shape=(1.06, .94))
    _, bench_edge = cam.point((0, 1.51, 11.65))
    canvas.save()
    canvas.clipRect(skia.Rect(0, 0, W, bench_edge), doAntiAlias=True)
    kit.draw_char(canvas, x, y, scale, spec, face=-.11, light=-1, rim='#FFE3A6',
                  eyes='half', mouth='flat', brow=-.15, arms=('down', 'down'))
    canvas.restore()


def court_bench_camera():
    zoom = 2.17
    return Camera(center=960, horizon=H*.50+(COURT_WIDE.horizon-444)*zoom,
                  eye_x=COURT_WIDE.eye_x, eye_y=COURT_WIDE.eye_y,
                  focal=COURT_WIDE.focal*zoom, offset=COURT_WIDE.offset)


def draw(canvas):
    courtroom(canvas, court_bench_camera())
