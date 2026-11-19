"""Approved set drawings in 960 × 540 design coordinates. The set renderer scales them to HD."""
import math
import random
import numpy as np
from engine import kit
from engine.core import GOLD, F_TITLE, F_LABEL, F_TYPE, H, W
from engine.widgets import text

PAPER, SILVER, MID, BLUE, NAVY, INK = '#F4ECDA', '#A7B4C8', '#657799', '#384C73', '#1E3055', '#17171A'
r, p, l, o, dot = kit.rect, kit.poly, kit.line, kit.oval, kit.circ


def foliage(c, x, y, width, height, seed, palette):
    rng = random.Random(seed)
    for row in range(4):
        for i in range(14):
            u = (i + rng.random()) / 14
            a = math.sin(math.pi * u) ** .55
            rx = rng.uniform(.065, .14) * width
            ry = rng.uniform(.12, .30) * height
            px = x + u * width
            py = y - a * height * (.14 + row * .19) + rng.uniform(-.06, .06) * height
            o(c, px-rx, py-ry, px+rx, py+ry, palette[min(row//2, len(palette)-1)], 0)
    for i in range(int(width / 4)):
        u = rng.random()
        a = math.sin(math.pi * u)
        px, py = x+u*width, y-a*height*rng.uniform(.36,.87)
        l(c, px, py, px+3, py-2, 1.4, palette[-1])


def sash(c, x, y, w, h):
    r(c,x-5,y-5,x+w+5,y+h+5,PAPER,2)
    r(c,x,y,x+w,y+h,BLUE,2)
    p(c,[(x+2,y+h*.67),(x+w*.64,y+2),(x+w*.85,y+2),(x+w*.22,y+h*.75)],'#6884AC',0)
    for u in (.32,.68):
        l(c,x+w*u,y,x+w*u,y+h*.36,2,PAPER)
    l(c,x,y+h*.36,x+w,y+h*.36,3,PAPER)
    r(c,x-7,y+h+4,x+w+7,y+h+9,SILVER,1)


def home(c):
    c.clear(kit.hx('#BDCBDD'))
    for x,y,w in [(36,80,160),(714,60,171),(150,43,100)]:
        for dx,dy,rx in [(0,0,.22),(.23,-6,.22),(.39,2,.25),(.57,5,.2)]:
            o(c,x+w*dx,y+dy,x+w*(dx+rx*2),y+16,PAPER,0)
    for x in [-100,42,770,890]:
        r(c,x,226,x+160,327,'#B2BBC8',1)
        p(c,[(x-13,229),(x+72,166),(x+172,224)],'#7688A4',1.3)
        sash(c,x+28,247,27,41)
        sash(c,x+101,247,30,41)
    r(c,0,326,960,540,'#ABB7C7',0)
    for x in range(0,961,13):
        p(c,[(x,325),(x,272),(x+5,267),(x+10,272),(x+10,325)],PAPER,1)
    for x in [-30,795]:
        foliage(c,x,340,180,40,9,(BLUE,MID,SILVER))
    # Three-quarter side wall and dark projecting eaves.
    p(c,[(696,185),(791,211),(791,350),(696,372)],'#8292A9',2)
    for y in range(211,358,10):
        l(c,696,y,790,211+(y-185)*.77,1,'#687893')
    r(c,169,185,696,367,'#E3DECB',2)
    for y in range(196,369,9):
        l(c,170,y,695,y,1,'#9CA8B5')
    r(c,609,61,644,151,'#969CA4',2)
    r(c,605,58,648,66,PAPER,2)
    for y in range(72,136,8):
        l(c,610,y,643,y,1,'#616C80')
        l(c,618+(y%16),y,618+(y%16),y+7,1,'#616C80')
    roof=[(137,194),(246,105),(655,105),(734,193)]
    path=p(c,roof,BLUE,2.5)
    c.save()
    c.clipPath(path)
    for j,y in enumerate(range(108,199,7)):
        l(c,135,y,740,y,1.1,'#7187A9')
        for x in range(135+(j%2)*11,735,22):
            l(c,x,y,x-2,y+6,.75,'#7286A8')
    c.restore()
    p(c,[(655,105),(730,130),(816,211),(734,194)],NAVY,2)
    p(c,[(138,193),(734,193),(816,211),(811,216),(730,202),(138,202)],PAPER,2)
    # Dormer above the short porch roof.
    r(c,341,125,471,165,'#CFD3D5',2)
    p(c,[(332,126),(401,92),(482,122),(478,130),(402,101),(338,133)],NAVY,2)
    sash(c,363,130,40,24)
    sash(c,409,130,40,24)
    sash(c,575,228,91,85)
    sash(c,704,231,28,53)
    r(c,201,218,537,350,'#828D9E',2)
    for y in range(229,348,10):
        l(c,201,y,535,y,.9,'#627088')
    sash(c,235,241,71,65)
    r(c,380,227,446,350,PAPER,2)
    r(c,386,232,440,349,NAVY,2)
    r(c,392,238,434,270,'#859BB6',1)
    for x in [405,419]:
        l(c,x,239,x,270,1.5,PAPER)
    for x in [392,415]:
        r(c,x,278,x+17,337,BLUE,1)
    dot(c,432,301,2.8,GOLD,1)
    r(c,452,244,476,254,BLUE,1)
    text(c,'24',464,252,8,PAPER,F_LABEL,'center')
    l(c,367,222,367,237,1.5,INK)
    p(c,[(360,238),(374,238),(372,249),(362,249)],GOLD,1.6)
    p(c,[(166,219),(237,174),(495,174),(554,216)],BLUE,2)
    for y in [185,195,205]:
        l(c,234-(y-174)*1.45,y,494+(y-174)*1.28,y,1,'#7081A0')
    r(c,166,215,554,225,PAPER,2)
    r(c,185,346,538,362,'#9DA7B6',2)
    for x in [192,507]:
        r(c,x-7,303,x+24,356,'#91A1B7',2)
        for y in (316,331,345):
            l(c,x-7,y,x+24,y,1,'#546783')
        p(c,[(x-2,303),(x+3,225),(x+15,225),(x+21,303)],PAPER,2)
        r(c,x-9,301,x+26,308,PAPER,1.4)
    # A porch swing suspended from the beam.
    for x in [251,313]:
        l(c,x,226,x+2,309,1.35,BLUE)
    r(c,246,305,323,319,'#869BB6',1.2,2)
    for y in [309,314]:
        l(c,250,y,319,y,1,NAVY)
    p(c,[(245,319),(324,319),(329,324),(241,324)],PAPER,1.4)
    for j in range(4):
        r(c,352-j*5,349+j*6,462+j*5,355+j*6,PAPER,1.2)
    p(c,[(0,422),(137,399),(204,398),(151,407),(238,405),(206,415),(101,428),(39,441),(0,447)],'#70839C',0)
    p(c,[(741,461),(808,449),(815,449),(746,464)],'#65799A',0)
    p(c,[(337,374),(478,374),(578,540),(205,540)],PAPER,1.6)
    for y in (397,436,491):
        u=(y-374)/166
        l(c,337-132*u,y,478+100*u,y,1.3,'#9AA8B6')
    for x,y,w,h in [(130,366,112,37),(244,369,87,29),(534,367,172,49),(694,360,79,29)]:
        foliage(c,x,y,w,h,x,(NAVY,BLUE,'#879AB2'))
    # Street mailbox and a slim edge canopy give the camera a foreground.
    r(c,736,395,745,462,'#768398',2)
    r(c,721,379,770,403,BLUE,2,6)
    r(c,720,380,736,403,'#6F83A0',1.3,5)
    l(c,753,392,753,377,2.3,GOLD)
    r(c,753,376,763,381,GOLD,0)
    p(c,[(-12,440),(25,439),(33,212),(92,148),(84,143),(28,185),(19,111),(-10,101)],NAVY,1)
    foliage(c,-104,127,270,175,27,(BLUE,NAVY,'#6F819C'))
    foliage(c,824,132,195,148,30,(BLUE,NAVY,'#879AB2'))
    rng=random.Random(22)
    for i in range(125):
        x,y=rng.randrange(960),rng.randrange(379,533)
        if x<319-(y-379)*.82 or x>489+(y-379)*.63:
            l(c,x,y,x+3,y-2,1,'#7A8BA2')


def chandelier(c,x,y,scale):
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    for offset in (-46,0,46):
        l(c,offset*.55,-56,offset,0,1.2,BLUE)
    o(c,-62,-8,62,8,PAPER,2)
    for i in range(-56,57,4):
        bottom=9+7*math.sqrt(max(0,1-(i/60)**2))
        l(c,i,1,i,bottom,1.2,'#92A3BE')
    o(c,-55,8,55,17,None,1.4,BLUE)
    c.restore()


def lectern(c):
    # Lectern with offset side wall, sloping reading shelf, and gooseneck mic.
    p(c,[(607,239),(643,243),(638,301),(611,301)],'#9A856E',1.8)
    p(c,[(643,243),(656,235),(650,297),(638,301)],BLUE,1.5)
    p(c,[(602,238),(644,245),(658,237),(617,230)],PAPER,1.6)
    r(c,615,252,635,267,NAVY,1)
    for a in range(3):
        l(c,619+a*4,262,619+a*4,258-a*2,1.8,GOLD)
    l(c,635,233,632,221,1.6,INK)
    l(c,632,221,623,217,1.6,INK)
    o(c,619,214,625,218,INK,0)


def ballroom(c, slide_title='Investor seminar'):
    c.clear(kit.hx('#E9E3D5'))
    p(c,[(0,0),(960,0),(837,84),(152,84)],'#D1D6DA',1)
    for dx in (-160,130,420,720,1020):
        p(c,[(dx,0),(dx+14,0),(460+(dx-460)*.56,84),(452+(dx-460)*.56,84)],SILVER,1)
    p(c,[(0,16),(153,83),(153,319),(0,378)],'#AAB4C1',2)
    p(c,[(837,83),(960,20),(960,385),(837,319)],'#D0D3D5',2)
    for x in (15,71,116,853,895,946):
        frac = min(x/153,(960-x)/123)
        top=40+54*frac
        bot=350-40*frac
        r(c,x,top,x+7,bot,BLUE,1)
    r(c,148,78,841,318,'#C1C6CF',2)
    r(c,146,78,842,90,PAPER,1.5)
    p(c,[(0,376),(152,313),(839,313),(960,378),(960,540),(0,540)],'#A8B4C7',1)
    for x in range(-780,1741,68):
        l(c,474+(x-474)*.19,316,x,540,1.6,'#899BB6')
    for y in [361,389,425,477,538]:
        l(c,0,y,960,y,1.3,'#879AB4')
    r(c,207,104,778,303,NAVY,2)
    for x in range(211,774,17):
        p(c,[(x,106),(x+6,106),(x+10,299),(x-2,299)],BLUE,0)
        l(c,x+7,107,x+10,298,1.6,'#8394AF')
    # A sample seminar slide fits within the replaceable projection screen.
    r(c,295,124,543,250,INK,2)
    r(c,300,130,538,243,PAPER,1)
    if slide_title:
        r(c,311,141,315,231,GOLD,0)
        text(c,slide_title,328,195,21,NAVY,F_TITLE)
        l(c,329,206,394,206,2,GOLD)
    r(c,290,119,548,127,'#596983',1.5,2)
    p(c,[(204,290),(766,290),(810,327),(169,327)],'#BCC3CE',2)
    r(c,169,327,810,346,NAVY,2)
    for x in range(177,810,12):
        l(c,x,331,x,343,1,'#7185A3')
    for i in range(3):
        x=774+i*5
        y=324+i*6
        r(c,x,y,x+38+i*4,y+6,SILVER,1)
    lectern(c)
    for x in (221,749):
        r(c,x,257,x+16,284,NAVY,1.4,2)
        dot(c,x+8,274,4,'#7184A2',1)
        dot(c,x+8,263,2,'#7184A2',.7)
        l(c,x+8,284,x+8,291,1.3,INK)
    for x in [183,802]:
        r(c,x-3,168,x+3,198,'#A18B6B',1)
        r(c,x-8,163,x+8,179,PAPER,1,3)
    chandelier(c,211,49,.85)
    chandelier(c,741,49,.85)
    # Padded banquet chairs grow toward camera, leaving a walkable center aisle.
    for row,(y,s) in enumerate([(364,.55),(390,.72),(427,.93),(480,1.22),(550,1.65)]):
        for side in (-1,1):
            for index in range(10):
                x=478+side*(48+row*10+index*56*s)
                if not -45 < x < 1005:
                    continue
                c.save()
                c.translate(x,y)
                c.scale(s,s)
                for a in (-14,14):
                    l(c,a,-8,a*1.19,11,2.3,BLUE)
                r(c,-16,-32,16,-5,'#C3B39B',2.6,5)
                r(c,-13,-29,13,-9,BLUE,1.2,3)
                l(c,-10,-26,10,-26,1,'#8DA3BE')
                r(c,-16,-6,16,-2,'#8B9AB0',1,2)
                c.restore()


def evidence(c,x,y,w,h,angle,title,kind):
    c.save()
    c.translate(x,y)
    c.rotate(angle)
    r(c,2,3,w+2,h+3,NAVY,0)
    r(c,0,0,w,h,PAPER,1.4)
    text(c,title,7,15,10,INK,F_LABEL)
    l(c,7,20,w-7,20,1.2,BLUE)
    if kind=='bank':
        p(c,[(8,38),(w/2,25),(w-8,38)],BLUE,1)
        for dx in [14,26,38,50]:
            r(c,dx,40,dx+4,55,BLUE,0)
        r(c,8,55,w-8,60,BLUE,0)
    elif kind=='book':
        for i in range(4):
            l(c,7,26+i*8,w-6,26+i*8,1.15,INK)
        for dx in [w*.52,w*.72]:
            l(c,dx,24,dx,h-7,1.2,INK)
    else:
        for i,portion in enumerate([.82,.66,.76,.49]):
            l(c,7,29+8*i,w*portion,29+8*i,1.4,INK)
    dot(c,w*.52,4.2,2.7,GOLD,.7)
    c.restore()


def folder(c,x,y,scale,angle,label):
    c.save()
    c.translate(x,y)
    c.rotate(angle)
    c.scale(scale,scale)
    p(c,[(0,8),(8,8),(12,1),(48,1),(54,8),(108,8),(114,54),(-8,54)],'#D7B97F',1.6)
    p(c,[(0,13),(104,13),(108,49),(-4,49)],PAPER,1)
    p(c,[(-4,19),(105,19),(115,56),(-10,56)],'#D8C8A9',1.6)
    r(c,8,25,63,37,PAPER,1)
    text(c,label,12,34,8.5,INK,F_TYPE)
    c.restore()


def investigation(c):
    c.clear(kit.hx('#818795'))
    p(c,[(0,0),(113,37),(113,340),(0,379)],'#53657F',2)
    p(c,[(797,37),(960,0),(960,376),(797,339)],'#697684',2)
    r(c,113,36,799,341,'#87919B',2)
    r(c,115,326,799,340,'#525E75',1)
    p(c,[(0,379),(112,340),(799,340),(960,375),(960,540),(0,540)],'#64697A',1)
    for x in range(-430,1430,80):
        l(c,479+(x-479)*.22,342,x,540,1,'#898B8D')
    # Slats and their cord set the far wall into shadow.
    r(c,0,72,99,287,NAVY,2)
    for y in range(82,285,14):
        l(c,0,y-7,97,y+3,3.6,'#6B82A1')
    l(c,85,83,85,286,1,SILVER)
    # Steel cabinet behind the desk.
    r(c,75,171,201,367,'#687B98',2.4)
    p(c,[(201,171),(221,162),(221,350),(201,367)],BLUE,2)
    p(c,[(75,171),(95,162),(221,162),(201,171)],SILVER,1.5)
    for y in (180,239,298):
        r(c,82,y,194,y+50,'#718099',1.4)
        r(c,121,y+7,155,y+16,PAPER,1)
        l(c,128,y+23,149,y+23,3.4,INK)
    # A small, structured evidence trail for financial investigations.
    r(c,281,63,748,265,'#4D596D',2.4)
    r(c,287,69,742,259,'#9C8C78',1.3)
    r(c,299,79,433,99,NAVY,1)
    text(c,'TRANSFER REVIEW',306,94,14,PAPER,F_LABEL)
    points=[(347,148),(477,134),(627,170),(487,210)]
    for u,v in [(0,1),(1,2),(2,3)]:
        l(c,*points[u],*points[v],2,GOLD)
    evidence(c,308,118,65,68,-5,'BANK','bank')
    evidence(c,449,106,74,68,4,'LEDGER','book')
    evidence(c,615,134,78,77,-3,'TRANSFER','text')
    evidence(c,452,188,72,57,-4,'INVOICE','book')
    for i in range(4):
        l(c,706,91+i*3,728,91+i*3,1.1,'#596273')
    # Bound archive boxes on a separate side shelf.
    for j,(x,y) in enumerate([(786,260),(866,260),(814,224)]):
        r(c,x,y,x+68,y+37,'#A89B84',1.6)
        r(c,x-2,y-2,x+70,y+5,'#C4B9A2',1)
        r(c,x+20,y+12,x+48,y+24,PAPER,1)
        l(c,x+27,y+17,x+41,y+17,1.2,INK)
    r(c,774,300,958,311,BLUE,2)
    for x in [779,937]:
        r(c,x,311,x+6,364,NAVY,1)
    # Back of a working chair, partly hidden by the desk.
    r(c,507,264,583,343,BLUE,2,9)
    r(c,514,270,575,313,'#546988',1,5)
    investigation_desk(c)


def investigation_desk(c):
    # Desk broad enough for seated or standing talent.
    p(c,[(236,312),(736,312),(850,413),(125,413)],'#AA947F',2.8)
    p(c,[(125,413),(850,413),(847,427),(125,427)],'#705F56',2.6)
    p(c,[(151,427),(313,427),(313,528),(162,516)],'#796C63',2)
    for y in [435,466,494]:
        r(c,174,y,288,y+19,'#91877C',1)
        l(c,219,y+7,244,y+7,2.3,INK)
    p(c,[(768,426),(811,426),(795,514),(768,518)],'#6A635F',2)
    p(c,[(313,427),(767,427),(767,470),(313,470)],'#6D655F',1.5)
    folder(c,359,326,.92,-6,'CASE 041')
    folder(c,578,328,.70,3,'RECEIPTS')
    # A small open ledger in the light.
    p(c,[(418,359),(464,354),(493,359),(508,352),(550,350),(569,382),(515,389),(500,395),(479,390),(427,395)],PAPER,1.6)
    l(c,493,360,500,393,1.5,INK)
    for n in range(4):
        l(c,429,368+n*5,483,364+n*5,1.15,INK)
        l(c,506,364+n*5,546,360+n*5,1.15,INK)
    l(c,552,389,572,367,2,INK)
    dot(c,572,367,1.5,GOLD,0)
    # Articulated inspection lamp, silhouette and hinge hardware.
    o(c,243,350,284,362,BLUE,1.8)
    for dx in (0,5):
        l(c,262+dx,353,244+dx,307,2.6,INK)
        l(c,244+dx,307,289+dx,266,2.6,'#585E6A')
    for x,y in [(265,351),(247,307),(292,266)]:
        dot(c,x,y,4.1,BLUE,1.4)
        dot(c,x,y,1.3,PAPER,0)
    p(c,[(285,270),(295,259),(308,263),(320,278),(302,290)],BLUE,1.7)
    p(c,[(301,288),(320,276),(322,280),(304,292)],GOLD,1)
    # In/out trays, built up with individual paper edges.
    for j in range(2):
        y=358-11*j
        p(c,[(665,y),(713,y-3),(737,y+8),(678,y+13)],PAPER,1.2)
        p(c,[(663,y+1),(679,y+10),(737,y+6),(737,y+12),(677,y+17),(662,y+7)],BLUE,1.4)



def investigation_lighting():
    yy, xx = np.ogrid[:H, :W]
    lamp = np.exp(-(((xx - 777) / 403)**2 + ((yy - 692) / 200)**2))
    board = np.exp(-(((xx - 1002) / 510)**2 + ((yy - 337) / 231)**2))
    return .12 + np.maximum(.79 * lamp, .62 * board)
