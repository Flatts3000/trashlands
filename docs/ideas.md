# Ideas backlog

**Status:** unlocked ideas, captured as they come. This is the holding pen - nothing here is
decided. An idea graduates to a numbered decision in [`design_decisions.md`](design_decisions.md)
(and a row in [`feature_matrix.md`](feature_matrix.md)) once its shape is locked. Each entry is
faithful to the original pitch, plus a few sharp notes and the open questions to resolve before
it can be built. Numbered `I-N` so they can be referenced.

---

## I-1: Junk Cooler (auto-feeder curio)

**Idea:** a **Junk Cooler** that holds **only food** and **automatically feeds you** when you
get hungry. Gets **its own Curios slot**.

**Fit / notes:**
- Sits in the food tier (P1.9). Thematically a salvaged mini-fridge/cooler dug out of the dump -
  on-brand (WALL-E salvage), and it quietly reconnects the "fridge = preserved food" fiction that
  was dropped when the appliance was cut (see P1.11). A cooler is a natural **Bulky Waste find**
  candidate, or crafted from scrap + a cooling element.
- Pure QoL: removes hunger micromanagement. Aligns with "not a survival-pressure pack" (no thirst,
  no grind) - it makes the already-low survival friction lower, it does not add pressure.
- **Its own Curios slot** (a dedicated "cooler" slot type, not competing with other trinkets) is
  the right call so it is an always-on utility, not a slot-cost trade-off.

**Depends on:**
- **Curios API** - a **new dependency**; the lineup so far is Create + Mekanism only. Curios is
  light and widely used, but adding it is a pack-level decision (affects every future trinket-style
  item too, so it may be worth it beyond just this one). Flag before committing.

**Open questions:**
- **What does it auto-eat, and when?** Threshold (eat when hunger drops below N), and which food
  first - worst-first to clear risky stock, or best-first for saturation?
- **Does it auto-eat the risky tin cans** (random-effect food)? Auto-eating a gamble can is funny
  and dangerous - a deliberate design lever (maybe it only auto-eats "safe" food, or maybe the risk
  is the point and you curate what you load).
- **Powered or passive?** Passive fits the food/early tier. If food spoilage ever exists, a
  Mekanism-energy "keeps it cold" version becomes meaningful; no spoilage today, so passive.
- **Found or crafted (or both)?** Bulky Waste find vs. a scrap recipe - or found broken, repaired
  like the furnace (find-and-fix beat).
- **Capacity** and whether it feeds from its own inventory only or also the hotbar.

## I-2: Collectibles -> Trophies

**Idea:** **collectible** items found in the garbage that you gather and craft into **trophies**.
First example: collect **Rubik's Cube Pieces** and craft a **Rubik's Cube Trophy**.

**Fit / notes:**
- **This is the pack's thesis as a mechanic.** `concept.md`'s "why sifting garbage is fun" says
  the pleasure is being *the one who spots it* - the asymmetric score (someone threw this away,
  everyone walked past, you got it for the price of dirty hands). A rare collectible is exactly
  that moment. The trophy is the tangible proof: "the world called this worthless and I proved it
  wrong," made displayable.
- **It is the WALL-E anchor, literally.** WALL-E's whole character is a trash-picker who *hoards
  found curios* - the Zippo, the rubber duck, the spork. A shelf of dug-out trophies is the most
  on-brand thing this pack could ship. `concept.md` already names WALL-E as the tonal anchor.
- **It is a system, not one item.** Rubik's Cube is example #1; "collectible pieces -> display
  trophy" is a **data-driven catalog** (loot-table lines + a recipe + a trophy block), the same
  add-a-line-not-code shape as Bulky Waste finds. Candidates: rubber duck, hubcap, action figure,
  cassette, snow globe, bowling trophy (a trophy of a trophy).
- **Satisfies the found-economy invariant** ("nothing enters the found economy without an exit"):
  the exit is **craft-into-trophy** - a display sink - so collectibles never become clutter.

**Depends on:** nothing new (found item + crafted display block). Optional: an advancement/
achievement per completed trophy; a dedicated "trophy case" or pedestal block to show them off.

**Open questions:**
- **Trademark:** "Rubik's Cube" is a registered mark - for a distributed pack use a generic name
  (**Puzzle Cube**, "Twist Cube"). Applies to every real-brand collectible; keep names generic.
- **Pieces per trophy** and how they're found: a flat rare drop, or a **region-flavored** rarity
  (household -> toys, e-waste -> gadgets, scrapyard -> car/industrial curios)? Rarity must be low
  enough that a find is an *event* - the whole point is that the junk is load-bearing.
- **Trophy form:** a placeable **display block** (implied by "trophy"), pure cosmetic. Does
  completing one grant anything (advancement, a quest reward), or is the flex the reward?
- Do partial sets show progress (e.g. a Jade/tooltip "3/6 pieces"), or is it silent until complete?
- Whether pieces are also a **teardown** input later (a collectible you could tear down for its
  materials instead of trophying) - probably not; the trophy *is* the point.

## I-3: Mounds of vanilla concrete

**Idea:** worldgen **mounds made of vanilla concrete** - dig concrete out of the dump.

**Fit / notes:**
- **Fills a gap the design already named.** `material_economy.md` calls construction & demolition
  debris "the largest real waste stream ... currently a gap in our regions," and lists concrete as
  the source of aggregate (gravel / sand / **andesite** for the Create spine). Concrete mounds are
  that stream, made concrete (literally).
- **A found clean/colored building material** that complements the P1.12 scrap building blocks:
  scrap reads as a shanty; vanilla concrete reads as *rebuilt* - smooth, painted, civic. And it
  hands the player vanilla concrete without its normal craft (powder + dye + water), which fits
  "the old world already made this; you're just recovering it."
- **Two exits, both useful:** buildable directly (a real building palette), and **crushable to
  aggregate** at tier 2 (gravel / sand / andesite), feeding the Create-spine materials the pack
  otherwise has no honest stone source for (no ore, no stone).
- Could be a **mound variant** scattered among garbage mounds, or the seed of the **demolition-yard
  / construction-debris region** that `material_economy.md` leaves as an open "where rubble lives"
  thread. Region is the stronger long-term home; a mound variant is the cheap first step.

**Depends on:** nothing new (vanilla blocks + worldgen feature, reusing the `MoundFeature` shape).

**Open questions:**
- **The no-pickaxe wrinkle (important).** Vanilla concrete is `requiresCorrectToolForDrops` with a
  pickaxe - which this world does not have. Found concrete would drop nothing by hand. Needs a fix:
  a block-tag/hardness override so the shovel or prybar (or bare hand) frees it, same call we made
  for the building blocks. Do NOT ship it pickaxe-gated by accident.
- **Colors:** a grubby grey/mixed rubble palette (realistic C&D), or does this become the player's
  full colored-concrete access? Rubble-grey early, full color as a later reward feels right.
- **Reinforced concrete tie-in:** rebar already exists (the universal handle) - concrete + rebar as
  a sturdier build block is an obvious pairing.
- Mound variant now vs. holding it for the demolition-yard region (P1.5 regions).
- Does concrete powder also appear (the pre-set stage), or only cured concrete?

## I-4: Mounds of tires

**Idea:** worldgen **mounds of tires** - the iconic tire-dump pile.

**Fit / notes:**
- **Tire dumps are one of the most recognizable waste sights there is** (and a real environmental
  blight - fire hazard, mosquito breeding). Perfect for a dump world, and the stacked-tire tower
  reads instantly, like the Compacted Bale does for the WALL-E cube language.
- **It's the found source for `rubber`** - already one of "our intermediates" in
  `material_economy.md` (scrap, cullet, muck, plastic sheet, **rubber**) but with no origin named.
  Tires are the obvious one. This is the strongest hook: it gives an orphaned material a home.
- **Secondary yields, all real recycling streams:** **steel wire** from steel-belted radials (a
  little scrap metal), and **tire-derived fuel** - tires burn hot and dirty, which ties straight
  into the junk-fuel / burn-barrel line (P2.2). A hotter (dirtier) fuel than junk is a natural
  mid-fuel step.
- **Soft, so it fits the no-pickaxe world:** cut a tire with the **scrap knife** for rubber (the
  same "cut it open" verb as the bale and the mattress), or hand-break. No tool wrinkle like the
  concrete has.
- **Decorative builds:** stacked tires are their own vernacular - retaining walls, playground
  swings, planters. A tire block earns its place as deco even before the rubber matters.

**Depends on:** nothing new. Reuses `MoundFeature` and the knife-cut verb; rubber becomes a real
material once something consumes it (see below).

**Open questions:**
- **What does `rubber` actually make?** The intermediate needs a downstream or it's a dead-end -
  belts/conveyor, seals/gaskets, tubing, waterproof boots or a hazmat layer, Create/Mekanism
  inputs. Worth deciding rubber's job when this lands.
- **Tires as fuel:** hotter than junk but dirty - a flavor/pollution angle, or just a better burn?
- **Tire fire** as a config-gated hazard/flavor event (the notorious tire-dump fire) - never a
  threat to builds or cleared land, per the P2 pressure-loop rule. Optional set dressing.
- **Home:** mound variant now, or part of a **scrapyard / auto-wrecking region** where tires
  cluster with cars and car batteries (the lead/battery stream)?
