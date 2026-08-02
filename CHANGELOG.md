# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The `## [X.Y.Z]` headings are load-bearing: `.github/workflows/release.yml` regex-extracts the
matching section for the GitHub release notes and the CurseForge changelog. Keep the exact shape,
and ASCII punctuation only.

## [Unreleased]

### Added
- (nothing yet)

## [0.1.0] - 2026-08-02

First alpha. The pack is Recompile plus the four mods it integrates with, on a garbage world.

### Added
- Minecraft 26.1.2 on NeoForge 26.1.2.76.
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

### Known gaps
- Teardown returns materials, not recipes. Recovering the recipe off a torn-down item is the mod's
  main idea and is still being built.
- No quest book. The guidebook is the only progression guide.
- Drop rates, recipe costs, and teardown yields are first-pass numbers chosen to prove the
  mechanics, not balanced against play. Expect them to move.
