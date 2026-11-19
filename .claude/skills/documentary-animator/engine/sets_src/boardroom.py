"""The approved daytime boardroom and its conference table layer."""

import random

import numpy as np

from engine import kit
from engine.core import GOLD
from engine.sets_src.sales_floor import Camera, box, face, horizontal, polygon, segment, side_wall

CAMERA = Camera(center=1120, horizon=322, eye_x=1.81, eye_y=2.65, focal=960, offset=3.74)
CHAIR_DEPTHS = (1.12, 2.62, 4.20, 5.78, 7.36, 8.94, 10.52, 12.10)
INK = '#161820'
WOOD_DARK = '#68564F'
BRASS = '#E1B162'
PAPER = '#F8EDD3'

SPOTS = {
    'head_of_table': (*CAMERA.point((.10, 0, 13.65)), .28),
    'window_aisle': (*CAMERA.point((4.41, 0, 4.0)), .68),
    'near_table': (*CAMERA.point((.40, 0, .18)), 1.06),
}


def daytime_city_view(canvas, cam, x):
    """Give the skyline its own cool value range inside the navy window frames."""
    side_wall(canvas, cam, x, 0, -.75, 4.05, 15.4, '#EDE1C9')
    side_wall(canvas, cam, x-.01, .63, -.75, 3.93, 15.4, '#B8C7DA')

    rng = random.Random(211)
    for z in np.arange(-.6, 15.2, .60):
        height = rng.uniform(1.13, 2.52)
        width = rng.uniform(.38, .57)
        side_wall(canvas, cam, x-.02, .63, z, height, min(z+width, 15.4), '#8493AD')

    towers = (
        (3.24, .71, 2.44, '#293A5C'), (4.24, .92, 3.09, '#1D2C4C'),
        (5.66, .82, 2.41, '#506285'), (6.81, .54, 1.88, '#4C6087'),
        (7.75, 1.16, 3.23, '#31476B'), (9.41, .84, 2.41, '#1D2C4C'),
        (10.73, .65, 1.71, '#506285'), (11.68, .68, 2.72, '#31476B'),
        (12.78, .82, 2.02, '#506285'), (13.85, 1.24, 2.86, '#35476B'),
    )
    for z, width, height, color in towers:
        side_wall(canvas, cam, x-.034, .64, z, height, z+width, color)
        side_wall(canvas, cam, x-.036, height, z+width*.56, height+.14, z+width*.88, color)
        side_wall(canvas, cam, x-.038, .64, z+.055, height, z+width*.19, '#687DA3')
        for level in np.arange(.92, height-.12, .23):
            for offset in (.30, .58, .81):
                start = z+width*offset
                side_wall(canvas, cam, x-.039, level, start, level+.060,
                          start+width*.108, '#C5D0E0')

    for z in (.5, 3.5, 6.5, 9.5, 12.5, 15.3):
        side_wall(canvas, cam, x-.055, .59, z-.055, 3.98, z+.055, INK)
        segment(canvas, cam, (x-.06, .69, z+.057), (x-.06, 3.91, z+.057),
                2, '#859FC4')
    for height, width in ((.61, 6.5), (3.94, 5.5)):
        segment(canvas, cam, (x-.065, height, -.75), (x-.065, height, 15.4), width, INK)


def executive_chair(canvas, cam, x, z, left):
    """Facing the table across the room, with its back and seat drawn in perspective."""
    side = -1 if left else 1
    scale = cam.scale(z)
    px, py = cam.point((x, .013, z))
    kit.oval(canvas, px-scale*.45, py-7, px+scale*.43, py+8,
             '#959CAA', 0)
    for dx, dz in ((-.32, -.19), (.31, -.16), (.08, .29)):
        segment(canvas, cam, (x, .12, z), (x+dx, .035, z+dz), 3.8,
                '#455775')
        kit.circ(canvas, *cam.point((x+dx, .044, z+dz)), max(2, scale*.03), INK, 0)
    segment(canvas, cam, (x, .11, z), (x, .54, z), 6, '#52627D')
    box(canvas, cam, x-.29, .46, z-.35, x+.29, .55, z+.36,
        '#67748A', '#45536D', '#323B53', 3)
    bx = x+side*.30
    shape = [(bx, .50, z-.36), (bx+side*.10, 1.32, z-.32),
             (bx+side*.10, 1.37, z+.35), (bx, .50, z+.37)]
    polygon(canvas, cam, shape, '#43516B', INK, 4)
    segment(canvas, cam, (bx+side*.045, .86, z-.32), (bx+side*.045, .86, z+.33), 1.8, '#7D8EA8')
    for dz in (-.33, .32):
        segment(canvas, cam, (x, .54, z+dz), (x, .75, z+dz), 3.3, '#75849C')
        segment(canvas, cam, (x-.19, .75, z+dz), (x+.20, .75, z+dz), 4.5, '#576984')


def board_packet(canvas, cam, x, z, closed):
    color = '#435C83' if closed else '#DFD0AE'
    horizontal(canvas, cam, x-.25, z-.24, x+.25, z+.29, .975, '#A99580', INK, 2.5)
    horizontal(canvas, cam, x-.27, z-.23, x+.24, z+.29, .995, color, INK, 2)
    for line in (0, 1, 2):
        segment(canvas, cam, (x-.15, 1.001, z+.13-line*.086),
                (x+.12, 1.001, z+.13-line*.086), 1.4, '#B7B3A9' if closed else '#6B5C52')
    if closed:
        horizontal(canvas, cam, x+.16, z-.12, x+.24, z+.21, 1.006, GOLD)


def draw_table(canvas):
    """The table, board packets, and carafe in front of actors."""
    cam = CAMERA
    for z in (1.35, 6.12, 10.85):
        box(canvas, cam, -.90, .05, z, .93, .83, z+.70, WOOD_DARK,
            '#485B7B', '#716459', 4)
        face(canvas, cam, -.74, .11, .76, .77, z-.008,
             '#627493', INK, 2.5)
    top = [(-1.60, .94, .22), (1.60, .94, .22), (1.97, .94, .88),
           (1.80, .94, 12.48), (1.48, .94, 13.06), (-1.48, .94, 13.06),
           (-1.80, .94, 12.48), (-1.97, .94, .88)]
    polygon(canvas, cam, [(x, y-.108, z) for x, y, z in top], '#715850', INK, 4)
    polygon(canvas, cam, top, '#D0C2AA', INK, 5)
    for z in (1.22, 4.05, 7.04, 10.07):
        polygon(canvas, cam, [(1.75, .942, z), (1.75, .942, z+1.74),
                              (-.96, .942, z+2.24), (-.96, .942, z+.50)],
                '#FAF0D9')
    for x in np.linspace(-1.52, 1.52, 21):
        segment(canvas, cam, (x, .944, .28), (x*.95, .944, 12.89), 1.1,
                '#CCC2AF')
    horizontal(canvas, cam, -.13, 1.1, .13, 12.52, .95, '#5A514F', INK, 3)
    for z in (2.85, 6.2, 9.48):
        horizontal(canvas, cam, -.11, z, .11, z+.38, .954, '#8296AC', INK, 2)
    for x, z, closed in ((-1.23, 1.6, False), (1.25, 2.74, True), (-1.22, 4.20, True),
                          (1.25, 6.62, False), (-1.24, 9.54, False)):
        board_packet(canvas, cam, x, z, closed)
    x, y = cam.point((.55, 1.42, 4.19))
    s = cam.scale(4.19)
    kit.poly(canvas, [(x-s*.06, y), (x+s*.07, y), (x+s*.11, y+s*.10),
                      (x+s*.095, y+s*.43), (x-s*.10, y+s*.43), (x-s*.10, y+s*.10)],
             '#799BC9', 2.2, INK)
    kit.line(canvas, x-s*.05, y+s*.14, x-s*.05, y+s*.34, 2.5, PAPER)


def draw(canvas):
    """Draw the daylight room and its furniture with the approved perspective."""
    cam = CAMERA
    back = 15.38
    horizontal(canvas, cam, -7.4, -.75, 7.4, back, 0, '#B0B2B4')
    for z in range(0, 16):
        segment(canvas, cam, (-7.4, .006, z), (7.4, .006, z), 1,
                '#919FB1')
    for z in (.64, 3.57, 6.54, 9.57, 12.69):
        polygon(canvas, cam, [(7.4, .008, z), (7.4, .008, z+2.32),
                              (1.04, .008, z+2.53), (1.04, .008, z+.21)],
                '#FDF5E2')
    side_wall(canvas, cam, -7.4, 0, -.75, 4.05, back, '#DFD0B6')
    for z in np.arange(0, back, .44):
        segment(canvas, cam, (-7.385, .20, z), (-7.385, 3.90, z), 2,
                '#B2A895')
    daytime_city_view(canvas, cam, 7.4)
    face(canvas, cam, -7.4, 0, 7.4, 4.05, back, '#EBE1CD', INK, 2)
    face(canvas, cam, -6.4, .43, -2.73, 3.41, back-.03, '#38445B', INK, 5)
    face(canvas, cam, -6.09, .63, -3.02, 3.18, back-.05, '#222E47', '#637CA7', 2)
    face(canvas, cam, 3.79, 0, 6.50, 3.24, back-.04, '#695952', INK, 3.5)
    face(canvas, cam, 4.02, .31, 6.29, 2.96, back-.06,
         '#CEBEA5', '#514B4C', 2)
    segment(canvas, cam, (4.25, 1.40, back-.08), (4.46, 1.40, back-.08), 4, BRASS)
    horizontal(canvas, cam, -7.4, -.75, 7.4, back, 4.05, '#F1E5D0')
    horizontal(canvas, cam, -3.15, -.65, 3.8, back, 4.02,
               '#BCB2A0', INK, 4)
    for z in (.8, 3.9, 7, 10.1, 13.2):
        horizontal(canvas, cam, -3.18, z, 3.84, z+.08, 4.01, PAPER, INK, 1.4)
    for z in np.arange(0, back, 1.35):
        segment(canvas, cam, (-3.09, 4.018, z), (3.72, 4.018, z), 1.4,
                '#A49B8C')
    for z in reversed(CHAIR_DEPTHS):
        executive_chair(canvas, cam, -2.65, z, left=True)
    executive_chair(canvas, cam, -.04, 13.77, left=True)

    horizontal(canvas, cam, -1.76, .61, 1.89, 13.05, .016, '#929BAC')
    draw_table(canvas)
    for z in reversed(CHAIR_DEPTHS):
        executive_chair(canvas, cam, 2.65, z, left=False)
