"""Original shot direction for 50% in 45 Days, using the channel's locked engine.

The house drawing kit derives from 2D Animation Long Form, made by aivxer.
"""
import math

import skia

from engine import anim, kit, shots, widgets as art
from engine.actor import Actor
from engine.cast import person
from engine.core import F_LABEL, F_TITLE, GOLD, NAVY, NAVY2, ORANGE, PAPER, WHITE

SHOT_BREAKS = tuple(f"n{i:03d}" for i in range(1, 48)) + ("n029b",)
FLAGS = (
    "Guaranteed returns",
    "Gains that never dip",
    "Secret strategy",
    "Unregistered seller",
    "Trouble withdrawing",
)


def ponzi(x, y, scale, **expressions):
    return Actor("ponzi", x, y, scale, hat=True, **expressions)


def queue(advancing=False):
    actors = []
    for index, name in enumerate(("saver", "worker", "retiree", "investor", "banker", "grad")):
        actor = Actor(name, 425 + index * 111, 868 + index * 2, .36,
                      face=.65, hat=name == "worker")
        actor.pose(0, ("hold", "pocket"))
        if advancing:
            actor.walk_to(.2 + .11 * index, .95 + .11 * index, actor.x + 36)
        actors.append(actor)
    return actors


def track(draw, travel, seconds):
    def moving(canvas, t):
        canvas.save()
        canvas.translate(-travel * kit.ease(kit.K(t, 0, seconds)), 0)
        draw(canvas, t)
        canvas.restore()

    return moving


def label(c, text, x=960, y=180, size=78, maxw=1450, color=WHITE):
    art.big_label(c, text, x, y, 1, color=color, size=size, maxw=maxw)


def card(c, text, lines, t):
    art.paper_card(c, 960, 550, text, lines, .23 + t, w=1120, h=630, rot=-2)


def downward_arrow(c, x, y, u):
    c.save()
    c.translate(x, y)
    c.rotate(90)
    art.arrow(c, 0, 0, 174, 0, u, ORANGE, wdt=34)
    c.restore()


def phone(c, x, y, t, *, title="Investment pitch", lines=(), alert=None, scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    kit.rect(c, -236, -330, 236, 330, NAVY2, 9, r=36)
    kit.rect(c, -211, -282, 211, 264, PAPER, 4, r=18)
    kit.rect(c, -54, -306, 54, -299, WHITE, 0, r=4)
    art.text(c, title, 0, -166, 51, NAVY, F_LABEL, "center")
    for index, line in enumerate(lines):
        art.text(c, line, 0, -62 + index * 70, 45, NAVY, F_LABEL, "center")
    if alert:
        if t > .5:
            downward_arrow(c, 0, 27, kit.K(t, .5, .4))
            art.text(c, alert, 0, 225, 45, NAVY, F_LABEL, "center")
    else:
        kit.rect(c, -156, 145, 156, 208, GOLD, 4, r=10)
        art.text(c, "VIEW DETAILS", 0, 190, 40, NAVY, F_LABEL, "center")
    c.restore()


def promise(c, t, caption):
    label(c, caption)
    art.paper_card(c, 530, 586, "Money sent", ["$100"], .35, w=615, h=420, rot=0)
    art.arrow(c, 867, 588, 1053, 588, kit.K(t, 0, .45), GOLD, 38)
    art.paper_card(c, 1390, 586, "Promised in 45 days", ["$150"], .27 + t, w=615, h=420, rot=0)


def build(tl):
    result = []
    mouths = tl.mouths()
    first_lines = {}
    for line in tl.lines:
        if line["chapter"]:
            first_lines.setdefault("chapter:" + line["beat"][2:], line["id"])
    sequence = []
    for line in tl.lines:
        id_ = line["id"]
        chapter = "chapter:" + line["beat"][2:]
        if first_lines.get(chapter) == id_:
            sequence.append(chapter)
        sequence.append(id_)
        if id_ == "n006":
            sequence.append("title")
    sequence.extend(("outro", "endscreen", "end"))
    next_marker = dict(zip(sequence, sequence[1:]))

    def duration(key):
        return tl.dur(key, next_marker[key])

    def lead(key):
        return tl.start(key) - tl.at(key)

    def add(key, draw, **options):
        span = duration(key)
        options.setdefault("zoom", (1.0, 1.055))
        if "sfx" in options:
            options["sfx"] = [(at, name) for at, name in options["sfx"] if 0 <= at < span]
        result.append(dict(dur=span, draw=draw, **options))
        if key != sequence[len(result) - 1]:
            raise ValueError(f"Unexpected shot order at {key}")

    def graphic(key, draw, **options):
        # Keep the double frame inside the picture; motion lives inside the frame.
        options.setdefault("zoom", (1.0, 1.014))
        add(key, shots.plain(draw), **options)

    def wide(key, place, actors, overlay=None, front=False, travel=0, **options):
        back, foreground = ((), actors) if front else (actors, ())
        draw = shots.wide(place, back, foreground, overlay, tl.at(key))
        if travel:
            draw = track(draw, travel, duration(key))
        add(key, draw, **options)

    def close(key, actor, bg_focus, overlay=None):
        add(key, shots.closeup("night/office", actor, focus=bg_focus,
                               overlay=overlay, t0=tl.at(key)), zoom=(1.01, 1.065))

    def text_card(key, words=()):
        # Typography starts at the shot boundary, before the spoken line.
        draw = shots.card("text", tl.cues[key][1], text=tl.by_id[key]["text"], gold_words=words)
        add(key, draw, zoom=(1.0, 1.035))

    def chapter(number):
        key = f"chapter:{number}"
        add(key, shots.card("chapter", duration(key), n=number,
                            title=tl.by_id[first_lines[key]]["chapter"]))

    def counter(c, t, key, x, y, *, label_text=None, size=106):
        value = tl.by_id[key]["counter"]
        art.counter(c, x, y, value["from"], value["to"],
                    kit.K(t, lead(key) + .2, 1.4), unit=value["unit"], size=size,
                    label=label_text, decimals=2 if value["to"] == 2.5 else 0)

    def tag(c, t):
        art.lower_third(c, "Charles Ponzi", "Boston, 1920", kit.K(t, 0, .38), x=100, y=872)

    def opening(c, t):
        kit.rect(c, 404, 490, 811, 570, NAVY, 5, r=14)
        art.text(c, "50% IN 45 DAYS", 608, 546, 57, GOLD, F_LABEL, "center")
        art.lower_third(c, "Boston", "July 1920", 1, x=335, y=840)

    wide("n001", "night/street1920", queue(True), opening, front=True,
         travel=160, focus=(755, 637), zoom=(1.45, 1.51))
    wide("n002", "night/street1920", queue(), front=True,
         focus=(765, 713), zoom=(1.73, 1.80))
    graphic("n003", lambda c, t: promise(c, t, "The promise"), sfx=[(.4, "coin")])
    close("n004", ponzi(1010, 1390, 1.92, face=.35, eyes="half"),
          (930, 580), lambda c, t: (anim.prison_bars(c, t, .58), tag(c, t)))
    close("n005", ponzi(775, 1370, 1.84, face=.48), (810, 620),
          lambda c, t: phone(c, 1416, 576, t, title="New message",
                             lines=("A guaranteed return",), scale=.75))
    graphic("n006", lambda c, t: (label(c, "A letter from abroad"),
                                  anim.envelope(c, 960, 685, t, "Reply coupon", ())),
            sfx=[(.5, "paper")])
    add("title", shots.card("title", duration("title"), title="50% in 45 Days", gold_word="50%"))

    chapter(1)
    graphic("n007", lambda c, t: (
        label(c, "Boston · 1903"),
        art.paper_card(c, 960, 610, "Charles Ponzi", ["Arrived from Italy"], .29 + t,
                       w=1100, h=540, rot=-3)), sfx=[(.46, "paper")])
    graphic("n008", lambda c, t: (label(c, "His cash on arrival"),
                                  counter(c, t, "n008", 960, 560, label_text="by his account", size=168)))
    graphic("n009", lambda c, t: (card(c, "Montreal", ["Forgery conviction"], t),
                                  anim.prison_bars(c, max(0, t - 1.1), .40)),
            sfx=[(1.5, "stamp")])
    guard = Actor("agent", 1070, 1365, 1.88, face=-.56, eyes="half")
    guard.pose(.20, ("chin", "down")).say(tl, "n010", mouths)
    close("n010", guard, (1190, 650),
          lambda c, t: art.lower_third(c, "Dramatization", "Montreal", 1))
    detained = ponzi(895, 1370, 1.82, face=.53, eyes="dot").say(tl, "n011", mouths)
    close("n011", detained, (675, 610), lambda c, t: anim.prison_bars(c, .6))
    graphic("n012", lambda c, t: (
        card(c, "Court record", ["Montreal", "Convicted of forgery"], t),
        art.stamp(c, "FILED", 1130, 691, t - .5, size=96)),
        sfx=[(.5, "stamp")])
    graphic("n013", lambda c, t: (label(c, "Back in Boston"),
                                  anim.envelope(c, 960, 695, t, "Reply coupon", ("International postage",))),
            sfx=[(.46, "paper")])

    chapter(2)
    graphic("n014", lambda c, t: card(c, "International reply coupon", ["Prepaid postage", "For one reply"], t),
            sfx=[(.3, "paper")])
    graphic("n015", lambda c, t: anim.map_route(c, t, dur=duration("n015") * .64))
    graphic("n016", lambda c, t: (
        label(c, "Postwar exchange rates"),
        art.paper_card(c, 532, 568, "Europe", ["Cheaper coupon"], .35, w=625, h=398, rot=0),
        art.paper_card(c, 1390, 568, "United States", ["More postage"], .25 + t, w=625, h=398, rot=0),
        art.arrow(c, 884, 573, 1033, 573, kit.K(t, 0, .6), GOLD, 35)))
    graphic("n017", lambda c, t: anim.map_route(c, t + .15, dur=duration("n017") * .7,
                                                label_a="Coupon", label_b="Postage"))
    graphic("n018", lambda c, t: (label(c, "Postage isn't rent"),
                                  anim.hand_slam(c, 1030, 584, t, item="paper", title="Rent due",
                                                 lines=("Payment in cash",), hit=.43)),
            sfx=[(.43, "stamp")])
    investor = Actor("worker", 1080, 1360, 1.92, face=-.55, eyes="wide")
    investor.pose(.2, ("chin", "down")).say(tl, "n019", mouths)
    close("n019", investor, (1160, 630),
          lambda c, t: art.lower_third(c, "Dramatization", "Investor", 1))
    speaker = ponzi(835, 1380, 1.95, face=.66, eyes="half", mouth="smirk")
    speaker.pose(.22, ("pocket", "gesture")).say(tl, "n020", mouths)
    close("n020", speaker, (745, 590))
    graphic("n021", lambda c, t: (
        label(c, "Where did the cash come from?"),
        anim.ledger(c, 960, 590, t, [("Cash received", ""), ("Payments out", "")], flips=3)),
        sfx=[(.25, "paper")])

    chapter(3)
    wide("n022", "night/street1920", queue(True), front=True, focus=(975, 584), zoom=(1.43, 1.51))
    graphic("n023", lambda c, t: (
        label(c, "Who paid whom?"), anim.pyramid(c, 960, 840, t + .25, levels=4)))
    graphic("n024", lambda c, t: (
        label(c, "The line had to grow"), anim.pyramid(c, 960, 870, t + 1.1, levels=5,
                                                     wobble=kit.K(t, .75, 1.4))))
    graphic("n025", lambda c, t: (
        label(c, "Money taken in"), art.falling_money(c, t, n=8, area=(240, 240, 1680, 710)),
        counter(c, t, "n025", 960, 547, label_text="Smithsonian estimate", size=138)))
    graphic("n026", lambda c, t: (
        label(c, "Where it went"),
        art.paper_card(c, 541, 598, "Property", ["A mansion"], .35, w=650, h=448, rot=-4),
        art.paper_card(c, 1368, 598, "Bank stock", ["A stake in a bank"], .3 + t, w=650, h=448, rot=4)),
        sfx=[(.36, "paper")])
    wide("n027", "night/street1920", queue(), front=True,
         focus=(1010, 669), zoom=(1.68, 1.74))

    graphic("n028", lambda c, t: (
        label(c, "The withdrawals"),
        anim.hand_slam(c, 960, 556, t, item="cash", hit=.42, side="left")),
        sfx=[(.42, "cash")])
    text_card("n029", ("publicist",))
    graphic("n029b", lambda c, t: (
        label(c, "The tip came from inside"),
        anim.newspaper(c, 960, 610, t + .36, "The Boston Post", "A story from inside")),
        sfx=[(.36, "paper")])

    chapter(4)
    mcmasters_spec = person("banker", suit=NAVY2, suit_d=NAVY, tie="#B8A268",
                            moustache=False, bowtie=False)
    mcmasters_tag = lambda c, t: art.lower_third(c, "William McMasters", "Publicist", 1)
    mcmasters = Actor("banker", 875, 1225, 1.55, spec=mcmasters_spec, face=.48)
    mcmasters.pose(.3, ("hold", "gesture"))
    close("n030", mcmasters, (825, 580), mcmasters_tag)
    mcmasters = Actor("banker", 840, 1355, 1.97, spec=mcmasters_spec, face=.44, eyes="wide")
    mcmasters.pose(.31, ("present", "down")).say(tl, "n031", mouths)
    close("n031", mcmasters, (780, 610), mcmasters_tag)
    editor = Actor("ceo", 1110, 1370, 1.93, face=-.55, eyes="half")
    editor.pose(.2, ("point", "down")).say(tl, "n032", mouths)
    close("n032", editor, (1340, 610),
          lambda c, t: art.lower_third(c, "Dramatization", "Editor", 1))
    graphic("n033", lambda c, t: (
        label(c, "August 2, 1920"),
        anim.newspaper(c, 960, 620, t + .37, "The Boston Post",
                       "Hopelessly insolvent", "McMasters on Ponzi’s debts")),
        sfx=[(.34, "paper")])
    text_card("n034", ("coupons", "money"))
    graphic("n035", lambda c, t: (
        card(c, "Court record", ["Montreal", "Convicted of forgery"], t),
        anim.prison_bars(c, max(0, t - .72), .35)), sfx=[(1.07, "stamp")])
    graphic("n036", lambda c, t: (
        label(c, "Arrest and collapse"),
        anim.handcuffs(c, 675, 580, t, close_at=.42),
        art.paper_card(c, 1330, 580, "Bank", ["Failed"], .35, w=580, h=420, rot=-3)),
        sfx=[(.42, "stamp")])
    graphic("n037", lambda c, t: (
        label(c, "The investors were left with the losses", size=72),
        art.paper_card(c, 820, 610, "Promissory note", ["Payment stopped"], .35, w=1080, h=458, rot=-3),
        downward_arrow(c, 1470, 460, kit.K(t, 0, .75))),
        sfx=[(.62, "falling")])
    graphic("n038", lambda c, t: (
        card(c, "The outcome", ["Federal mail fraud plea", "Public Service Pulitzer"], t),
        art.stamp(c, "GUILTY PLEA", 1210, 710, t - .58, size=83)),
        sfx=[(.58, "stamp")])
    graphic("n039", lambda c, t: (
        label(c, "Real coupon. False promise.", size=78),
        art.paper_card(c, 617, 577, "Postage", ["A real coupon"], .35, w=700, h=442, rot=0),
        art.paper_card(c, 1330, 577, "The pitch", ["A promise of profit"], .28 + t, w=660, h=442, rot=0)))

    chapter(5)
    saver = Actor("saver", 700, 1015, 1.14, face=.5, light=1, rim="#FFE3A6", eyes="wide")
    saver.pose(.21, ("phone", "down"))
    wide("n040", "day/living", [saver], front=True, focus=(890, 615), zoom=(1.07, 1.14),
         overlay=lambda c, t: phone(c, 1300, 583, t, title="Forwarded message", scale=.9))
    wide("n041", "day/living", [saver], front=True, focus=(1065, 560), zoom=(1.10, 1.16),
         overlay=lambda c, t: phone(c, 1345, 568, t, title="Account balance", lines=("Displayed balance", "$150"), scale=.97))
    graphic("n042", lambda c, t: promise(c, t, "The same pitch today"))
    wide("n043", "day/living", [saver], front=True, focus=(1000, 605), zoom=(1.08, 1.15),
         overlay=lambda c, t: phone(c, 1310, 562, t, title="Withdrawal", alert="Still pending", scale=.94))

    analyst = Actor("analyst", 626, 1005, 1.20, face=.55, light=1, rim="#FFE3A6")
    analyst.pose(.25, ("down", "point"))
    line_words = tl.by_id["n044"]["text"].split()
    first_words = ("guaranteed", "gains", "secret", "unregistered", "trouble")
    starts = [lead("n044") + tl.cues["n044"][1] * next(
        i for i, word in enumerate(line_words) if word.lower().strip(",.") == trigger) / len(line_words)
        for trigger in first_words]

    def board(c, t):
        kit.rect(c, 829, 128, 1735, 891, PAPER, 7, r=15)
        art.text(c, "SEC RED FLAGS", 1282, 239, 72, NAVY, F_TITLE, "center")
        for i, (flag, start) in enumerate(zip(FLAGS, starts)):
            u = kit.K(t, start, .23)
            if u > 0:
                y = 355 + i * 110
                kit.poly(c, [(908, y - 48), (949, y - 48), (928, y - 10)], ORANGE, 2)
                art.text(c, flag, 978, y, 58, NAVY, F_LABEL, alpha=int(255 * u))

    wide("n044", "day/lesson", [analyst], board, front=True,
         focus=(1125, 550), zoom=(1.025, 1.08), sfx=[(x, "pop") for x in starts])
    wide("n045", "day/lesson", [analyst], front=True, focus=(1100, 555),
         overlay=lambda c, t: anim.hand_slam(c, 1260, 568, t, item="sticky",
                                            title="Check Investor.gov", hit=.45),
         sfx=[(.45, "paper")])

    modern = [Actor(name, x, y, .58, face=.55).pose(0, ("phone", "down"))
              for name, x, y in (("worker", 699, 890), ("saver", 925, 903), ("grad", 1150, 916))]

    def screens(c, t):
        for actor in modern:
            x, y = kit.hand_pos(actor.x, actor.y, actor.s, ("phone", "down"), -1)
            kit.rect(c, x - 26, y - 48, x + 26, y + 29, NAVY, 5, r=7)
            kit.rect(c, x - 19, y - 41, x + 19, y + 20, "#F8E5AC", 3, r=3)
            if math.sin(t * 2) > 0:
                kit.rect(c, x - 13, y - 24, x + 13, y - 19, GOLD, 0)

    wide("n046", "night/street", modern, screens, front=True,
         focus=(943, 727), zoom=(1.78, 1.86))
    text_card("n047", ("line?",))
    add("outro", lambda c, t: anim.outro(c, t, channel="50% IN 45 DAYS"), zoom=(1.0, 1.015))
    add("endscreen", anim.end_screen, zoom=(1.0, 1.018))
    assert len(result) == len(next_marker)
    return result
