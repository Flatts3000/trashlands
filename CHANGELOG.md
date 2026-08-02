# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The `## [X.Y.Z]` headings are load-bearing: `.github/workflows/release.yml` regex-extracts the
matching section for the GitHub release notes and the CurseForge changelog. Keep the exact shape,
and ASCII punctuation only.

## [Unreleased]

### Added
- **Spawn Detective** - point it at a block, pick a mob, and it tells you which rule is stopping that
  mob from spawning there: the mob cap, the light level, the floor, the biome's spawn list, the
  chunk not ticking, or another mod's veto. Useful once you start baiting animals onto reclaimed
  ground and one of them refuses to settle.
- **FTB Chunks** - a minimap, and chunk claiming for servers. The plain has no landmarks and the
  mounds grow back, so knowing where you have been is a real problem.
- **FTB Essentials** - `/home`, `/tpa`, and `/back`. `/back` picks up where GraveStone leaves off.
- **FTB Quests** and its dependencies (FTB Library, FTB Teams) - the quest engine. **No quests are
  written yet**, so the book opens empty for now.

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
