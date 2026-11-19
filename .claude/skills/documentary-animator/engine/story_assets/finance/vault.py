"""A bank vault interior drawn with Dirty Dollar night print."""
import math
from engine import kit

r,p,l,d=kit.rect,kit.poly,kit.line,kit.circ
NAVY='#263A58'
GOLD='#FCA311'
PAPER='#E6E1D5'
INK='#1C212A'

def scene(c):
    c.save()
    c.scale(2,2)
    c.clear(kit.hx('#747E8B'))
    p(c,[(0,0),(960,0),(818,83),(140,83)],'#A5ABB0',2)
    p(c,[(0,0),(140,83),(140,412),(0,479)],'#788391',2)
    p(c,[(818,83),(960,0),(960,479),(818,412)],'#697687',2)
    r(c,140,83,818,412,'#535F75',2)
    p(c,[(0,479),(140,412),(818,412),(960,479),(960,540),(0,540)],'#858D97',2)
    for x in range(-300,1300,100):
        l(c,480+(x-480)*.3,413,x,540,1,'#B1B4B3')
    for y in (449,491,537):
        l(c,0,y,960,y,1,'#ADB1B3')
    # Walls of individually lockable deposit boxes.
    for x in range(482,796,57):
        for y in range(106,385,41):
            r(c,x,y,x+52,y+37,'#78869A',1.7)
            l(c,x+3,y+33,x+48,y+33,1.2,'#495874')
            r(c,x+8,y+7,x+25,y+13,PAPER,1)
            d(c,x+42,y+24,3,NAVY,1)
            l(c,x+7,y+29,x+24,y+29,1,NAVY)
    # Heavy circular vault door with concentric steel rings.
    d(c,294,245,198,'#4F6071',4,INK)
    d(c,294,245,181,'#B3BBC0',4,INK)
    d(c,294,245,161,'#748697',4,INK)
    d(c,294,245,144,'#748491',3,INK)
    for tilt in (-23, -15, -7):
        l(c,217,197+tilt,324,129+tilt,2,'#B4BCC5')
    for angle in range(0,360,30):
        a=math.radians(angle)
        dx,dy=math.cos(a),math.sin(a)
        d(c,294+171*dx,245+171*dy,7,'#D9D7CA',2,INK)
        l(c,294+64*dx,245+64*dy,294+128*dx,245+128*dy,4,NAVY)
    d(c,294,245,71,'#8393A1',3,INK)
    d(c,294,245,55,'#435577',3,INK)
    for angle in range(0,360,45):
        a=math.radians(angle)
        l(c,294,245,294+50*math.cos(a),245+50*math.sin(a),3.5,'#AEB8C8')
    d(c,294,245,12,GOLD,3,INK)
    r(c,82,212,116,281,'#838F99',3,3)
    for y in (222,240,258,274):
        l(c,89,y,107,y,2,NAVY)
    # Evidence boxes on a low trolley.
    r(c,547,98,693,105,'#1D2D47',2)
    l(c,553,103,687,103,2,GOLD)
    for x,y in ((593,372),(676,372),(634,337)):
        r(c,x,y,x+75,y+35,'#A4A094',2,2)
        r(c,x-2,y-3,x+77,y+5,PAPER,2,2)
        r(c,x+25,y+12,x+49,y+23,PAPER,1)
        l(c,x+29,y+17,x+45,y+17,1,NAVY)
    r(c,572,409,768,419,'#5C6B77',2)
    for x in (584,756):
        l(c,x,419,x,443,5,INK)
        d(c,x,448,6,NAVY,2)
    c.restore()
    return [((542,385),360,243,.57),((1326,761),327,153,.62)]
