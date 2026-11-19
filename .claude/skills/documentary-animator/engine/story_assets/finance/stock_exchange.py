"""Stock exchange exterior study in the Dirty Dollar day print."""
from engine import kit
from engine.core import F_TITLE
from engine.widgets import text

r,p,l=kit.rect,kit.poly,kit.line
NAVY='#223554'
PAPER='#F5ECD7'

def scene(c):
    c.save()
    c.scale(2,2)
    c.clear(kit.hx('#D4E2ED'))
    # Tall office facades frame the exchange.
    for x,w,h in [(-40,245,510),(740,255,490)]:
        r(c,x,20,x+w,h,'#8799AD',2,v='#536C8B')
        for col in range(int(w/34)):
            for row in range(14):
                r(c,x+12+col*34,42+row*28,x+29+col*34,59+row*28,'#485D7E',0)
                l(c,x+14+col*34,46+row*28,x+27+col*34,46+row*28,1,'#8195AE')
    r(c,0,486,960,540,'#A5AAB1',0)
    for y in (487,514):
        l(c,0,y,960,y,1,'#D9D7CE')
    p(c,[(145,188),(482,48),(813,188)],PAPER,3)
    p(c,[(177,181),(482,76),(781,181)],'#7286A4',2)
    for x in range(250,732,36):
        h=max(0,95-abs(x-482)*.36)
        if h>6:
            p(c,[(x,177),(x+12,177-h*.55),(x+20,177)],PAPER,1)
    r(c,168,185,791,217,PAPER,3)
    text(c,'STOCK EXCHANGE',480,208,22,NAVY,F_TITLE,'center')
    r(c,185,216,775,454,'#667B99',2)
    r(c,185,216,775,248,'#34496A',0)
    for y in range(257,433,21):
        l(c,187,y,773,y,1.3,'#A8B8C9')
    for x in (224,323,422,521,620,719):
        r(c,x-25,221,x+25,427,PAPER,2)
        r(c,x+10,230,x+24,420,'#B0BBC7',0)
        for dx in (-15,-7,1,9,17):
            l(c,x+dx,236,x+dx,421,1.25,'#798DA5')
        r(c,x-31,219,x+31,233,'#E9E1D0',2)
        r(c,x-32,419,x+32,435,'#D1D1C9',2)
    for x in (272,472,672):
        r(c,x-28,346,x+28,433,NAVY,2)
        r(c,x-23,351,x+23,428,'#677D97',1)
        l(c,x,351,x,428,2,PAPER)
        l(c,x-23,388,x+23,388,2,PAPER)
    for i in range(4):
        r(c,152-i*13,439+i*10,806+i*13,449+i*10,PAPER,2)
    for x in (128,832):
        r(c,x-4,420,x+4,482,NAVY,2)
        kit.oval(c,x-13,399,x+13,425,'#E3D7BD',2)
        l(c,x-10,412,x+10,412,2,NAVY)
    for x in range(0,960,73):
        l(c,x,503,x+38,503,2,'#D3D1C9')
    c.restore()
