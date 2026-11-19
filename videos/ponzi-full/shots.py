"""Shot list - 50% in 45 Days (full, ~4.5-5 min). One picture per sentence.
Night print for the story, day print for the lesson (Ch5). Applies FIXES.md: start close, vary angles, framed stage,
documents fill the frame, story animations every 20-30 s, red-flags board, big phones at the end, outro + end screen."""
import math, skia
from engine import shots, widgets as Wd, anim as A, kit
from engine.actor import Actor
from engine.cast import person
from engine.core import W, H, GOLD, ORANGE, WHITE, NAVY, NAVY3, PAPER, F_LABEL, F_TYPE, F_TITLE
from engine.sets import get_set

SHOT_BREAKS = tuple(f'n{i:03d}' for i in range(1, 48)) + ('n029b',)
NR, DR = '#9FB8F0', '#FFE3A6'                                   # night rim, day rim
MCMASTERS = person('analyst', suit='#2E2E38', suit_d='#1E1E26', tie='#14213D', hair='slick', hair_col='#3A2A20', glasses=False, skin='#F0CDA4', skin_d='#D2AC80')
EDITOR = person('banker', bowtie=False, tie='#14213D', suit='#3A3F4A', suit_d='#2A2E36', hanky=None, glasses=True)
GUARD = person('agent', suit='#2B3A55', suit_d='#1E2A40', hat_col='#1E2A40', hat_band='#0E1424')

queue, held, stamp_shake = A.queue, A.held, A.stamp_shake        # now in the shared library (engine/anim.py)

def build(tl):
    S = []; at = tl.at; mouths = tl.mouths()
    order = [l['id'] for l in tl.lines]
    def mk(ev): return f"chapter:{ev['n']}" if ev['kind'] == 'chapter' else ev['kind']
    def nxt(lid):
        """Next shot boundary after a line: next line, or an inserted card / outro."""
        i = order.index(lid); cands = [e for e in tl.events if e['t0'] > tl.start(lid) + .01]
        nl = order[i + 1] if i + 1 < len(order) else None
        ev = min(cands, key=lambda e: e['t0']) if cands else None
        if ev and (nl is None or ev['t0'] < at(nl)): return mk(ev)
        return nl
    def add(lid, draw, **kw): S.append(dict(name=lid, dur=tl.dur(lid, nxt(lid)), draw=draw, **kw))
    def card_shot(marker, draw, **kw): S.append(dict(name=marker.replace(':', ''), dur=tl.dur(marker, nxt_ev(marker)), draw=draw, zoom=kw.pop('zoom', (1, 1.02)), **kw))
    def nxt_ev(marker):
        t0 = at(marker); later = [l for l in order if at(l) > t0 + .01]; ev = [e for e in tl.events if e['t0'] > t0 + .01]
        c1 = at(later[0]) if later else 1e9; c2 = min((e['t0'] for e in ev), default=1e9)
        if c2 < c1: return mk(min(ev, key=lambda e: e['t0']))
        return later[0] if later else 'end'
    def say(a, lid): return a.say(tl, lid, mouths)
    T = lambda lid: tl.cues[lid][1]

    # ================= HOOK =================
    q = queue()
    add('n001', shots.wide('night/street1920', q, t0=at('n001')), hud=lambda c, t: Wd.place_tag(c, 'Boston', t / .4, 'July 1920'),
        zoom=(1.7, 1.55), focus=((380, 700), (930, 640)), sfx=[(.1, 'whoosh')])                     # start close, travel to his door
    q2 = queue()
    add('n002', shots.wide('night/street1920', q2, overlay=lambda c, t: held(c, q2, 'cash', t), t0=at('n002')), zoom=(2.3, 2.4), focus=((560, 720), (720, 720)))
    add('n003', shots.card('text', T('n003'), text=tl.by_id['n003']['text'], gold_words=['fifty', 'percent']), zoom=(1, 1.02))
    p4 = Actor('ponzi', 930, 950, 1.08, face=-.2, rim=NR, hat=True).pose(.2, ('pocket', 'hip')).expression(0, mouth='smirk', eyes='half')
    add('n004', shots.wide('night/office', [p4], t0=at('n004')), hud=lambda c, t: Wd.lower_third(c, 'Charles Ponzi', 'Boston, 1920', (t - .3) / .5),
        zoom=(1.15, 1.3), focus=(930, 600))
    p5 = Actor('ponzi', 960, 1390, 2.15, face=-.3, rim=NR, hat=True).expression(0, mouth='smile', eyes='dot').expression(1.2, mouth='smirk', eyes='half')
    add('n005', shots.closeup('night/office', p5, focus=(930, 520), overlay=lambda c, t: Wd.pop_label(c, 'the Ponzi scheme', 960, 190, (t - 1.4) / .4, GOLD, 96, rot=-3), t0=at('n005')),
        zoom=(1.0, 1.05), sfx=[(1.4, 'pop')])
    p6 = Actor('ponzi', 960, 1390, 2.15, face=.2, rim=NR, hat=True).pose(.3, ('down', 'hat')).expression(.3, mouth='smirk', eyes='closed', sparkle=1.0)
    add('n006', shots.closeup('night/office', p6, focus=(1100, 520), t0=at('n006')), zoom=(1.0, 1.06))
    card_shot('title', shots.card('title', 2.5, title='50% in 45 Days', gold_word='50%'))
    card_shot('chapter:1', shots.card('chapter', 2.2, n=1, title='Two Dollars and Fifty Cents'))

    # ================= CH1 =================
    p7 = Actor('ponzi', 300, 905, .6, face=.6, rim=NR, hat=True).pose(0, ('down', 'hold')).walk_to(0, T('n007') + .3, 760)
    def suitcase(c, t):
        x = 300 + (760 - 300) * min(t / (T('n007') + .3), 1); kit.rect(c, x + 34, 770, x + 92, 812, '#6B4A33', 4, r=6)
    add('n007', shots.wide('night/street1920', [p7], overlay=suitcase, t0=at('n007')), hud=lambda c, t: Wd.place_tag(c, 'Boston', t / .4, '1903'), zoom=(1.3, 1.4), focus=((520, 640), (760, 640)), sfx=[(.2, 'whoosh')])
    add('n008', shots.plain(lambda c, t: (Wd.counter(c, 960, 470, 0, 2.5, (t - .2) / 1.0, label='by his own account', decimals=2, size=150),)), zoom=(1, 1.05), sfx=[(1.2, 'coin')])
    hit9 = 1.4
    def ch1_crime(c, t):
        A.hand_slam(c, 960, 520, t, 'paper', 'Court record', ['Canada', 'Charge: forgery'], hit=.3)
        Wd.stamp(c, 'Forgery', 1250, 380, t - hit9, ORANGE, rot=-10, size=110)
        if t > T('n009') - .9: A.prison_bars(c, t - (T('n009') - .9))
    add('n009', shots.plain(ch1_crime), zoom=(1, 1.04), shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t, hit=.3) if t < 1 else stamp_shake(hit9)(t),
        sfx=[(.3, 'stamp'), (hit9, 'stamp')])
    gd = say(Actor('agent', 960, 1390, 2.15, face=.5, rim=NR, spec=GUARD).expression(0, mouth='flat', eyes='half', brow=-.3), 'n010')
    add('n010', shots.closeup('night/office', gd, focus=(500, 500), overlay=lambda c, t: A.prison_bars(c, 9), t0=at('n010')), zoom=(1.0, 1.03))
    p11 = say(Actor('ponzi', 960, 1390, 2.15, face=-.4, rim=NR, hat=False).expression(0, mouth='smirk', eyes='half', sparkle=1.0).pose(.2, ('down', 'count')), 'n011')
    add('n011', shots.closeup('night/office', p11, focus=(1300, 500), overlay=lambda c, t: A.prison_bars(c, 9), t0=at('n011')), zoom=(1.0, 1.05))
    add('n012', shots.plain(lambda c, t: (Wd.paper_card(c, 960, 520, 'Prison record', ['Canada, 1908', 'Remember this.'], t, w=900, h=520, rot=-2), Wd.stamp(c, 'Filed', 1240, 380, t - 1.0, GOLD, rot=-10, size=100))),
        zoom=(1, 1.08), shake=stamp_shake(1.0), sfx=[(.1, 'paper'), (1.0, 'stamp')])
    p13 = Actor('ponzi', 930, 950, 1.08, face=0, rim=NR, hat=False).pose(.2, ('chin', 'down')).expression(0, eyes='half', mouth='flat', brow=.3).expression(T('n013') - 1, eyes='wide', mouth='o')
    add('n013', shots.wide('night/office', [p13], overlay=lambda c, t: A.envelope(c, 1230, 610, -1 if t < T('n013') - .6 else 0) if False else Wd.paper_card(c, 1240, 640, 'Letter', ['Air mail'], (t - .8), w=300, h=200, rot=8), t0=at('n013')),
        zoom=(1.1, 1.25), focus=(1000, 620))
    card_shot('chapter:2', shots.card('chapter', 2.2, n=2, title='The Loophole'))

    # ================= CH2 =================
    add('n014', shots.plain(lambda c, t: A.envelope(c, 960, 640, t, 'Reply coupon', ['International', 'postage coupon'])), zoom=(1, 1.06), sfx=[(.1, 'paper'), (.5, 'paper')])
    add('n015', lambda c, t: A.map_route(c, t, dur=T('n015') * .8, label_a='Italy', flag_a='italy', flag_b='usa'), zoom=(1, 1.04))
    add('n016', shots.plain(lambda c, t: (Wd.big_label(c, 'Money in Europe', 960, 210, 1, WHITE, 90),
                                          Wd.line_chart(c, 300, 300, 1620, 880, [100, 96, 88, 70, 55, 40, 30, 24], t / (T('n016') * .8), ORANGE, labels=['1914', '', '1916', '', '1918', '', '1920', '']),
                                          Wd.pop_label(c, 'coupon price: same', 1350, 330, (t - T('n016') * .6) / .4, GOLD, 70))), zoom=(1, 1.04), sfx=[(T('n016') * .8, 'falling')])
    def coupon_scene(c, t):
        Wd.big_label(c, 'Europe', 480, 230, t / .4); Wd.big_label(c, 'United States', 1440, 230, (t - .3) / .4)
        Wd.arrow(c, 680, 400, 1220, 400, (t - .5) / .8); Wd.paper_card(c, 1340, 720, 'Postal reply', ['INTERNATIONAL', 'POSTAGE COUPON'], t - 1.3, w=640, h=440, rot=4, slam=True)
        Wd.pop_label(c, 'cheap', 480, 640, (t - .9) / .4, WHITE, 80); Wd.pop_label(c, 'more stamps', 1340, 1010, (t - 2.2) / .4, GOLD, 64, rot=0)
    add('n017', shots.plain(coupon_scene), zoom=(1, 1.04), sfx=[(1.3, 'stamp')])
    def rent(c, t):
        Wd.paper_card(c, 560, 560, 'Stamps', ['x 1,000'], 1, w=640, h=480, rot=-4)
        for i in range(12): kit.rect(c, 330 + (i % 6) * 78, 650 + (i // 6) * 80, 392 + (i % 6) * 78, 712 + (i // 6) * 80, '#E9C09A' if i % 2 else '#AEB4C4', 3)
        A.hand_slam(c, 1350, 560, t - .6, 'paper', 'Rent due', ['$40.00', 'Cash only'], hit=.25, side='right')
        if t > 2.0: Wd.stamp(c, 'No', 560, 560, t - 2.0, ORANGE, rot=-12, size=140)
    add('n018', shots.plain(rent), zoom=(1, 1.04), shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t - .6, hit=.25), sfx=[(.85, 'stamp'), (2.0, 'stamp')])
    inv = say(Actor('worker', 960, 1390, 2.15, face=.6, rim=NR, hat=True).expression(0, eyes='wide', mouth='flat', brow=.6, brow_tilt=-.4), 'n019')
    add('n019', shots.closeup('night/office', inv, focus=(1350, 600), t0=at('n019')), zoom=(1.0, 1.04))
    p20 = say(Actor('ponzi', 960, 1390, 2.15, face=-.6, rim=NR, hat=True).pose(.1, ('down', 'chin')).expression(0, eyes='half', mouth='smirk', sparkle=1.0), 'n020')
    add('n020', shots.closeup('night/office', p20, focus=(700, 520), t0=at('n020')), zoom=(1.0, 1.05))
    add('n021', shots.plain(lambda c, t: (A.hand_slam(c, 960, 560, t, 'cash', hit=.3), A.hand_slam(c, 760, 640, t - .9, 'cash', hit=.3, rot=8) if t > .9 else None,
                                          A.hand_slam(c, 1180, 470, t - 1.6, 'cash', hit=.3, rot=-14) if t > 1.6 else None)),
        zoom=(1, 1.05), shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t, hit=.3), sfx=[(.3, 'cash'), (1.2, 'stamp'), (1.9, 'stamp')])
    card_shot('chapter:3', shots.card('chapter', 2.2, n=3, title='Forty-Five Days'))

    # ================= CH3 =================
    q22 = queue(n=6, x0=930)
    add('n022', shots.wide('night/street1920', q22, t0=at('n022')), hud=lambda c, t: Wd.place_tag(c, 'Boston', t / .4, 'January 1920'), zoom=(2.0, 2.2), focus=(930, 520))
    add('n023', shots.plain(lambda c, t: A.pyramid(c, 960, 930, t + .35, 3, step=T('n023') / 4)), zoom=(1, 1.04), sfx=[(.4, 'pop'), (1.0, 'pop'), (1.6, 'pop')])
    add('n024', shots.plain(lambda c, t: A.pyramid(c, 960, 930, 9 + t, 5, wobble=min(t / T('n024'), 1) * .8)), zoom=(1.04, 1.1), rot=(0, 1.5))
    p25 = Actor('ponzi', 930, 950, 1.08, face=-.1, rim=NR, hat=True).pose(.1, ('cheer', 'hip')).expression(0, mouth='open', eyes='closed')
    add('n025', shots.wide('night/office', [p25], overlay=lambda c, t: (Wd.falling_money(c, t, n=16, area=(250, 0, 1650, 950)), Wd.counter(c, 960, 180, 0, 10000000, (t - .2) / 1.6, label='poured in')), t0=at('n025')),
        zoom=(1.0, 1.07), focus=(930, 540), sfx=[(.1, 'cash')])
    def bought(c, t):
        A.hand_slam(c, 600, 560, t, 'paper', 'Deed', ['A mansion', 'Lexington, Mass.'], hit=.3, rot=-5)
        A.hand_slam(c, 1330, 560, t - 1.4, 'paper', 'Bank shares', ['Hanover Trust Co.', 'Controlling stake'], hit=.3, rot=5) if t > 1.4 else None
        Wd.stamp(c, 'Sold', 650, 380, t - .8, GOLD, rot=-10, size=90); Wd.stamp(c, 'Owner', 1380, 380, t - 2.2, GOLD, rot=8, size=90)
    add('n026', shots.plain(bought), zoom=(1, 1.04), sfx=[(.3, 'stamp'), (.8, 'stamp'), (1.7, 'stamp'), (2.2, 'stamp')])
    q27 = queue(worried=True, n=14, x0=930)
    add('n027', shots.wide('night/street1920', q27, t0=at('n027')), zoom=(1.6, 1.8), focus=(760, 680))

    # ================= TWIST =================
    p28 = Actor('ponzi', 1060, 868, .38, face=-.6, rim=NR, hat=True).pose(.2, ('present', 'down')).expression(0, mouth='smile', eyes='closed')
    q28 = queue(worried=True, n=12, x0=950)
    add('n028', shots.wide('night/street1920', q28 + [p28], overlay=lambda c, t: held(c, q28[:3], 'cash', t), t0=at('n028')), zoom=(2.1, 2.3), focus=(930, 690))
    add('n029', shots.card('text', T('n029'), text=tl.by_id['n029']['text'], gold_words=['publicist.']), zoom=(1, 1.03))
    p29 = Actor('ponzi', 930, 950, 1.08, face=.3, rim=NR, hat=True).pose(T('n029b') * .6, ('present', 'hip')).expression(0, mouth='smile')
    mc = Actor('analyst', 1700, 1070, 1.05, face=-.5, rim=NR, spec=MCMASTERS).walk_to(0, T('n029b') * .6, 1380).pose(T('n029b') * .6, ('present', 'down'))
    add('n029b', shots.wide('night/office', [p29], [mc], t0=at('n029b')), hud=lambda c, t: Wd.lower_third(c, 'William McMasters', 'Ponzi\'s publicist', (t - .4) / .5, x=1100),
        zoom=(1.05, 1.12), focus=(1100, 600))
    card_shot('chapter:4', shots.card('chapter', 2.2, n=4, title='The Insider'))

    # ================= CH4 =================
    add('n030', shots.plain(lambda c, t: A.ledger(c, 960, 560, t, [('Money in', '$10,000,000'), ('Coupons', 'almost none'), ('Owed', '-$2,000,000')], title="Ponzi's books")),
        zoom=(1, 1.05), sfx=[(.1, 'paper'), (.35, 'paper'), (.6, 'paper')])
    mcc = say(Actor('analyst', 960, 1390, 2.15, face=.5, rim=NR, spec=MCMASTERS).expression(0, eyes='wide', brow=.5), 'n031')
    add('n031', shots.closeup('night/desk', mcc, focus=(700, 500), t0=at('n031')), zoom=(1.0, 1.04))
    ed = say(Actor('banker', 960, 1390, 2.15, face=-.5, rim=NR, spec=EDITOR).pose(.15, ('down', 'push')).expression(0, eyes='half', brow=-.4), 'n032')
    add('n032', shots.closeup('night/desk', ed, focus=(1300, 500), t0=at('n032')), zoom=(1.0, 1.04), shake=stamp_shake(.35), sfx=[(.35, 'stamp')])
    add('n033', shots.plain(lambda c, t: A.newspaper(c, 960, 560, t, 'The Boston Post', 'Declares Ponzi is now hopelessly insolvent', 'August 2, 1920')),
        zoom=(1, 1.06), sfx=[(.05, 'whoosh'), (.7, 'stamp')])
    add('n034', shots.card('text', T('n034'), text=tl.by_id['n034']['text'], gold_words=['27,000']), zoom=(1, 1.03))
    def exposed(c, t):
        A.newspaper(c, 960, 560, 9, 'The Boston Post', 'Ponzi served time in Canadian prison', 'Investigation continues')
        Wd.stamp(c, 'Exposed', 1300, 380, t - .9, ORANGE, rot=-10, size=110)
    add('n035', shots.plain(exposed), zoom=(1.0, 1.08), shake=stamp_shake(.9), sfx=[(.9, 'stamp')])
    def arrest(c, t):
        A.handcuffs(c, 700, 540, t, .5)
        Wd.paper_card(c, 1350, 560, 'Hanover Trust', ['Bank closed', 'by the state'], (t - 1.4), w=620, h=440, rot=4, slam=True)
        Wd.stamp(c, 'Closed', 1380, 560, t - 2.0, ORANGE, rot=-12, size=120)
    add('n036', shots.plain(arrest), zoom=(1, 1.04), shake=lambda t: A.handcuffs(skia.Surface(4, 4).getCanvas(), 0, 0, t, .5) if t < 1.5 else stamp_shake(2.0)(t),
        sfx=[(.5, 'stamp'), (1.4, 'stamp'), (2.0, 'stamp')])
    add('n037', shots.plain(lambda c, t: (Wd.counter(c, 960, 430, 0, 20000000, (t - .2) / 1.6, loss=True, label='lost by investors (est.)', size=120),
                                          Wd.pop_label(c, 'back: under 30¢ per $1', 960, 820, (t - T('n037') * .55) / .4, WHITE, 70, rot=0))), zoom=(1, 1.04))
    def guilty(c, t):
        Wd.paper_card(c, 960, 560, 'United States v. Ponzi', ['Mail fraud', 'Plea: guilty', 'Five years'], 1, w=1000, h=640, rot=-2)
        Wd.stamp(c, 'Guilty', 1200, 420, t - .6, ORANGE, rot=-10, size=110); Wd.stamp(c, 'Pulitzer prize', 760, 820, t - 1.8, GOLD, rot=6, size=70)
    add('n038', shots.plain(guilty), zoom=(1, 1.05), shake=stamp_shake(.6), sfx=[(.6, 'stamp'), (1.8, 'stamp')])
    add('n039', shots.plain(lambda c, t: (Wd.paper_card(c, 760, 560, 'Rio de Janeiro', ['1949', 'Charity ward'], 1, w=760, h=520, rot=-3),
                                          Wd.counter(c, 1460, 560, 0, 75, (t - T('n039') * .6) / .8, label='left behind', size=110))), zoom=(1.0, 1.06))
    card_shot('chapter:5', shots.card('chapter', 2.2, n=5, title='Your Wallet'))

    # ================= CH5 (day) =================
    sv = Actor('saver', 760, 985, .98, face=.3, light=1, rim=DR).pose(.3, ('phone', 'down')).expression(0, eyes='wide', mouth='o', brow=.5)
    add('n040', shots.wide('day/living', [], [sv], t0=at('n040')), zoom=(1.15, 1.3), focus=(800, 600), whip_in=True, sfx=[(0, 'whoosh')])
    an = Actor('analyst', 470, 1000, 1.1, face=.35, light=1, rim=DR).pose(.2, ('down', 'point'))
    def board_bg(c): kit.rect(c, 600, 110, 1500, 640, '#F8FAFD', 8, r=10)
    def madoff(c, t):
        board_bg(c); Wd.text(c, 'BERNIE MADOFF, 2009', 1050, 200, 60, NAVY, F_TITLE, 'center')
        Wd.counter(c, 1050, 350, 0, 65, (t - .5) / 1.4, unit='$', suffix='B', label='', size=100)
        Wd.text(c, 'ON STATEMENTS', 1050, 500, 44, NAVY, F_LABEL, 'center'); Wd.stamp(c, 'Fake', 1300, 520, t - T('n041') * .75, ORANGE, rot=-10, size=100)
    add('n041', shots.wide('day/lesson', [], [an], overlay=madoff, t0=at('n041')), zoom=(1.0, 1.05), focus=(1000, 520), shake=stamp_shake(T('n041') * .75), sfx=[(T('n041') * .75, 'stamp')])
    an2 = Actor('analyst', 470, 1000, 1.1, face=.35, light=1, rim=DR).pose(.2, ('down', 'present')).expression(0, mouth='flat', brow=.5)
    def fbi(c, t):
        board_bg(c); Wd.text(c, 'INVESTMENT FRAUD, 2024', 1050, 200, 56, NAVY, F_TITLE, 'center')
        Wd.counter(c, 1050, 380, 0, 6570000000, (t - .4) / 1.8, loss=True, size=84); Wd.text(c, 'REPORTED TO THE FBI', 1050, 520, 44, NAVY, F_LABEL, 'center')
    add('n042', shots.wide('day/lesson', [], [an2], overlay=fbi, t0=at('n042')), zoom=(1.0, 1.05), focus=(1000, 520))
    sv2 = Actor('saver', 760, 985, .98, face=.3, light=1, rim=DR).pose(0, ('phone', 'down')).expression(0, eyes='half', mouth='flat')
    def costume(c, t):
        for i, (lbl, x, y, r) in enumerate((('Crypto apps', 1250, 260, -5), ('Trading groups', 1400, 430, 4), ("Can't-lose funds", 1240, 600, -3))):
            Wd.pop_label(c, lbl, x, y, (t - .4 - i * .7) / .35, GOLD if i != 2 else WHITE, 72, rot=r)
    add('n043', shots.wide('day/living', [], [sv2], t0=at('n043')), hud=costume, zoom=(1.15, 1.22), focus=(960, 560), sfx=[(.4, 'pop'), (1.1, 'pop'), (1.8, 'pop')])
    an3 = Actor('analyst', 470, 1000, 1.1, face=.35, light=1, rim=DR).pose(.2, ('down', 'point'))
    flags = ['Guaranteed high returns', 'Returns never go down', 'A secret strategy', 'Seller not registered', "Can't get money out"]
    fl_t = [1.0 + i * (T('n044') - 1.5) / 5 for i in range(5)]
    def flags_board(c, t):
        board_bg(c); Wd.text(c, 'RED FLAGS', 1050, 190, 72, NAVY, F_TITLE, 'center')
        for i, (f, s0) in enumerate(zip(flags, fl_t)):
            u = kit.K(t, s0, .35)
            if u > 0:
                y = 270 + i * 76; kit.poly(c, [(660, y - 30), (660, y + 6), (694, y - 12)], ORANGE, 4); c.drawLine(660, y - 30, 660, y + 24, kit.ink(6))
                Wd.pop_label(c, f, 1070, y, u, NAVY, 54, rot=0, stroke=0)
    add('n044', shots.wide('day/lesson', [], [an3], overlay=flags_board, t0=at('n044')), zoom=(1.0, 1.05), focus=(1000, 500), sfx=[(x, 'pop') for x in fl_t])
    an4 = Actor('analyst', 470, 1000, 1.1, face=.35, light=1, rim=DR).pose(.1, ('down', 'present')).expression(0, mouth='smile')
    def check(c, t):
        board_bg(c); Wd.text(c, 'BEFORE YOU INVEST', 1050, 210, 64, NAVY, F_TITLE, 'center')
        A.hand_slam(c, 1050, 430, t - .3, 'sticky', 'Check them at investor.gov', hit=.25, rot=-4, sleeve_col='#E5E5E5')
    add('n045', shots.wide('day/lesson', [], [an4], overlay=check, t0=at('n045')), zoom=(1.0, 1.06), focus=(1000, 480),
        shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t - .3, hit=.25), sfx=[(.55, 'stamp')])

    # ================= ENDING =================
    q46 = queue(phones=True, n=14, x0=1180, s=.42, y=880)
    add('n046', shots.wide('night/street', q46, overlay=lambda c, t: held(c, q46, 'phone', t), t0=at('n046')), zoom=(1.9, 2.05), focus=((560, 720), (800, 720)), whip_in=True, sfx=[(0, 'whoosh')])
    # ================= ROUND 2: a NEW picture every 2-3 s (owner) - split static shots, add story details =================
    def slot(lid): return tl.dur(lid, nxt(lid))
    def part(base, d, name, **over):
        x = dict(base); x.update(over); x['name'] = name; x['dur'] = d; x['sfx'] = [e for e in x.get('sfx', ()) if e[0] < d]; return x
    def two(lid, d1, a, b):
        tot = slot(lid); d1 = min(d1, tot - 1.0); return [part(a, d1, lid + 'a'), part(b, tot - d1, lid + 'b')]
    def bshot(draw, **kw): return dict(draw=draw, **kw)
    by = {x['name']: x for x in S}; R = {}
    sign = shots.wide('night/street1920', queue(n=4), t0=at('n001'))
    R['n001'] = two('n001', 2.0, bshot(sign, zoom=(2.7, 2.9), focus=(930, 360), sfx=[(.1, 'whoosh')]), by['n001'])
    sv2c = Actor('saver', 960, 1390, 2.15, face=.5, rim=NR).pose(0, ('down', 'hold')).expression(0, eyes='wide', mouth='flat', brow=.6, brow_tilt=-.4)
    def saver_cash(c, t): hx, hy = kit.hand_pos(960, 1390, 2.15, ('down', 'hold'), 1); Wd.bill(c, hx + 10, hy - 10, -12, 1.4)
    R['n002'] = two('n002', 2.1, by['n002'], bshot(shots.closeup('night/street1920', sv2c, focus=(500, 640), overlay=saver_cash, t0=at('n002') + 2.1), zoom=(1.0, 1.05)))
    def secret(c, t): Wd.paper_card(c, 960, 540, 'Prison record', ['Canada, 1908', 'Charge: forgery'], t, w=880, h=560, rot=-3); Wd.stamp(c, 'Secret', 1250, 420, t - .9, ORANGE, rot=-10, size=110)
    R['n004'] = two('n004', 2.8, by['n004'], bshot(shots.plain(secret), zoom=(1, 1.05), shake=stamp_shake(.9), sfx=[(.1, 'paper'), (.9, 'stamp')]))
    chat = [('Guaranteed 50% in 45 days!', 'in'), ('Is it safe?', 'out'), ('Zero risk. Act fast.', 'in')]
    R['n005'] = two('n005', 3.0, by['n005'], bshot(shots.plain(lambda c, t: A.phone_screen(c, 960, 560, t, chat, s=1.0, every=.9)), zoom=(1.0, 1.06), sfx=[(.2, 'pop'), (1.1, 'pop'), (2.0, 'pop')]))
    p9 = Actor('ponzi', 960, 1390, 2.15, face=-.3, rim=NR, hat=False).expression(0, eyes='half', mouth='smirk')
    R['n009'] = two('n009', 3.6, by['n009'], bshot(shots.closeup('night/office', p9, focus=(600, 500), overlay=lambda c, t: A.prison_bars(c, t - .3), t0=at('n009') + 3.6),
                                                   zoom=(1.0, 1.04), shake=lambda t: A.prison_bars(skia.Surface(4, 4).getCanvas(), t - .3), sfx=[(.65, 'stamp')]))
    R['n013'] = two('n013', 3.2, by['n013'], bshot(shots.plain(lambda c, t: (A.envelope(c, 960, 620, -1), Wd.stamp(c, 'Air mail', 1150, 520, t - .5, GOLD, rot=-12, size=80),
                                                                            Wd.pop_label(c, 'from abroad', 960, 960, (t - 1.2) / .4, WHITE, 70, rot=0))), zoom=(1.0, 1.08), sfx=[(.5, 'stamp')]))
    p22 = Actor('ponzi', 930, 950, 1.08, face=0, rim=NR, hat=True).pose(.2, ('cheer', 'present')).expression(0, mouth='open', eyes='closed')
    R['n022'] = two('n022', 2.6, by['n022'], bshot(shots.wide('night/office', [p22], t0=at('n022') + 2.6), zoom=(1.1, 1.2), focus=(930, 560)))
    p28c = Actor('ponzi', 960, 1390, 2.15, face=-.5, rim=NR, hat=True).pose(.1, ('present', 'down')).expression(0, mouth='smile', eyes='closed', sparkle=1.0)
    def pay(c, t): hx, hy = kit.hand_pos(960, 1390, 2.15, ('present', 'down'), -1); Wd.bill(c, hx - 30, hy - 20, 15, 1.5)
    R['n028'] = two('n028', 2.6, by['n028'], bshot(shots.closeup('night/street1920', p28c, focus=(1000, 640), overlay=pay, t0=at('n028') + 2.6), zoom=(1.0, 1.05)))
    cuffed = Actor('ponzi', 1150, 868, .38, face=-.5, rim=NR, hat=True).pose(0, ('cross', 'cross')).expression(0, eyes='wide', mouth='o', brow=.8, sweat=0)
    cop = Actor('agent', 1235, 870, .38, face=-.4, rim=NR, spec=GUARD).pose(0, ('down', 'push'))
    arrest = shots.wide('night/street1920', [cuffed, cop], overlay=lambda c, t: A.police_car(c, 560, 930, t, .55, spot_target=(1160, 800)), t0=at('n036'))
    R['n036'] = two('n036', 3.0, bshot(arrest, zoom=(1.45, 1.6), focus=(900, 660), sfx=[(.2, 'whoosh')]), by['n036'])
    R['n037'] = two('n037', 3.6, by['n037'], bshot(shots.plain(lambda c, t: (A.coin_rain(c, t), Wd.pop_label(c, 'back: under 30¢ per $1', 960, 540, (t - .3) / .4, WHITE, 90, rot=0))), zoom=(1, 1.04), sfx=[(.2, 'falling')]))
    R['n038'] = two('n038', 3.3, by['n038'], bshot(shots.plain(lambda c, t: (A.newspaper(c, 960, 560, t, 'The Boston Post', 'Wins the Pulitzer Prize', 'Public Service, 1921'),
                                                                            Wd.stamp(c, 'Pulitzer', 1300, 330, t - .9, GOLD, rot=8, size=90))), zoom=(1, 1.05), sfx=[(.05, 'whoosh'), (.9, 'stamp')]))
    R['n039'] = two('n039', 3.6, bshot(lambda c, t: A.map_route(c, t, dur=2.6, a=(1450, 520), b=(470, 470), label_a='United States', label_b='Italy, 1934', icon='PONZI', flag_a='usa', flag_b='italy'), zoom=(1, 1.04)), by['n039'])
    def statement(c, t):
        A.hand_slam(c, 960, 540, t, 'paper', 'Account statement', ['Balance: $65,000,000,000', 'Real money: most never existed'], hit=.3)
        Wd.stamp(c, 'Fake', 1250, 400, t - 1.4, ORANGE, rot=-10, size=120)
    R['n041'] = two('n041', 5.5, by['n041'], bshot(shots.plain(statement), zoom=(1, 1.05), shake=lambda t: A.hand_slam(skia.Surface(4, 4).getCanvas(), 0, 0, t, hit=.3) if t < 1 else stamp_shake(1.4)(t),
                                                   sfx=[(.3, 'stamp'), (1.4, 'stamp')]))
    svc = Actor('saver', 960, 1390, 2.15, face=.4, light=1, rim=DR).pose(0, ('phone', 'down')).expression(0, eyes='wide', mouth='o', brow=.7, sweat=0)
    R['n042'] = two('n042', 4.5, by['n042'], bshot(shots.closeup('day/living', svc, focus=(700, 560), t0=at('n042') + 4.5), zoom=(1.0, 1.05)))
    chat2 = [('Guaranteed 50% in 45 days!', 'in'), ('Sounds familiar...', 'out')]
    R['n046'] = two('n046', 2.6, by['n046'], bshot(shots.plain(lambda c, t: A.phone_screen(c, 960, 560, t, chat2, s=1.0, every=1.0)), zoom=(1.05, 1.12), sfx=[(.2, 'pop'), (1.2, 'pop')]))
    # --- quality-check fixes (Claude QC, round 2)
    R['n002'][0] = part(by['n002'], R['n002'][0]['dur'], 'n002a', zoom=(3.4, 3.6), focus=((560, 790), (700, 790)))            # tight on the cash in their hands
    g38 = lambda c, t: (Wd.paper_card(c, 960, 560, 'United States v. Ponzi', ['Mail fraud', 'Plea: guilty', 'Five years'], 1, w=1000, h=640, rot=-2), Wd.stamp(c, 'Guilty', 1200, 420, t - .6, ORANGE, rot=-10, size=110))
    R['n038'][0] = part(by['n038'], R['n038'][0]['dur'], 'n038a', draw=shots.plain(g38), sfx=[(.6, 'stamp')])                  # Pulitzer only once (next shot)
    R['n038'][1]['draw'] = shots.plain(lambda c, t: (A.newspaper(c, 960, 560, t, 'The Boston Post', 'Wins the Pulitzer Prize', 'Public Service, 1921'), Wd.stamp(c, 'Pulitzer', 1330, 760, t - .9, GOLD, rot=8, size=90)))
    rio = lambda c, t: (Wd.paper_card(c, 760, 560, 'Rio de Janeiro', ['1949', 'Charity ward'], t, w=760, h=520, rot=-3), Wd.counter(c, 1460, 560, 0, 75, (t - .9) / .9, label='left behind', size=110))
    R['n039'][1] = part(by['n039'], R['n039'][1]['dur'], 'n039b', draw=shots.plain(rio), sfx=[(.1, 'paper'), (1.8, 'coin')])
    def statement2(c, t):
        Wd.paper_card(c, 960, 540, 'Account statement', ['Balance: $65,000,000,000', 'Most of it never existed'], t, w=1180, h=600, rot=-2, slam=True)
        Wd.stamp(c, 'Fake', 1350, 380, t - 1.3, ORANGE, rot=-10, size=120)
    R['n041'][1]['draw'] = shots.plain(statement2); R['n041'][1]['shake'] = stamp_shake(1.3); R['n041'][1]['sfx'] = [(.45, 'stamp'), (1.3, 'stamp')]
    S[:] = [y for x in S for y in R.get(x['name'], [x])]

    S.append(dict(name='n047', dur=tl.dur('n047', 'outro'), draw=shots.card('text', T('n047'), text=tl.by_id['n047']['text'], gold_words=['line?']), zoom=(1, 1.02)))
    S.append(dict(name='outro', dur=tl.dur('outro', 'endscreen'), draw=lambda c, t: A.outro(c, t), zoom=(1, 1.02)))
    S.append(dict(name='endscreen', dur=tl.dur('endscreen', 'end'), draw=lambda c, t: A.end_screen(c, t), zoom=(1, 1)))
    return S
