# Progression gates: what is available when

**Purpose.** One page answering "can the player have X yet?" - and, just as importantly, "does anything the
player already has become useless or unreachable if I change this?"

This exists because that question kept getting answered wrong from memory. On 2026-07-30 a proposal to gate
iron behind a better smelter would have soft-locked the demolition yard: the Cutting Torch cost an iron
ingot, and the only iron came from steel beams that need the torch to cut. The circle was invisible until
someone traced every recipe and loot table by hand. This page is that trace, kept current.

**Scope.** The Recompile engine's own economy. Modpack additions layer on top and can only loosen these
gates, never tighten them.

---

## How to use this when changing the economy

Before removing or gating a material, walk this checklist:

1. **What is the first source?** Not the bulk source - the *first* one. Bulk sources are usually downstream
   of a tool that costs the very thing they produce.
2. **What does that first source cost?** If the answer includes the material itself, you have a circle.
3. **What becomes unreachable?** Trace forward from anything the gated material feeds.
4. **What becomes useless?** A drop with no consumer is as broken as a missing drop - it just fails quietly
   instead of loudly.
5. **Does a machine that enforces the gate actually exist yet?** Gating a material before its replacement
   processor ships means removing the only path and providing nothing.

Update this page in the same change that moves a gate. A stale gate table is worse than none, because it
gets trusted.

---

## Tier 0 - bare hands

Available at spawn, no tools required.

| Material | Source |
|---|---|
| Garbage blocks, trash bags, bales | The dump surface; pick through by hand |
| The seven base materials | Pull streams: scrap metal, plastic scrap, glass shards, organic muck, fiber scrap, e-scrap, junk |
| Rebar | Scrap-metal pull stream. The universal handle - this world's stick |
| Dump mushrooms, tin cans | Foraging and pulls |
| **Raw Roach** | Disturbed out of a Block of Garbage while picking through (#78) |

**Not available:** wood, stone, ore, any metal. There are no trees and nothing to mine.

> **Roaches are the earliest renewable food in the game** (2026-07-31, #78), and that is a deliberate
> exception to how thin tier 0 is. Everything else here is *found* - a can, a mushroom - and renewable
> protein otherwise waits until rung 5 behind the Compost Heap, Fertilizer and the whole reclamation
> ladder. Cooked Roach is pinned at the tin can's nutrition rather than above it, and the drop requires a
> player kill so it cannot be farmed. Those two constraints are what keep it from undercutting the ladder;
> raising either is a progression change, not a tuning pass.

## Moving a pile is its own gate (2026-08-05, Recompile 0.7.0)

**Sorting is free; hauling is not.** Every pile still picks through bare-handed at the same rate, but
carrying one away needs a tool, and swinging without it leaves the pile standing and says what it
wants.

| Pile | Picks up with | Sorts with |
|---|---|---|
| Trash Bag | bare hands | bare hand |
| Block of Garbage | any shovel | bare hand |
| Stone Rubble | any shovel | bare hand |
| Mechanical Waste | any pickaxe | bare hand |
| Compacted Bale | Scrap Knife | Scrap Knife |

Any vanilla shovel or pickaxe works; the Junk Shovel is not special-cased. **This makes the Junk
Shovel load-bearing rather than a convenience** - it is the first tool that lets a player move
garbage at all, and the Sorting Tarp is unusable without one, since feeding the tarp means carrying
blocks to it.

**Rebar is the scarcest of the base materials, despite being the crafting spine.** It is weight 40 in
`household_pulls` against junk's 200 and scrap metal's 75 - roughly 7% of pulls. "The universal
handle" describes its job, not its supply, and anything costing several rebar costs more than it
looks.

## Mounds regrow, and healing retires them (2026-08-05, Recompile 0.7.0)

Phase 5 shipped, so the pack's central tension is finally live rather than designed.

| Want | Source | Gated by |
|---|---|---|
| A mound that refills | Quarry it and wait | Nothing. Regrowth runs only near a player |
| A mound gone for good | Green its **Mound Ground** with the Grass Spreader | The reclamation ladder, so rung 1 |

**Mound Ground** is the dark earth under a footprint: coarse dirt with a different name and a darker
face, same hardness and same shovel. Dark ground means that mound comes back. Encroachment can take
the grass back but never back to Mound Ground, so only the green is contested and a retired mound
stays retired.

**It needs a new world.** The memory of what a mound was is written when the world generates, so a
save made before 0.7.0 has none and its mounds stay finite.

## Tier 1 - trash tools

| Material | Source | Gated behind |
|---|---|---|
| Scrap knife, prybar, junk shovel | Crafted from rebar + base materials | Tier 0 pulls |
| Bulky Waste finds (mattress etc.) | Prying open Bulky Waste | Prybar |
| Oily Rag | Fiber scrap + organic muck | Tier 0 pulls |

## Tier 2 - the Burn Barrel (first smelter)

The Burn Barrel burns **refuse only** - food, plus `#recompile:burn_barrel_smeltable` (scrap metal, kelp).
Food is matched by the `FOOD` data component, so every edible works without being listed.

| Material | Source | Gated behind |
|---|---|---|
| **Copper** | Scrap metal -> copper nugget; 9 per ingot, or 6 nuggets -> 3 copper pipes | Burn Barrel |
| Cooked food | Any edible | Burn Barrel |
| Dried kelp | Kelp | Burn Barrel |

**Deliberately NOT available from the barrel:** glass, stone, charcoal, and every metal except copper. It is
an allowlist, so anything new fails closed by default.

> **Copper is the everyman metal** (`material_economy.md`, owner 2026-07-17). Iron is the gated upgrade.
> This is the tier where that rule is actually enforced.

## Tier 3 - the demolition yard biome

Reached by travelling: `RegionBiomeSource` places `demolition_yard` on a distance gradient from spawn.

| Material | Source | Gated behind |
|---|---|---|
| Stone shards -> stone types | Sifting Rubble (rubble piles) | Travel |
| **Steel I-Beam** | Steel piles | Travel |
| **Reinforced Concrete** | Steel piles | Travel |
| Gravel, sand, concrete powder, rebar | Sledgehammering Reinforced Concrete | Copper sledgehammer |
| **Concrete** | concrete powder + water | Rain Collector |
| **Cutting Torch** | Copper pipe + plastic scrap + rebar + oily rag | **Copper**, not iron |
| **Steel Offcut** (unrefined) | Cutting Steel I-Beams | Cutting Torch |

> **The Cutting Torch costs copper, not iron** (owner, 2026-07-30). It used to cost an iron ingot, which
> became circular the moment iron moved behind the Cupola: the torch would have needed iron in order to cut
> the steel that is the only source of iron. Copper breaks the circle.

## The sewers (2026-08-17, Recompile #90)

Under the demolition yard, so they inherit its gate: **travel**, plus a **Prybar** to lift the cover.
Nothing in them skips a tier - that was the acceptance criterion and it is the reason the table is dull
on purpose.

| Yield | Source | Gated behind |
|---|---|---|
| Scrap metal, plastic scrap, e-scrap, rebar, cullet glass | Sewer barrels | Travel + Prybar |
| String, bone | Sewer barrels, and cobwebs with shears | Travel + Prybar |
| **Glass bottle** | Sewer barrels | Travel + Prybar. A second source for a `found_only` item |
| **Cobweb** | Sewer corridors, cut with shears | The only source in the game |
| **Slimeball** | Slimes, which live only in sewers | A deposit against the redstone tier, worth little now |
| **Trident, nautilus shell** | Drowned, from the sewer's spawner | Owner call: a prize at this depth, not a spike |
| **Bulb, Pump, Motor, Machine Frame** | Sewer barrels, own loot pool | Travel + Prybar. All `blueprint_crafting`, so a found one is a single unit that teaches nothing - the blueprint gate is untouched |
| **Mud** | The frog den's floor | Travel + Prybar. **New material, accepted by owner 2026-08-17.** Nothing else in this world produces it |
| **Sand** | The turtle den's floor | Travel + Prybar. Not new - sledgehammering Reinforced Concrete already yields it |

**Mud is a deliberate addition, not a leak** (owner, 2026-08-17). The frog den is floored in it because
`#minecraft:frogs_spawnable_on` is grass block, mud and the two mangrove roots, and mud is the only one
of those a sewer could plausibly contain - so the substrate is the mob rule rather than decoration.
What it opens downstream is **packed mud and mud bricks**, a building-block family this world otherwise
has no route to. Bounded the same way everything else down there is: travel, a prybar, and a finite
structure that does not regenerate.
| Turtles, frogs | Placed, finite | Not renewable - a sewer has the ones it generated with |

**Nothing here is renewable except the mobs the spawner makes.** The barrels roll once, on first
opening, and the placed animals cannot breed (no seagrass, no sand). That is deliberate: the sewer is
cleared rather than farmed.

**The one thing worth watching** is the glass bottle. It is `found_only` and its scarcity is what the
P1.10 water economy leans on; a sewer barrel is now a second route to one. Bounded by travel and a
finite structure, so it is a reward rather than a tap - but it is a second route, and the balance pass
(#36) should look at it with that in mind.

## Tier 4 - the Cupola Furnace

Upgrade from the Burn Barrel using demolition-yard materials (any concrete + copper pipe + the barrel
itself). **The metal tier and the region gate are the same step** (owner, 2026-07-30).

A **metal furnace**: `RecipeType.BLASTING`, so it melts scrap into copper and offcuts and rebar into iron,
and it does not cook. Food and refuse stay with the Burn Barrel, which is still craftable on its own. It also
automates, which the barrel deliberately does not, so upgrading buys a metal tier and a machine tier at once.

(It was an unrestricted smelting furnace until 2026-08-01. See the gate note below for why that changed.)

| Material | Source | Gated behind |
|---|---|---|
| **Iron ingot** | Steel Offcut from beams | Cupola Furnace |
| Iron nugget | Rebar (9 per ingot - a trickle) | Cupola Furnace |

> **The Cupola contains no iron in its recipe**, deliberately. It is the only iron source, so any iron in
> its recipe would recreate exactly the circle the torch's copper substitution removed.
>
> **How iron is gated: a recipe type.** Both iron recipes are `minecraft:blasting` and the Cupola is a
> `RecipeType.BLASTING` machine. A vanilla furnace cannot run a blasting recipe at all, and a vanilla blast
> furnace costs **5 iron ingots**, so it is circular and unreachable before iron. The gate is a property of
> the machine, and no fact about what the world can produce has to hold for it to work.
>
> **The previous gate failed silently, and it is the worked example for why this page exists** (recompile
> #91, 2026-08-01). It was: iron recipes are ordinary `smelting`, gated because the barrel refuses them and
> *no other furnace exists*. That second clause died when the Tree Nursery shipped. Wood makes a wooden
> pickaxe; plain `deepslate` is in `mineable/pickaxe` and in **no** `needs_*_tool` tag, so a wooden pickaxe
> drops cobbled deepslate; and that is in `#minecraft:stone_crafting_materials`. `stone_from_shards` was a
> second route and world deepslate two blocks down a third. Worst of all, **`rebar` is a weight-40 entry in
> `household_pulls`** - the starting biome's stream - so a player could stockpile it on day one and make
> iron at rung 4 with no demolition yard, no Cutting Torch and no Cupola.
>
> The old note here warned in bold that adding a pickaxe before iron would open the gate silently. It then
> happened, from an unrelated feature, and every test stayed green for weeks. **A gate built from the
> absence of a material dies the moment anything adds the material.** The mod now asserts it instead:
> `no_smelting_recipe_turns_a_mod_item_into_iron`.

## Above the Cupola

**Deliberately undecided** (owner, 2026-07-30). The yield ladder previously ended at an "induction recycler",
which named an electric machine this world has no grid for - the only power source is solar panels. A further
rung can be added if a real power system justifies one.

---

## The bed, and the blueprint gate

**Shipped 2026-08-02 (Recompile #95).** Beds are the first thing in this world gated on *knowledge*
rather than on materials, so they do not sit on the metal ladder above and are recorded separately.

| Want | Source | Gated by |
|---|---|---|
| **Idea Fragment** | Tearing a Dirty Mattress down at the Recompile Workbench, 25% a go | Prybar (to find the mattress), Scrap Knife (to tear it) |
| **Clean Mattress blueprint** | 4 fragments about it, crafted together | Four successful rolls |
| **Filing Cabinet** | Bulky Waste find, weight 2 | Prybar. Optional - carrying the sheet also works |
| **Clean Mattress** | 3 wool + 3 string, **Scrap Crafting Table only, blueprint in reach** | The blueprint |
| **String** | 2 Fiber Scrap, or 4 from a mattress teardown | Nothing |
| **Wool** | 4 string, vanilla | Nothing |
| **Any bed** | Clean Mattress + 3 planks; dye the mattress to pick the colour | **Planks**, so the Tree Nursery |

**The Hydroponics Bay is gated the same way (2026-08-02).**

| Want | Source | Gated by |
|---|---|---|
| **Hydroponics Bay blueprint** | 6 Idea Fragments from tearing down broken washing machines | Prybar (the find and the teardown) |
| **Hydroponics Bay** | 6 glass + 2 copper pipe + 1 Machine Frame, **blueprint in reach** | The blueprint, **and glass** - so the demolition yard for sand |

That is two gates on one machine and it is deliberate: the yard supplies the sand, the dump supplies
the knowledge, and neither substitutes for the other. Worth watching in playtest - it is the deepest
thing in the mod and the first object behind two unrelated gates at once.

## The gem tier (2026-08-03)

Past iron the world had nothing at all: no gold, no diamond, no redstone, no lapis, no amethyst, and
worldgen carries no ores. This is the first thing above iron. Spec: `../recompile/docs/gem_tier_spec.md`.

| Want | Source | Gated by |
|---|---|---|
| **Industrial scrap** | Picking a Mechanical Waste pile bare-hand | **The demolition yard**, so travel. Nothing else |
| **Amethyst** | 12 Quartz Grit in a Separator | The Separator, and power |
| **Diamond** | 16 Spent Abrasive in a Separator | The Separator, and power |
| **Redstone** | 16 Magnet Scrap in a Separator | The Separator, power, **and the pull weights** - magnet scrap is the rare entry |
| **The Separator** | 4 iron + 2 Steel I-Beam + 1 Machine Frame, plus 3 beams and 8 frames to build | **Iron**, so the Cupola |
| **Lapis** | Tearing down a **Printer** at the Recompile Workbench (about half of them carry one) | Nothing but finding one. A Bulky Waste spine find, so it arrives long before the yard |
| **Ink, so black and grey dye** | The same Printer teardown, every time | The same. This is the only ink in the world |

**The gate is arithmetic, and that is the whole point.** It is not "you cannot get diamond", it is "one
piece of scrap is worth nothing". A ratio has no failure mode that an absence has: if another mod floods
the player with circuit boards, they reach the gem using that mod's boards, which is correct rather than
a leak. This is the direct answer to how the first iron gate died (#91), and it is why **this gate must
never be re-expressed as a missing item or an uncraftable machine.**

**Redstone is the one that matters** and it is gated in the loot table, not the recipe. It drags fifteen
vanilla items behind it, so it is the automation tier in a single material. But a player needs redstone in
*quantity*, so making one unit cost thirty inputs would be punishing rather than gating. The scarcity
lives in `mechanical_pulls` instead.

**Nothing precious ever falls out of the pile.** `mechanical_waste_never_drops_a_gem` asserts it, and
`no_teardown_recipe_yields_a_gated_material` asserts the other door is shut - teardown is an allowlist, so
the jukebox can hold a diamond (#117) without leaking one.

**Lapis is deliberately not in this tier** (owner, 2026-08-02; shipped #112, 2026-08-04). It comes out of
a Printer instead, and the two halves of the rule above now differ: the pile must still never drop lapis,
but a teardown may. Lapis is a pigment, so it belongs in a printer and does not belong in machinery, which
contains none of it; vanilla puts it at `needs_stone_tool` beside iron and copper rather than beside
diamond, so arriving before the yard is where vanilla already has it. It costs no control, because its one
real job is enchanting and that still needs obsidian.

**Not gated by this tier:** enchanting. It needs obsidian as well as diamond and lapis, and obsidian is
deliberately out of scope. The gem tier can ship complete with enchanting still unreachable.

**Three circles to not re-open.**

- *Bed needs planks -> planks need a tree -> the Tree Nursery needs an Unknown Seedling.* **Holds**, and
  deliberately: the mattress is a day-one find, so a player can hold the blueprint for hours before they
  can use the bed. That is the intended shape - the knowledge arrives early and the materials arrive
  late - but it means **anything that made planks harder would silently push beds out of reach**.
- *Wool used to make a bed directly.* All sixteen recipes are deleted, which also deleted every
  **coloured** bed. The colour ladder came back by dyeing the Clean Mattress; if the dye recipes are
  ever cut, the world has exactly one bed colour.
- *A vanilla crafting table would bypass the blueprint.* **Cannot**, and needs no guard: blueprint
  recipes are their own recipe type, so a vanilla table does not resolve them at all. This is a
  stronger gate than the Cupola's, which the table above still lists as fragile.

**One thing that is NOT a gate and looks like one.** Fiber Scrap now makes string, which makes wool.
Wool is therefore day-one cheap. That was fine to do only because wool no longer makes a bed - under
the old recipes it would have handed every player a bed on the first afternoon.

## Known circles and near-misses

Kept as worked examples, because each was invisible until traced.

| Circle | Status |
|---|---|
| Torch needs iron -> iron needs beams -> beams need torch | **Broken 2026-07-30** by costing the torch copper |
| Cupola refines iron -> Cupola recipe needs iron | **Open risk.** Must be avoided when #50 is specced |
| Burn Barrel gates iron -> Burn Barrel is the only smelter | **Broken 2026-07-30** by shipping the Cupola in the same change |
| Cupola gates iron -> a vanilla furnace would bypass it | **Holds today** only because no cobblestone and no pickaxe exist. Fragile; see Tier 4 |
| Bed needs a blueprint -> blueprint needs mattress teardowns -> mattresses are a day-one find | **Holds by design.** The knowledge arrives early and the planks arrive late; the wait is the shape, not a bug |
| Cupola needs concrete -> concrete needs Reinforced Concrete -> nothing placed it | **Broken 2026-07-30** by the steel pile. The recipe had been written against materials the biome was *meant* to have; nothing checked it was in the world, and iron was unreachable in survival with every test green |

## Changelog

- **2026-08-17** - Recompile 0.10.0. **The Separator stops sorting**; a Block of Garbage, Trash Bag,
  Compacted Bale, Stone Rubble or Mechanical Waste fed to it now does nothing, and unattended sorting
  is the **Trommel's** job (demolition yard: a core, four Steel I-Beams, a Motor, two Machine Frames).
  It yields exactly what a Sorting Tarp yields per block, so the reward is not throughput. The
  **Pulverizer** (a core, a Motor, two Machine Frames, four Steel I-Beams) opens two gates that had no
  source at all: **gold**, by grinding four E-Scrap to Circuit Powder and blasting it in a Cupola, and
  **clay**, by crushing a pottery sherd to grog, mixing three with a Kitty Litter and using the result
  on a water cauldron. Sherds and kitty litter join the dump's pulls. Clay unlocks 43 vanilla items.
  Both new machines are gated behind the yard, so gold and clay sit above iron, not below it.

- **2026-08-12** - Recompile 0.9.0. The **Dead Fridge** replaces the Broken Fan and the Light Fixture
  in Bulky Waste, and a teardown yields exactly one of a motor, a pump or a bulb, with the knowledge
  following whichever came out. **Its freezer is the only ice or snow in the world**, so those are a
  Bulky Waste gate rather than a weather one. Teardowns roll their materials instead of paying a fixed
  pile, averages unchanged. The top of the pull streams got much rarer: buckets, shears, flint and
  steel and leads about every half hour each, name tags hourly, collectibles 480 times rarer. Bulk
  material is untouched, so the early loop's pace is unchanged and only the landmark finds moved.

- **2026-08-11** - Recompile 0.8.0. **Found, not crafted**: anything a person would throw away comes
  out of the dump rather than a grid. Buckets, bowls, shears, flint and steel, leads, name tags,
  paper, books, bundles, glass bottles and all four pieces of leather armour lost their recipes, and
  the rule is enforced against every recipe at load rather than remembered. This is the gate behind
  Salvage ending on a bucket. **Leachate** pools appear on the open ground: it looks like water, will
  not fill a Rain Collector, will not water a crop, and makes you hungry to stand in.

- **2026-08-05** - Recompile 0.7.0. Mound regrowth and Mound Ground ship, so quarry-versus-heal is a
  live decision. Moving a pile now needs a tool while sorting stays bare-handed, which promotes the
  Junk Shovel from convenience to gate. Recorded that rebar is the scarcest base material at weight
  40, against the "universal handle" framing that reads as though it were common.

- **2026-08-02** - The blueprint gate (Recompile #95). Beds move behind knowledge: Idea Fragments from
  mattress teardowns, a Clean Mattress blueprint, and the mod's own crafting table. The sixteen
  wool-to-bed recipes are gone and colour returns through dyeing the mattress. Fiber Scrap now makes
  string, which makes wool cheap - safe only because wool no longer makes a bed.

- **2026-07-30** - Created. Captures the Burn Barrel refuse-only gate, the torch's copper substitution,
  rebar -> iron nugget moving to the Cupola, and the ladder ending at the Cupola.
- **2026-07-30** - Steel piles placed in the demolition yard: the survival source of Steel I-Beams and
  Reinforced Concrete. Closes the gap where the Cupola's recipe called for concrete that nothing produced.
- **2026-07-30** - Cupola Furnace built. Unrestricted smelting furnace, automates, no iron in its recipe.
  Iron recipes are plain smelting; the gate is the barrel's allowlist plus the absence of any other furnace.
- **2026-07-30** - Steel Offcut replaces raw iron as the beam's drop. `minecraft:raw_iron` has left the mod
  entirely; the offcut remelts to iron in the Cupola and nowhere else.
