# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

The `## [X.Y.Z]` headings are load-bearing: `.github/workflows/release.yml` regex-extracts the
matching section for the GitHub release notes and the CurseForge changelog. Keep the exact shape,
and ASCII punctuation only.

## [Unreleased]

### Added
- **Recompile 0.13.0**, which closes three things this world could not reach. The **Sintering Kiln**
  fires pressed powder back into a solid, and four blaze powder pressed and fired gives a blaze rod,
  so brewing no longer needs a fortress. A **Worn Forging Die** turns up in the depths and tears down
  into the netherite smithing template vanilla will only sell you a copy of. And **zombie villagers**
  now walk the demolition yard, so curing one is the only trade in the world and the only emeralds.
- **Easy Villagers.** Pick a villager up and carry it, check trades without opening the trading
  screen, and automate trading, breeding and curing with its own blocks. Getting a first villager is
  the hard part here and that has not changed: no villages generate in this world, so the route is
  curing a zombie villager, which wants a golden apple and a weakness potion. This makes what happens
  after that far less tedious.
- **Simple Magnets.** Items come to you instead of being walked over. Its recipes are the mod's own
  for now.
- **Storage and automation, all at once.** Sophisticated Backpacks and Storage, Functional Storage,
  Applied Energistics 2, Ender IO, Modular Routers, and Apotheosis for loot and enchanting.

## [0.8.0] - 2026-08-19

There is a Nether now, and it is a dump you mine rather than a place you cross.

### Added
- **The Nether is open** (Recompile 0.12.0). The compacted depths are solid from the bedrock floor to
  the bedrock ceiling, and you pick through techno-organic waste down there the same way you pick
  through a mound up here. Nothing vanilla generates in the rock. Netherrack, basalt, blackstone
  and both nyliums are crafted from shards you sort out of slag rubble, and soul sand and soul soil
  from clumps, so the dimension is somewhere to mine rather than somewhere to cross.
- **Obsidian, and so a portal.** The Cupola Furnace rakes off a lump of slag every eighth smelt, and
  the Slag Furnace vitrifies one lump into one block over a burn twice the length of a smelt. It is
  the only obsidian in this world, and those eight smelts are what it actually costs.
- **Coal.** Lignite comes out of the techno-organic waste down in the depths, and smelting it gives
  coal. That is the only route to coal in this world, so coal is a Nether material now. Lignite also
  burns on its own at half a coal, so it is worth something the moment you find it.

### Changed
- **Circuit Powder now costs one E-Scrap, not four.** Gold got four times cheaper in material, and
  the Pulverizer's time and power per operation are unchanged. A GUI-less machine cannot take four
  of anything: it has nothing to open, so a remainder is invisible and you never get it back, and
  the pull streams hand scrap out one item at a time, which makes a remainder the normal case.
- **Recompile 0.11.0 -> 0.12.0**, plus FTB Quests. Extreme Sound Muffler is deliberately held on
  3.58.1; its 4.x line is alpha.

## [0.7.0] - 2026-08-18

Something built, under the yard. And a server pack, so more than one of you can find it.

### Added
- **A dedicated server pack.** Every release now builds `trashlands-server-<version>.zip`, attaches
  it to the GitHub release, and uploads it to CurseForge alongside the client file. Unzip it, accept
  the EULA, run `setup.sh` or `setup.bat`, and it installs NeoForge and boots. It ships with
  `level-type=recompile:garbage` already set, which is the only thing that makes a server world this
  world rather than an ordinary one.
- **Sewers under the demolition yard** (Recompile 0.11.0). Brick corridors running downhill with a
  leachate channel down the middle, and the first place here that was built rather than dumped. The
  way in is a square of pale concrete with a rusted plate in it, and the plate comes up with a
  Prybar and nothing else.
- **The only slimes in the world** live down there. Both routes vanilla gives a slime need something
  this world does not have, so a slimeball had no source at all until now. Roaches live there too,
  rather than only turning up when a garbage block is disturbed, and there are turtles and frogs in
  dens of their own. A sewer's animals are the animals it was built with; they cannot breed there.
- **An access chamber with barrels** off one of the runs, holding scrap and sometimes a Bulb, a Pump,
  a Motor or a Machine Frame. It is somewhere you have to walk to rather than the room you arrive in.
- **An echo shard in the sump**, one per sewer and the only source of one here. It sits under standing
  leachate in the dark with a drowned spawner on the walkway, so the hazard the room already had is
  what guards it.
- **Suspicious sand and gravel in the silt.** Brush it and mostly you get silt, because that is what
  silt is, and now and then something that went down a drain a long time ago comes back. Mining a
  deposit gives nothing: brush it into ordinary sand or gravel first.

### Changed
- **The ground is deep now.** The world was a coarse-dirt slab 7 to 11 blocks thick over about 120
  blocks of nothing; it is 59 to 63 blocks thick, with bedrock still underneath and the void still
  below that. Nothing you can see or stand on changed. **It only affects newly generated land**, so an
  existing save keeps the thin slab in chunks it has already visited and will never hold a sewer
  there. The seam is visible where you walk into fresh chunks. A new world avoids both.
- **Leachate can drown you**, everywhere, including the surface pools out in the sprawl. It is checked
  at the eye, so one block deep is enough while crawling or swimming; walking through a pool is still
  fine. It still does no damage on contact and still leaves you hungry.
- **Ten mods are marked client-only** - Sodium, FancyMenu, Melody, Konkrete, Controlling, Searchables,
  Mouse Tweaks, Toast Control, Default World Type and Extreme Sound Muffler. No difference to a
  client install, which still gets all 47. It is what lets the server pack ship the 37 a server
  actually runs instead of handing it a rendering mod.
- **Recompile 0.10.0 -> 0.11.0**, plus JEI, FTB Quests and FTB XMod Compat.

### Fixed
- **A Water Tank, Solar Panel or Rain Collector Funnel placed on its own no longer vanishes when you
  break it.** The block you place and the block a formed machine uses are the same one for those
  three, and the rule that stops a formed machine dropping loose parts was taking them too. All three
  are on the Groundwork build path, so this was losable.
- **Turtles no longer suffocate in their own den.** A turtle is wider than the block it stands on and
  three were being placed a block apart, so they spawned inside each other and inside the walls.

## [0.6.0] - 2026-08-17

A third chapter, and the ground stops being something you only dig.

### Added
- **Groundwork**, a chapter about turning the dump back into land. Nineteen quests running the whole
  reclamation ladder: the Grass Spreader that greens coarse dirt and costs nothing to run, the
  Compost Heap and Fertilizer, farmland you craft because this world has no hoe, the Tree Nursery
  that is the only source of a sapling anywhere in the game, and the animal baits that put wildlife
  back on land that was garbage. It ends on a bait that seeds a breeding pair, so the herd keeps
  itself going.
- **The chapter is built around the fight rather than the machines.** Each rung answers the one
  before it. Grass reverts at the border, plants on the border are stripped instead of the soil
  under them, farmland has to stay wet or it goes back, and trees are the only thing that holds
  ground for good. Welcome has warned about this since v0.2.0; this is where it starts.
- **The Trommel** (Recompile 0.10.0). A four-block rotating drum in the demolition yard that sorts
  while you are elsewhere. It yields exactly what a Sorting Tarp yields per block, so what you buy
  is not throughput, it is not having to stand there. Drop scrap along it or park a container on it.
- **The Pulverizer.** A sealed steel box that grinds things finer. You cannot see inside it, which
  is the point of it, so the roof carries a hatch to show you where material goes in.
- **Gold, out of circuit boards.** Grind four E-Scrap to Circuit Powder and blast it in a Cupola
  Furnace. A tonne of boards carries more gold than a tonne of ore, which is why this world has none
  in the ground and plenty in the rubbish. Burning a board whole gets you nothing.
- **Clay, out of broken pots.** Crush a pottery sherd for grog, mix three with a Kitty Litter, and
  right-click the result on a water cauldron at the cost of a level. Sherds and cat litter turn up in
  the dump now. It unlocks 43 vanilla items: every brick, all sixteen terracotta, all sixteen glazed,
  the flower pot and the decorated pot.

### Changed
- **The Separator no longer sorts.** Feeding it a Block of Garbage, Trash Bag, Compacted Bale, Stone
  Rubble or Mechanical Waste does nothing; that job is the Trommel's. Everything else about the
  machine is unchanged and one you have already built keeps running. A shear shredder tears things
  apart, which is the opposite of telling them apart.
- **Recompile 0.9.0 -> 0.10.0**, plus JEI, Jade, Balm, GraveStone, FancyMenu and Trash Cans.

### Fixed
- **Breaking a machine gives back every part, including the machine itself.** Breaking a Separator or
  Trommel core with the wrong tool used to destroy it outright while breaking any other block of it
  handed it back, so the rule was opt-out and a wrong swing could cost you the build.
- **Breaking one cell returns the part you put in it.** A Separator's Motor came back as a Machine
  Frame, and a Trommel's cells came back as pieces with no recipe at all.
- **Machines wider than three blocks come apart properly.** A cell far enough from its core never
  found it, so the machine stayed assembled with a hole in it and kept running.
- The Trommel and Pulverizer accept energy from a generator at all, and the Trommel's drum stops
  turning when the machine is stopped.

## [0.5.0] - 2026-08-12

The quest book stops reading you recipes, and the dump starts handing you objects instead of ingredients.

### Added
- **Salvage teaches the Scrap Network.** The one thing about Recompile that nothing in the world
  tells you is that scrap blocks touching face to face are one system - no pipes, no wires, nothing
  to connect. Four quests now say it where you meet it: the Scrap Barrel catching what the Sorting
  Tarp throws, the Burn Barrel moving finished smelts across, the Workbench dropping teardown into
  the barrel instead of onto its own top, and the Scrap Crafting Table's right-hand panel listing
  what the whole network holds. Touching means sharing a face; a diagonal is a separate network.
- **A Fuel quest**, because "it needs fuel and there is no coal or wood here" was a sentence with
  nowhere to go. One Oily Rag burns as long as charcoal does, and Junk burns at two items a piece,
  which is worth knowing when you are standing in a pile of it.
- **The Dead Fridge** (Recompile 0.9.0). A two-block appliance in Bulky Waste that replaces the
  Broken Fan and the Light Fixture. Pry it open and it gives eight pieces of scrap, something out of
  the freezer, and exactly one of a motor, a pump or a bulb - and whichever you pull is the one you
  come away knowing. Its freezer is the only ice or snow in this world; nothing here snows and
  nothing freezes, so if you want either you go looking for fridges.
- **Leachate** (Recompile 0.8.0). Pools of runoff sit on the open ground between mounds. It looks
  like water and is not: it will not fill a Rain Collector, it will not water a crop, and standing
  in it makes you hungry.

### Changed
- **The quest book stopped reciting recipes.** Quests were listing ingredients JEI already shows -
  "eight Scrap Metal in a ring", "two Scrap Metal over two Fiber Scrap". They say what the block
  does now, and what it costs is left to the recipe viewer.
- **Found, not crafted** (Recompile 0.8.0 and 0.9.0). Anything a person would actually throw away
  comes out of the dump rather than a grid: buckets, bowls, shears, flint and steel, leads, name
  tags, paper, books, bundles, glass bottles and all four pieces of leather armour lost their
  recipes. Materials and what you build out of them are still yours to make. The rule is enforced at
  load rather than remembered.
- **Teardowns roll their materials.** A fridge does not hand over a fixed pile; it rolls eight times
  across metal, plastic and electronics, so no two come apart the same way. The Printer, the Washing
  Machine, the Dirty Mattress and the Hydroponics Bay all work this way now. Averages are unchanged.
  What was guaranteed stays guaranteed.
- **The pull streams are much rarer at the top end.** Buckets, shears, flint and steel and leads now
  turn up about every half hour each rather than every couple of minutes; name tags about hourly;
  collectibles 480 times rarer than they were. Bulk material - junk, scrap, plastic, glass shards -
  is untouched. The rates were derived from measured playtime rather than guessed.
- **One workstation, not three objects in a row.** The Scrap Crafting Table, the Sorting Tarp and the
  Teardown Workbench share a bench profile, so a lined-up Scrap Network cluster reads as one
  continuous work surface. Their tops run the full block width; there used to be a two-pixel gap.
- **Recompile 0.7.0 -> 0.9.0**, plus JEI, Modonomicon, Sodium and SuperMartijn642's Core Lib.

### Fixed
- **The bucket quest was reading odds off the wrong tree.** It taught three copper ingots into a
  bucket. There is no bucket recipe - vanilla's is switched off - and buckets come out of household
  garbage instead.
- **Copper is nuggets, not ingots.** Burning Scrap Metal returns one nugget per scrap, and the quest
  said nine of those make an ingot as though that were the goal. Nothing you can build early takes an
  ingot; the nuggets go to Copper Pipes.
- **The Rain Collector is two blocks.** The collector holds water but gathers none without the funnel
  stacked on top, and no quest said so.
- **The Pump is not the water gate, copper is.** The quest treated the found Pump as the wall, when
  the teardown also gives an idea toward the Pump - four of those and you can craft them outright, so
  the first washing machine is the only one you have to find.
- **Jade and JEI could not read a single teardown** in a packaged install (Recompile 0.9.0). They
  read the mod's own recipe files through a lookup that only worked on an unpacked folder, which is a
  development layout and not one any player has had. Salvage worked the whole time, so the only tell
  was every viewer quietly insisting your Dirty Mattress was worthless.
- **The Scrap Crafting Table could not see everything in a connected barrel.** The network reported
  at most eighteen distinct materials, fewer than one barrel holds, so a barrel of nineteen Rebar
  would report "Not in your inventory or any connected storage". The cap is gone and multiple barrels
  aggregate.

### Removed
- **The Broken Fan and the Light Fixture.** The Dead Fridge carries the weight both had between them.
  Any you have placed or stored are gone after the update - tear them down for their Motor and Bulb
  first if you want the value. Everything else in an existing world carries over, and the fridge only
  appears in Bulky Waste you have not opened yet.
- **Music discs from the pull streams.** A disc every couple of hours was not worth the slot.
- **Wool carpets from trash bags.** A rug you find every few minutes is not worth finding. Wool is
  still a bag pull, so you make carpets the ordinary way again.

## [0.4.0] - 2026-08-05

A quest book you can follow, and mounds that grow back.

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
