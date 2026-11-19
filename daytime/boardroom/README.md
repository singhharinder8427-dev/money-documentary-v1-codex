# Daytime boardroom

The approved boardroom uses cream interior surfaces, cool blue-grey glass, navy window frames, and layered navy buildings. Daylight from the windows crosses the conference table and floor. The wide shot applies the approved soft vignette.

[Approved preview](boardroom-preview.jpg)

Use `day/boardroom` in a wide shot. Stage the actor at the head of the table behind the furniture layer. Use `window_aisle` and `near_table` for standing actors in front of the table.

```python
from engine import sets, shots
from engine.actor import Actor

room = sets.get_set('day/boardroom')
x, y, scale = room.spots['head_of_table']
chair = Actor('ceo', x, y, scale, light=room.light, rim=room.rim)
shot = shots.wide('day/boardroom', back_actors=[chair])
```

The [drawing code](../../.claude/skills/documentary-animator/engine/sets_src/boardroom.py) draws the window wall, chairs, board packets, and carafe. The [Gensler boardroom photo](https://www.gensler.com/projects/baring-private-equity-asia) was a reference for the long table and the skyline glazing.
