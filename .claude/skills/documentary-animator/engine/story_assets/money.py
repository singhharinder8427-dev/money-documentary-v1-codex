"""Money movement props with fictional sample information."""
from .drawing import (
    BLUE, CREAM, F_TITLE, F_TYPE, GOLD, INK, MIST, NAVY, WHITE, dot, kit, label, line, oval, poly, rect,
)
from .prop_stage import paper, render_props, rows, sample


def check(c):
    rect(c,183,150,761,416,NAVY,5,12)
    rect(c,198,165,756,400,MIST,2,8)
    paper(c,223,115,559,260,'CHECK')
    label(c,'NO. 0041',753,151,16,BLUE,'right')
    rows(c,246,218,500,[('PAY TO','Example Supply Co.'),('AMOUNT','$2,450.00'),('MEMO','Equipment deposit')])
    sample(c,247,350)
    line(c,617,341,746,341,2,BLUE)
    label(c,'SIGNATURE',616,360,14,BLUE)


def wire(c):
    paper(c,255,89,450,365,'WIRE RECEIPT')
    rows(c,280,200,400,[('REFERENCE','WR-0041'),('RECIPIENT','Example Supply Co.'),
                        ('STATUS','Sent'),('AMOUNT','$8,400.00')],46)
    sample(c,280,413)


def deposit(c):
    paper(c,204,118,552,304,'DEPOSIT SLIP')
    rows(c,229,226,496,[('CASH','$540.00'),('CHECKS','$2,450.00'),('TOTAL','$2,990.00')],51)
    sample(c,229,385)


def card(c):
    rect(c,226,113,739,440,'#101B35',0,25)
    rect(c,216,100,729,427,'#314C7C',4,25)
    poly(c,[(475,103),(709,103),(726,120),(726,290)],'#47618A',0)
    rect(c,257,177,326,231,GOLD,2.5,9)
    for y in (193,212):
        line(c,260,y,323,y,1.7,INK)
    line(c,286,178,286,231,1.7,INK)
    for width in (19,28,38):
        path=kit.skia.Path()
        path.arcTo(kit.skia.Rect(646-width,161-width,646+width,161+width),-55,110,True)
        c.drawPath(path,kit.ink(2.4,WHITE))
    label(c,'••••  ••••  ••••  0041',258,308,27,WHITE,font=F_TYPE)
    label(c,'DEMO CARD',258,365,22,WHITE)
    label(c,'EXAMPLE BANK',684,370,17,WHITE,'right')


def terminal(c):
    rect(c,343,78,616,470,NAVY,5,33)
    rect(c,365,100,594,222,'#B8C9DD',2,10)
    label(c,'TOTAL',386,131,18,BLUE)
    label(c,'$42.00',573,193,35,INK,'right',F_TITLE)
    for row in range(4):
        for column in range(3):
            x=376+column*72
            y=241+row*42
            rect(c,x,y,x+54,y+30,GOLD if (row,column)==(3,2) else BLUE,1.5,5)
            if (row,column)==(3,2):
                line(c,x+18,y+15,x+24,y+21,2.5,INK)
                line(c,x+24,y+21,x+37,y+9,2.5,INK)
            else:
                label(c,'123456789*0'[3*row+column],x+27,y+22,18,WHITE,'center')
    rect(c,408,428,551,442,'#0D1933',2,3)


def statement(c):
    paper(c,244,53,471,437,'BANK STATEMENT')
    rect(c,266,144,693,207,'#D7E1ED',1,4)
    label(c,'CLOSING BALANCE',282,172,18,INK)
    label(c,'$5,610.00',668,184,31,INK,'right',F_TITLE)
    rows(c,270,247,419,[('JUN 01  OPENING','$6,950.00'),('JUN 10  PAYMENT','–$2,450.00'),
                        ('JUN 18  DEPOSIT','$1,110.00')],48)
    sample(c,269,456)


def cash_drawer(c):
    rect(c,211,140,747,421,NAVY,4,16)
    rect(c,227,152,731,375,'#182845',3,10)
    for index,denom in enumerate((1,5,10,20)):
        x=246+index*117
        rect(c,x,176,x+105,312,BLUE,2,4)
        for offset in (8,4,0):
            rect(c,x+14,189+offset,x+92,293+offset,CREAM,1,4)
        oval(c,x+31,215,x+75,264,MIST,1.5)
        label(c,f'${denom}',x+53,248,22,INK,'center',F_TITLE)
        line(c,x+53,178,x+53,207,4,INK)
    for index in range(5):
        x=252+index*97
        rect(c,x,326,x+84,364,BLUE,1.6,6)
        for n in range(3):
            dot(c,x+25+n*14,345+(n%2)*4,9,GOLD if index in (0,3) else MIST,1.4)
    rect(c,437,390,520,409,CREAM,2.2,4)


PROPS=[
    ('check-and-checkbook','Check and checkbook',check),('wire-receipt','Wire receipt',wire),
    ('deposit-slip','Deposit slip',deposit),('credit-card','Credit card',card),
    ('payment-terminal','Payment terminal',terminal),('bank-statement','Bank statement',statement),
    ('cash-drawer','Cash drawer',cash_drawer),
]


def render(output):
    return render_props(output,PROPS)
