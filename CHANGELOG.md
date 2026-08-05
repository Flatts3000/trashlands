# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The `## [X.Y.Z]` headings are load-bearing: `.github/workflows/release.yml` regex-extracts the
matching section for the GitHub release notes and the CurseForge changelog. Keep the exact shape,
and ASCII punctuation only.

## [Unreleased]

### Added
- **A quest book with something in it.** Two chapters and 21 quests, from your first Block of
  Garbage to your first Bucket of Water. **Welcome** covers what this world is, what spawns here,
  where the water is, and the fact that coarse dirt takes green ground back. **Salvage** runs the
  whole early game: the trash tools, Bulky Waste, food, storage, the Sorting Tarp, the Workbench,
  and the two lines that meet at a bucket, one through a found Pump and rain, the other through the
  Burn Barrel and copper.
- **The Salvager's Manual is handed to you** on the first quest instead of being something you have
  to work out how to craft.
- **Quests pay XP**, weighted by what they ask. Ten for something you only have to read, a hundred
  for the Bucket of Water.
- **FTB XMod Compat**, which is what lets JEI work inside the quest book.
- **Mounds grow back.** Recompile 0.7.0 makes a quarried mound rebuild itself toward the footprint
  and height it had, delivered as garbage falling out of the sky, so you can see across the plain
  which ones are refilling. It never grows past what it was and never seeds a new one.
- **Healing a mound retires it for good.** The dark earth under a footprint is Mound Ground, and
  greening it with the Grass Spreader ends that mound permanently. A regrowing mound is income and
  healed ground is not, so the trade the pack is named for is now a decision you make rather than
  one the world makes for you.
- **Gems, out of the demolition yard.** Recompile 0.6.0 adds Mechanical Waste and the Separator, a
  multiblock that pulls amethyst, diamond and redstone back out of industrial scrap. The ratios are
  the gate: 12 quartz grit for an amethyst, 16 spent abrasive for a diamond, 16 magnet scrap for
  redstone. Magnet scrap is the rare one, so redstone is the thing you work toward.
- **The Separator also sorts garbage unattended**, at exactly the Sorting Tarp's rate. It runs while
  you are elsewhere; it does not yield more.
- **Printers** turn up in Bulky Waste. Tearing one down gives paper, plastic, scrap, an ink sac, and
  about half the time a lapis lazuli. Ink is the only black dye in this world, so printers are the
  only route to grey and black beds.
- **Shears, flint and steel, and a spyglass** now turn up in the dump, already worn.
- **Cats, dogs and pigeons** live on the plain, rarely. A pigeon will walk to a pile of garbage and
  peck something out of it, without wearing the pile down.

### Changed
- **Bare hands no longer carry a pile away.** A Block of Garbage or Stone Rubble wants a shovel,
  Mechanical Waste wants a pickaxe, and a Compacted Bale wants the Scrap Knife. Any vanilla shovel
  or pickaxe does. Swing without one and the pile stays put and tells you what it wants. Sorting is
  untouched: every pile still picks through bare-handed at the same rate, so sorting is free and
  hauling is not. Trash Bags still come up by hand.
- **A Dirty Mattress is spent by sleeping on it.** It survives one night and breaks when you get up.
  Sneak-right-click to set spawn without burning it; setting spawn is not sleeping.
- **A pickaxe returns a Steel I-Beam** instead of destroying it, so a girder can be moved.
- **Leads are Rope and bundles are Luggage**, with new art. Searching JEI for "lead" or "bundle"
  still finds them.
- **Shift-clicking a craft no longer empties the Scrap Network.** One shift-click is one batch.
- FTB Chunks, FTB Library, and FTB Quests moved up a patch version each.

### Heads up if you already have a world
**Mound regrowth needs a new world.** The memory of what a mound was is written into the ground when
the world generates, so a save made before this update has none and its mounds stay finite. Nothing
breaks; the mounds simply do not come back.

Dirty Mattresses now wear out. Nothing breaks, but a mattress you were treating as a permanent bed
will be gone after one night.

## [0.3.0] - 2026-08-03

Teardown finally teaches you something. Recompile 0.5.0 brings blueprints, which is the idea the
whole pack was named after.

### Added
- **Blueprints.** Tearing anything down at the Recompile Workbench now gives you an Idea Fragment
  toward whatever that recipe teaches. Collect enough about one thing and they craft into a
  blueprint sheet, which unlocks the recipe at the Scrap Crafting Table. Every teardown counts;
  there is no chance roll.
- **The Filing Cabinet**, found in Bulky Waste. It stores sheets, condenses loose fragments on its
  own, and works from anywhere in your scrap cluster, so you do not carry sheets around.
- **The Hydroponics Bay.** Grows a crop from water and power with no soil. The crop you put in is
  never consumed, and a second slot catches byproducts. It is the first machine that spends power.
- **Recovered paintings.** Six real works turn up in Bulky Waste, and unlike vanilla paintings they
  keep which one they are when you break and replace them.
- **A proper title screen.** The pack wordmark replaces the Minecraft logo, with Discord and GitHub
  buttons in the corner.
- **A much fuller guidebook** - twelve systems that had no entry now have one, and the four
  multiblocks have 3D pages that project the build into the world in front of you.

### Changed
- **Water no longer spreads.** Two source blocks will not fill in a third, so every bucket you pour
  out is a bucket gone. The Rain Collector stays worth having.
- **Iron needs a Cupola Furnace.** Rebar and Steel Offcuts became blasting recipes, so an ordinary
  furnace will not smelt them any more.
- **Beds are made differently.** The wool-to-bed recipes are gone; a bed is a Clean Mattress plus
  three planks, and Clean Mattresses come from a blueprint. Coloured beds want the matching colour
  of mattress.
- **Roaches are far rarer** - about one per 128 blocks of garbage instead of one per 16.
- **Fertilizer speeds up crops and saplings** the way bone meal would, which matters because this
  world has no bone meal and cannot have any.

### Fixed
- **The pack's resource pack now loads at all.** It declared `pack_format` where Minecraft 26.1
  wants `min_format` and `max_format`, so the game rejected it on every launch and quietly removed
  it from your options. The Discord badge in the quest book has been a missing-texture square in
  every release that shipped it.
- Biomes have names again instead of showing `biome.recompile.household_sprawl`.

### Heads up if you already have a world
Three of these reach worlds made before this release: water stops spreading, iron stops smelting in
an ordinary furnace, and the old bed recipes disappear. Nothing breaks and nothing is lost - if you
are sleeping in a Dirty Mattress it keeps working - but if you were about to craft a vanilla bed you
will need to tear down Dirty Mattresses at the Workbench first.

## [0.2.0] - 2026-08-02

Power arrives, the world type is nailed down, and the quest book is no longer empty.

### Added
- **Spawn Detective** - point it at a block, pick a mob, and it tells you which rule is stopping that
  mob from spawning there: the mob cap, the light level, the floor, the biome's spawn list, the
  chunk not ticking, or another mod's veto. Useful once you start baiting animals onto reclaimed
  ground and one of them refuses to settle.
- **FTB Chunks** - a minimap, and chunk claiming for servers. The plain has no landmarks and the
  mounds grow back, so knowing where you have been is a real problem.
- **FTB Essentials** - `/home`, `/tpa`, and `/back`. `/back` picks up where GraveStone leaves off.
- **FTB Quests** and its dependencies (FTB Library, FTB Teams), plus a **Welcome** chapter with the
  Discord link. It is one page. The real quest line is not written yet, so the guidebook is still
  where progression is explained.
- **Power, and the tools that run on it** - Powah for generation and storage, then Building Gadgets,
  Charging Gadgets, Mining Gadgets, LaserIO, and Just Dire Things.

### Changed
- **New worlds are always the garbage world now.** The world type is fixed to Recompile's Garbage
  World and the world-type button is gone from world creation, so there is no way to start a normal
  Minecraft world by accident.

## [0.1.0] - 2026-08-02

First alpha. Recompile and the four mods it integrates with, on a garbage world, plus a
quality-of-life layer that stays out of the way.

### Added
- Minecraft 26.1.2 on NeoForge 26.1.2.94.
- **Recompile 0.4.0** - the garbage world, Blocks of Garbage and hand sorting, trash tools, the
  Sorting Tarp and Recompile Workbench, the Scrap Network, the Cupola Furnace and the demolition
  yard, water and food, the reclamation ladder from Grass Spreader through animals, collectibles,
  and the in-game guidebook.
- **Just Enough Items 29.21.0.66** - recipes, plus Recompile's Sorting, Cutting, and Prying
  categories.
- **Jade 26.1.8** - block tooltips, including which tool a block wants and how far a sort has got.
- **Modonomicon 2.2.0** - the engine the guidebook runs on. Without it the guide is inert data.
- **Pipez 1.2.31** - item, fluid, and energy pipes. Every Recompile block's automation behaviour is
  written and tested against it, so what connects and what refuses to connect is deliberate.

### Quality of life
- **Inventory and UI** - AppleSkin (food values on the HUD), Mouse Tweaks and Inventory Essentials
  (drag-move and bulk transfers), Controlling and Searchables (search the keybind list), Toast
  Control (mute advancement popups), Clumps (XP orbs merge instead of piling up).
- **Storage cleanup** - TrashSlot and Trash Cans, for the parts of the trash you actually do not want.
- **Performance** - FerriteCore and ModernFix (memory and load time), Lithium (tick optimisation),
  FastFurnace, FastWorkbench and FastSuite (recipe lookup caching), Sodium (rendering).
- **Death and safety** - GraveStone keeps your items and XP where you died. Simple Backups takes
  automatic world snapshots.
- **Extreme Sound Muffler** - mute individual sounds, globally or by radius.

### Known gaps
- Teardown returns materials, not recipes. Recovering the recipe off a torn-down item is the mod's
  main idea and is still being built.
- No quest book. The guidebook is the only progression guide.
- Drop rates, recipe costs, and teardown yields are first-pass numbers chosen to prove the
  mechanics, not balanced against play. Expect them to move.
