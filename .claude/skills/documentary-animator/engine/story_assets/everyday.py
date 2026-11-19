"""Everyday settings for walks, conversations, and transactions."""
import random
from .drawing import (
    BLUE, CREAM, F_TITLE, GOLD, INK, MIST, NAVY, PAPER, SLATE, WHITE, city_window, dot, floor_seams, kit, label, line, oval, panel_wall, poly, rect, room, skyline,
)
from .furniture import bench, queue_posts, rotary_phone
from .law import panel_door


def tree(c,x,y,scale,seed):
    rng=random.Random(seed)
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    poly(c,[(-13,0),(12,0),(8,-81),(40,-131),(27,-133),(2,-108),(-6,-146),(-18,-142),(-12,-99),(-49,-133),(-57,-128),(-17,-67)],NAVY,2)
    for index in range(29):
        xx=rng.uniform(-72,72)
        yy=rng.uniform(-194,-127)
        radius=rng.uniform(17,36)
        oval(c,xx-radius,yy-radius,xx+radius,yy+radius,
             ('#647A99', '#9AADC5', '#C2B48F', '#B6A276' if scale<1 else '#C2984D')[index%4],0)
    c.restore()


def public_park(c):
    c.clear(kit.hx('#D5E4ED'))
    skyline(c,0,58,960,209)
    rect(c,0,270,960,540,'#B1BCCD',0)
    for i,x in enumerate(range(-18,1020,68)):
        tree(c,x,296,.55,i+57)
    path=kit.skia.Path()
    path.moveTo(448,263)
    path.cubicTo(400,341,418,382,211,540)
    path.lineTo(770,540)
    path.cubicTo(744,429,505,332,489,263)
    path.close()
    kit.shape(c,path,'#F8EFDA',2.4,'#526885')
    for i,(x,y,s) in enumerate(((118,426,1.5),(851,431,1.7),(315,344,.75),(651,359,1.0))):
        tree(c,x,y,s,i+10)
    for x,y,w in ((120,426,220),(851,431,242),(278,348,110)):
        oval(c,x-w/2,y-9,x+w/2,y+10,'#8197B2',0)
    bench(c,38,446,214)
    bench(c,699,467,205)
    for x,y in ((379,348),(618,398)):
        line(c,x,y-93,x,y,4,NAVY)
        dot(c,x,y-94,8,CREAM,1.7)
    rng=random.Random(7)
    for _ in range(72):
        x,y=rng.randint(0,960),rng.randint(342,539)
        if x<235 or x>765:
            oval(c,x,y,x+5,y+2,'#768BA8',0)


def booth(c,x,y,reverse):
    chair_back=[(x,y),(x+96,y-22),(x+96,y-151),(x+24,y-140),(x,y-124)]
    if reverse:
        chair_back=[(2*x+96-xx,yy) for xx,yy in chair_back]
    poly(c,chair_back,BLUE,3)
    for height in (46,72,98):
        x0=x+7
        x1=x+89
        line(c,x0,y-height if not reverse else y-height-17,
             x1,y-height-17 if not reverse else y-height,2,MIST)
    rect(c,x,y-19,x+96,y+3,NAVY,2,5)


def cafe(c):
    room(c, wall='#DAD0BD')
    city_window(c,187,82,580,214)
    panel_wall(c,144,321,672,79,7,SLATE)
    booth(c,175,461,False)
    booth(c,683,461,True)
    rect(c,264,310,333,446,BLUE,2,11)
    rect(c,625,310,698,446,BLUE,2,11)
    poly(c,[(267,407),(325,392),(389,417),(288,445)],SLATE,2)
    poly(c,[(625,394),(687,406),(675,446),(572,421)],SLATE,2)
    oval(c,306,379,660,458,PAPER,3)
    rect(c,474,448,492,512,NAVY,2)
    oval(c,430,505,536,520,BLUE,2)
    for x,y in ((398,413),(558,425)):
        oval(c,x-20,y,x+25,y+10,CREAM,1.7)
        rect(c,x-12,y-15,x+12,y+4,PAPER,2,5)
        oval(c,x+9,y-11,x+20,y+1,None,2)
    poly(c,[(455,416),(491,408),(513,428),(472,437)],CREAM,2)
    line(c,466,419,495,416,1.6,INK)
    rect(c,236,89,375,120,INK,2,4)
    label(c,'COFFEE',305,112,22,WHITE,'center',F_TITLE)
    line(c,483,0,483,76,3,NAVY)
    poly(c,[(459,76),(506,76),(521,99),(444,99)],BLUE,2)
    line(c,449,99,516,99,4,GOLD)


def hallway(c):
    room(c, wall='#AAB6C4', floor='#74849A',left='#879BB6',right='#98A7B7')
    floor_seams(c)
    panel_door(c,108,97,180,284,'204')
    panel_door(c,671,98,180,285,'205')
    rect(c,370,120,590,362,BLUE,3)
    rect(c,383,131,577,362,'#BCC8D3',2)
    line(c,480,134,480,360,3,INK)
    rect(c,441,105,517,121,NAVY,2,2)
    label(c,'2',479,118,13,WHITE,'center')
    poly(c,[(413,365),(546,365),(644,540),(315,540)],'#364C71',2)
    for x in (401,530):
        rect(c,x,57,x+34,65,PAPER,2,2)
    return [((960,460),500,385,.79)]


def shop(c):
    room(c,wall='#DDD6C6')
    floor_seams(c)
    city_window(c,575,87,207,216)
    rect(c,157,83,548,289,'#B5C0CB',3)
    for y in (141,201,274):
        rect(c,160,y,544,y+9,BLUE,2)
        for x in range(170,525,39):
            h=18+((x+y)%19)
            rect(c,x,y-h,x+25,y,(CREAM,SLATE,GOLD)[(x//39+y)%3],1.3,2)
            line(c,x+4,y-h+6,x+20,y-h+6,1.2,NAVY)
    poly(c,[(208,329),(662,329),(822,397),(139,397)],PAPER,3)
    panel_wall(c,139,398,683,93,5,BLUE)
    rect(c,570,334,646,371,NAVY,2,4)
    rect(c,581,338,633,354,MIST,1)
    for x in range(578,637,9):
        line(c,x,359,x,365,2.5,PAPER)
    poly(c,[(268,345),(382,345),(401,371),(257,371)],MIST,2)
    rect(c,291,350,350,366,PAPER,1.6,2)
    queue_posts(c,18,530,116)


def station(c):
    c.clear(kit.hx('#D3D9DE'))
    skyline(c,475,113,485,220)
    rect(c,0,342,960,540,'#9CAEBF',0)
    poly(c,[(0,443),(960,333),(960,443),(0,540)],PAPER,2.8)
    line(c,0,466,960,360,5,SLATE)
    line(c,0,481,960,377,2,BLUE)
    poly(c,[(0,0),(960,0),(960,87),(0,174)],BLUE,3)
    for x in (40,358,713,935):
        line(c,x,95,x,420-x*.09,11,NAVY)
    poly(c,[(495,235),(917,197),(959,216),(959,359),(482,412),(462,389),(462,271)],'#657D9D',3)
    poly(c,[(475,275),(959,221),(959,286),(475,333)],PAPER,1.6)
    for i in range(6):
        x=483+i*77
        y=282-i*8.5
        rect(c,x,y,x+55,y+36,NAVY,2,4)
        line(c,x+8,y+8,x+45,y+8,1.8,MIST)
    rect(c,63,129,450,246,NAVY,3,6)
    label(c,'DEPARTURES',82,158,23,WHITE)
    for y,destination,departure in ((189,'Riverside','10:24'),(222,'Central','10:41')):
        line(c,80,y-21,430,y-21,1.2,SLATE)
        label(c,destination,83,y,20,WHITE)
        label(c,departure,424,y,20,GOLD,'right')
    bench(c,102,416,226)


SETS = [
    ('public-park','Public park',public_park,False),
    ('cafe-booth','Café booth',cafe,False),
    ('apartment-hallway','Apartment hallway',hallway,True),
    ('shop-counter','Small-business shop counter',shop,False),
    ('train-station','Train station',station,False),
]
