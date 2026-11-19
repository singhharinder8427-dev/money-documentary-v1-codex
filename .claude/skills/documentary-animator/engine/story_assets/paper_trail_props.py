"""Evidence and corporate paperwork props."""
from .drawing import (
    BLUE, CREAM, F_TITLE, F_TYPE, GOLD, INK, MIST, NAVY, PAPER, SLATE, WHITE, kit, label, line, oval, poly, rect,
)
from .prop_stage import paper, render_props, rows, sample


def pitch_deck(c):
    for offset in (25,13):
        rect(c,185-offset,120+offset,775-offset,424+offset,MIST,3,8)
    rect(c,185,120,775,424,CREAM,3,8)
    rect(c,186,121,774,199,NAVY,1,7)
    label(c,'Investor pitch',214,173,35,WHITE,font=F_TITLE)
    line(c,215,231,430,231,3,BLUE)
    for y,end in ((257,401),(279,417),(303,373)):
        line(c,216,y,end,y,2,SLATE)
    for i,h in enumerate((35,64,89,123)):
        rect(c,497+i*54,363-h,530+i*54,363,GOLD if i==3 else BLUE,1)
    line(c,464,364,732,364,2,INK)
    label(c,'Illustrative projections',497,392,15,BLUE)


def prospectus(c):
    rect(c,296,67,682,477,NAVY,4,8)
    rect(c,310,76,700,460,MIST,2,6)
    paper(c,256,59,421,410,'PROSPECTUS')
    label(c,'Example Growth Fund',280,174,26,INK,font=F_TITLE)
    label(c,'OFFERING OVERVIEW',280,216,20,BLUE)
    for y,end in ((253,633),(280,643),(304,607),(332,629)):
        line(c,281,y,end,y,2.4,SLATE)
    sample(c,282,426)


def contract(c):
    paper(c,253,47,456,430,'SIGNED CONTRACT')
    rows(c,278,163,405,[('PARTIES','Example parties'),('EFFECTIVE DATE','June 10'),('TERM','12 months')])
    for y in (291,301,311):
        line(c,278,y,673,y,1.7,SLATE)
    for x,name in ((281,'Jordan Example'),(490,'Taylor Sample')):
        line(c,x,388,x+180,388,1.5,BLUE)
        kit.label(c,name,x+3,380,20,INK,rot=-4)
        label(c,'SIGNATURE',x,409,14,BLUE)
    sample(c,279,452)


def audit(c):
    paper(c,210,84,540,364,'AUDIT MEMO')
    rows(c,237,196,486,[('SUBJECT','Revenue review'),('REVIEWER','Example auditor')])
    rect(c,233,254,729,365,'#DAE3ED',1,3)
    label(c,'Finding',248,281,20,INK)
    label(c,'Invoices missing supporting records.',248,320,22,INK,font=F_TYPE)
    sample(c,238,412)


def filing(c):
    paper(c,246,65,468,410,'CORPORATE FILING')
    rows(c,270,175,421,[('ENTITY','Example Holdings'),('RECORD NO.','CF-0041'),
                         ('FILED','June 10'),('STATUS','Accepted')],47)
    oval(c,559,379,670,426,None,3,BLUE)
    label(c,'FILED',614,411,22,BLUE,'center',F_TITLE)
    sample(c,270,447)


def exhibit(c):
    rect(c,258,123,704,424,CREAM,4,14)
    rect(c,273,138,689,410,PAPER,3,10)
    rect(c,275,140,687,228,GOLD,1.5,8)
    label(c,'COURT EXHIBIT',481,197,32,INK,'center',F_TITLE)
    label(c,'EXHIBIT',304,271,18,BLUE)
    label(c,'A-04',632,282,36,INK,'right',F_TITLE)
    line(c,305,300,655,300,2,BLUE)
    rows(c,305,332,347,[('PROCEEDING','Civil hearing')])
    sample(c,305,384)


def evidence_bag(c):
    poly(c,[(298,68),(656,68),(678,467),(281,467)],'#ABC0D8',3)
    rect(c,294,75,661,109,NAVY,3,3)
    for y in (85,97):
        line(c,309,y,646,y,2.6,GOLD)
    poly(c,[(350,141),(567,128),(603,368),(386,382)],CREAM,2)
    for y in range(166,303,22):
        line(c,383,y,553,y-9,2,SLATE)
    rect(c,310,304,650,425,PAPER,2.5,5)
    label(c,'EVIDENCE BAG',331,339,24,INK,font=F_TITLE)
    line(c,332,351,627,351,1.7,BLUE)
    label(c,'ITEM 04  /  DOCUMENTS',331,383,19,INK,font=F_TYPE)


def archive(c):
    poly(c,[(216,183),(676,183),(782,247),(312,247)],MIST,3.7)
    rect(c,312,247,782,414,CREAM,4)
    poly(c,[(216,183),(312,247),(312,414),(216,341)],SLATE,3.5)
    rect(c,308,240,788,270,PAPER,3.2,3)
    rect(c,402,289,692,379,PAPER,2.5,6)
    label(c,'ARCHIVE',546,332,29,INK,'center',F_TITLE)
    label(c,'CASE 04  /  FILES 01–08',546,359,18,BLUE,'center',F_TYPE)
    rect(c,240,267,282,289,INK,2,8)


PROPS=[
    ('pitch-deck','Pitch deck',pitch_deck),('prospectus','Prospectus',prospectus),
    ('signed-contract','Signed contract',contract),('audit-memo','Audit memo',audit),
    ('corporate-filing','Corporate filing',filing),('court-exhibit-sticker','Court exhibit sticker',exhibit),
    ('evidence-bag','Evidence bag',evidence_bag),('archive-box','Archive box',archive),
]


def render(output):
    return render_props(output,PROPS)
