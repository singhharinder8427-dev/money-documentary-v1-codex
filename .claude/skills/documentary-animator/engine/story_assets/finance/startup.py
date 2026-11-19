"""Collaborative startup space, drawn with Dirty Dollar's daytime print."""
from engine import kit
from engine.core import F_LABEL, GOLD
from engine.widgets import text

r,p,l,o=kit.rect,kit.poly,kit.line,kit.oval
NAVY='#283B5C'
DARK='#171A21'
CREAM='#F7EFDD'

def laptop(c,x,y):
    p(c,[(x,y),(x+73,y-7),(x+74,y+37),(x+1,y+41)],NAVY,3)
    p(c,[(x+5,y+4),(x+69,y-2),(x+70,y+31),(x+6,y+35)],'#8094AE',1)
    l(c,x+12,y+16,x+38,y+13,2,CREAM)
    l(c,x+12,y+24,x+52,y+20,1.3,'#273C60')
    p(c,[(x+1,y+41),(x+74,y+37),(x+88,y+46),(x+8,y+50)],CREAM,2)

def stool(c,x,y):
    o(c,x-24,y-6,x+24,y+5,NAVY,2)
    l(c,x-15,y+4,x-21,y+48,3,DARK)
    l(c,x+15,y+4,x+21,y+48,3,DARK)
    l(c,x-18,y+28,x+18,y+28,2,DARK)

def scene(c):
    c.save()
    c.scale(2,2)
    c.clear(kit.hx('#DFD9CF'))
    p(c,[(0,0),(960,0),(820,70),(145,70)],'#D9D4C8',2)
    p(c,[(0,0),(145,70),(145,362),(0,404)],'#B0A194',2)
    p(c,[(820,70),(960,0),(960,404),(820,362)],'#B2ADA6',2)
    r(c,145,70,820,362,'#C9BAA8',2)
    # Brick texture on the loft wall.
    for y in range(77,358,15):
        l(c,148,y,817,y,1.45,'#6D8199')
        for x in range(149+(y//15%2)*18,817,36):
            l(c,x,y,x,y+14,1.45,'#6D8199')
    p(c,[(0,404),(145,362),(820,362),(960,404),(960,540),(0,540)],'#B8B9B5',2)
    for x in range(-400,1400,90):
        l(c,480+(x-480)*.2,362,x,540,1,'#9D9F9F')
    for y in (410,449,496):
        l(c,0,y,960,y,1,'#9D9F9F')
    # Tall industrial windows and skyline.
    for left in (160,300):
        r(c,left,96,left+124,313,NAVY,3)
        r(c,left+6,102,left+118,307,'#E2EAF1',1)
        for i in range(5):
            x=left+9+i*22
            h=34+(i*31+left)%93
            r(c,x,306-h,x+19,306,('#687E9F' if i%2 else '#4E668B'),0)
            for yy in range(310-h,303,13):
                r(c,x+5,yy,x+8,yy+4,CREAM,0)
        for dx in (40,80):
            l(c,left+dx,102,left+dx,307,3,NAVY)
        for y in (166,236):
            l(c,left+6,y,left+118,y,3,NAVY)
    # Window light breaks up the tinted floor.
    for x in (153,216,280):
        p(c,[(x,364),(x+46,364),(x+5,537),(x-55,537)],CREAM,0)
    # Planning wall and pinned notes.
    r(c,485,103,787,282,'#B5A998',2)
    r(c,493,111,779,274,CREAM,2.5)
    text(c,'PROJECT PLAN',510,135,15,NAVY,F_LABEL)
    l(c,510,144,763,144,1.5,'#60789B')
    for x,y,col in ((518,159,GOLD),(556,157,'#B4C4D3'),(596,159,'#D2C5A9'),(644,156,GOLD),(690,157,'#B4C4D3'),(530,206,'#B4C4D3'),(576,207,GOLD),(624,207,'#D2C5A9'),(677,205,GOLD)):
        r(c,x,y,x+30,y+29,col,1)
        l(c,x+5,y+10,x+24,y+10,1,NAVY)
        l(c,x+5,y+16,x+20,y+16,1,NAVY)
    for x in (585,710):
        l(c,x,0,x,54,2,DARK)
        p(c,[(x-13,53),(x+13,53),(x+24,76),(x-24,76)],NAVY,2)
        l(c,x-20,77,x+20,77,3,GOLD)
    # Shared table and laptops.
    p(c,[(262,344),(680,333),(791,400),(191,415)],'#F3E8CC',3)
    p(c,[(191,415),(791,400),(791,411),(191,426)],'#4C6282',2)
    for x,y in ((242,425),(732,413)):
        l(c,x,y,x-10,y+96,7,NAVY)
    laptop(c,322,317)
    laptop(c,514,311)
    for x,y in ((454,366),(641,367)):
        r(c,x,y,x+18,y+18,CREAM,2,3)
        o(c,x+17,y+4,x+25,y+13,None,2)
    p(c,[(568,373),(612,370),(621,379),(576,382)],CREAM,1)
    for n in range(3):
        l(c,577,375+n*2,605,373+n*2,1,NAVY)
    o(c,251,487,312,495,'#889AB6',0)
    o(c,480,491,561,499,'#889AB6',0)
    o(c,701,474,776,482,'#889AB6',0)
    stool(c,284,442)
    stool(c,520,447)
    stool(c,738,431)
    c.restore()
