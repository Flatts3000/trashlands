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

**Not available:** wood, stone, ore, any metal. There are no trees and nothing to mine.

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
| Stone shards -> stone types | Sifting Rubble | Travel |
| Reinforced concrete, more rebar | Sledgehammer | Copper sledgehammer |
| **Cutting Torch** | Copper pipe + plastic scrap + rebar + oily rag | **Copper**, not iron |
| Raw iron (unrefined) | Cutting Steel I-Beams | Cutting Torch |

> **The Cutting Torch costs copper, not iron** (owner, 2026-07-30). It used to cost an iron ingot, which
> became circular the moment iron moved behind the Cupola: the torch would have needed iron in order to cut
> the steel that is the only source of iron. Copper breaks the circle.

## Tier 4 - the Cupola Furnace (#50, NOT BUILT)

Upgrade from the Burn Barrel using demolition-yard materials. **The metal tier and the region gate are the
same step** (owner, 2026-07-30).

| Material | Source | Gated behind |
|---|---|---|
| **Iron ingot** | Raw iron from beams | Cupola Furnace |
| Iron nugget | Rebar (9 per ingot - a trickle) | Cupola Furnace |

> **Currently a dead end.** Beams drop raw iron and *nothing* refines it until this ships. That is a
> deliberate "you found it, now build the smelter" beat, but it does mean raw iron stockpiles with no use on
> `main` today. It is the single most load-bearing unbuilt thing in the economy.
>
> **The Cupola must not cost iron.** It is the only iron source, so any iron in its recipe recreates exactly
> the circle the torch's copper substitution just removed.

## Above the Cupola

**Deliberately undecided** (owner, 2026-07-30). The yield ladder previously ended at an "induction recycler",
which named an electric machine this world has no grid for - the only power source is solar panels. A further
rung can be added if a real power system justifies one.

---

## Known circles and near-misses

Kept as worked examples, because each was invisible until traced.

| Circle | Status |
|---|---|
| Torch needs iron -> iron needs beams -> beams need torch | **Broken 2026-07-30** by costing the torch copper |
| Cupola refines iron -> Cupola recipe needs iron | **Open risk.** Must be avoided when #50 is specced |
| Burn Barrel gates iron -> Burn Barrel is the only smelter | **Broken 2026-07-30** by moving iron to BLASTING, which only the Cupola will run |

## Changelog

- **2026-07-30** - Created. Captures the Burn Barrel refuse-only gate, the torch's copper substitution,
  rebar -> iron nugget moving to the Cupola, and the ladder ending at the Cupola.
