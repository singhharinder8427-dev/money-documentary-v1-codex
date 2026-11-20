"""Episode-local shot coverage for The Investigation That Reached Nvidia's CEO."""
import json
from pathlib import Path

import skia

from engine import anim, kit, shots, widgets as w
from engine.actor import Actor
from engine.cast import person
from engine.core import BLACK, FPS, F_LABEL, F_TITLE, GOLD, H, NAVY, PAPER, WHITE, W
from engine.sets import SETS

SCRIPT = json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'))
LINES = SCRIPT['lines']
SHOT_BREAKS = tuple(
    line['id'] for i, line in enumerate(LINES)
    if i == 0 or line['visual'] != LINES[i - 1]['visual']
)
JENSEN = person('ceo', skin='#D7A27E', skin_d='#B77D5E', hair='silver', hair_col='#E5E5E5',
                glasses=True, outfit='open', suit='#272C37', suit_d='#121722',
                shirt='#131721', tie=None)

STEEL = '#6D83A6'
DARK = '#0F182C'
MID = '#39577E'
PALE = '#CBD9EB'

# Reuse perspective families deliberately. The framing and action differ on each return.
HALL = {
    'inspection': (0, 'A', 'flashlight'),
    'rack_check': (1, 'A', 'inventory'),
    'screen_glow': (2, 'A', 'console'),
    'rack_wide': (0, 'B', 'status'),
    'server_console': (2, 'B', 'console'),
    'inspection_return': (1, 'A', 'check'),
    'server_after': (0, 'C', 'status'),
    'return_aisle': (0, 'A', 'return'),
    'closing_rack': (1, 'A', 'return'),
}

FILES = {
    'investigation_pin': ('COMMERCE INQUIRY', 'OPENED 2024', 'Potential chip diversion'),
    'sales_records': ('RECORDS REQUEST', 'MAY 2025', 'Direct and indirect sales'),
    'separate_rooms': ('TWO INQUIRIES', 'SINGAPORE   •   UNITED STATES', 'Separate laws and findings'),
    'split_file': ('SINGAPORE POLICE', 'FEBRUARY 2026', 'Insufficient evidence on declaration offenses'),
    'warning': ('SEPARATE WARNING', 'SINGAPORE POLICE', 'Information about her role'),
    'board_file': ('BOARD STATEMENT', 'NOVEMBER 8, 2026', 'Independent review opened'),
    'capitol_letter': ('HOUSE REQUEST', 'NOVEMBER 4, 2026', 'Security procedures and interactions'),
    'subpoena': ('CALIFORNIA DOJ', 'NOVEMBER 19, 2026', 'Investigative subpoena'),
    'return_form': ('DESTINATION REVIEW', 'CONFIRMED LEG', 'Singapore to Malaysia'),
}

SETS_BY_SCENE = {
    'remote_user': 'night/kitchen',
    'singapore_aisle': 'day/warehouse',
    'handoff': 'day/warehouse',
    'press_monitor': 'night/investigation_room',
    'board_door': 'night/office',
    'board_push': 'day/boardroom',
    'jensen_exit': 'night/office',
    'call_wide': 'day/boardroom',
    'earnings_counter': 'day/boardroom',
    'congress_next': 'night/investigation_room',
    'wallet_room': 'day/living',
    'wallet_statement': 'day/living',
    'wallet_close': 'day/living',
    'wallet_hold': 'day/living',
}

EFFECTS = {
    'inspection': ((0.3, 'whoosh'),),
    'server_slide': ((0.9, 'tick'),),
    'handoff': ((1.05, 'tick'),),
    'sales_records': ((0.85, 'paper'),),
    'board_door': ((0.05, 'boom'),),
    'capitol_letter': ((0.85, 'paper'),),
    'subpoena': ((0.85, 'paper'),),
    'wallet_statement': ((0.85, 'paper'),),
}
VISUALS = set(HALL) | set(FILES) | set(SETS_BY_SCENE) | {'server_slide', 'graphics_pc', 'closed_order', 'route'}


def show_tag(c, text='ILLUSTRATION'):
    kit.rect(c, 1460, 55, 1830, 116, DARK, 3, r=8)
    w.text(c, text, 1645, 98, 30, WHITE, F_LABEL, 'center')


def fit_text(c, text, x, y, size, width, color=WHITE, font=F_LABEL, align='left'):
    measured = skia.Font(font, size).measureText(text)
    w.text(c, text, x, y, min(size, size * width / max(measured, 1)), color, font, align)


def backlight(c, x, y, r, bright=MID, dark=DARK):
    shader = kit.radial(x, y, r, [kit.col(bright), kit.col(dark)])
    c.drawPaint(skia.Paint(Shader=shader))


def hall(c, t, mode, rack, action, duration):
    if mode == 0:
        backlight(c, 960, 380, 1040)
        kit.poly(c, [(0, 1080), (710, 360), (1210, 360), (1920, 1080)], '#223652', 0)
        for x in (240, 540, 960, 1380, 1680):
            kit.line(c, 960, 399, x, 1080, 3, '#4F6A8B', 80)
        for i in range(5, 0, -1):
            size = 1 / (1 + i * .78)
            x = 960 - 650 * size
            y = 420 - 252 * size
            for left in (x - 530 * size, W - x):
                rack_face(c, left, y, 530 * size, 1190 * size, rack, t)
            width = 500 * size
            kit.rect(c, 960 - width / 2, y - 30, 960 + width / 2, y - 11, PALE, 0, r=6)
        if action == 'flashlight':
            u = kit.ease(kit.K(t, 0, 3.4))
            c.drawCircle(590 + 380 * u, 545 - 100 * u, 190, kit.fp('#BED8FF', 63, blur=50))
        return
    backlight(c, 840, 465, 1140)
    rack_face(c, 120, 108, 1120 if mode == 1 else 660, 835, rack, t)
    if mode == 1:
        x = kit.lerp(520, 1020, kit.ease(kit.K(t, .2, min(duration, 4.0))))
        if action == 'check':
            c.drawCircle(x, 405, 125, kit.fp('#D9ECFF', 72, blur=40))
            kit.line(c, x - 103, 403, x + 103, 403, 4, GOLD, 140)
        kit.rect(c, 1110, 288, 1720, 542, '#223754', 6, r=13)
        w.text(c, 'RACK INVENTORY', 1160, 381, 54, WHITE)
        w.text(c, 'DESTINATION CHECK', 1160, 467, 38, GOLD)
    else:
        monitor(c, 880, 210, 1707, 825, 'LOCATION / ACCESS',
                ('PHYSICAL INVENTORY', 'REMOTE SESSION'), t)


def rack_face(c, x, y, width, height, rack, t):
    kit.rect(c, x, y, x + width, y + height, '#293D5B', 4, r=10)
    kit.rect(c, x + width * .07, y + height * .065, x + width * .93, y + height * .93, DARK, 3, r=5)
    for row in range(7):
        top = y + height * (.10 + row * .112)
        kit.rect(c, x + width * .12, top, x + width * .88, top + height * .08, '#314968', 3, r=4)
        for col in range(4):
            sx = x + width * (.20 + col * .092)
            kit.line(c, sx, top + height * .024, sx, top + height * .057, max(2, width * .008), '#7A98BD', 80)
        live = int(158 + 56 * kit.ease(kit.K((t + row * .17) % 2.8, .1, .8)))
        c.drawCircle(x + width * .81, top + height * .044, max(2, width * .017), kit.fp(GOLD, live))
    if width > 200:
        fit_text(c, f'RACK {rack}', x + width * .14, y + height * .97, width * .052, width * .62, PALE)


def monitor(c, x, y, right, bottom, heading, lines, t):
    kit.rect(c, x, y, right, bottom, '#202F4A', 7, r=20)
    kit.rect(c, x + 25, y + 24, right - 25, bottom - 24, DARK, 4, r=12)
    fit_text(c, heading, x + 60, y + 120, 66, right - x - 116, GOLD)
    rules_y = y + 145
    kit.line(c, x + 61, rules_y, right - 61, rules_y, 4, MID)
    for i, value in enumerate(lines):
        alpha = int(150 + 105 * kit.ease(kit.K(t, .20 + .25 * i, .45)))
        fit_text(c, value, x + 61, rules_y + 90 + 65 * i, 43, right - x - 121, PALE)
        kit.line(c, x + 63, rules_y + 102 + 65 * i, x + 96, rules_y + 102 + 65 * i, 3, GOLD, alpha)


def workstation(c, t, device):
    backlight(c, 955, 580, 1150, '#4D6080')
    kit.rect(c, 270, 225, 1650, 890, '#1B2D49', 5, r=24)
    kit.rect(c, 292, 246, 1628, 867, '#395477', 3, r=13)
    kit.rect(c, 486, 399, 1338, 683, '#202D44', 6, r=11)
    u = kit.ease_out(kit.K(t, .25, .65))
    x = 1225 - 510 * u
    kit.rect(c, x, 438, x + 486, 646, '#2D3E58', 7, r=8)
    if device == 'GPU':
        for j in range(2):
            cx = x + 171 + 149 * j
            kit.circ(c, cx, 543, 54, NAVY, 4)
            for offset in (-17, 0, 17):
                kit.line(c, cx - 28, 543 + offset, cx + 28, 543 + offset, 5, STEEL)
    else:
        for j in range(9):
            kit.rect(c, x + 53 + 38 * j, 491, x + 72 + 38 * j, 593, '#17283F', 1, r=3)
    kit.line(c, x + 26, 629, x + 416, 629, 5, GOLD)
    if t < 1.45:
        anim.sleeve(c, 1710, 1060, x + 345 + 500 * kit.ease(kit.K(t, .86, .59)), 625 + 260 * kit.ease(kit.K(t, .86, .59)))
    w.text(c, device, 525, 770, 46, PAPER)


def paper(c, x, y, title, date, description, angle=0):
    c.save()
    c.translate(x, y)
    c.rotate(angle)
    kit.rect(c, -430, -233, 448, 251, '#233751', 0, r=10)
    kit.rect(c, -440, -247, 436, 233, PAPER, 5, r=9)
    fit_text(c, title, -380, -120, 70, 752, NAVY)
    fit_text(c, date, -379, -49, 42, 750, MID)
    kit.line(c, -379, -15, 372, -15, 5, GOLD)
    fit_text(c, description, -380, 72, 38, 756, NAVY)
    for i, length in enumerate((646, 524, 580)):
        kit.line(c, -379, 107 + i * 32, -379 + length, 107 + i * 32, 3, '#8395AA')
    c.restore()


def evidence(c, t, fields, variant):
    backlight(c, 900, 520, 1210, '#576786' if variant % 2 else MID)
    kit.rect(c, 250, 192, 1670, 884, '#1A2942', 5, r=39)
    kit.rect(c, 275, 217, 1645, 859, '#303E57', 3, r=25, v=STEEL)
    if variant in (2, 5, 8):
        kit.rect(c, 1060, 285, 1518, 729, '#AB8B64', 4, r=12)
        kit.rect(c, 1122, 331, 1475, 384, PAPER, 2, r=5)
        w.text(c, 'CASE MATERIALS', 1145, 368, 29, NAVY)
    u = kit.ease_out(kit.K(t, .10, .75))
    x = kit.lerp(1080, 900 + 31 * (variant % 3), u)
    y = kit.lerp(660, 527, u)
    paper(c, x, y, *fields, angle=(-5, 0, 5)[variant % 3])
    if t < 1.1:
        release = kit.ease(kit.K(t, .65, .45))
        anim.sleeve(c, W + 100, H, x + 405 + 450 * release, y + 156 + 330 * release)


def room_route(c, t):
    w.framed_bg(c)
    w.text(c, 'DOCUMENTED SERVER MOVEMENT', 960, 305, 63, WHITE, F_TITLE, 'center')
    for x, label in ((520, 'SINGAPORE'), (1180, 'MALAYSIA')):
        kit.circ(c, x, 570, 25, GOLD, 4)
        w.text(c, label, x, 671, 62, WHITE, F_LABEL, 'center')
    w.arrow(c, 554, 570, 1145, 570, kit.ease(kit.K(t, .15, 1.75)), wdt=24)
    for x in range(1244, 1530, 52):
        kit.circ(c, x, 570, 6, STEEL, 0)
    w.text(c, '?', 1554, 588, 67, PALE)
    w.text(c, 'ONWARD DESTINATION UNDER INVESTIGATION', 960, 805, 42, WHITE, F_LABEL, 'center')


def crate(c, t, *, closed=False):
    x = kit.lerp(605, 822, kit.ease_out(kit.K(t, .1, .95)))
    kit.poly(c, [(x, 814), (x + 413, 814), (x + 506, 752), (x + 98, 752)], '#AD8A60', 5)
    kit.rect(c, x, 815, x + 414, 971, '#8D6C4D', 6, r=6)
    kit.poly(c, [(x + 414, 815), (x + 506, 752), (x + 506, 900), (x + 414, 971)], '#65513E', 5)
    kit.rect(c, x + 75, 840, x + 360, 937, PAPER, 3, r=6)
    w.text(c, 'ORDER ON HOLD' if closed else 'SERVER EQUIPMENT', x + 97, 899, 42, NAVY)


def laptop(c, t, heading, lines):
    kit.rect(c, 915, 882, 1712, 944, '#7087A5', 6, r=18)
    monitor(c, 1000, 489, 1653, 888, heading, lines, t)


def wallet(c, t, scene):
    if scene == 'wallet_statement':
        evidence(c, t, ('SPY HOLDINGS', 'NOVEMBER 18, 2026', 'NVIDIA • 5.78% OF FUND'), 4)
        kit.rect(c, 636, 803, 1279, 916, NAVY, 5, r=10)
        w.text(c, '$578', 780, 875, 69, GOLD, F_LABEL, 'center')
        w.text(c, 'PER $10,000 IN SPY', 864, 874, 45, WHITE)
    elif scene == 'wallet_close':
        fold = kit.ease(kit.K(t, .65, .95))
        top = kit.lerp(577, 846, fold)
        kit.rect(c, 901, 870, 1710, 930, STEEL, 5, r=10)
        kit.poly(c, [(980, top), (1649, top), (1654, 876), (964, 876)], '#2B415E', 5)
        kit.line(c, 981, 873, 1631, 873, 2, PALE)
    elif scene == 'wallet_hold':
        c.save()
        c.translate(1330, 760)
        c.scale(.67, .67)
        paper(c, 0, 0, 'FUND HOLDINGS', 'NVIDIA', 'A dated disclosure', -5)
        c.restore()
    else:
        laptop(c, t, 'FUND HOLDINGS', ('NVIDIA', 'VIEW FUND HOLDINGS'))


def closed_door(c, t):
    backlight(c, 1110, 430, 1080)
    kit.rect(c, 621, 138, 1346, 976, '#3C5577', 6, r=3)
    kit.rect(c, 659, 159, 1306, 965, '#202D48', 4, r=3)
    kit.rect(c, 727, 280, 1238, 668, '#2D4162', 3, r=7)
    kit.line(c, 1277, 165, 1277, 922, 3, '#829BC1', 94)
    kit.rect(c, 836, 425, 1140, 511, DARK, 4, r=11)
    w.text(c, 'BOARDROOM', 988, 481, 49, PALE, F_LABEL, 'center')
    kit.rect(c, 1176, 695, 1255, 715, GOLD, 3, r=9)


def case_folder(c, t):
    y = kit.lerp(940, 803, kit.ease_out(kit.K(t, .27, .75)))
    kit.poly(c, [(824, y), (1308, y), (1405, y - 119), (921, y - 119)], '#BE9B68', 5)
    kit.poly(c, [(957, y - 91), (1334, y - 91), (1274, y - 21), (898, y - 21)], PAPER, 3)
    w.text(c, 'BOARD REVIEW', 963, y - 40, 35, NAVY)


def conference_speaker(c, t):
    kit.oval(c, 790, 685, 1130, 880, '#14223A', 6)
    kit.oval(c, 806, 673, 1113, 848, '#2A4164', 5)
    for i in range(5):
        kit.line(c, 899, 713 + i * 14, 1023, 713 + i * 14, 3, STEEL)
    c.drawCircle(961, 811, 7, kit.fp(GOLD, int(155 + 90 * kit.ease(kit.K(t % 3, .2, .7)))))
    w.text(c, 'NOVEMBER 17, 2026', 960, 959, 37, WHITE, F_LABEL, 'center', stroke=5)


def choose_body(scene, start, duration, first):
    if scene in HALL:
        mode, rack, action = HALL[scene]
        return lambda c, t: hall(c, t, mode, rack, action, duration)
    if scene in FILES:
        number = tuple(FILES).index(scene)
        return lambda c, t: evidence(c, t, FILES[scene], number)
    if scene in ('server_slide', 'graphics_pc'):
        device = 'GPU' if scene == 'graphics_pc' else 'SERVER BLADE'
        return lambda c, t: workstation(c, t, device)
    if scene == 'route':
        return room_route
    if scene == 'board_door':
        return closed_door
    place = SETS_BY_SCENE.get(scene, 'day/warehouse')
    if scene == 'jensen_exit':
        actor = Actor('ceo', 1080, 1310, 2.0, face=-.45, spec=JENSEN, mouth='flat')
        actor.pose(.4, ('pocket', 'down'))
        return shots.closeup(place, actor, focus=(970, 526), t0=start)
    if scene.startswith('wallet'):
        if scene == 'wallet_statement':
            return lambda c, t: wallet(c, t, scene)
        saver = Actor('saver', 678, 1050, 1.24, face=.45, light=1, rim='#FFE3A6', mouth='flat')
        saver.pose(.62, ('down', 'present')).pose(2.4, ('down', 'down'))
        return shots.wide(place, front_actors=[saver], overlay=lambda c, t: wallet(c, t, scene), t0=start)
    if scene == 'earnings_counter':
        def overlay(c, t):
            monitor(c, 560, 240, 1375, 837, 'QUARTERLY SALES', ('QUARTER ENDED OCTOBER 25, 2026',), t)
            u = kit.K(t, first, 1.37)
            w.counter(c, 960, 650, 0, 115.8, u, suffix='B', decimals=1, size=124, panel=False)
        return shots.wide(place, overlay=overlay, t0=start)
    if scene in ('handoff', 'closed_order'):
        return shots.wide(place, overlay=lambda c, t: crate(c, t, closed=scene == 'closed_order'), t0=start)
    panels = {
        'remote_user': ('REMOTE SESSION', ('LAPTOP HERE', 'EQUIPMENT ELSEWHERE')),
        'press_monitor': ('NEWS REPORTS', ('OCTOBER 2026', 'REPORTED INTELLIGENCE CONCERNS')),
        'congress_next': ('INTERVIEW SCHEDULE', ('DEC 1   •   JENSEN HUANG', 'DEC 2   •   TIM TETER')),
    }
    if scene in panels:
        heading, values = panels[scene]
        return shots.wide(place, overlay=lambda c, t: monitor(c, 990, 356, 1700, 858, heading, values, t), t0=start)
    overlay = {'board_push': case_folder, 'call_wide': conference_speaker}.get(scene)
    return shots.wide(place, overlay=overlay, t0=start)


def named_body(scene, start, duration, first):
    # Lazy construction lets timeline checks and the audio stage run without writing set previews.
    resolved = None
    def draw(c, t):
        nonlocal resolved
        if resolved is None:
            resolved = choose_body(scene, start, duration, first)
        resolved(c, t)
    def hud(c, t):
        show_tag(c)
        if scene == 'jensen_exit':
            w.lower_third(c, 'JENSEN HUANG', 'Nvidia co-founder', t)
    if scene in HALL:
        focus = (960, 520) if scene != 'return_aisle' else ((1140, 551), (834, 514))
    elif scene in ('singapore_aisle', 'handoff', 'closed_order'):
        focus = ((845, 553), (1035, 638))
    elif scene.startswith('wallet'):
        focus = ((960, 564), (1040, 597)) if scene != 'wallet_close' else ((1040, 597), (876, 558))
    else:
        focus = (960, 540)
    zoom = {'route': (1, 1), 'return_aisle': (1.13, 1.02), 'graphics_pc': (1.09, 1.17),
            'board_door': (1.00, 1.16), 'server_slide': (1.01, 1.12)}.get(scene, (1.00, 1.08))
    draw.vignette = .37 if scene.startswith('wallet') or scene == 'route' else .68
    draw.vignette_inner = .42
    effects = list(EFFECTS.get(scene, ()))
    if scene == 'earnings_counter':
        effects.extend(((first + .11, 'tick'), (first + 1.43, 'ding')))
    return dict(draw=draw, hud=hud, focus=focus, zoom=zoom, sfx=effects,
                rot=(-.4, .4) if scene in FILES else (0, 0))


def title(c, t, duration):
    c.drawRect(skia.Rect(0, 0, W, H), kit.fp(BLACK))
    u = .92 + .08 * kit.ease_out(kit.K(t, 0, max(duration * .55, .1)))
    c.save()
    c.translate(960, 540)
    c.scale(u, u)
    fit_text(c, 'THE INVESTIGATION THAT', 0, -32, 95, 1600, WHITE, F_TITLE, 'center')
    fit_text(c, 'REACHED NVIDIA’S CEO', 0, 121, 115, 1610, GOLD, F_TITLE, 'center')
    kit.line(c, -265, 186, 265, 186, 6, GOLD)
    c.restore()


def build(tl):
    """Use the house cut markers and quantize each boundary once, at the approved FPS."""
    ordered = [(tl.at(line_id), line_id, tl.by_id[line_id]['visual']) for line_id in SHOT_BREAKS]
    for event in tl.events:
        kind = event['kind']
        name = f"chapter{event['n']}" if kind == 'chapter' else kind
        ordered.append((event['t0'], name, event))
    ordered.sort(key=lambda row: row[0])
    total = round(tl.total * FPS)
    cuts = [round(row[0] * FPS) for row in ordered] + [total]
    picture = []
    for i, (_, name, content) in enumerate(ordered):
        t0 = cuts[i] / FPS
        duration = (cuts[i + 1] - cuts[i]) / FPS
        if isinstance(content, str):
            shot = named_body(content, t0, duration, tl.start(name) - t0)
        else:
            kind = content['kind']
            if kind == 'chapter':
                draw = shots.card('chapter', duration, n=content['n'], title=content['title'])
            elif kind == 'title':
                draw = lambda c, t, d=duration: title(c, t, d)
            else:
                draw = anim.outro if kind == 'outro' else anim.end_screen
            shot = dict(draw=draw, zoom=(1.0, 1.0))
        picture.append(dict(shot, name=name, dur=duration, t0=t0,
                            setting=content if isinstance(content, str) else content['kind']))
    return picture
