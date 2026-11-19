"""Four reusable evidence props for the Dirty Dollar framed document stage."""

import skia

from engine import kit, widgets
from engine.core import F_LABEL, F_LABEL2, F_TITLE, F_TYPE, GOLD, WHITE

PAPER = '#F7EDDA'
WARM = '#E2D4B6'
LINE = '#A29683'
INK = '#15223C'
VIOLET_INK = '#354C74'


def label(canvas, words, x, y, size=29, color=INK, align='left'):
    widgets.text(canvas, words, x, y, size, color, F_LABEL, align)


def data_text(canvas, words, x, y, size=25, align='left'):
    widgets.text(canvas, words, x, y, size, INK, F_TYPE, align)


def shadow(canvas, left, top, right, bottom):
    shape = skia.RRect.MakeRectXY(skia.Rect(left+10, top+11, right+12, bottom+16), 9, 9)
    canvas.drawRRect(shape, kit.fp('#090D20', 171, blur=10))


def ledger(canvas, record, amount):
    """An open bound book with opposing ruled pages and a visible spine."""
    shadow(canvas, -316, -142, 315, 153)
    kit.rect(canvas, -321, -136, 321, 156, '#293E63', 6, r=14, v=INK)
    kit.rect(canvas, -309, -127, 309, 145, WARM, 3, r=7, v=INK)
    for offset in (4, 10, 16):
        kit.line(canvas, -299, 144-offset, 298, 144-offset, 2, '#B09D7B')
    for side in (-1, 1):
        page = skia.Path()
        page.moveTo(0, -113)
        page.cubicTo(65*side, -148, 210*side, -147, 298*side, -143)
        page.lineTo(302*side, 116)
        page.cubicTo(205*side, 113, 74*side, 111, 0, 141)
        page.close()
        kit.shape(canvas, page, PAPER if side < 0 else '#EEE2C7', 4, INK)
    kit.poly(canvas, [(0, -113), (16, -119), (16, 134), (0, 142), (-15, 134), (-15, -118)],
             '#CDBD99', 0)
    kit.line(canvas, 0, -112, 0, 137, 3.5, '#8D7958')
    for left, divider in ((-285, -188), (21, 91)):
        for y in (-53, -16, 22, 60, 97):
            kit.line(canvas, left, y, left+264, y, 1.55, LINE)
        kit.line(canvas, divider, -55, divider, 99, 1.65, LINE)

    label(canvas, 'GENERAL LEDGER', -281, -77, 36)
    label(canvas, 'REFERENCE', -281, -26, 20)
    label(canvas, 'DETAILS', -175, -26, 20)
    data_text(canvas, 'OPENING ENTRY', -175, 10, 18)
    data_text(canvas, record, -281, 49, 19)
    data_text(canvas, 'VENDOR PAYMENT', -175, 49, 18)
    label(canvas, 'DISBURSEMENTS', 24, -76, 30)
    label(canvas, 'DATE', 25, -27, 22)
    label(canvas, 'AMOUNT', 283, -27, 22, align='right')
    for y, date, value in ((10, '04/08', '$725'), (47, '04/12', amount), (86, '04/21', '$180')):
        data_text(canvas, date, 26, y, 17)
        data_text(canvas, value, 280, y, 23, align='right')
    kit.line(canvas, 197, 53, 282, 53, 2.4, VIOLET_INK)


def document_base(canvas):
    shadow(canvas, -191, -152, 184, 154)
    for dx, dy, paper in ((17, 12, '#C8C9CD'), (-9, 5, WARM)):
        kit.rect(canvas, -189+dx, -151+dy, 189+dx, 151+dy, paper, 3, r=4, v=INK)
    kit.poly(canvas, [(-189, -152), (154, -152), (189, -117),
                      (189, 150), (-189, 150)], PAPER, 4, INK)
    kit.poly(canvas, [(154, -152), (154, -117), (189, -117)], WARM, 2, '#8E7B5F')
    kit.line(canvas, -165, -83, 157, -83, 2.9, INK)


def transfer_record(canvas, record, amount):
    document_base(canvas)
    label(canvas, 'TRANSFER RECORD', -163, -102, 38)
    for row, (key, value) in enumerate((
        ('REFERENCE', record), ('DATE', 'APRIL 12'), ('MEMO', 'VENDOR PAYMENT'),
    )):
        y = -45 + row*38
        label(canvas, key, -161, y, 22, VIOLET_INK)
        data_text(canvas, value, 158, y, 23, align='right')
        kit.line(canvas, -161, y+9, 158, y+9, 1.3, LINE)
    kit.rect(canvas, -165, 73, 160, 126, '#E9DBB9', 2, r=5, v=LINE)
    label(canvas, 'AMOUNT', -149, 107, 26)
    data_text(canvas, amount, 147, 108, 34, align='right')


def invoice(canvas, record, amount):
    document_base(canvas)
    label(canvas, 'VENDOR INVOICE', -163, -102, 38)
    data_text(canvas, record, -158, -43, 23)
    label(canvas, 'APRIL 12', 158, -43, 24, VIOLET_INK, align='right')
    kit.rect(canvas, -161, -21, 160, 19, '#DED6C2', 2, r=3, v=LINE)
    label(canvas, 'DESCRIPTION', -151, 7, 22, VIOLET_INK)
    label(canvas, 'AMOUNT', 149, 7, 22, VIOLET_INK, align='right')
    data_text(canvas, 'Services', -149, 58, 26)
    data_text(canvas, amount, 147, 58, 28, align='right')
    kit.line(canvas, -162, 76, 159, 76, 2, INK)
    label(canvas, 'TOTAL', -150, 114, 30)
    data_text(canvas, amount, 148, 116, 34, align='right')


def evidence_folder(canvas, record, amount):
    del amount
    shadow(canvas, -237, -133, 240, 126)
    back = [(-232, -131), (-95, -131), (-67, -103), (238, -103),
            (238, 122), (-232, 122)]
    kit.poly(canvas, back, '#9C7B48', 5, INK)
    canvas.save()
    canvas.rotate(-7)
    kit.rect(canvas, -165, -136, 199, 90, PAPER, 3, r=4, v=INK)
    for y in (-117, -94, -73):
        kit.line(canvas, -145, y, 170, y, 1.8, LINE)
    canvas.restore()
    kit.poly(canvas, [(-243, -56), (-94, -56), (-69, -33), (246, -33),
                      (227, 121), (-226, 121)], '#D2AE69', 5, INK)
    kit.line(canvas, -216, 112, 224, 112, 2.5, '#AB854B')
    kit.rect(canvas, -190, -8, 61, 85, PAPER, 2.7, r=5, v='#AD854C')
    label(canvas, 'CASE FILE', -174, 32, 40)
    data_text(canvas, record, -171, 65, 26)
    for x, y in ((141, 11), (141, 79)):
        kit.circ(canvas, x, y, 14, '#61492E', 3, INK)
        kit.circ(canvas, x, y, 4.2, '#DBB77D', 0)
    cord = skia.Path()
    cord.moveTo(137, 11)
    cord.cubicTo(176, -13, 159, 39, 141, 49)
    cord.cubicTo(108, 65, 122, 104, 145, 80)
    cord.cubicTo(158, 65, 141, 49, 126, 42)
    canvas.drawPath(cord, kit.ink(3.4, '#6B512F'))


def draw_sheet(canvas, record, amount):
    widgets.framed_bg(canvas)
    widgets.text(canvas, 'PAPER TRAIL', 960, 145, 72, WHITE, F_TITLE, 'center')
    kit.line(canvas, 850, 169, 1070, 169, 5, GOLD)
    placements = (
        (ledger, 514, 373, 0),
        (transfer_record, 1391, 370, -3),
        (invoice, 517, 730, 2),
        (evidence_folder, 1392, 733, 1),
    )
    for draw, x, y, angle in placements:
        canvas.save()
        canvas.translate(x, y)
        canvas.rotate(angle)
        draw(canvas, record, amount)
        canvas.restore()
    widgets.text(canvas, 'ILLUSTRATIVE RECORDS', 960, 962, 32, '#D7E0F0', F_LABEL2, 'center')
