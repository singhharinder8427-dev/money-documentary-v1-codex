# Dirty Dollar story asset library

This expansion adds 22 sets, 32 props and screens, and seven characters. The stills are the approved visual references at 1920 × 1080. Use the set keys with the engine’s normal shot renderer.

| Category | Assets | Preview |
|---|---:|---|
| Finance and business | 6 | [Contact sheet](finance-six-reviewed.jpg) · [Contrast comparison](finance-six-contrast-comparison.jpg) |
| Law and consequences | 6 | [Contact sheet](law-preview.jpg) · [Visiting-room coverage](visiting-coverage-preview.jpg) |
| Everyday life | 5 | [Contact sheet](everyday-preview.jpg) |
| Wealth and public image | 5 | [Contact sheet](wealth-preview.jpg) |
| Money movement | 7 | [Contact sheet](money-preview.jpg) |
| Paper trail | 8 | [Contact sheet](paper_trail_props-preview.jpg) |
| Digital scams | 7 | [Contact sheet](digital-preview.jpg) |
| Furniture and dressing | 10 | [Contact sheet](dressing-preview.jpg) |
| People | 7 | [Contact sheet](people-preview.jpg) |

## Sets

| Set key | Approved still |
|---|---|
| `night/private_banker` | [Private banker’s office](finance/private-banker-night.png) · [Phone](finance/private-banker-night-phone.jpg) |
| `day/ordinary_office` | [Ordinary office floor](finance/ordinary-office-day.png) · [Phone](finance/ordinary-office-day-phone.jpg) |
| `day/startup_workspace` | [Startup workspace](finance/startup-day.png) · [Phone](finance/startup-day-phone.jpg) |
| `day/stock_exchange` | [Stock exchange exterior](finance/stock-exchange-day.png) · [Phone](finance/stock-exchange-day-phone.jpg) |
| `night/bank_vault` | [Bank vault](finance/bank-vault-night.png) · [Phone](finance/bank-vault-night-phone.jpg) |
| `day/warehouse` | [Warehouse floor](finance/warehouse-day.png) · [Phone](finance/warehouse-day-phone.jpg) |
| `day/visiting_room` | [Jail visiting room](law/visiting-room.png) |
| `day/courthouse_exterior` | [Courthouse exterior and steps](law/courthouse-exterior.png) |
| `day/deposition_room` | [Deposition room](law/deposition-room.png) |
| `day/regulator_hearing_room` | [Regulator hearing room](law/regulator-hearing-room.png) |
| `day/jail_intake_desk` | [Jail intake desk](law/jail-intake-desk.png) |
| `night/cell_corridor` | [Cell corridor](law/cell-corridor.png) |
| `day/public_park` | [Public park](everyday/public-park.png) |
| `day/cafe_booth` | [Café booth](everyday/cafe-booth.png) |
| `night/apartment_hallway` | [Apartment hallway](everyday/apartment-hallway.png) |
| `day/shop_counter` | [Small-business shop counter](everyday/shop-counter.png) |
| `day/train_station` | [Train station](everyday/train-station.png) |
| `day/mansion_exterior` | [Mansion exterior](wealth/mansion-exterior.png) |
| `night/luxury_apartment` | [Luxury apartment](wealth/luxury-apartment.png) |
| `night/charity_gala` | [Charity gala](wealth/charity-gala.png) |
| `day/press_conference` | [Press-conference stage](wealth/press-conference.png) |
| `night/tv_interview_studio` | [TV interview studio](wealth/tv-interview-studio.png) |

```python
from engine import shots
from engine.story_assets import visiting_coverage

park = shots.wide('day/public_park')
visit = visiting_coverage.shot('two_shot')
```

The visiting-room scene has a clean background, plus a [two-shot](law/visiting-room-two-shot.png), [visitor close-up](law/visiting-room-visitor.png), and [detainee close-up](law/visiting-room-detainee.png). The `shot()` view names are `two_shot`, `visitor`, and `detainee`. Use `back_actors` with `day/visiting_room` to stage custom actors behind the counter and glass divider. The `day/visiting_room_call` set has empty handset cradles for a conversation in progress.

## Props and characters

The individual prop drawing functions use a 960 × 540 design canvas. Call them on a canvas scaled by 2 for a full-frame overlay, or apply a custom transform for a scene insert. The financial records and screens use fictional sample entries. Furniture functions accept positions and can be composed independently. Use `people.draw_person(canvas, slug, x, y, scale, **pose)` for the supporting cast with their identifying clothing and accessories.

**Money movement.** [Drawing code](../../.claude/skills/documentary-animator/engine/story_assets/money.py)

[Check and checkbook](money/check-and-checkbook.png) · [Wire receipt](money/wire-receipt.png) · [Deposit slip](money/deposit-slip.png) · [Credit card](money/credit-card.png) · [Payment terminal](money/payment-terminal.png) · [Bank statement](money/bank-statement.png) · [Cash drawer](money/cash-drawer.png)

**Paper trail.** [Drawing code](../../.claude/skills/documentary-animator/engine/story_assets/paper_trail_props.py)

[Pitch deck](paper_trail_props/pitch-deck.png) · [Prospectus](paper_trail_props/prospectus.png) · [Signed contract](paper_trail_props/signed-contract.png) · [Audit memo](paper_trail_props/audit-memo.png) · [Corporate filing](paper_trail_props/corporate-filing.png) · [Court exhibit sticker](paper_trail_props/court-exhibit-sticker.png) · [Evidence bag](paper_trail_props/evidence-bag.png) · [Archive box](paper_trail_props/archive-box.png)

**Digital scams.** [Drawing code](../../.claude/skills/documentary-animator/engine/story_assets/digital.py)

[Investment dashboard](digital/investment-dashboard.png) · [Transaction history](digital/transaction-history.png) · [Fake profit screen](digital/fake-profit-screen.png) · [Withdrawal error](digital/withdrawal-error.png) · [Message thread](digital/message-thread.png) · [Call log](digital/call-log.png) · [Email window](digital/email-window.png)

**Furniture and dressing.** [Drawing code](../../.claude/skills/documentary-animator/engine/story_assets/furniture.py)

[Cubicle walls](dressing/cubicle-walls.png) · [Desk](dressing/desk.png) · [Conference chair](dressing/conference-chair.png) · [Filing cabinet](dressing/filing-cabinet.png) · [Podium](dressing/podium.png) · [Queue posts](dressing/queue-posts.png) · [Street sign](dressing/street-sign.png) · [Park bench](dressing/park-bench.png) · [Period phone](dressing/period-phone.png) · [Period lamp](dressing/period-lamp.png)

**People.** [Drawing code](../../.claude/skills/documentary-animator/engine/story_assets/people.py)

[Judge](people/judge.png) · [Court clerk](people/court-clerk.png) · [Attorney](people/attorney.png) · [Compliance officer](people/compliance-officer.png) · [Auditor](people/auditor.png) · [Call-center operator](people/call-center-operator.png) · [Small-business owner](people/small-business-owner.png)

## References

The drawings use original geometry and the Dirty Dollar palette. Layout and prop references included the following.

- Finance · [SMBC private banking consultation room](https://www.smbctb.co.jp/globalcompass/tips/prestia-benefits-for-foreign-nationals/) · [AFC open office](https://www.afcindia.in/projects/air-india) · [Knoll innovation workspace](https://www.knoll.com/story/design-plan/1717-innovation-center) · [NYSE façade](https://en.wikipedia.org/wiki/New_York_Stock_Exchange_Building) · [University National Bank vault](https://hunterscapital.com/university-national-bank-building/) · [Warehouse aisle](https://cedarvalleycheese.com/warehouse)
- Law · [NYC non-contact visiting room](https://www.nyc.gov/assets/borojails/downloads/pdf/queens/public-meeting-materials/2026/BBJ-QN-FAC-CDW4-Presentation-4.28.26.pdf) · [SEC open meeting](https://www.forbes.com/sites/jonmcgowan/2024/02/23/to-survive-legal-challenges-sec-must-remove-scope-3-from-sustainability-reporting-rule/)
- Everyday life · [Central Park Mall and Literary Walk](https://www.centralparknyc.org/locations/the-mall-literary-walk) · [Freiberg station](https://www.archlab.de/projekte/historisch/bahnhof-freiberg/)
- Wealth and public image · [Meliá Milano event room](https://thevendry.com/venue/222841/melia-milano-milano-italy/space/116809)
- Props · [Miami-Dade deposit-slip example](https://www.miamidade.gov/technology/library/informs/presentation/fin-204-receivables-processing.pdf) · [FTC investment scam descriptions](https://consumer.ftc.gov/articles/investment-scams)
