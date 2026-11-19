"""Warehouse storage aisle in Dirty Dollar's day print."""
from engine.sets_src.sales_floor import Camera,box,face,horizontal,segment,side_wall

def scene(c):
    cam=Camera(center=960,horizon=330,eye_x=0,eye_y=2.6,focal=940,offset=3.6)
    back=22
    horizontal(c,cam,-7,-.6,7,back,0,'#A6B2BF')
    horizontal(c,cam,-2.1,-.6,2.1,back,.004,'#EEE8DA')
    for x in range(-7,8):
        segment(c,cam,(x,.01,-.6),(x,.01,back),2,'#9AA3AB')
    for z in range(0,22,3):
        segment(c,cam,(-7,.01,z),(7,.01,z),1.4,'#A6A9A9')
    face(c,cam,-7,0,7,5,back,'#D5D5CC','#6B7F94',3)
    face(c,cam,-1.35,0,1.35,3,back-.1,'#586D8C','#33445C',3)
    for y in (0.5,1,1.5,2,2.5):
        segment(c,cam,(-1.3,y,back-.11),(1.3,y,back-.11),2,'#D1D7D4')
    horizontal(c,cam,-7,-.6,7,back,5,'#9FAFC0')
    for z in range(1,22,4):
        segment(c,cam,(-7,4.97,z),(7,4.97,z),3,'#8A99A6')
        horizontal(c,cam,-.8,z,.8,z+1.2,4.94,'#FFF4DB','#5E7592',3)
    for side in (-1,1):
        x0,x1=(-6.8,-2.2) if side<0 else (2.2,6.8)
        for z in reversed((0,4,8,12,16)):
            for level in (0,1.30,2.60):
                for j in range(3):
                    xx=x0+.15+j*1.4
                    gap=(z//4+j+int(level))%3
                    if gap==0 and z in (4,12) and level>0:
                        continue
                    upper=level+.79+gap*.15
                    box(c,cam,xx,level+.12,z+.25,xx+1.25,upper,z+2.8,
                        '#F5EAD2','#EDE2CC','#899BB1',2)
                    inside=xx+1.252 if side<0 else xx-.002
                    side_wall(c,cam,inside,level+.35,z+.72,level+.60,z+1.27,
                              '#F8EFDD','#4E6485',1.7)
                    segment(c,cam,(inside,level+.13,z+1.64),(inside,upper,z+1.64),
                            3.4,'#738CAD')
                    segment(c,cam,(xx+.16,level+.67,z+.24),(xx+.55,level+.67,z+.24),2,'#55657A')
            for height in (.06,1.36,2.66,3.96):
                box(c,cam,x0,height,z,x1,height+.09,z+3.6,'#7487A1','#536783','#425875',2)
            for xx in (x0,x1-.12):
                box(c,cam,xx,.05,z,xx+.12,4.2,z+.12,'#8495A7','#455B78','#5B6F87',2)
    # Neutral lane paint leaves the shelf labels as the point of interest.
    for x in (-1.65,1.65):
        segment(c,cam,(x,.016,-.5),(x,.016,back),4,'#6C84A0')
