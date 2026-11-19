"""The channel's cast. The first five are LOCKED looks (BRAND.md). The rest are reusable archetypes in the same
style. Real people: copy an archetype and change only their signature traits (hair, colour, glasses, outfit),
and identify them with a name tag (lower third). Never a likeness of a photo."""
from engine.core import NAVY, GOLD, GREY, WHITE

LOCKED = {
 'ceo': dict(skin='#F8E2D2', skin_d='#E6C4AE', suit=NAVY, suit_d='#0C152B', shirt=WHITE, tie=GOLD, hair='silver', hair_col='#ECECF1',
             glasses=True, moustache=True, moustache_col='#FFFFFF', moustache_outline=True, moustache_dy=10),
 'analyst': dict(skin='#C8875A', skin_d='#A86C43', suit=GREY, suit_d='#BDBDBD', shirt=WHITE, tie=NAVY, hair='slick', hair_col='#1A1414', glasses=True),
 'worker': dict(skin='#F0CDA4', skin_d='#D2AC80', suit='#6B4A2E', suit_d='#4F3520', shirt='#F4EFE2', tie='#2B4A7A', hair='slick', hair_col='#7A4A26',
                hat_col='#3A3F4A', hat_band=GOLD),   # wears the hat with hat=True
 'banker': dict(skin='#E2B48C', skin_d='#C49468', suit='#2E2E38', suit_d='#1E1E26', shirt=WHITE, tie=GOLD, bowtie=True, hair='slick', hair_col='#3A2A20',
                moustache=True, hanky=GOLD),
 'investor': dict(skin='#8D5A3B', skin_d='#6F4429', suit=GOLD, suit_d='#D88A06', shirt=WHITE, tie=NAVY, hair='bob', hair_col='#15110F'),
}
ARCHETYPES = {
 'saver': dict(skin='#E9B98F', skin_d='#CC9A6E', suit='#2B4A7A', suit_d='#1F3860', shirt='#F4EFE2', outfit='sweater', hair='long', hair_col='#4A2E1C'),
 'grad': dict(skin='#B97A50', skin_d='#9A6038', suit='#3A3F4A', suit_d='#2A2E36', shirt='#F4EFE2', outfit='hoodie', hair='curly', hair_col='#1A1414'),
 'scammer': dict(skin='#F2D3B5', skin_d='#D9B593', suit='#1E1E26', suit_d='#121218', shirt='#2E2E38', outfit='open', hair='slick', hair_col='#0E0E12', glasses=True),
 'agent': dict(skin='#7E4E32', skin_d='#633A22', suit='#24304A', suit_d='#18203A', shirt=WHITE, tie='#0E1424', hair='buzz', hair_col='#121212'),
 'reporter': dict(skin='#F5D9C4', skin_d='#DDBBA3', suit=GREY, suit_d='#BDBDBD', shirt=NAVY, outfit='open', hair='bun', hair_col='#8A5A2E', glasses=True),
 'retiree': dict(skin='#EFCFB2', skin_d='#D4AF8F', suit='#6B5A46', suit_d='#52432F', shirt='#F4EFE2', outfit='sweater', hair='bald', hair_col='#D9D9DE', glasses=True),
}
CAST = {**LOCKED, **ARCHETYPES}
# Real people (our style, signature traits only - always shown with a name tag)
REAL = {
 # Charles Ponzi (1882-1949), from period photos: short + dapper, slicked-back side-parted dark hair, thin trimmed
 # moustache, straw boater, light suit, pocket square, high starched collar, gold-handled cane (kit.cane), easy smile.
 'ponzi': dict(skin='#E6BC93', skin_d='#C99E76', suit='#E3DAC6', suit_d='#C7BCA3', shirt='#FFFFFF', tie='#2B2B36', hair='slick', hair_col='#15110F',
               hair_part=True, moustache=True, moustache_style='pencil', moustache_col='#15110F', wing_collar=True,
               hat_style='boater', hat_col='#E8C77A', hat_band='#14213D', hanky='#FFFFFF'),   # wear with hat=True; he was short: use ~0.9x scale
}
CAST.update(REAL)
NAMES = {'ceo': 'THE CEO', 'analyst': 'THE ANALYST', 'worker': 'THE WORKER', 'banker': 'THE BANKER', 'investor': 'THE INVESTOR',
         'saver': 'THE SAVER', 'grad': 'THE GRAD', 'scammer': 'THE SCAMMER', 'agent': 'THE AGENT', 'reporter': 'THE REPORTER', 'retiree': 'THE RETIREE'}

def person(base, **changes):
    """New character from a cast entry: person('ceo', hair='slick', suit='#2E2E38', glasses=False)."""
    d = dict(CAST[base]); d.update(changes); return d
