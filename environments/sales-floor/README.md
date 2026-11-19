# Night sales floor

An after-hours call-center set with a deep central aisle, rows of workstations, city windows, and a lit supervisor’s office. The approved look uses the Dirty Dollar night-print pass, paper grain on the background, and the standard shot vignette. Characters are drawn over the background after the print pass.

[Approved Ponzi staging still](ponzi-preview.jpg) · [Workstation prop sheet](workstation-props.jpg)

Use `night/sales_floor` for a wide story shot. Place standing actors in the aisle using the supplied `front_aisle` spot.

```python
from engine import sets, shots
from engine.actor import Actor

floor = sets.get_set('night/sales_floor')
x, y, scale = floor.spots['front_aisle']
character = Actor('ponzi', x, y, scale, hat=True, light=floor.light, rim=floor.rim)
shot = shots.wide('night/sales_floor', front_actors=[character])
```

The desk with drawers, cubicle divider, monitor, chair, desk phone, and complete workstation are reusable drawing functions in [`sets_src/sales_floor.py`](../../.claude/skills/documentary-animator/engine/sets_src/sales_floor.py). They share a perspective camera, so you can lay out new rows or build a closer workstation shot.
