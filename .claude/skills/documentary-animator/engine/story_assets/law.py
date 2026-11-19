"""Law and consequences backgrounds."""
from .drawing import (
    BLUE, CREAM, F_TITLE, GOLD, INK, MIST, NAVY, PAPER, SLATE, WHITE, city_window, dot, floor_seams, kit, label, line, mic, panel_wall, poly, rect, room, skyline,
)
from .furniture import bench, cabinet, chair, desk, podium, queue_posts, rotary_phone


def panel_door(c,x,y,w,h,name=None):
    rect(c,x-5,y-5,x+w+5,y+h,NAVY,2)
    rect(c,x,y,x+w,y+h,BLUE,2)
    rect(c,x+w*.22,y+16,x+w*.78,y+h*.48,MIST,2)
    line(c,x+w*.22,y+h*.35,x+w*.78,y+h*.35,2,PAPER)
    rect(c,x+w-13,y+h*.59,x+w-8,y+h*.64,GOLD,1)
    if name:
        label(c,name,x+w*.5,y+h*.54,16,WHITE,'center')


def handset(c,x,y):
    rect(c,x-12,y-22,x+12,y+29,NAVY,2,3)
    rect(c,x-6,y-25,x+4,y+23,BLUE,2,5)
    for yy in (y-28,y+13):
        rect(c,x-10,yy,x+8,yy+15,INK,1.5,4)
    path=kit.skia.Path()
    path.moveTo(x,y+23)
    path.cubicTo(x-3,y+65,x+24,y+60,x+22,y+22)
    c.drawPath(path,kit.ink(2.8,NAVY))


def visiting_room(c, phones_on_hooks=True):
    room(c, wall='#BECCD9', floor='#879AB2', left=SLATE, right=SLATE)
    floor_seams(c)
    rect(c,143,93,817,301,'#859BB3',2)
    for y in range(104,307,25):
        line(c,147,y,813,y,1.25,'#5F7593')
        for x in range(168+(y//25%2)*26,810,52):
            line(c,x,y,x,y+24,1.2,'#5F7593')
    for start in (177,576):
        rect(c,start,112,start+205,277,'#4B648A',2,3)
        for y in range(134,274,24):
            line(c,start+2,y,start+203,y,1.2,'#8095AF')
    for x in (211,676):
        rect(c,x,83,x+97,92,PAPER,2,3)
    panel_door(c,414,131,130,171)
    for x in (263,695):
        chair(c,x,380)
    visiting_counter(c)
    # The center division and faint diagonal reflections read as clear glazing.
    visiting_divider(c)
    poly(c,[(251,113),(270,113),(439,234),(425,234)],kit.fp('#F4EAD7',72),0)
    poly(c,[(502,148),(673,113),(710,113),(502,161)],kit.fp('#F4EAD7',93),0)
    for x in (408,551):
        if phones_on_hooks:
            handset(c,x,273)
        else:
            rect(c,x-12,251,x+12,302,NAVY,2,3)
            rect(c,x-5,257,x+5,281,SLATE,1.7,2)
            dot(c,x,292,3,MIST,1)
    rect(c,447,369,514,377,SLATE,1.6)


def visiting_counter(c):
    poly(c,[(118,326),(839,326),(921,373),(37,373)],PAPER,2.8)
    rect(c,37,373,921,396,NAVY,3)
    for x in (78,865):
        rect(c,x,396,x+12,481,BLUE,2)

def visiting_divider(c):
    rect(c,467,80,491,373,INK,2)
    rect(c,474,86,485,355,'#869BB7',2)


def visiting_foreground(c):
    visiting_counter(c)
    visiting_divider(c)
    rect(c,447,369,514,377,SLATE,1.6)


def courthouse(c):
    c.clear(kit.hx('#D5E2EB'))
    skyline(c,0,135,960,278)
    rect(c,0,414,960,540,'#B7C6D5',0)
    poly(c,[(122,188),(842,188),(891,228),(887,417),(99,417)],'#93A4B8',2.8)
    rect(c,148,170,807,413,CREAM,3)
    rect(c,215,208,743,405,'#7386A4',3)
    for x in (288,427,558,685):
        panel_door(c,x-32,268,64,128)
    rect(c,196,190,766,224,NAVY,2)
    label(c,'UNITED STATES COURTHOUSE',481,213,20,WHITE,'center',F_TITLE)
    rect(c,169,160,793,190,PAPER,3)
    for x in (221,347,479,611,742):
        rect(c,x-22,223,x+22,400,PAPER,2.5)
        rect(c,x+9,224,x+21,398,'#A8B7C8',0)
        rect(c,x-29,220,x+29,231,CREAM,2)
        rect(c,x-29,389,x+29,406,CREAM,2)
    for i in range(8):
        y=402+i*11
        rect(c,153-i*12,y,811+i*12,y+11,PAPER if i%2==0 else MIST,1.8)
    for x in (257,697):
        line(c,x,434,x-18,498,3,INK)
        line(c,x-4,444,x-4,468,2.5,NAVY)
        line(c,x-16,483,x-16,507,2.5,NAVY)
    rect(c,0,513,960,519,PAPER,0)


def deposition(c):
    room(c,wall='#C4CDD5')
    floor_seams(c)
    panel_wall(c,146,233,668,128,7)
    city_window(c,183,81,301,174)
    rect(c,544,102,738,223,BLUE,2)
    rect(c,555,113,727,212,PAPER,2)
    poly(c,[(557,206),(615,149),(657,180),(692,140),(727,168),(727,212),(557,212)],SLATE,0)
    for x in (322,637):
        chair(c,x,359)
    desk(c,171,443,623,116)
    rect(c,200,443,765,485,BLUE,2)
    for x in (360,600):
        mic(c,x,362,1.2)
    rect(c,445,365,527,395,SLATE,2,5)
    label(c,'REC',486,385,15,INK,'center')
    dot(c,506,378,3.2,GOLD,0)
    poly(c,[(244,377),(330,370),(346,399),(255,406)],PAPER,2)
    for y in (383,390,397):
        line(c,261,y,322,y-4,1.3,INK)
    poly(c,[(639,394),(721,402),(705,434),(618,423)],CREAM,2)


def hearing(c):
    room(c, wall='#DCE1DF')
    floor_seams(c)
    panel_wall(c,148,69,665,297,9)
    dot(c,480,144,45,NAVY,2.5)
    dot(c,480,144,37,CREAM,2.5,v=GOLD)
    for x,y,h in ((464,158,19),(480,158,29),(496,158,37)):
        rect(c,x-4,y-h,x+4,y,BLUE,0)
    for x in (265,372,480,588,695):
        chair(c,x,270)
    poly(c,[(236,266),(722,266),(794,308),(164,308)],CREAM,2.5)
    panel_wall(c,164,308,630,77,6,BLUE)
    names=('COUNSEL','MEMBER','CHAIR','MEMBER','COUNSEL')
    for x,name in zip((265,372,480,588,695),names):
        mic(c,x,299)
        rect(c,x-36,312,x+36,329,PAPER,1.4,1)
        label(c,name,x,325,13,INK,'center')
    desk(c,301,461,358,41)
    mic(c,466,450,1.25)


def jail_intake(c):
    room(c,wall='#D8DCD6',floor='#8F9FB0')
    floor_seams(c)
    panel_door(c,669,105,133,248,'STAFF')
    cabinet(c,160,177,91,169)
    rect(c,285,99,617,273,NAVY,3)
    rect(c,297,109,605,254,'#BBCAD4',2)
    for x in (371,527):
        line(c,x,110,x,252,3,BLUE)
    rect(c,348,123,555,156,INK,2)
    label(c,'INTAKE',452,147,25,WHITE,'center')
    poly(c,[(234,315),(638,315),(768,374),(163,374)],PAPER,3)
    panel_wall(c,163,374,605,94,5,BLUE)
    rect(c,321,306,395,345,NAVY,2,4)
    rect(c,330,314,386,336,'#B3C5D2',1)
    poly(c,[(490,336),(555,336),(571,358),(482,358)],SLATE,2)
    poly(c,[(499,330),(549,330),(561,351),(493,351)],PAPER,1.5)
    queue_posts(c,240,507,483)


def cell_corridor(c):
    c.clear(kit.hx('#737C90'))
    poly(c,[(0,0),(960,0),(612,142),(348,142)],'#A9B2BA',2)
    rect(c,345,142,615,370,'#7B899B',2)
    poly(c,[(0,540),(345,369),(615,369),(960,540)],'#9FAAB6',2)
    for y in (404,450,510):
        line(c,0,y,960,y,1.2,'#617A9C')
    panel_door(c,434,195,92,175)
    for side in (-1,1):
        for start, end, top, base in ((295,347,126,392),(225,295,95,419),(122,225,53,468),(9,122,10,522)):
            xs=sorted([480+side*(480-start),480+side*(480-end)])
            a,b=xs
            mirror=side>0
            upper=(top+26,top) if mirror else (top,top+26)
            lower=(base-25,base) if mirror else (base,base-25)
            poly(c,[(a,upper[0]),(b,upper[1]),(b,lower[1]),(a,lower[0])],NAVY,2.8)
            for i in range(1,5):
                frac=i/5
                x=a+frac*(b-a)
                line(c,x,upper[0]+frac*(upper[1]-upper[0]),x,lower[0]+frac*(lower[1]-lower[0]),3.5,'#A3B5CB')
            line(c,a,(upper[0]+lower[0])*.5,b,(upper[1]+lower[1])*.5,3,'#AABAD0')
    for y,w in ((13,136),(79,79),(123,42)):
        rect(c,480-w/2,y,480+w/2,y+9,PAPER,2,4)
    return [((960,555),302,410,.55),((960,973),385,175,.54)]


SETS = [
    ('visiting-room','Jail visiting room',visiting_room,False),
    ('courthouse-exterior','Courthouse exterior and steps',courthouse,False),
    ('deposition-room','Deposition room',deposition,False),
    ('regulator-hearing-room','Regulator hearing room',hearing,False),
    ('jail-intake-desk','Jail intake desk',jail_intake,False),
    ('cell-corridor','Cell corridor',cell_corridor,True),
]
