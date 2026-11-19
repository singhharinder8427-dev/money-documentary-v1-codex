"""Reusable furniture and dressing with a consistent local coordinate system."""
from .drawing import (
    BLUE, CREAM, GOLD, INK, MIST, NAVY, OUTLINE, PAPER, SLATE, WHITE, dot, kit, label, line, mic, oval, poly, rect,
)


def desk(c, x, y, w, depth=62, fill=CREAM):
    poly(c, [(x+24,y-depth),(x+w-24,y-depth),(x+w,y),(x,y)], fill, 2.5)
    rect(c,x,y,x+w,y+12,NAVY,2)
    rect(c,x+13,y+12,x+23,y+74,BLUE,2)
    rect(c,x+w-23,y+12,x+w-13,y+74,BLUE,2)


def bench(c, x, y, w=220):
    for offset in (15,w-15):
        line(c,x+offset,y-43,x+offset,y+23,6,OUTLINE)
        line(c,x+offset-7,y+23,x+offset+7,y+23,4,INK)
    for row in range(3):
        rect(c,x,y-49+row*12,x+w,y-40+row*12,BLUE,2,2)
    poly(c,[(x+7,y-11),(x+w-7,y-11),(x+w,y),(x,y)],CREAM,2)


def chair(c,x,y,fill=BLUE):
    oval(c,x-42,y+25,x+43,y+37,'#263857',0)
    for offset in (-25,25):
        line(c,x+offset,y-1,x+offset*1.26,y+31,4,INK)
    rect(c,x-34,y-82,x+34,y-9,fill,2.8,11)
    rect(c,x-28,y-76,x+28,y-18,SLATE,1.5,8)
    poly(c,[(x-33,y-19),(x+33,y-19),(x+40,y-5),(x+39,y+3),(x-39,y+3),(x-40,y-5)],fill,2.8)


def cabinet(c,x,y,w=110,h=168):
    rect(c,x,y,x+w,y+h,BLUE,3)
    poly(c,[(x,y),(x+14,y-13),(x+w+14,y-13),(x+w,y)],MIST,2)
    poly(c,[(x+w,y),(x+w+14,y-13),(x+w+14,y+h-13),(x+w,y+h)],NAVY,2)
    for i in range(3):
        top=y+5+i*(h-6)/3
        rect(c,x+5,top,x+w-5,top+(h-18)/3,SLATE,1.5)
        rect(c,x+w*.33,top+6,x+w*.67,top+15,CREAM,1)
        line(c,x+w*.37,top+24,x+w*.63,top+24,3,INK)


def podium(c,x,y,w=113):
    rect(c,x+10,y-100,x+w-10,y,NAVY,3)
    rect(c,x+21,y-86,x+w-21,y-12,BLUE,2)
    poly(c,[(x-4,y-112),(x+w-8,y-112),(x+w+3,y-96),(x,y-96)],CREAM,3)
    rect(c,x,y-6,x+w,y+4,INK,1)
    mic(c,x+w*.62,y-106,.9)


def queue_posts(c,x,y,w=155):
    path=kit.skia.Path()
    path.moveTo(x,y-62)
    path.quadTo(x+w*.5,y-31,x+w,y-62)
    c.drawPath(path,kit.ink(8,INK))
    c.drawPath(path,kit.ink(4,SLATE))
    for xx in (x,x+w):
        oval(c,xx-13,y-3,xx+13,y+4,NAVY,1.5)
        line(c,xx,y-69,xx,y,7,INK)
        line(c,xx,y-69,xx,y,3.5,SLATE)
        dot(c,xx,y-70,6,GOLD,1.5)


def street_sign(c,x,y,name='MAIN ST'):
    line(c,x,y-115,x,y,8,INK)
    line(c,x,y-115,x,y,3.4,SLATE)
    rect(c,x-53,y-110,x+54,y-85,BLUE,2,3)
    label(c,name,x,y-92,17,WHITE,'center')
    rect(c,x-29,y-79,x+77,y-57,SLATE,2,3)
    label(c,'2ND AVE',x+24,y-63,14,INK,'center')


def lamp(c,x,y):
    oval(c,x-41,y-9,x+41,y+8,BLUE,2.5)
    line(c,x,y,x,y-59,7,INK)
    line(c,x-1,y-1,x-1,y-57,2.5,SLATE)
    poly(c,[(x-41,y-83),(x+41,y-83),(x+31,y-58),(x-31,y-58)],GOLD,2.5)
    line(c,x-29,y-62,x+29,y-62,2.4,PAPER)


def rotary_phone(c,x,y,scale=1):
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    poly(c,[(-52,9),(-44,-39),(44,-39),(53,9)],NAVY,3)
    oval(c,-27,-37,27,1,CREAM,2)
    oval(c,-11,-28,11,-8,BLUE,2)
    for xx,yy in ((-19,-18),(-12,-29),(0,-33),(12,-29),(19,-18),(12,-9),(0,-5),(-12,-9)):
        dot(c,xx,yy,2.5,NAVY,0)
    rect(c,-53,-53,53,-35,BLUE,3,8)
    rect(c,-55,-54,-37,-30,NAVY,2,7)
    rect(c,37,-54,55,-30,NAVY,2,7)
    c.restore()


def cubicle(c,x,y):
    poly(c,[(x,y-84),(x+93,y-92),(x+93,y-14),(x,y)],SLATE,2.5)
    poly(c,[(x+93,y-92),(x+176,y-74),(x+176,y+2),(x+93,y-14)],MIST,2.5)
    for xx, yy in [(x,y),(x+93,y-14),(x+176,y+2)]:
        line(c,xx,yy-78,xx,yy+11,4,NAVY)
    line(c,x+5,y-40,x+89,y-50,2,PAPER)
    line(c,x+98,y-50,x+172,y-34,2,PAPER)
