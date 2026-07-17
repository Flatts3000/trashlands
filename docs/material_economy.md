# Material economy - working doc

**Status:** candidates, not locked (2026-07-14). The framework below came out of the P2.2 discussion; individual rows get locked as their tiers are designed. Companion to [`design_decisions.md`](design_decisions.md).

---

## The two governing principles

**1. Purity as yield, not as parallel items** (locked in P2.2). Processed outputs are vanilla items wherever vanilla has them; what improves with tech tier is the conversion ratio, never a parallel "reclaimed X" item. Identity lives in the inputs and intermediates (scrap, cullet, muck, plastic sheet, rubber), which are ours.

**2. The found-to-made arc applies to materials, not just recipes.** Every material has a **found source** (a thematic garbage stream) and eventually a **made source** (synthesis or refinement at higher tier). Early game you scavenge it; endgame you manufacture it. This mirrors the recipe knowledge arc - the whole catalog migrates from found economy to made economy.

---

## Metals - real recycling streams, carried by teardown tables

Bulk **scrap metal** smelts to **copper** in a basic furnace (the Burn Barrel) - a **gameplay-gating** call (owner, 2026-07-17) that inverts the old iron-baseline. Copper is the accessible everyman metal; **iron becomes the gated upgrade**, from a better process than the barrel, not basic smelting. The yield ladder (burn barrel lossy -> repaired furnace -> induction recycler near-lossless) stands and now doubles as a **metal-tier** ladder: copper first, iron later. Realism is traded for sequencing - a real dump smelts mostly to iron, but copper-first is a cleaner Create on-ramp (copper feeds the brass/casing side early; iron gates Create's core, since andesite alloy needs an iron nugget).

Specific metals come from tearing down specific found components - no typed-scrap item bloat, no new mechanics, and adding a metal later is one component item + JSON tables. Real-world streams:

| Metal | Garbage stream (found source) | Made source (late tier) |
|---|---|---|
| Copper | Bulk scrap in a basic furnace (the everyman metal, copper-first); wire spools, motors, pipes, transformers | Mixed-scrap fine separation |
| Iron/steel | **Gated** - a better smelter than the burn barrel (upper rungs of the ladder, or teardown finds; open) | - |
| Aluminum | Cans, window frames, foil | Mixed-scrap fine separation |
| Lead | Car batteries, old pipes, CRT glass, wheel weights | Battery recycling chain |
| Gold | Circuit boards, connectors (e-waste) | E-scrap chemical recovery |
| Silver | Electronics, mirrors, photographic scrap | E-scrap chemical recovery |
| Zinc | Galvanized steel coating, dry-cell batteries | De-galvanizing step |
| Nickel / Lithium | Batteries (the battery chain is its own mini-tree) | Battery recycling chain |
| Tin | Cans (tinplate), solder on boards | Solder reclaim |
| Netherite / ancient debris | The Nether's compacted depths (dump you mine) | - |

Side effect worth keeping: the player learns where metals actually live in real garbage. Material literacy is flavor AND tutorial.

## Gems - the found-to-made arc in miniature

| Tier | Diamond source |
|---|---|
| Early (found) | **Jewelry** in household pulls - rare; people really do throw out rings |
| Mid (found, reliable) | **Industrial diamond tooling** - saw blades, drill bits, grinding wheels in scrapyard/slag field |
| Late (made) | **The synthesis press** - carbon from junk/organics compressed to lab-grown diamond. Garbage into diamond is the pack's thesis as a single recipe. |

- **Emerald:** jewelry stream early; villager economy returns post-reclamation (see the final chapter).
- **Amethyst/quartz:** see quartz row below; decorative gems can ride the jewelry stream.

## The vanilla problem materials

Every vanilla material that has no honest garbage presence gets the same treatment: found stream + made path.

| Material | Found source | Made source |
|---|---|---|
| Redstone | Electronics teardown (boards, motors, sensors) | E-scrap refinement |
| Quartz | Circuit oscillators (real!), old clocks, countertops | Slag-field silica processing |
| Glowstone | Lamps, CRT/fluorescent phosphor coatings | Chemical tier |
| Lapis | Pigment containers, dyes, old paint | Chemical tier |
| Coal | NOT found - junk is the early fuel (locked P0.4/P2.2) | Charcoal from recovered wood; carbon black from plastic processing |
| Obsidian | Not found - made only (melt slag/glass; portal gate is earned) | Slag furnace |
| Ender pearls | E-waste rare drop ("eyes of ender from e-waste" - locked in Dimensions bridge) | End access |
| Wood | Pallet fragments, furniture (mid-tier treasure, locked P1.1) | Tree farms post-reclamation - trees are nearly endgame |
| Diamond/gems | See gems table | Synthesis press |

## The Create spine (belts are Create's job - locked P2.3 direction)

Create's progression chokepoints are andesite alloy and brass. Both resolve inside the framework, plus one new principle:

**Alloys obey found-to-made too - you can FIND an alloy before you can MAKE it.**

| Need | Found source (early, bulk) | Made source (later) |
|---|---|---|
| Brass | Plumbing fixtures, faucets, valves, instruments, lamp bases - scrap brass is among the most-recycled metals IRL; scrapyard commons | Copper + zinc, Create's own mixer chain |
| Bronze | Bushings, bearings, statues, bells | Copper + tin |
| Zinc (bulk) | **Corrugated galvanized roofing sheet** (iconic dump material) - de-galvanize into zinc + clean steel | Battery chain stays the trickle source |
| Andesite | **Construction rubble** (C&D debris - the largest real waste stream; currently a gap in our regions): concrete chunks/masonry crush to aggregate = gravel, sand, andesite | - (bulk found is enough) |
| Copper (bulk) | Wire spools, motors (already in matrix) - must be pull-table commons | Mixed-scrap fine separation |

**Volume principle:** Create-spine materials ride bulk commons (rubble, corrugated sheet, wire, fixtures), never rare extras. If automation materials are slot-machine pulls, the tier dies. Tune pull tables so the spine flows.

**Open:** where construction rubble lives - seeded through scrapyard/slag pulls, or its own minor region (demolition yard) when regions expand.

## The Mekanism spine (Mekanism is in the pack lineup - later-tier processing/chemical endgame)

Mekanism's ore needs map to the later regions (decided 2026-07-14):

| Need | Found source |
|---|---|
| Uranium | **Hazmat quarantine** - spent fuel containers, radioactive medical waste, reactor components. The hard-gate region's treasure: the reason to build protection is the fuel of the endgame. |
| Osmium | **The Nether (compacted depths)** - the dump you mine. Osmium and first RF power both originate here (see P3.5). |
| Fluorite | Slag field - industrial flux, water-treatment chemicals. |
| Lead / Tin | Already in the metals matrix (batteries, pipes / cans, solder). |

Reframe: Mekanism's ore-multiplication machinery reads as ultimate recycling efficiency (purity-as-yield's top tier).

**Energy note:** the first RF power originates in the Nether (P3.5). Tiers 1-2 are fuel/manual only (no energy); RF generation unlocks with Nether access, feeding the mid/late electrical tiers.

## Open threads for later tiers

- **Mixed-scrap fine separation** (copper/aluminum out of bulk scrap) is the tier 3-4 sorting payoff - possibly the Magnetism hook if that mod ever happens; works without it.
- **The battery chain** (lead, nickel, lithium, zinc) is dense enough to be its own quest arc inside e-waste.
- **Washing/degreasing** ("oily scrap" from slag field needs cleaning before smelting well) - optional processing texture, parked for the slag region's identity.
- **Ratio table per tier** (burn barrel -> furnace -> induction) needs real numbers when the economy is tuned against playtests.
