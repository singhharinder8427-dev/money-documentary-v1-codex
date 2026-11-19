"""Wealth, publicity, and media backgrounds."""
from .drawing import (
    BLUE, CREAM, F_TITLE, GOLD, INK, MIST, NAVY, OUTLINE, PAPER, SLATE, WHITE, city_window, dot, floor_seams, kit, label, line, mic, oval, panel_wall, poly, rect, room,
)
from .furniture import chair, lamp, podium
from .everyday import tree


def sash(c,x,y,w,h):
    rect(c,x-4,y-4,x+w+4,y+h+4,CREAM,2)
    rect(c,x,y,x+w,y+h,NAVY,2)
    poly(c,[(x+3,y+h*.68),(x+w*.64,y+3),(x+w*.82,y+3),(x+w*.2,y+h*.69)],SLATE,0)
    line(c,x+w*.5,y,x+w*.5,y+h,2,PAPER)
    line(c,x,y+h*.5,x+w,y+h*.5,2,PAPER)


def mansion(c):
    c.clear(kit.hx('#D5E2E9'))
    for x,y,w in ((93,76,133),(582,64,166)):
        oval(c,x,y,x+w,y+24,PAPER,0)
        oval(c,x+w*.25,y-13,x+w*.9,y+25,PAPER,0)
    rect(c,0,359,960,540,'#A3B2C2',0)
    poly(c,[(180,219),(303,147),(699,147),(844,230),(845,398),(166,398)],'#ABB8C7',2.8)
    rect(c,247,183,750,395,CREAM,2.5)
    rect(c,164,235,278,390,'#C3CDD3',2.5)
    rect(c,730,235,842,390,'#B9C3CB',2.5)
    poly(c,[(151,233),(208,181),(287,235)],BLUE,2.7)
    poly(c,[(721,237),(782,181),(853,236)],BLUE,2.7)
    poly(c,[(221,186),(313,118),(684,118),(781,186)],NAVY,3)
    for y in (133,151,167):
        inset=(185-y)*1.23
        line(c,225+inset,y,777-inset,y,1.6,SLATE)
    for x in (283,578,668):
        sash(c,x,212,42,58)
        sash(c,x,304,46,64)
    for x in (193,770):
        sash(c,x,260,38,74)
    poly(c,[(348,258),(485,177),(624,258)],PAPER,3)
    poly(c,[(368,253),(485,192),(601,253)],SLATE,2)
    oval(c,463,216,505,246,CREAM,2)
    rect(c,358,257,613,270,CREAM,2)
    rect(c,402,273,567,394,NAVY,2.5)
    sash(c,450,284,67,108)
    for x in (375,591):
        rect(c,x-11,271,x+11,391,PAPER,2)
        rect(c,x-16,384,x+16,395,CREAM,2)
    for y,w in ((393,135),(404,149),(415,163)):
        rect(c,485-w,y,485+w,y+11,PAPER,2)
    poly(c,[(322,427),(649,427),(822,540),(151,540)],CREAM,2)
    for x,y,s,seed in ((86,427,1.34,16),(884,433,1.38,32),(279,406,.53,2),(705,410,.61,9)):
        tree(c,x,y,s,seed)


def sofa(c,x,y,w):
    rect(c,x+8,y-104,x+w-8,y-21,BLUE,3,17)
    for index in range(3):
        left=x+17+index*(w-34)/3
        rect(c,left,y-96,left+(w-40)/3,y-35,SLATE,2,10)
    rect(c,x,y-33,x+w,y+5,NAVY,3,10)
    rect(c,x-6,y-65,x+22,y-13,BLUE,2,8)
    rect(c,x+w-22,y-65,x+w+6,y-13,BLUE,2,8)
    for dx in (13,w-22):
        rect(c,x+dx,y+5,x+dx+9,y+16,INK,2)


def luxury(c):
    room(c,wall='#BAC8D3',floor='#AEAFAE',left=SLATE,right='#8C9EB6')
    floor_seams(c)
    city_window(c,155,81,647,259,night=True)
    rect(c,151,268,808,272,CREAM,0)
    poly(c,[(246,391),(698,391),(818,540),(156,540)],'#B9AC9A',3)
    for x in (180,230,282):
        line(c,x,531,x+95,404,2,SLATE)
    sofa(c,192,405,376)
    sofa(c,670,385,128)
    oval(c,392,389,696,452,CREAM,3)
    for x in (443,643):
        line(c,x,437,x,481,6,INK)
    rect(c,592,404,650,422,NAVY,2,2)
    line(c,599,412,646,412,1.7,GOLD)
    line(c,739,308,739,118,5,OUTLINE)
    poly(c,[(708,113),(773,113),(785,156),(697,156)],GOLD,2.5)
    rect(c,710,156,774,161,PAPER,0)
    return [((1260,823),565,190,.72),((1467,416),270,230,.50),((427,671),240,160,.34)]


def chandelier(c,x,y):
    line(c,x,0,x,y-10,3,INK)
    oval(c,x-66,y-15,x+66,y+12,NAVY,2.7)
    oval(c,x-58,y-10,x+58,y+7,GOLD,2)
    for i in range(-5,6):
        line(c,x+i*10,y+4,x+i*10,y+18+(5-abs(i))*1.8,2.1,PAPER)


def gala_table(c,x,y,scale):
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    for dx in (-110,110):
        chair(c,dx,25)
    oval(c,-121,4,121,52,SLATE,2.5)
    poly(c,[(-118,22),(118,22),(99,75),(-99,75)],'#B7B1A4',2)
    oval(c,-121,-3,121,42,PAPER,2.5)
    for xx in (-80,-36,36,80):
        oval(c,xx-13,19,xx+13,25,CREAM,1.4)
        line(c,xx-5,17,xx-5,6,1.7,BLUE)
        oval(c,xx-10,0,xx,8,MIST,1)
    for xx,dy in ((-15,6),(0,0),(15,8)):
        line(c,xx,13,xx,-30+dy,2.2,INK)
        dot(c,xx,-33+dy,3.8,GOLD,0)
    c.restore()


def gala(c):
    room(c,wall='#878B96',floor='#6A7893',left='#495D7E',right='#526584')
    panel_wall(c,147,68,667,291,7,'#6F8299')
    rect(c,303,132,660,274,NAVY,3)
    rect(c,316,143,648,262,BLUE,2.2,v=SLATE)
    label(c,'BENEFIT DINNER',482,208,30,WHITE,'center',F_TITLE)
    line(c,424,221,539,221,3,GOLD)
    for x in (275,480,684):
        chandelier(c,x,77 if x==480 else 108)
    for x,y,s in ((223,323,.63),(731,320,.63),(345,439,.91),(697,454,.97)):
        gala_table(c,x,y,s)
    return [((976,422),420,235,.61),((684,887),346,185,.68),((1379,915),339,187,.63)]


def camera(c,x,y,s=1):
    c.save()
    c.translate(x,y)
    c.scale(s,s)
    for xx in (-43,0,44):
        line(c,0,13,xx,103,6,OUTLINE)
    rect(c,-39,-30,34,14,NAVY,3,5)
    poly(c,[(30,-21),(61,-30),(61,4),(31,-2)],BLUE,2.5)
    rect(c,-28,-40,7,-27,SLATE,2,3)
    rect(c,-32,-20,-6,-1,SLATE,1,2)
    dot(c,17,-15,4,GOLD,0)
    c.restore()


def press(c):
    room(c,wall='#CDD3D7',floor='#A3B1C3')
    rect(c,182,91,783,337,NAVY,3)
    for x in (185,779):
        rect(c,x-13,90,x+13,338,SLATE,2)
    for x in range(199,781,38):
        line(c,x,94,x,334,1.3,'#60789D')
    rect(c,289,128,677,197,'#253B61',2)
    label(c,'PRESS BRIEFING',483,172,29,WHITE,'center',F_TITLE)
    poly(c,[(184,335),(783,335),(836,389),(126,389)],CREAM,3)
    rect(c,126,389,836,408,BLUE,2)
    podium(c,425,385,124)
    mic(c,461,280,.7)
    mic(c,502,280,.7)
    camera(c,183,447,.9)
    camera(c,795,452,.9)


def studio(c):
    room(c,wall='#69798F',floor='#6580A2',left='#405476',right='#405476')
    rect(c,180,87,785,327,NAVY,2.8)
    for x in (202,218,748,764):
        rect(c,x,91,x+5,327,GOLD,0)
    city_window(c,245,104,474,205,night=True)
    poly(c,[(269,387),(696,387),(815,540),(145,540)],'#A5B5C9',2.5)
    c.save()
    c.translate(344,409)
    c.scale(1.2,1.2)
    chair(c,0,0)
    c.restore()
    c.save()
    c.translate(619,410)
    c.scale(1.2,1.2)
    chair(c,0,0)
    c.restore()
    oval(c,434,398,530,423,PAPER,2)
    line(c,482,418,482,476,4,INK)
    oval(c,462,470,505,480,BLUE,2)
    for x in (290,486,683):
        rect(c,x-29,28,x+29,59,BLUE,2,5)
        rect(c,x-23,36,x+23,55,PAPER,1.3,4)
    camera(c,123,419,1.05)
    camera(c,835,427,.85)
    return [((958,816),433,162,.71),((963,363),310,170,.26)]


SETS=[
    ('mansion-exterior','Mansion exterior',mansion,False),
    ('luxury-apartment','Luxury apartment',luxury,True),
    ('charity-gala','Charity gala',gala,True),
    ('press-conference','Press-conference stage',press,False),
    ('tv-interview-studio','TV interview studio',studio,True),
]
