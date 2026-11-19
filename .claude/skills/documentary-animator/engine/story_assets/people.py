"""Original supporting cast in the existing Dirty Dollar character rig."""
from engine.cast import person
from .drawing import (
    BLUE, CREAM, F_TITLE, GOLD, INK, NAVY, SLATE, WHITE, dot, kit, label, line, oval, poly, rect,
)
from .prop_stage import render_props


PEOPLE = [
    ('judge','Judge',person('retiree',suit='#1F2940',suit_d='#111A2C',shirt=CREAM,
                            hair='silver',outfit='sweater'), 'ROBE / COLLAR'),
    ('court-clerk','Court clerk',person('reporter',skin='#B97B53',skin_d='#925637',
                                        hair='bun',hair_col='#2E2224',suit='#C3CBDB',
                                        suit_d='#8998B4',shirt=INK,glasses=False), 'JACKET / COURT FILES'),
    ('attorney','Attorney',person('agent',suit='#2D4169',suit_d='#1A2B4D',tie='#AA8053',
                                  hair='slick',hair_col='#211C22',face_shape=(.95,1.04)), 'SUIT / TIE'),
    ('compliance-officer','Compliance officer',person('analyst',skin='#E3BA9B',
        skin_d='#C49679',hair='bob',hair_col='#4A3332',suit='#4E6588',suit_d='#314665',
        outfit='open',shirt=CREAM), 'JACKET / ID BADGE'),
    ('auditor','Auditor',person('analyst',hair='silver',hair_col='#CAD0DC',
                                skin='#74513E',skin_d='#553829',suit='#746D65',suit_d='#514A44',
                                tie='#314871',face_shape=(1.08,.95)), 'SUIT / GLASSES'),
    ('call-center-operator','Call-center operator',person('grad',skin='#A97050',
        skin_d='#8C5438',suit='#62779D',suit_d='#425679',outfit='sweater'), 'SWEATER / HEADSET'),
    ('small-business-owner','Small-business owner',person('saver',hair='long',hair_col='#2E2629',
        skin='#CF9771',skin_d='#A66F53',suit='#A69B83',suit_d='#786952',shirt=CREAM), 'APRON / WORK SHIRT'),
]


def identifiable_detail(c,slug,x,y,s):
    c.save()
    c.translate(x,y)
    c.scale(s,s)
    if slug=='judge':
        for left in (-28,7):
            rect(c,left,kit.BODY_TOP+5,left+19,kit.BODY_TOP+47,CREAM,3,2)
    elif slug=='court-clerk':
        poly(c,[(-101,-224),(61,-232),(67,-153),(-94,-143)],'#BEAC86',4)
        poly(c,[(-85,-228),(47,-240),(55,-203),(-82,-193)],CREAM,3)
        line(c,-61,-218,24,-225,3,BLUE)
        dot(c,-92,-172,13,'#B97B53',4)
    elif slug=='call-center-operator':
        path=kit.skia.Path()
        path.arcTo(kit.skia.Rect(-108,kit.HEAD_CY-120,108,kit.HEAD_CY+92),195,150,True)
        c.drawPath(path,kit.ink(9,BLUE))
        rect(c,-108,kit.HEAD_CY-52,-83,kit.HEAD_CY+12,INK,4,8)
        line(c,-95,kit.HEAD_CY,-72,kit.HEAD_CY+44,7,INK)
        oval(c,-80,kit.HEAD_CY+36,-49,kit.HEAD_CY+51,BLUE,2)
    elif slug=='compliance-officer':
        poly(c,[(-31,kit.BODY_TOP+11),(3,kit.BODY_TOP+76),(31,kit.BODY_TOP+11)],
             None,5,'#8BB0D2')
        rect(c,-17,kit.BODY_TOP+74,22,kit.BODY_TOP+120,CREAM,3,3)
        line(c,-10,kit.BODY_TOP+106,14,kit.BODY_TOP+106,3,INK)
    elif slug=='small-business-owner':
        poly(c,[(-21,kit.BODY_TOP+11),(21,kit.BODY_TOP+11),(54,-154),(-54,-154)],BLUE,4)
        line(c,-12,kit.BODY_TOP+4,-29,kit.BODY_TOP+34,5,NAVY)
        line(c,12,kit.BODY_TOP+4,29,kit.BODY_TOP+34,5,NAVY)
        rect(c,-28,-227,28,-190,SLATE,3,3)
    c.restore()


def draw_person(c, slug, x, y, scale, **pose):
    """Draw a supporting character and its identifying accessory."""
    spec = _SPECS[slug]
    kit.draw_char(c, x, y, scale, spec, **pose)
    identifiable_detail(c, slug, x, y, scale)


_SPECS = {slug: spec for slug, _, spec, _ in PEOPLE}

def stage(slug,title,detail):
    def draw(c):
        label(c,title.upper(),84,109,29,WHITE,font=F_TITLE)
        label(c,detail,84,144,21,'#D6E0F0')
        line(c,85,161,293,161,3,GOLD)
        for x,y,s,face in ((336,466,.52,-.15),(699,661,.91,.50)):
            if x>500:
                c.save()
                c.clipRect(kit.skia.Rect(490,84,885,472))
            else:
                oval(c,x-79,y-7,x+79,y+11,'#132445',0)
            draw_person(c,slug,x,y,s,face=face,brow=.12,mouth='flat',rim='#9FB3DE')
            if x>500:
                c.restore()
                line(c,522,471,868,471,2,SLATE)
        label(c,'FULL BODY',336,503,17,'#CFDBEC','center')
        label(c,'CLOSE-UP',699,503,17,'#CFDBEC','center')
    return draw


def render(output):
    return render_props(output,[
        (slug,title,stage(slug,title,detail)) for slug,title,_,detail in PEOPLE
    ])
