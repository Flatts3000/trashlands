# CurseForge project page

Source of truth for the Trashlands CurseForge listing. Edit here, then paste to CurseForge.
The step-by-step for the first submission is in [`cf_submission_checklist.md`](./cf_submission_checklist.md).

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
this table. `Quests` does **not** apply to the alpha - there is no quest mod in the lineup yet.

---

<!-- PASTE MARKER - everything below this line goes in the CurseForge Description field, as-is -->

# Trashlands

A coarse-dirt plain with garbage mounds on it. There is no ore and no wood. Everything you build
starts as a Block of Garbage you dug out of a mound and picked apart by hand.

Mine a mound and it grows back. Heal the ground underneath it and it is gone for good. That is the
tension the pack runs on: garbage is your only income, and the only way to make the world green is
to give that income up.

## The loop

Dig Blocks of Garbage. Sort them. Bare hands work but the block crumbles after a few pulls, so you
build a Sorting Tarp, then better tools, then machines that do it while you are somewhere else.

Sorting gives you the base materials plus whatever was buried in the block: bags, bales, Bulky
Waste, and found items that came out of the old world intact. Found items go to the Recompile
Workbench, where holding right-click with the right tool takes them back apart into what they were
made of.

There is no pickaxe in the early game. That is deliberate. Nothing here is worth mining.

## Reclamation

Grass does not spread on this world. A Grass Spreader puts it down, and the coarse earth takes it
back from the edges unless you hold the border. Bare grass reverts first. Plant cover absorbs a hit
and gets stripped instead. Trees hold a border permanently.

So every green block is paid for by a machine you built and keep running. Nothing renews on its own.
Your builds are never touched, and nothing erodes while you are logged off.

Past the grass: vegetation, farmland, a Compost Heap, a Tree Nursery, and baits that settle animals
on ground green enough to hold them.

## What else is in

- **Demolition yard** - rubble, steel beams, a cutting torch, reinforced concrete.
- **The Cupola Furnace** - how you get iron without an ore vein.
- **The Scrap Network** - Scrap Bins that bind to a material, plus barrels for the overflow.
- **Water and food** - a Rain Collector, because the water here does not refill an infinite source.
- **Collectibles** - a Puzzle Cube in nine pieces, rare intact finds, and a Display Pedestal that
  floats and spins whatever you put on it.
- **An in-game guidebook** that covers the systems, so you are not reading a wiki in another window.

## What is not in yet

This is an alpha and it is short in specific places.

- **Teardown gives you materials, not recipes.** Recovering the *recipe* off a torn-down item is the
  mod's main idea and it is still being built. Right now the workbench is a disassembler.
- **No quest book.** Progression is the guidebook and whatever you work out.
- **Balance numbers are first-pass.** Drop rates, recipe costs, and teardown yields were picked to
  prove the mechanic, not tuned against real play. Expect them to move.

Bug reports and balance complaints are useful right now, more than they will be later.

## Getting started

1. Dig a Block of Garbage out of a mound with your hands.
2. Place it, then right-click it empty-handed to pull items out. It crumbles after a few pulls.
3. Craft the Scrap Crafting Table, then a prybar and a scrap knife.
4. Build a Sorting Tarp so the blocks stop crumbling on you.
5. Open the guidebook for the rest.

Rain is your water. Plan for that before you plan anything else.

## Mods

| Mod | What it does here |
|---|---|
| [Recompile](https://www.curseforge.com/minecraft/mc-mods/recompile) | The world, the garbage, the machines, the reclamation ladder. Everything above. |
| [Just Enough Items](https://www.curseforge.com/minecraft/mc-mods/jei) | Recipes, plus the pack's own Sorting, Cutting, and Prying categories. |
| [Jade](https://www.curseforge.com/minecraft/mc-mods/jade) | Tooltips. Tells you which tool a block wants and how far along a sort is. |
| [Modonomicon](https://www.curseforge.com/minecraft/mc-mods/modonomicon) | Runs the in-game guidebook. |
| [Pipez](https://www.curseforge.com/minecraft/mc-mods/pipez) | Item, fluid, and energy pipes. Every machine's automation behaviour is written against it. |

## Links

- **Source and design docs:** <https://github.com/Flatts3000/trashlands>
- **Bugs and balance feedback:** <https://github.com/Flatts3000/trashlands/issues>
- **The mod on its own:** <https://www.curseforge.com/minecraft/mc-mods/recompile>

## License

Pack content is MIT. Each bundled mod keeps its own license - check that mod's CurseForge page for
its terms.
