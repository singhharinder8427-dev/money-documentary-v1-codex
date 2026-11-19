"""Night sales floor and reusable, perspective-drawn workstation props."""

from dataclasses import dataclass
import math
import random

import numpy as np
import skia

from engine import kit, looks, widgets
from engine.core import F_LABEL, GOLD, H, NAVY, PAPER, W


INK = '#101A31'
FRAME = '#7190BE'
PALE = '#A2B6D6'


@dataclass(frozen=True)
class Camera:
    center: float = 980
    horizon: float = 347
    eye_x: float = -.31
    eye_y: float = 2.60
    focal: float = 1020
    offset: float = 3.65

    def point(self, xyz):
        x, y, z = xyz
        scale = self.scale(z)
        return self.center + (x - self.eye_x) * scale, self.horizon + (self.eye_y - y) * scale

    def scale(self, z):
        return self.focal / (self.offset + z)


def polygon(canvas, camera, points, fill, stroke=None, weight=0):
    return kit.poly(canvas, [camera.point(p) for p in points], fill, weight, stroke or INK)


def segment(canvas, camera, start, end, width, color):
    kit.line(canvas, *camera.point(start), *camera.point(end), width, color)


def horizontal(canvas, camera, x0, z0, x1, z1, y, fill, stroke=None, weight=0):
    return polygon(canvas, camera, [(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)], fill, stroke, weight)


def face(canvas, camera, x0, y0, x1, y1, z, fill, stroke=None, weight=0):
    return polygon(canvas, camera, [(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)], fill, stroke, weight)


def side_wall(canvas, camera, x, y0, z0, y1, z1, fill, stroke=None, weight=0):
    return polygon(canvas, camera, [(x,y0,z0),(x,y0,z1),(x,y1,z1),(x,y1,z0)], fill, stroke, weight)


def box(canvas, camera, x0, y0, z0, x1, y1, z1, top, front, end, width=1.8):
    near = x0 if (x0+x1)/2 > camera.eye_x else x1
    side_wall(canvas, camera, near, y0, z0, y1, z1, end, INK, width)
    face(canvas, camera, x0, y0, x1, y1, z0, front, INK, width)
    horizontal(canvas, camera, x0, z0, x1, z1, y1, top, INK, width)


def carpet(canvas, camera):
    horizontal(canvas, camera, -7, -.68, 7, 25, 0, '#1B2D4D')
    horizontal(canvas, camera, -1.32, -.68, 1.32, 25, .005, '#293F68')
    for x in (-1.35, 1.35):
        segment(canvas, camera, (x, .006, -.68), (x, .006, 25), 2, '#47618D')
    for i in range(24):
        z = -.58 + i * 1.13
        for x in range(-7, 7):
            if x in (-1, 0):
                continue
            if (x + i) % 3 == 0:
                horizontal(canvas, camera, x, z, x+1, z+1.13, .007, '#213657')
        segment(canvas, camera, (-7, .008, z), (7, .008, z), 1, '#253A5D')
    rng = random.Random(37)
    for _ in range(1100):
        x, z = rng.uniform(-7,7), rng.uniform(-.55,24)
        px, py = camera.point((x,.01,z))
        if 0 < px < W and 0 < py < H:
            kit.circ(canvas, px, py, min(1.7, camera.scale(z)*.008), '#365078', 0)
    for z in (.5, 7.3, 14.2):
        horizontal(canvas, camera, -.78, z, .92, z+.37, .012, '#344970')


def side_windows(canvas, camera, x, is_left):
    side_wall(canvas, camera, x, 0, -.7, 4.02, 25, '#263957' if is_left else '#1C2F50')
    for y, color, width in ((.13, FRAME, 4),(.86, '#3C5683', 3),(3.27, '#43709D', 3)):
        segment(canvas, camera, (x, y, -.7), (x, y, 25), width, color)
    if not is_left:
        for z in (3.6, 11.3, 18.5):
            side_wall(canvas, camera, x-.015, 1.08, z, 3.04, z+1.75, '#2C4266', FRAME, 3)
            side_wall(canvas, camera, x-.020, 1.19, z+.09, 2.93, z+1.66, '#192D4A', INK, 2)
            for y in (1.46, 1.69, 1.92, 2.15, 2.38, 2.61):
                segment(canvas, camera, (x-.025,y,z+.14), (x-.025,y,z+1.61), 1.15, '#34527D')
        return

    rng = random.Random(92)
    for z in (1.1, 4.9, 8.7, 12.5, 16.3, 20.1, 23.9):
        if z + 2.92 > 25:
            continue
        x_in = x + .017
        side_wall(canvas, camera, x_in, 1.01, z, 3.20, z+2.99, '#101E3B', FRAME, 3.8)
        for idx in range(6):
            start = z + .07 + idx * .48
            tower = rng.uniform(.35,1.29)
            side_wall(canvas, camera, x_in+.003, 1.06, start, 1.06+tower, start+.33,
                      ('#1A3157','#223C69','#182A4D')[idx%3])
            for row in range(int(tower/.15)):
                if rng.random() > .28:
                    h = 1.14 + row*.15
                    side_wall(canvas, camera, x_in+.005, h, start+.055, h+.036, start+.13,
                              '#C09C5E' if rng.random() < .29 else '#546B98')
        for dy in (1.88, 2.61):
            segment(canvas, camera, (x_in+.008,dy,z),(x_in+.008,dy,z+2.99), 1.8, '#395780')
        segment(canvas, camera, (x_in+.009,1.02,z+1.49),(x_in+.009,3.18,z+1.49), 3, FRAME)
        polygon(canvas, camera, [(x_in+.012,2.38,z+.06),(x_in+.012,2.89,z+.10),
                                (x_in+.012,3.13,z+1.30),(x_in+.012,2.73,z+1.35)], '#2A4169')


def ceiling(canvas, camera):
    y = 4.025
    horizontal(canvas, camera, -7, -.68, 7, 25, y, '#253956')
    for z in range(0,25,2):
        for i in range(-7,7,2):
            if (z//2 + i//2) % 4 == 0:
                horizontal(canvas, camera, i, z, min(7,i+2), z+1.93, y-.008, '#2C415F')
        segment(canvas, camera, (-7,y-.012,z),(7,y-.012,z), 1.3, '#3D5477')
    for x in range(-7,8,2):
        segment(canvas, camera, (x,y-.014,-.68),(x,y-.014,25), 1.6, '#3C5377')
    for z in (.5,5.0,9.5,14,18.5,23):
        for x in (-4.59, -.26, 4.13):
            box(canvas, camera, x, 3.925, z, x+1.06, y-.01, z+1.56,
                '#344B70', '#10213E', '#1D3151', 1.7)
            horizontal(canvas, camera, x+.10, z+.12, x+.96, z+1.45, 3.918,
                       '#C4D2E4' if x != -.26 else '#D6CBAF', INK, 1.3)
            for j in (.34,.69):
                segment(canvas, camera, (x+j,3.911,z+.16),(x+j,3.911,z+1.40), 1.4, '#8195B4')


def back_wall(canvas, camera):
    face(canvas, camera, -7, 0, 7, 4.03, 24.96, '#344968', FRAME, 3)
    face(canvas, camera, -6.60, .42, -.90, 3.13, 24.91, '#253A59', '#55739B', 2.7)
    for y in (1.12,1.54,1.96,2.38):
        segment(canvas, camera, (-6.36,y,24.88),(-1.14,y,24.88), 2, '#536D93')
        for i in range(9):
            x=-6.15+i*.52
            face(canvas, camera, x,y+.035,x+.17,y+.36,24.86,
                 ('#586F94','#8392AA','#C39858')[int(i+y*5)%3], INK, 1)
    face(canvas, camera, -.63, .02, 5.52, 3.22, 24.87, '#283A58', FRAME, 3.6)
    face(canvas, camera, -.42, .13, .88, 2.92, 24.83, '#495E7D', INK, 2)
    face(canvas, camera, -.27, 1.14, .73, 2.77, 24.82, '#617494', INK, 1.7)
    face(canvas, camera, 1.10, .60, 5.25, 2.92, 24.82, '#B5955E', INK, 2.3)
    face(canvas, camera, 1.19, .68, 5.16, 1.70, 24.80, '#514B4C')
    face(canvas, camera, 2.84, 1.14, 4.11, 1.91, 24.78, '#27354C', INK, 1.5)
    face(canvas, camera, 3.04, 1.29, 3.98, 1.80, 24.76, '#637B9F')
    for x in (1.08, 3.25, 5.28):
        segment(canvas, camera, (x,.64,24.75),(x,2.93,24.75), 4, '#26364E')
    segment(canvas, camera, (1.10,2.49,24.73),(5.24,2.49,24.73), 2, '#E4CC90')
    x,y = camera.point((2.51,3.40,24.79))
    s=camera.scale(24.79)
    kit.rect(canvas,x-2.12*s,y-.38*s,x+2.12*s,y+.29*s,'#162A4C',2,r=3,v=FRAME)
    widgets.text(canvas,'SUPERVISOR',x,y+.09*s,.42*s,GOLD,F_LABEL,'center')


def cubicle_divider(canvas, camera, x0, x1, z, light=False):
    width = max(1.45, min(3.5,camera.scale(z)*.017))
    frame = '#7388AA' if light else '#536E9A'
    box(canvas, camera, x0, .61, z, x1, 1.55, z+.085,
        '#A0ACBE' if light else '#60799F', '#657DA3' if light else '#455F8A', '#33496F', width)
    face(canvas, camera, x0+.045,.88,x1-.045,1.46,z-.015,'#7A8FAB' if light else '#4B658F')
    segment(canvas,camera,(x0+.04,1.46,z-.016),(x1-.04,1.46,z-.016),width,frame)
    segment(canvas,camera,(x0+.04,.91,z-.016),(x1-.04,.91,z-.016),width,'#354D75')
    for x in (x0+.07,x1-.07):
        box(canvas,camera,x-.022,.07,z-.016,x+.025,1.55,z+.081,frame,frame,'#354D75',1.3)


def desk(canvas, camera, x0, x1, z, lit=False):
    width=max(1.45,min(4,camera.scale(z)*.018))
    left_unit=(x0+x1)*.5 < camera.eye_x
    edge = '#B5A083' if lit else '#6C82A5'
    worktop = '#D3C3A8' if lit else '#8094B1'
    shadow = '#57647F' if lit else '#394F73'
    pedestal = x0+.085 if left_unit else x1-.56
    horizontal(canvas,camera,x0-.05,z-.09,x1+.07,z+.91,.025,'#172642')
    box(canvas,camera,pedestal,.045,z+.07,pedestal+.47,.78,z+.70,shadow,shadow,'#2A3E61',width)
    for y in (.23,.45,.66):
        segment(canvas,camera,(pedestal+.035,y,z+.066),(pedestal+.435,y,z+.066),width*.65,'#8297BB')
        segment(canvas,camera,(pedestal+.16,y-.056,z+.062),(pedestal+.32,y-.056,z+.062),width*.6,'#253956')
    leg = x1-.085 if left_unit else x0+.085
    box(canvas,camera,leg-.038,.028,z+.07,leg+.038,.795,z+.152,PALE,'#596E94','#263858',width*.65)
    box(canvas,camera,x0,.777,z,x1,.855,z+.81,worktop,edge,'#647797',width)
    segment(canvas,camera,(x0+.035,.861,z+.025),(x1-.035,.861,z+.025),width*.6,'#EBDEC3' if lit else '#ADC0DB')


def monitor(canvas, camera, x, z, *, active=True, base_y=.855):
    w=max(1.4,min(4,camera.scale(z)*.018))
    y=base_y
    box(canvas,camera,x-.22,y,z-.11,x+.22,y+.034,z+.13,'#8299BD','#40557B','#253856',w)
    box(canvas,camera,x-.048,y+.03,z+.036,x+.048,y+.20,z+.13,'#60789E','#293C5C','#1D3050',w*.75)
    box(canvas,camera,x-.37,y+.18,z+.03,x+.37,y+.68,z+.103,'#526D94','#1D2F50','#334D76',w)
    face(canvas,camera,x-.326,y+.227,x+.326,y+.629,z+.024,'#7F9CC7' if active else '#394C71','#172742',w*.65)
    if active:
        face(canvas,camera,x-.31,y+.552,x+.31,y+.609,z+.022,'#D6E0EF')
        for n in range(3):
            h=y+.48-n*.086
            segment(canvas,camera,(x-.268,h,z+.020),(x+.16+n*.032,h,z+.020),max(1,w*.56),'#3B577F')
        face(canvas,camera,x+.215,y+.273,x+.284,y+.507,z+.020,'#E7B964')
    segment(canvas,camera,(x-.27,y+.597,z+.018),(x-.22,y+.597,z+.018),w*.5,'#A6B9D5')


def desk_phone(canvas,camera,x,z,base_y=.855):
    w=max(1.2,min(3,camera.scale(z)*.016))
    box(canvas,camera,x-.142,base_y,z-.12,x+.145,base_y+.055,z+.14,'#405A83','#213759','#1D3151',w)
    box(canvas,camera,x-.130,base_y+.047,z-.096,x-.059,base_y+.091,z+.125,'#8197B7','#3B5377','#294165',w*.72)
    horizontal(canvas,camera,x-.02,z+.047,x+.104,z+.116,base_y+.061,'#AEC1DD',INK,w*.45)
    for i in range(3):
        for j in range(3):
            xx = x-.013+i*.040
            zz = z-.078+j*.034
            horizontal(canvas,camera,xx,zz,xx+.020,zz+.015,base_y+.060,'#8398BB')


def chair(canvas,camera,x,z):
    w=max(1.5,min(4,camera.scale(z)*.018))
    px,py=camera.point((x,.022,z))
    spread=camera.scale(z)*.36
    kit.oval(canvas,px-spread,py-spread*.28,px+spread,py+spread*.19,'#172642',0)
    for angle in (25,145,265):
        radians=math.radians(angle)
        dx,dz=math.cos(radians)*.31,math.sin(radians)*.26
        segment(canvas,camera,(x,.10,z),(x+dx,.055,z+dz),w*1.42,'#384E72')
        kit.circ(canvas,*camera.point((x+dx,.044,z+dz)),max(2,w*1.50),'#152643',1.5)
    box(canvas,camera,x-.021,.10,z-.027,x+.022,.525,z+.030,'#899EC2','#526D92','#263D62',w*.7)
    box(canvas,camera,x-.255,.474,z-.13,x+.255,.553,z+.36,'#536C93','#344A71','#2D446B',w)
    for dx in (-.26,.26):
        segment(canvas,camera,(x+dx,.54,z+.10),(x+dx,.73,z+.10),w*1.34,'#7890B4')
        segment(canvas,camera,(x+dx,.73,z-.09),(x+dx,.73,z+.23),w*1.44,'#455D86')
    # The back is toward the aisle-side camera while the seat faces the desk.
    x0,y0=camera.point((x-.25,.56,z-.15))
    x1,y1=camera.point((x+.25,1.11,z-.17))
    kit.rect(canvas,x0,y1,x1,y0,'#31486F',w,r=min(16,w*3),v=INK)
    kit.rect(canvas,x0+w*1.6,y1+w*1.7,x1-w*1.6,y0-w*2.2,'#4C658C',0,r=min(12,w*2.4))


def desktop(canvas,camera,x,z,lit,index):
    monitor(canvas,camera,x+.17,z+.52,active=lit or index%3!=1)
    desk_phone(canvas,camera,x-.54,z+.28)
    horizontal(canvas,camera,x-.14,z+.14,x+.47,z+.30,.863,'#354E76',INK,1.4)
    for j in (.17,.21,.25):
        segment(canvas,camera,(x-.088,.868,z+j),(x+.40,.868,z+j),1.3,'#859BBB')
    for i in (0,1):
        horizontal(canvas,camera,x+.57-i*.035,z+.17+i*.06,x+.84-i*.035,z+.42+i*.06,.865+i*.007,
                   PAPER if lit else '#A1ADC4',INK,1.15)
    if index%3 == 0:
        box(canvas,camera,x-.83,.855,z+.19,x-.69,1.002,z+.325,'#E1C280','#C4A15F','#92754A',1.45)
    if lit:
        lx=x+.75
        horizontal(canvas,camera,lx-.12,z+.52,lx+.13,z+.70,.878,'#A58147',INK,1.5)
        segment(canvas,camera,(lx,.889,z+.61),(lx+.074,1.32,z+.61),3.6,'#3C5174')
        px,py=camera.point((lx+.081,1.32,z+.61)); s=camera.scale(z+.61)
        kit.poly(canvas,[(px-.17*s,py+.032*s),(px+.14*s,py+.032*s),(px+.10*s,py-.106*s),
                         (px-.085*s,py-.115*s)],'#DAB66D',max(1.5,s*.017),INK)
        kit.line(canvas,px-.120*s,py+.021*s,px+.102*s,py+.021*s,2,'#F3D38F')


def workstation(canvas,camera,x0,x1,z,index,lit):
    middle=(x0+x1)*.5
    cubicle_divider(canvas,camera,x0-.015,x1+.022,z+.87,light=lit)
    desk(canvas,camera,x0,x1,z,lit)
    desktop(canvas,camera,middle,z,lit,index)
    chair(canvas,camera,middle+.22,z-.47)


def draw_sales_floor(canvas, camera=Camera()):
    canvas.clear(kit.hx(NAVY))
    carpet(canvas,camera)
    side_windows(canvas,camera,-7,True)
    side_windows(canvas,camera,7,False)
    ceiling(canvas,camera)
    back_wall(canvas,camera)

    banks = ((-6.55,-4.13),(-3.97,-1.43),(1.44,3.98),(4.15,6.61))
    for row,z in reversed(list(enumerate((1.05,4.35,7.65,10.98,14.35,17.70,21.03)))):
        for index,(x0,x1) in enumerate(banks):
            lit=(row,index) in {(0,1),(1,2),(3,0),(4,2),(5,1)}
            workstation(canvas,camera,x0,x1,z+(.39 if index>=2 else 0),row+index,lit)

    # A lit side of the room frames the closest conversation position.
    for z in (1.5,9.9,18.3):
        if z>3:
            box(canvas,camera,6.58,.04,z,6.94,1.59,z+.69,'#687E9F','#3C537B','#263A5B',1.6)


def sales_floor_light_map(camera):
    """Pools of fixture and desk light for the engine's halftone print pass."""
    yy, xx = np.ogrid[:H, :W]
    lighting = np.full((H, W), .14)

    pools = [
        ((-2.43, .97, 1.42), 1.15, .77, .75),  # nearest lit desk
        ((2.62, .95, 1.88), 1.06, .65, .56),   # opposite workstation
        ((2.95, 1.65, 24.7), 2.45, 1.55, .78),  # supervisor's office
        ((.10, 0, .60), 1.55, .82, .36),       # overhead light on the aisle
        ((-.08, 0, 5.30), 1.65, .64, .30),
    ]
    for z in (.5, 5.0, 9.5, 14, 18.5, 23):
        for x in (-4.06, .27, 4.66):
            pools.append(((x, 3.92, z+.75), .62, .26, .70))

    for position, width, height, intensity in pools:
        x, y = camera.point(position)
        scale = camera.scale(position[2])
        distance = ((xx-x)/(width*scale))**2 + ((yy-y)/(height*scale))**2
        np.maximum(lighting, .14 + intensity*np.exp(-distance), out=lighting)
    return lighting


AISLE_SPOT = (*Camera().point((-.87, 0, .74)), 1.10)


def build():
    """Return the 1080p night-print background as an opaque RGBA array."""
    camera = Camera()
    surface = skia.Surface(W, H)
    draw_sales_floor(surface.getCanvas(), camera)
    pixels = surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
    printed = looks.night_print(pixels[..., :3].astype(float), sales_floor_light_map(camera))
    pixels[..., :3] = np.clip(looks.grain(printed), 0, 255).astype(np.uint8)
    return pixels
