"""Shared preview stage for separately composable props."""
import skia
from engine import widgets
from engine.core import W,H
from .drawing import (
    BLUE, F_TYPE, INK, MIST, PAPER, SLATE, label, line, rect,
)


def render_props(output, props):
    entries=[]
    for slug,title,draw in props:
        path=output/(slug+'.png')
        surface=skia.Surface(W,H)
        canvas=surface.getCanvas()
        widgets.framed_bg(canvas)
        canvas.save()
        canvas.scale(2,2)
        draw(canvas)
        canvas.restore()
        surface.makeImageSnapshot().save(str(path),skia.kPNG)
        entries.append((title,path))
    return entries


def paper(c,x,y,w,h,title):
    rect(c,x+9,y+11,x+w+9,y+h+11,'#101B35',0,6)
    rect(c,x,y,x+w,y+h,PAPER,3,5)
    label(c,title,x+23,y+51,30,INK)
    line(c,x+23,y+68,x+w-23,y+68,2,SLATE)


def rows(c,x,y,w,fields,spacing=38):
    for index,(key,value) in enumerate(fields):
        yy=y+index*spacing
        label(c,key,x,yy,15,BLUE)
        label(c,value,x+w,yy,20,INK,'right',F_TYPE)
        line(c,x,yy+8,x+w,yy+8,1,MIST)


def sample(c,x,y):
    label(c,'ILLUSTRATIVE RECORD',x,y,14,BLUE)
