# CurseForge project page

Source of truth for the Trashlands CurseForge listing. Edit here, then paste to CurseForge.
The step-by-step for the first submission is in [`cf_submission_checklist.md`](./cf_submission_checklist.md).

**Voice for this page: spec sheet, not sales copy.** State what the pack contains and how it
behaves. No prose paragraphs where a list works, no selling, and no personifying blocks or the
world. "Coarse dirt reverts grass at the frontier" - not "the junkyard takes it back".

---

## Project creation form (paste-ready)

| Field | Value |
|---|---|
| **Project name** | `Trashlands` |
| **Summary** | `There is no ore and no wood. You dig garbage mounds, sort what comes out, and build from that.` |
| **Class** | `Modpacks` |
| **Main category** | `Small / Light` (5 mods, no kitchen sink) |
| **Additional categories** | `Tech` |
| **Allow Comments** | on |
| **Unlisted project** | off (leave public; it needs to be findable to get playtesters) |
| **Social links** | Issues: `https://github.com/Flatts3000/trashlands/issues`  ·  Source: `https://github.com/Flatts3000/trashlands` |
| **License** | `MIT` (pack content; each bundled mod keeps its own license) |
| **Logo** | `pack/icon.png`, square PNG. See the icon note in `cf_submission_checklist.md`. |

Summary is 94 characters. CurseForge asks you to keep the game name, category, and class out of it,
so it does not say "Minecraft" or "modpack".

**Category caveat:** CurseForge's modpack category list is only visible in the dropdown (the public
categories API needs a Core API key, which is separate from the upload token). `Small / Light` and
`Tech` are the intended picks; if the dropdown names them differently, match the closest and update
this table. `Quests` now applies as far as the mod list goes (FTB Quests is in), but the book holds
one page, so it stays off until there is real quest content.

---

<!-- PASTE MARKER - everything below this line goes in the CurseForge Description field, as-is -->

# Trashlands

Minecraft 26.1.2, NeoForge 26.1.2.94, 49 mods.

A coarse-dirt plain covered in garbage mounds. No ore generates, no trees grow, and the world
contains no water. Materials come from Blocks of Garbage dug out of the mounds.

Mined mounds regrow toward the footprint and height they had, delivered as garbage falling from the
sky. Healing the ground a mound stood on retires it permanently, so a regrowing mound is income and
healed ground is not.

New worlds always use the Garbage world type. The world-type button is removed from world creation.

## The loop

1. Dig a Block of Garbage out of a mound.
2. Sort it. Sorting by hand works, but the block crumbles after a few pulls. A Sorting Tarp stops
   the crumbling, and later machines sort unattended.
3. Sorting returns base materials plus what was buried in the block: bags, bales, Bulky Waste, and
   intact found items.
4. Take found items apart at the Recompile Workbench. Rack a Scrap Knife or Prybar on the bench
   first by right-clicking it with the tool, then hold right-click with the item. You get the
   materials it was made of.
5. Teardown also returns Idea Fragments. Enough fragments toward one recipe craft into a blueprint
   sheet, which unlocks that recipe at the Scrap Crafting Table. Every teardown counts; there is no
   chance roll.

## Reclamation

Grass does not spread on this world. Dirt, podzol, mud, and moss all revert to coarse dirt at the
frontier. The reclamation ladder determines what survives:

| Rung | Behaviour |
|---|---|
| Grass Spreader | Multiblock drip irrigator. Converts coarse dirt to grass within a radius. Consumes nothing once built. |
| Plant cover | Erodes first, leaving the soil under it intact. A border loses its plants before it loses its grass. |
| Trees | Stop erosion permanently. The Tree Nursery is the only source; saplings are not obtainable. |

Erosion rules:

- Only soil bordering unhealed ground erodes. Interior ground is unaffected until the edge reaches it.
- Placed blocks never erode.
- Erosion does not run while you are logged off.
- Wet farmland does not erode. Dry farmland does, and a crop on it drops rather than being destroyed.
- Soil reverts to plain coarse dirt, never back to Mound Ground. A retired mound stays retired.

## Contents

- **Demolition yard** - rubble, steel beams, a cutting torch, reinforced concrete.
- **Cupola Furnace** - iron without an ore vein. Rebar and Steel Offcuts are blasting recipes, so an
  ordinary furnace will not smelt them.
- **Scrap Network** - Scrap Bins bound to one material each, plus barrels for overflow. The Filing
  Cabinet stores blueprint sheets and works from anywhere in the cluster.
- **Hydroponics Bay** - grows a crop from water and power with no soil. The input crop is not
  consumed. A second slot catches byproducts.
- **Water** - a Rain Collector is the only source. Water does not spread, so two source blocks will
  not fill in a third.
- **Food** - tin cans, which apply a random effect on eating the way Suspicious Stew does, and
  foraged dump mushrooms. No thirst bar.
- **Collectibles** - a Puzzle Cube in nine pieces, intact found objects, six recovered paintings
  that keep their variant when broken and replaced, and a Display Pedestal.
- **Power and gadgets** - Powah for FE generation and storage, plus Building Gadgets, Mining
  Gadgets, Charging Gadgets, LaserIO, and Just Dire Things.
- **Guidebook** - in-game, covers every system. Multiblock entries have 3D pages that project the
  build into the world in front of you.

## Not in yet

This is an alpha. Two specific gaps:

- **The quest book covers the first two chapters.** Everything past your first Bucket of Water is
  the guidebook.
- **Balance numbers are first-pass.** Drop rates, recipe costs, and teardown yields were picked to
  prove the mechanics, not tuned against play. Expect them to move.

## Getting started

1. Dig a Block of Garbage out of a mound with your hands.
2. Place it, then right-click it empty-handed to pull items out. It crumbles after a few pulls.
3. Craft the Scrap Crafting Table, then a prybar and a scrap knife.
4. Build a Sorting Tarp.
5. The guidebook covers the rest.

Food and water come out of the same mounds as everything else. Farmland is built towards, not
started with.

## Mods

| Mod | Role here |
|---|---|
| [Recompile](https://www.curseforge.com/minecraft/mc-mods/recompile) | The world type, the garbage, the machines, teardown, the reclamation ladder. Everything above. |
| [Just Enough Items](https://www.curseforge.com/minecraft/mc-mods/jei) | Recipes, plus Recompile's own categories for sorting, prying, cutting, burning, and teardown. |
| [Jade](https://www.curseforge.com/minecraft/mc-mods/jade) | Block tooltips: which tool a block requires, and how far a sort has progressed. |
| [Modonomicon](https://www.curseforge.com/minecraft/mc-mods/modonomicon) | The guidebook engine. |
| [Pipez](https://www.curseforge.com/minecraft/mc-mods/pipez) | Item, fluid, and energy pipes. Every Recompile block's automation behaviour is written and tested against it. |
| [Spawn Detective](https://github.com/Flatts3000/spawn-detective) | Reports which rule is blocking a given mob from spawning at a given block. Relevant once you are baiting animals onto reclaimed ground. |

Also in: Powah, Building Gadgets, Mining Gadgets, Charging Gadgets, LaserIO, Just Dire Things, FTB
Quests, FTB Chunks, FTB Essentials, FTB Teams, AppleSkin, Mouse Tweaks, Inventory Essentials,
Controlling, Searchables, Toast Control, Clumps, TrashSlot, Trash Cans, GraveStone, Simple Backups,
Extreme Sound Muffler, FancyMenu, Default World Type, and the performance set (FerriteCore,
ModernFix, Lithium, Sodium, FastFurnace, FastWorkbench, FastSuite).

## Links

- **Source and design docs:** <https://github.com/Flatts3000/trashlands>
- **Bugs and balance feedback:** <https://github.com/Flatts3000/trashlands/issues>
- **The mod on its own:** <https://www.curseforge.com/minecraft/mc-mods/recompile>

## Art and licensing

Art sourced from elsewhere is public domain or CC0. The paintings are PD works off Wikimedia and the
collectibles are ported from CC0 asset kits. The rest was made for the mod.

Pack content is MIT. Each bundled mod keeps its own license - check that mod's CurseForge page for
its terms.
