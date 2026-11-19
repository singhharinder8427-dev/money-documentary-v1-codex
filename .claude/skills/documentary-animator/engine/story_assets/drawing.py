"""Palette and drawing primitives for the Dirty Dollar preview assets."""
from engine import kit
from engine.core import F_LABEL, F_LABEL2, F_TITLE, F_TYPE
from engine.widgets import text

INK = '#14213D'
NAVY = '#293D64'
BLUE = '#485F84'
SLATE = '#7187A8'
MIST = '#AEBBD0'
PAPER = '#F8EFDA'
CREAM = '#EDE4CF'
WHITE = '#FFFFFF'
GOLD = '#FCA311'
OUTLINE = '#171A23'

rect, poly, line, oval, dot = kit.rect, kit.poly, kit.line, kit.oval, kit.circ


def label(canvas, value, x, y, size=20, color=INK, align='left', font=F_LABEL):
    text(canvas, value, x, y, size, color, font, align)


def room(canvas, wall=CREAM, floor=MIST, left='#8B9DB5', right='#B2BECD'):
    """A 16:9 stage in 960 by 540 design coordinates."""
    canvas.clear(kit.hx(wall))
    poly(canvas, [(0, 0), (144, 59), (144, 361), (0, 405)], left, 2)
    poly(canvas, [(816, 59), (960, 0), (960, 406), (816, 361)], right, 2)
    poly(canvas, [(0, 405), (144, 361), (816, 361), (960, 406), (960, 540), (0, 540)], floor, 2)
    poly(canvas, [(0, 0), (960, 0), (816, 59), (144, 59)], '#CBD2D6', 2)


def floor_seams(canvas, horizon=359, color='#8193AB'):
    for end in range(-400, 1401, 110):
        line(canvas, 480+(end-480)*.22, horizon, end, 540, 1.4, color)
    for y in (397, 444, 507):
        line(canvas, 0, y, 960, y, 1.4, color)


def panel_wall(canvas, x, y, w, h, count=5, color='#8D9DAD'):
    rect(canvas, x, y, x+w, y+h, color, 2)
    for index in range(count):
        left = x + index*w/count
        rect(canvas, left+5, y+5, left+w/count-5, y+h-5, color, 1.6, v='#536785')


def skyline(canvas, x, y, w, h, night=False):
    rect(canvas, x, y, x+w, y+h, NAVY if night else '#E3EAF0', 0)
    for index in range(11):
        step = w/11
        left = x+index*step
        height = h*(.24+((index*37)%70)/100)
        fill = (BLUE, NAVY, SLATE)[index%3] if night else ('#5A7093', '#435A7F', '#8FA3BE')[index%3]
        rect(canvas, left, y+h-height, left+step*.91, y+h, fill, 0)
        for row in range(1, int(height/14)):
            for offset in (.18, .54):
                shade = GOLD if night and (row+index)%4 == 1 else '#C4CFDA'
                rect(canvas, left+step*offset, y+h-height+row*14, left+step*(offset+.15),
                     y+h-height+row*14+4, shade, 0)


def city_window(canvas, x, y, w, h, night=False):
    rect(canvas, x-5, y-5, x+w+5, y+h+5, INK, 2)
    skyline(canvas, x, y, w, h, night)
    for frac in (.33, .66):
        line(canvas, x+w*frac, y, x+w*frac, y+h, 4, INK)
    line(canvas, x, y+h*.41, x+w, y+h*.41, 4, INK)
    rect(canvas, x-9, y+h, x+w+9, y+h+6, CREAM, 2)


def mic(canvas, x, y, scale=1):
    oval(canvas, x-13*scale, y-3*scale, x+13*scale, y+3*scale, NAVY, 1.5)
    line(canvas, x, y, x-5*scale, y-15*scale, 2.5*scale, OUTLINE)
    line(canvas, x-5*scale, y-15*scale, x-13*scale, y-20*scale, 2.5*scale, OUTLINE)
    oval(canvas, x-18*scale, y-23*scale, x-9*scale, y-17*scale, BLUE, 1)
