"""Daytime office floor study for the Dirty Dollar set library."""
from engine.sets_src.sales_floor import Camera, face, horizontal, polygon, segment, side_wall, workstation

def office(c):
    cam=Camera(center=950,horizon=325,eye_x=.0,eye_y=2.65,focal=1000,offset=3.8)
    back=19
    horizontal(c,cam,-7,-.5,7,back,0,'#B6B9BA')
    horizontal(c,cam,-1.55,-.5,1.55,back,.006,'#F4ECDD')
    for x in (-1.55,1.55):
        segment(c,cam,(x,.01,-.5),(x,.01,back),2.8,'#506585')
    for x in (-7,-6,-5,-4,-3,-2,2,3,4,5,6,7):
        segment(c,cam,(x,.01,-.5),(x,.01,back),1.2,'#8392A3')
    for z in range(0,19,2):
        for left,right in ((-7,-1.55),(1.55,7)):
            segment(c,cam,(left,.01,z),(right,.01,z),1.2,'#9A9FA9')
    for x in (-7,7):
        side_wall(c,cam,x,0,-.5,4,back,'#DFD8CA')
        side_wall(c,cam,x,1,-.4,3.5,back,'#DDEAF2')
        inside=x-.01 if x>0 else x+.01
        side_wall(c,cam,inside,1,-.4,1.72,back,'#7E94AA')
        for z in range(1,19,3):
            side_wall(c,cam,inside,1.02,z+.21,1.98,z+.86,'#566F91')
        segment(c,cam,(x,3.5,-.4),(x,3.5,back),4,'#435877')
        for z in range(1,19,3):
            segment(c,cam,(x,1,z),(x,3.5,z),5,'#3F5678')
        segment(c,cam,(x,1,-.4),(x,1,back),4,'#435877')
        segment(c,cam,(x,2.5,-.4),(x,2.5,back),3,'#435877')
    face(c,cam,-7,0,7,4,back,'#DDD6C9')
    face(c,cam,-1.4,0,1.4,3.15,back-.1,'#99AABD','#34455E',3)
    face(c,cam,-1.15,.1,1.15,2.88,back-.2,'#587091','#34455E',3)
    segment(c,cam,(0,.1,back-.22),(0,2.88,back-.22),3,'#34455E')
    horizontal(c,cam,-7,-.5,7,back,4,'#A6B4C4')
    for z in range(1,19,3):
        segment(c,cam,(-7,3.98,z),(7,3.98,z),2,'#B0BBC2')
        for x in (-4,0,4):
            horizontal(c,cam,x-.7,z,x+.7,z+.8,3.97,'#FFF6DF','#637891',2)
    for z in reversed((1.4,4.7,8,11.3,14.6)):
        for i,(left,right) in enumerate(((-6.2,-3.85),(-3.8,-1.55),(1.55,3.8),(3.85,6.2))):
            workstation(c,cam,left,right,z,i,lit=z==1.4 and i==1)
