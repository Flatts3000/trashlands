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

**Status: v1 BUILT 2026-07-26** (Recompile `docs/collectibles_spec.md`). The **Puzzle Cube** shipped as
the reference artifact: nine `puzzle_cube_piece` (rare pull-stream drops) fill the 3x3 grid on the Scrap
Crafting Table into the cube. The cube is a **placeable full block, not an item trophy** - two states,
solved and scrambled, that craft into each other; a `block/cube` with six per-face 3x3 sticker textures
so it renders as a real 3D cube in hand, world, and on a **Display Pedestal** (the mod's one
BlockEntityRenderer, a scoped reversal of P1.11.6). Locked decisions: **per-collectible pieces** (not a
generic shard); a single pedestal that shows **any item** (owner's call - a general curio shelf, not
tag-gated); trademark = generic names; **all art procedural** (a twisty cube failed as AI and as a
downsampled 3D icon at 16px - fixed geometry draws crisper as code); completion reward deferred (the flex
is the display). More artifacts + advancements are v2.

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

**SHIPPED in Recompile 0.18.0 (pinned here 2026-09-04).** This entry is kept for the reasoning, not
as backlog. What actually landed: circular tire heaps across the household sprawl, some of them
permanently burning; hand-break for the tire, Scrap Knife for the rubber, Teardown Workbench for
three rubber plus the steel belts the knife cannot reach; a Pulverizer shreds them in bulk and loses
the wire. Nothing regrows a dump, so one you strip is one you leave. **The sink is the Pump**, whose
recipe moved off Plastic Scrap onto Rubber Scrap - not the Create belt this entry had decided on.
Neither tires nor rubber are fuel.

**Idea:** worldgen **mounds of tires** - the iconic tire-dump pile.

**Fit / notes:**
- **Tire dumps are one of the most recognizable waste sights there is** (and a real environmental
  blight - fire hazard, mosquito breeding). Perfect for a dump world, and the stacked-tire tower
  reads instantly, like the Compacted Bale does for the WALL-E cube language.
- **It's the found source for `rubber`** - already one of "our intermediates" in
  `material_economy.md` (scrap, cullet, muck, plastic sheet, **rubber**) but with no origin named.
  Tires are the obvious one. This is the strongest hook: it gives an orphaned material a home.
- **The chain was decided as** a tire **cut with the scrap knife -> `rubber scrap`** (naming matches
  the scrap family: scrap_metal, plastic_scrap, fiber_scrap), and **rubber scrap -> Create belts**,
  overriding Create's dried-kelp belt recipe, which is nonsense in a treeless dump.
  **That half is dead and cannot be revived:** Create has no NeoForge build past 1.21.1, so it is not
  in this pack and will not be (`CLAUDE.md`). The knife-cut half shipped as written. The sink 0.18.0
  actually used is the Pump, in the mod rather than as pack content, which also answers the
  Create-free-use question below.
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
All four were answered by shipping, three of them differently than this entry expected:

- ~~What does rubber make?~~ **The Pump**, in the mod. Create was the decided answer and is not
  available on this version, so the Create-free use was not optional after all.
- ~~Tires as fuel?~~ **No.** Neither tires nor rubber burn as fuel.
- ~~Tire fire as a config-gated hazard?~~ **Shipped, and it is set dressing exactly as the P2
  pressure-loop rule requires.** It never goes out, in rain or with time, but it does not eat the
  tires and there is nothing on bare dump ground for it to spread to. Water still puts it out.
- ~~Home?~~ **Its own placed feature in the household sprawl**, not a mound variant and not a
  scrapyard region.

## I-5: Bubble wrap you can actually pop

**Idea:** **bubble wrap** found in the trash that you can **actually pop** - right-click, it pops,
it's satisfying.

**Fit / notes:**
- **Pure charm, and that is the point.** `concept.md`'s "why sifting is fun" says the junk is
  load-bearing - it's the field your attention crosses, and part of the delight is the honest,
  human debris itself. Bubble wrap is the platonic packaging-trash object; being able to *pop it*
  is exactly the kind of delightful, no-reason interaction that makes the world feel real rather
  than a loot spreadsheet. Not every found object needs a mechanical payoff - some are just joy.
- **On-stream:** household / packaging refuse (plastics, packaging - the starter region's flavor).
  Common, low-value filler, which is what makes the actual finds mean something.
- **It still has an economy exit** (satisfies the found-economy invariant): pop it all down to
  **popped bubble wrap**, which shreds to **plastic scrap**. So the arc is *play with it, then
  recycle it* - the joy first, the material after. Elegant: the toy and the sink are the same item.

**Depends on:** a custom **pop sound event** (the whole payoff is the sound; no vanilla sound
really nails it). Everything else is a plain item + a use interaction + a recipe.

**Open questions:**
- **Finite or infinite pop?** Finite (each pop consumes a bubble; N pops -> popped wrap -> plastic
  scrap) gives it the clean exit above. Infinite (a forever fidget toy) is pure joy but leaves a
  never-consumed item - probably finite, with the popping being the fun on the way to the scrap.
- **Does popping do anything** (a tiny effect, or an advancement - "Popped 100 bubbles")? Likely
  nothing but the sound and the smile; maybe one cheeky advancement.
- **Multiplayer:** the pop is audible to nearby players (good - shared delight, or shared menace).

## I-6: Roads like rivers between the mounds

**Idea:** **roads** that wind between the mounds **like rivers** - a dump with real **space for
vehicles to maneuver**.

**Fit / notes:**
- **Gives the infinite dump structure and orientation.** Today it's "coarse-dirt plain crowded
  with mounds, dirt showing between them" (`concept.md`) - readable but formless. Roads turn that
  negative space into a **network**: mounds cluster into "blocks," roads are the channels between,
  and suddenly the player has landmarks in a world that is otherwise easy to get lost in. That
  anti-getting-lost value is real in an *infinite* world.
- **Authentic and on-brand.** Real dumps run on access roads for trucks, loaders, and dozers - and
  WALL-E trundles the cleared lanes of a trash city. Roads are the infrastructure that sells "this
  was an operating landfill," not just a random pile.
- **This is a worldgen-architecture shift, not another feature.** The mounds are placed as isolated
  domes (`MoundFeature`, no connectivity). Roads need **pathing/connectivity** - a river-like carve
  or meander that routes *between* clusters. That's a different generation problem (closer to river
  or structure-network gen than scattered features). The biggest cost of this idea is that
  algorithm; call it out before committing.
- **It forward-links to vehicles.** "Space to maneuver" implies a **traversal layer** - roads are
  most meaningful with something to drive (Create contraptions/trains, or a vehicle mod). Roads are
  useful *without* vehicles (navigation, flavor, content routing), but this idea is really the
  first half of a "vehicles in the dump" direction. Worth naming that explicitly.
- **Content routing:** roads are where the **big stuff** lives - abandoned trucks and cars, the
  auto-wrecking cluster (ties to I-4 tires + car batteries). The road *is* the questline of finds.

**Depends on:** a road/path worldgen generator (the hard part). Vehicles are a separate, larger
direction this sets up but does not require.

**Open questions:**
- **How do roads generate?** River-style carve, organic meander, or a loose grid of "blocks"? Do
  mounds get *re-placed* to cluster between roads, or do roads route around existing mounds?
- **Road surface:** packed dirt / gravel / tire-tracked mud / cracked old-world asphalt (a found
  material?). Should read as worn infrastructure, not a clean path.
- **Vehicles: is this greenlighting a vehicle system?** If yes, what drives them - Create, a
  vehicle mod, minecarts reflavored? That decision dwarfs the roads themselves.
- **Do roads carry content** (abandoned vehicles as big finds, roadside debris), or are they purely
  structural/navigational at first?
- Interaction with **mound regrowth** (P1.6): do roads stay clear, or do regrowing mounds reclaim
  them? A road that stays open is a permanent landmark; one that silts up reinforces the quarry-vs-
  heal tension.

## I-7: Coal ash ponds

**Idea:** a frontier region of **coal ash impoundments** - flat grey slurry ponds behind low
embankments, the residue of a power station that is no longer there.

**Fit / notes:**
- **It is a genuinely distinct silhouette.** Every region so far is a pile of something. An ash
  pond is the opposite: dead flat, wet, and enormous, held in by a berm you can walk the top of.
  That reads as a different kind of wrong from a mound field, which is what a frontier region has
  to earn.
- **The real material is useful and boring in the right way.** Fly ash is a cement extender, so
  the region ties straight into the concrete line (I-3, and the reinforced concrete already
  shipped). Ash plus the demolition yard's stone is a more honest concrete chain than either alone.
- **Bottom ash and fly ash are different products**, which gives the region two outputs without
  inventing anything: gritty bottom ash for aggregate, fine fly ash for the binder.
- **The hazard writes itself and is historically real.** Kingston, Tennessee, 2008: an ash pond
  embankment failed and released over a billion gallons. A region where the ground you are standing
  on is the wall holding the pond back is a strong place to stand.
- **Coal is deliberately not found in this world** (locked P0.4/P2.2 - junk is the early fuel). An
  ash region is the residue of coal without ever handing the player coal, which fits that lock
  rather than fighting it.

**Depends on:** the region system (shipped, Phase 4). A pond needs a water-like fill that is not
water, or shallow water over an ash bed.

**Open questions:**
- **Is the pond liquid?** A custom fluid is real cost. Shallow vanilla water over an ash floor may
  read well enough and costs nothing.
- **Does standing in it hurt you?** The P2 pressure-loop rule says never a threat to builds or
  cleared land, but a personal hazard is a different question and may be fine.
- **What gates it?** The demolition yard gates on travel distance. A second region at a similar
  onset would compete with it rather than follow it.
- Relationship to I-3 concrete: does ash *replace* part of that chain or feed it?

## I-8: Leachate pools

**Idea:** **pools of leachate** - the liquid that drains out of a dump - as terrain.

**Fit / notes:**
- **This is the most honest thing a landfill produces.** Rain falls through refuse, picks up
  everything soluble on the way down, and comes out the bottom as a dark liquid that is the single
  biggest reason engineered landfills have liners at all. A dump world without it is a dump world
  with the consequences edited out.
- **It is the natural antagonist to the water economy.** P1.10 made clean water something you
  collect and defend. Leachate is water that has been ruined by exactly the material the player
  spends all day handling, which makes it thematically load-bearing rather than set dressing.
- **Possible mechanic, not yet a design:** leachate as an *input* rather than only a hazard.
  Filtering or evaporating it is a real treatment process and would give the water tier something
  to work against.

**Status:** ~~Region or feature?~~ **Decided (owner, 2026-08-05): feature, not region.** Sparse
pools scattered through `household_sprawl` and the demolition yard - the counter-argument's side,
since leachate forms at every dump. Tracked as Recompile #156.

**Open questions:**
- **Custom fluid, or a retextured/tinted stand-in?** Same cost question as I-7, and the two should
  probably answer it the same way.
- **Does it interact with encroachment?** Ground that leaches is ground that stays hostile. There
  may be a link to `#hostile_ground` here, or that may be one system too many. **One half is already
  decided (owner, 2026-08-05): a pool does not irrigate**, so it never defends farmland from
  encroachment and is never a source of clean water. NeoForge routes farmland hydration through
  `FluidType.canHydrate`, which defaults to false, *not* through the `#minecraft:water` tag - so a
  custom fluid is safe without doing anything, and only literal tinted water re-opens it. See
  Recompile #156.
- What does contact do - damage, an effect, nothing? The P2 rule constrains threats to builds and
  cleared land, not to the player personally.
