"""Dirty Dollar Style 2 stills. Drawing kit based on aivxer's Claude 2D Animation Long Form."""
from pathlib import Path
import sys

import skia

OUTPUT = Path(__file__).resolve().parent
KIT = OUTPUT.parents[2] / ".claude" / "skills" / "documentary-animator"
sys.dont_write_bytecode = True
sys.path.insert(0, str(KIT))

from engine.core import F_LABEL, F_LABEL2, F_TITLE, GOLD, NAVY, PAPER, WHITE, W
from engine.kit import fp, ink
from engine.render import contact_sheet, still
from engine.widgets import framed_bg, text

CENTER = W // 2
TRUNK = 536
CARD_TOP = 760
OUTLINE = "#0A1124"
BRANCHES = (
    (388, "Retail", "100%"),
    (960, "Payments", "75%"),
    (1532, "Real estate", "60%"),
)
FILES = (
    "branching-01-holding.png",
    "branching-02-one-branch.png",
    "branching-03-two-branches.png",
    "branching-final.png",
)


def rounded(canvas, left, top, right, bottom, radius, paint):
    canvas.drawRoundRect(skia.Rect(left, top, right, bottom), radius, radius, paint)


def paper(canvas, x, top, width, height, title, secondary=None):
    left, right = x - width / 2, x + width / 2
    bottom = top + height
    rounded(canvas, left + 2, top + 10, right + 2, bottom + 10, 10, fp(OUTLINE, 165))
    rounded(canvas, left, top, right, bottom, 10, fp(PAPER))
    rounded(canvas, left, top, right, bottom, 10, ink(3, OUTLINE))
    canvas.drawLine(left + 22, top + 16, right - 22, top + 16, ink(4, GOLD))
    if secondary:
        text(canvas, title, x, top + 90, 70, NAVY, F_LABEL, "center")
        text(canvas, secondary, x, top + 139, 43, NAVY, F_LABEL2, "center")
    else:
        text(canvas, title, x, top + 98, 76, NAVY, F_LABEL, "center")


def draw(canvas, count):
    framed_bg(canvas)
    text(canvas, "Ownership structure", CENTER, 190, 84, WHITE, F_TITLE, "center")
    canvas.drawLine(CENTER - 45, 225, CENTER + 45, 225, ink(5, GOLD))
    active = BRANCHES[:count]
    if active:
        link = ink(8, GOLD)
        canvas.drawLine(CENTER, 448, CENTER, TRUNK, link)
        canvas.drawLine(active[0][0], TRUNK, max(CENTER, active[-1][0]), TRUNK, link)
        for x, name, stake in active:
            canvas.drawLine(x, TRUNK, x, CARD_TOP, link)
            canvas.drawCircle(x, TRUNK, 6, fp(GOLD))
            rounded(canvas, x - 103, 596, x + 103, 690, 47, fp(NAVY))
            rounded(canvas, x - 103, 596, x + 103, 690, 47, ink(3, GOLD))
            text(canvas, stake, x, 667, 70, GOLD, F_LABEL, "center")
            paper(canvas, x, CARD_TOP, 474, 167, name, "Business")
        canvas.drawCircle(CENTER, TRUNK, 7, fp(GOLD))
        text(canvas, "Illustrative ownership stakes", CENTER, 985, 48, WHITE, F_LABEL2, "center")
    paper(canvas, CENTER, 306, 640, 150, "Holding company")


if __name__ == "__main__":
    paths = [str(OUTPUT / filename) for filename in FILES]
    for count, path in enumerate(paths):
        still(draw, count, path)
    contact_sheet(paths, str(OUTPUT / "branching-contact-sheet.jpg"), cols=2)
