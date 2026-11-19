"""Fictional screens for documentary reenactments."""
from .drawing import (
    BLUE, F_TITLE, F_TYPE, GOLD, INK, MIST, NAVY, SLATE, WHITE, dot, label, line, poly, rect,
)
from .prop_stage import render_props


def window(c,title,subtitle='ILLUSTRATIVE SCREEN'):
    rect(c,153,75,807,480,'#0F1B35',0,18)
    rect(c,145,65,797,470,'#EBEFF2',4,15)
    rect(c,145,65,797,136,NAVY,3,14)
    rect(c,148,121,794,140,NAVY,0)
    label(c,title,174,112,32,WHITE)
    label(c,subtitle,772,111,14,'#D0DAEC','right')


def chart(c,x,y,w,h,values):
    for j in range(4):
        yy=y+j*h/3
        line(c,x,yy,x+w,yy,1.2,MIST)
    pts=[(x+i*w/(len(values)-1),y+h-v*h) for i,v in enumerate(values)]
    poly(c,[*pts,(x+w,y+h),(x,y+h)],'#CCD9E8',0)
    for start,end in zip(pts,pts[1:]):
        line(c,*start,*end,3.4,NAVY)
    dot(c,*pts[-1],5,GOLD,1.4)


def investments(c):
    window(c,'PORTFOLIO OVERVIEW')
    label(c,'ACCOUNT VALUE',176,174,17,BLUE)
    label(c,'$24,850.00',176,220,40,INK,font=F_TITLE)
    rect(c,172,242,771,440,WHITE,1.6,6)
    chart(c,205,267,530,133,[.09,.18,.15,.34,.29,.52,.47,.67,.74])
    label(c,'JAN',205,423,16,BLUE)
    label(c,'JUN',736,423,16,BLUE,'right')


def transactions(c):
    window(c,'TRANSACTION HISTORY')
    for x,name in ((175,'DATE'),(305,'DESCRIPTION'),(770,'AMOUNT')):
        label(c,name,x,175,19,BLUE,'right' if x==770 else 'left')
    items=[('JUN 02','Opening deposit','$2,000.00'),('JUN 07','Transfer in','$500.00'),
           ('JUN 12','Fee','–$18.00'),('JUN 17','Withdrawal','–$250.00')]
    for i,(date,description,amount) in enumerate(items):
        y=215+i*56
        rect(c,164,y-26,780,y+15,'#DCE5EE' if i%2==0 else WHITE,0,3)
        label(c,date,175,y,18,INK)
        label(c,description,305,y,20,INK)
        label(c,amount,769,y,20,INK,'right',F_TYPE)


def fake_profit(c):
    window(c,'REPORTED PROFIT','UNVERIFIED FIGURES')
    label(c,'Displayed gain',177,179,20,BLUE)
    label(c,'+$18,600',176,225,41,INK,font=F_TITLE)
    rect(c,174,244,770,407,WHITE,1.7,6)
    chart(c,197,265,549,111,[.08,.12,.22,.33,.40,.60,.73,.9])
    rect(c,173,421,363,447,GOLD,1.3,3)
    label(c,'SIMULATED RESULT',185,440,17,INK)


def withdrawal(c):
    window(c,'WITHDRAWAL')
    rect(c,199,180,741,421,WHITE,2,9)
    dot(c,270,249,32,GOLD,2)
    label(c,'!',270,263,36,INK,'center',F_TITLE)
    label(c,'Withdrawal unavailable',322,247,30,INK)
    label(c,'Your transfer could not be completed.',322,284,21,INK)
    line(c,226,318,715,318,1.5,MIST)
    label(c,'Request status',231,362,18,BLUE)
    label(c,'Declined',698,364,22,INK,'right')
    label(c,'Reference WD-0041',231,395,17,BLUE,font=F_TYPE)


def messages(c):
    window(c,'MESSAGE THREAD')
    for x,y,w,who,message,fill in [
        (170,158,416,'INVESTOR','When can I withdraw the balance?',WHITE),
        (356,242,417,'SUPPORT','Your request is still being reviewed.','#CDD9E8'),
        (170,328,416,'INVESTOR','Please send the transfer receipt.',WHITE),
    ]:
        rect(c,x,y,x+w,y+69,fill,1.8,8)
        label(c,who,x+16,y+21,15,BLUE)
        label(c,message,x+16,y+49,22,INK)
    label(c,'Conversation excerpt',173,448,17,BLUE)


def calls(c):
    window(c,'CALL LOG')
    items=[('10:24','Unknown caller','MISSED'),('10:37','Account support','OUTGOING'),('12:06','Unknown caller','MISSED'),('14:53','Account support','INCOMING')]
    for i,(time,name,state) in enumerate(items):
        y=194+65*i
        dot(c,189,y-8,8,GOLD if state=='MISSED' else BLUE,1)
        label(c,name,214,y,23,INK)
        label(c,state,545,y,16,BLUE)
        label(c,time,768,y,22,INK,'right',F_TYPE)
        line(c,173,y+19,768,y+19,1.3,MIST)


def email(c):
    window(c,'EMAIL')
    rect(c,160,143,302,455,'#CFDBEA',0,3)
    for y,name in ((184,'INBOX'),(225,'SENT'),(265,'DRAFTS')):
        label(c,name,179,y,19,INK)
    label(c,'Withdrawal status update',326,189,26,INK)
    label(c,'FROM  Account support',326,227,18,BLUE)
    line(c,326,242,773,242,1.4,SLATE)
    label(c,'Your withdrawal is still pending.',326,282,23,INK)
    label(c,'Please check your account for updates.',326,316,21,INK)
    rect(c,325,358,540,398,'#DCE5ED',1.5,4)
    label(c,'Status summary',340,385,20,INK)


PROPS=[
    ('investment-dashboard','Investment dashboard',investments),('transaction-history','Transaction history',transactions),
    ('fake-profit-screen','Fake profit screen',fake_profit),('withdrawal-error','Withdrawal error',withdrawal),
    ('message-thread','Message thread',messages),('call-log','Call log',calls),('email-window','Email window',email),
]


def render(output):
    return render_props(output,PROPS)
