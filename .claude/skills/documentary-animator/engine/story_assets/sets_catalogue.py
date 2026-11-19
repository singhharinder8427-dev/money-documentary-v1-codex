"""Stock scene names and their rendering settings."""
from functools import partial

from . import everyday, law, wealth
from .finance import ordinary_office, private_banker, startup, stock_exchange, vault, warehouse
from .lighting import office_light_map, projected_light_map


# Coordinates are frame pixels and follow the same feet/scale convention as the legacy sets.
FINANCE = {
    'night/private_banker': dict(draw=private_banker.office, light_map=office_light_map),
    'day/ordinary_office': dict(draw=ordinary_office.office, spots={'aisle': (960, 1010, .75)}),
    'day/startup_workspace': dict(draw=startup.scene, spots={'near_table': (910, 967, .65)}),
    'day/stock_exchange': dict(draw=stock_exchange.scene, spots={'steps': (955, 1000, .55)}),
    'night/bank_vault': dict(draw=vault.scene, light_map=office_light_map),
    'day/warehouse': dict(draw=warehouse.scene, spots={'aisle': (960, 994, .63)}),
}


def _story_sets():
    catalogue = {}
    for group in (law.SETS, everyday.SETS, wealth.SETS):
        for slug, _, draw, night in group:
            kind = 'night' if night else 'day'
            name = f"{kind}/{slug.replace('-', '_')}"
            settings = dict(draw=draw, scale=2)
            if night:
                settings.update(light_map=projected_light_map, vignette=(.76, .42))
            catalogue[name] = settings
    return catalogue


STORY_SETS = {**FINANCE, **_story_sets()}
STORY_SETS['day/visiting_room_call'] = dict(
    draw=partial(law.visiting_room, phones_on_hooks=False), scale=2,
)
STORY_SETS['day/visiting_room']['furniture'] = law.visiting_foreground


for name, settings in STORY_SETS.items():
    settings.setdefault('spots', {})
    settings.setdefault('vignette', (.78, .42) if name.startswith('night/') else (.28, .50))
