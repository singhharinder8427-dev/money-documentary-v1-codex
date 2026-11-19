# Approved sets and paper-trail props

These full-resolution stills are the owner's visual references for future Dirty Dollar episodes. The backgrounds use the engine's day or night print pass, paper grain, and a scene-specific vignette. Use the set key in `shots.wide()` to render the approved framing.

| Set | Staging | Approved still |
|---|---|---|
| `day/suburban_home` | Use the front walkway for arrivals. The porch swing, mailbox, and neighboring roofs establish the residential street. | [Suburban exterior](suburban-home-day.png) |
| `day/hotel_ballroom` | Place a speaker behind the lectern in the `speaker` spot. The sample slide reads “Investor seminar.” | [Seminar stage](hotel-ballroom-day.png) |
| `night/investigation_room` | Place the investigator behind the desk in the `behind_desk` spot. The lamp lights the ledger and a second pool picks out the transfer board. | [Investigation room](investigation-room-night.png) |
| `day/courtroom` | Keep the close bench framing in daylight. The `judge` spot puts the actor behind the furniture layer. | [Empty courtroom](courtroom-day-bench.png) · [Ponzi reenactment](courtroom-day-ponzi.png) |

Use `sets.get_set(name).spots` for feet coordinates and scale. The ballroom, investigation room, and courtroom accept `back_actors` for furniture occlusion. The [courtroom staging example](ponzi_courtroom.py) reproduces the Ponzi plea scene, with the boater on the defense table and the prosecutor holding an exhibit. It accepts an output PNG path when the animator skill is on the Python module path.

## Paper trail

The [approved prop sheet](paper-trail.png) shows the general ledger, transfer record, vendor invoice, and case folder. Each can be drawn independently from `engine.paper_trail` by translating the canvas to its center and calling `ledger`, `transfer_record`, `invoice`, or `evidence_folder` with the canvas, reference string, and display amount. The composite is available as `draw_sheet(canvas, record, amount)`. The dates, descriptions, and surrounding ledger entries are illustrative. Use sourced details when depicting an actual record.

## Design references

The suburban set takes its porch proportions from an [Arts and Crafts bungalow](https://www.oldcalifornia.com/1908-arts-and-crafts-bungalow/). The ballroom takes its theater seating and draped stage from the [Westin Portland Harborview](https://www.marriott.com/en-us/hotels/pwmwi-the-westin-portland-harborview/photos/). The investigative workspace takes its desk lamps and wall of pinned files from [ATL Film Studios](https://www.atlfilmstudios.com/sets/police-bullpen/). Each set is drawn in code.
