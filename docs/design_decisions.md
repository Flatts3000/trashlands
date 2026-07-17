# Design decisions log

Running log of locked per-feature decisions from the feature-by-feature walkthrough of [`feature_matrix.md`](feature_matrix.md). One section per feature, in walkthrough order. "Locked" means design intent is settled; everything still ships config-gated per the architecture principle.

---

## Walkthrough status (the bookmark - update every session)

**As of 2026-07-15:** P0 fully locked (P0.1-P0.5). P1 fully locked (P1.1-P1.11; food/foraging tier P1.9 and the sorting-tarp mechanic revision both added in a later 2026-07-14 session; water P1.10 and Bulky Waste P1.11 added 2026-07-15, the latter superseding P1.1's appliance row; building-blocks tier P1.12 added and shipped 2026-07-16). **P2 fully locked (P2.1-P2.8).** **The knowledge system (P1.4) is under review** - see the note at the head of P1.4; its enforcement model does not survive contact with modded autocrafting, and its scope is being questioned. Dimensions, the knowledge system, mound regrowth, the material economy ([`material_economy.md`](material_economy.md)), and the narrative layer ([`the_twist.md`](the_twist.md), spoilers) are locked. Mod lineup so far: Create (belts/logistics), Mekanism (chemical/radiation endgame). (Productive Frogs crossover dropped 2026-07-14.)

**Walkthrough is COMPLETE except the endgame/postgame cluster, which is PARKED (Jason's call, 2026-07-14) - worry about it later.**

P3 results: P3.2 Field Manual locked; P3.5 Nether, P3.6 End DONE; P3.1 sky dumps, P3.3 degraded recipes, P3.4 blueprint scraps, P3.7 frogs, P3.8 win-tracking, P3.9 circular-economy all CUT.

**Parked for a future session (do not resume until Jason reopens):**
1. **Endgame redesign** - circular economy cut (P3.9); needs a new mechanical endgame that leads into the Overworld Gate and resolves quarry-vs-heal affordability. Three seed directions captured in chat: Gate-as-megaproject (throughput), Gate-as-one-of-everything (completion), Gate-as-power-problem (energy). Not chosen.
2. **The final chapter / postgame** - narrative frame + staged payoff, authored against the_twist.md. Depends on the endgame being chosen first.

Everything upstream of the endgame (P0, P1, P2, the material economy, dimensions, knowledge, regrowth, the twist framing) is locked and ready to prototype.

**Open threads not on the matrix:** pack name (working: Trashlands), Nether theme name ("compacted depths" placeholder), the quest-narrator question (who wrote the quest book - see the_twist.md), where construction rubble lives (see material_economy.md).

**Governing principle - minimize authored prose (2026-07-14):** only two sanctioned writing surfaces - quests (quest-voice skill) and technical guidance (terse, functional). No ambient lore documents, archivist notes, or readable flavor text. Players distrust AI writing; every prose surface is a liability. Carry meaning through environment and mechanics, not writing.

---

## P0.1 - Custom world preset (locked 2026-07-13)

1. **Vertical profile:** a few layers of coarse dirt, then several layers of deepslate, then a single bedrock layer. Solid all the way down - no caves, no voids, no ores. Digging down is pointless by design and the player discovers it fast.
2. **Terrain:** gently rolling, low-amplitude noise. Reads as buried plains, not a debug superflat.
3. **Water:** scattered pools of leachate (murky, mildly harmful, later a chemical-tier input). Clean water is made, not found.
4. **Mobs:** peaceful biomes and hostile biomes - hostility is a regional property, so safety is geography (starter regions calm, deeper regions dangerous). Vanilla mobs only for now; custom mobs possible later.

## P0.2 - Garbage surface layer (locked 2026-07-13)

1. **No continuous burial.** The overworld is an endless coarse-dirt plain crowded with garbage mounds - no garbage sheet covering everything. Walkable from minute one; "clearing" means removing mounds, which makes progress crisp and countable.
2. **Mounds vary in height and width.** Short flat spreads and tall trash hills both generate. Density tunable via config; default dense enough that mounds crowd the horizon.
3. **Stratification is by biome, not depth.** Garbage composition varies by region (the garbage-regions system), not by loose-on-top/compacted-below layering.
4. **Buried surprises: yes.** Wanted; catalog below is candidates, not locked. Surprises live mostly inside mounds so every dig has slot-machine potential.

### Buried-surprise candidates (brainstorm 2026-07-13)

- **Loot pinatas:** appliances (fridge = preserved food, early food source; washer, stove - prybar targets), crushed cars (metal + battery chance), tire stacks, pipe bundles, wire spools.
- **Knowledge caches:** filing cabinets / briefcases (drop schematic items), dead computers and TVs (e-waste + data recovery), time capsules (rare; a guaranteed full schematic). Caches drop whole schematics (P1.4.C), an alternative to studying the item yourself.
- **Utility finds:** broken machines repairable into working ones (find-and-fix beats craft for the fantasy - your first furnace might be excavated), dumpsters as working storage, mattresses as field respawn points.
- **Hazards:** rusty chemical-waste barrels (leak if broken carelessly, but are chemical-tier inputs), pocketed garbage gas (fire/poison puff on careless digging).
- **Lore set-dressing:** buried road segments, street lamps, bus stops, signage - the old world's skeleton.

## P0.3 - The Block of Garbage (locked 2026-07-14)

1. **Drops itself.** The block is the unit of mixed trash: carry it, stack it, build with it (trash walls as first shelter), feed it whole into sorting stations. Loose mixed-trash items still exist (from bags, loot) but the block stays whole when dug.
2. **Hand-breakable but slow; shovel-class fast.** Zero-barrier start. Tougher variants needing prybar/knife arrive in P1.
3. **Gravity on, config-gated.** Gravel-style falling. Mounds slump when quarried; digging into a tall mound's base can bury you. Ties into mound regrowth (same falling-block behavior).
4. **One block, randomized texture/model variants** (protruding bag, jutting pipe, compressed face) so mounds read as heterogeneous junk without multiplying block IDs. Region palettes come with the regions system.

## P0.4 - Mixed trash and hand-sorting (locked 2026-07-14)

1. **Tier-zero sorting = picking through a placed block.** Right-click a placed garbage block with an empty hand; each pull yields one drop from its table; after 4-6 pulls the block is exhausted and crumbles. No UI, no station. The Sorting Tarp (P1) is the batch version, machines the automated version - same verb at three speeds.
2. **Base material vocabulary (7):** scrap metal, plastic scrap, glass shards, organic muck, fiber scrap, e-scrap (rare), junk (filler majority). Every machine tier speaks this language; keep the set small and stable.
3. **Junk is fuel, not worthless.** Burns poorly, compacts back into buildable trash blocks. Nothing is worthless; some things are barely worth anything - the pack's moral stance as an item.
4. **Region-weighted pull tables from day one.** JSON per region; slice ships one (household). Scrapyard skews metal, e-waste skews e-scrap - regions gate materials.

## P0.5 - Teardown table schema (locked 2026-07-14)

1. **Two systems, two formats.** Garbage-block pulls use vanilla loot tables (free tooling, modder familiarity). Teardown gets a custom recipe type (`recompile:teardown`). One format is not forced to do both jobs.
2. **Output shape: fixed core + weighted extras.** Deterministic bones (plan an economy around it) plus chance-weighted bonuses (stays interesting).
3. **`teaches` field in the schema from day one** even though the knowledge mechanic is P1: recipe(s) revealed, chance, `scraps_required` = how many teardowns of the item complete the study (P1.4.B deterministic study points; NOT a fragment/blueprint-scrap system - that was cut). The distinct axis is not retrofitted into a shipped schema.
4. **`station` field for tier gating** (hand / tarp / machine / advanced) - one format covers the whole progression; pack authors gate cross-mod teardowns with one string.

Reference sketch:

```json
{
  "type": "recompile:teardown",
  "input": "minecraft:iron_door",
  "station": "recompile:workbench",
  "results": [ { "item": "recompile:scrap_metal", "count": 2 } ],
  "extras": [ { "item": "recompile:hinge", "chance": 0.35 } ],
  "teaches": [ { "recipe": "minecraft:iron_door", "chance": 0.25, "scraps_required": 3 } ]
}
```

**P0 is now fully specified.** Slice = world preset (P0.1) + mounds (P0.2) + one garbage block (P0.3) + pick-through sorting with one household loot table (P0.4) + one teardown table proving the data pipeline (P0.5).

## P1.1 + P1.2 - Block variants and trash-tier tools (locked 2026-07-14)

Variants and tools are one interlocking matrix:

| Block | Tool to open efficiently | Character |
|---|---|---|
| Garbage (P0 block) | Hands slow, shovel fast | The bulk commodity |
| Trash bags | Hands, instantly | Soft surface litter; quick small pulls |
| Compacted bale | Scrap knife (cut strapping) | Dense; 2-3x the pulls of a garbage block |
| ~~Appliance~~ | ~~Prybar~~ | **DROPPED 2026-07-15 - replaced by Bulky Waste (P1.11). Not rolled in: deleted.** |

1. **Starter tool trio from tier-zero materials:** scrap knife (bales, fiber), prybar (**Bulky Waste**, weak weapon; also the Scrap Barrel's mining tool), junk shovel (digs garbage fast). No pickaxe in the starter set - nothing to mine, and its absence tells the player that.
2. **Rebar is the universal handle** (drops from scrap-metal pulls). Wood recovery stays a mid-tier treasure, not a tool gate.
3. **Bags/bales feed sorting (random pulls); Bulky Waste feeds teardown.** *(Amended 2026-07-15: this said "appliances feed teardown ... appliances are the on-ramp to the knowledge system". The appliance is dropped and P1.4 is under review, so the on-ramp is whatever Bulky Waste turns out to hold.)*
4. **Generation:** bags on mound surfaces, bales in mound cores (mound shape does the depth-reward work), **Bulky Waste an uncommon pocket find** (inheriting the appliance's playtested 5% - see P1.11). Region palettes reweight all three.

## P1.3 - Sorting Tarp (locked 2026-07-14; mechanic revised 2026-07-14 - see revision below)

The batch tier of the sorting verb, designed with sifting's (Ex Nihilo lineage) lessons baked in:

1. **Form:** single flat block, tarp-with-junk-heap model. No multiblock ceremony at tier one.
2. **Interaction:** small UI (input slots for garbage/bags/bales, outputs accumulate) - the interface pattern later machines inherit. **Hold-to-sort, never click-spam** (sieving's RSI lesson, fixed preemptively). One operation sorts one whole block vs 4-6 hand pulls.
3. **Screen slot (mesh-tier lesson):** screens change *what*, not *how much* - a metal screen skews pulls toward scrap metal, an organics screen toward muck. Player-chosen filtering, no raw-value inflation; richer odds stay the machine tier's selling point.
4. **Bales batch (compression lesson):** sorting a bale is one operation yielding 2-3 blocks' worth. Knife -> bale pipeline is the anti-tedium upgrade.
5. **Recipe:** fiber scrap + rebar, pure tier-zero, buildable in the first 15 minutes.
6. **Drop tables visible in JEI/EMI from day one.** Non-negotiable. *(Shipped 2026-07-16, JEI: Sorting/Cutting/Prying categories + the Scrap Crafting Table as the crafting station, plus Jade tool-hint and sort-progress tooltips. Reads bundled pull-table JSON, since loot tables are not client-synced - a datapack retune is not reflected in JEI, and remote-server pulls fall back to the mod defaults. EMI not wired; teardown JEI is still a Phase 3 item.)*
7. **In-world charm:** the junk heap on the tarp visibly shrinks as you sort.
8. **Hopper compatibility off at this tier** (config-gated) - the tarp is manual by identity.

**Revised 2026-07-14 - sieve-free, no-GUI, world-drop, no screen (supersedes points 1, 2, 3, 7; sharpens 8):**

Two problems surfaced walking the concept: a mesh "sieve/screen" is the wrong real-world tool (sieves separate *fine* material by size - soil, ash; coarse mixed trash is hand-picked by material into sacks, never sieved), and any internal inventory is an automation surface that fights "manual by identity." The revised design:

1. **Form: a jury-rigged sorting TABLE, not a flat tarp and not a sieve.** Waist-height, custom model + `VoxelShape`: a salvaged frame (crates / drums / bent rebar) with a worn tarp thrown over the top as the work surface, mixed junk spread on it, ringed by the mouths of striped woven-polypropylene bulk sacks - the iconic object of informal recycling, and welcome color against the muted palette. Keeps the "tarp" name/id (the tarp *is* the tabletop). Explicitly not a sieve: coarse trash is hand-sorted in real life.
2. **Interaction: no GUI, no inventory.** Right-click holding a garbage block / bag / bale -> sift one batch -> sorted materials **drop into the world as item entities** (bales still batch 2-3x, point 4). Hold right-click to keep sifting. There is **no input slot, no output buffer, and no screen slot** - the block is stateless. The sorting act itself is the manual gate; collecting the drops is the player's logistics problem (the Create seam, ~line 175). Hopper-proof by construction, which promotes point 8's config-gated "manual" into a structural guarantee. Deletes the menu/screen GUI classes the first cut carried.
3. **Screen dropped entirely (supersedes point 3).** With no sieve there is nothing for a screen to mesh, and any held-item slot reintroduces an automation surface. Player-chosen *what-you-recover* bias moves to a later tier (the powered sorter, or a possible magnet mechanic) - not the tarp. The `metal_screen` / `organics_screen` items are removed.

**Recovery ladder (tuned 2026-07-15, in play):** the pull table says what is *in* a block; **the method decides how much of it you get out**. The ladder is **hand << tarp << automation**, and the lever is rolls per block, so retuning a table moves every tier together. First playtest exposed the ladder inverted: hand pulls averaged 4.9 / 2.5 / 6.9 (garbage / bag / bale) against a tarp giving 5 / 2 / 12, so the tarp was a wash on garbage blocks and *strictly worse* on bags - the station you crafted was a downgrade, and materials arrived far too fast. Now hand averages **1.9 / 1.5 / 2.9** against a tarp of **5 / 3 / 8**, a consistent **2.0-2.8x**. Hand must stay visibly worse: it needs no station, no hauling, and no cooldown. Automation must clear the tarp by a similar margin when it lands, so the tarp is deliberately not maxed out. (Averages are expected pulls over the crumble curve, not the max.)

## P1.4 - Recompile Workbench + teardown-as-knowledge (locked 2026-07-14; UNDER REVIEW 2026-07-15)

> **Under review - do not build against this section yet.** Nothing below is retracted, but two problems surfaced walking it before implementation, and the second is the serious one.
>
> **1. The gate is at the wrong layer, and it cannot be fixed by effort.** The locked plan leans on `doLimitedCrafting` + recipe-book grants. That is real and it works - verified in the 26.1.2 source: `CraftingMenu.slotChangedCraftingGrid` only assembles a result if `resultSlots.setRecipeUsed(serverPlayer, recipe)` passes, which returns false when the rule is on and the player has not learned it. But look at the signature: `setRecipeUsed(**ServerPlayer**, ...)`. The gate is **player-scoped**, bolted on at the menu layer. A machine has no player, so Create's mechanical crafters, AE2 and Refined Storage do not bypass it by oversight - that gate structurally cannot see them. Create is in this pack's lineup, so the hole is real, not theoretical.
>
> One layer down, `Recipe.matches(input, **Level**)` takes no player, and *every* crafting system resolves through `RecipeManager.getRecipeFor(type, input, level)` -> `matches`. So a custom `CraftingRecipe` (still `RecipeType.CRAFTING`, so it works in every grid) checking **world/team** knowledge in `matches` would be obeyed by all of them, with no mixins. **The catch: that requires knowledge to be world/team state, never per-player** - point D's per-player config and an enforceable gate are the same problem wearing two hats. (Unverified: AE2 caches encoded patterns and may replay `assemble` without re-matching.)
>
> **2. The scope is the actual problem.** "The arc of the pack is moving the whole catalog across that line" is what generates every symptom: the authoring burden, the JEI greying, the artifact flood (sorting pays doors long after you have learned doors), and the leak mattering at all. Planet Crafter and Palworld - the reference points for this feel - gate a **curated spine of tens of nodes**, not every recipe in the game. Meanwhile this world already gates materials harder than any pack alive: **no ore, no wood, no coal**. No autocrafter can conjure matter. Material scarcity is the robust gate and it is already built; knowledge does not need to be DRM on ten thousand recipes.
>
> **The open identity question.** A first-principles pass (a real person in an infinite dump) suggests the sharper axis: in an infinite dump **materials are worthless and function is precious**. There is infinite scrap; there is not an infinite supply of *working motors*. That reframes teardown as recovering **function**, not recipes - you tear down a washing machine for the motor, which is a thing you cannot forge from any amount of scrap. It also makes sorting a **search engine** rather than a factory, and it needs no gating machinery at all, because "do you have a motor" is the most mod-proof gate there is. Whether the mod's axis stays **teardown-as-knowledge** or becomes **teardown-as-function** is unresolved, and the mod is named for the first one.



1. **It's a workbench, not a machine.** Player-operated, hold-to-disassemble with progress bar (mirrors hold-to-sort). Powered automated disassembler is a tier-3+ upgrade - same ladder shape as sorting.
2. **Tool rack:** 2-3 tool slots; racked tools (knife, prybar, later screwdriver/shears/torch) decide speed and which `extras` can drop. Tools matter at the bench, not just in the field.
3. **No teardown table = bench rejects it** ("no salvage value"); JEI makes supported items browsable. Config fallback (default off): unknown items shred to junk.

### The knowledge system (locked 2026-07-14)

- **A. Lock scope: survival free, technology locked.** Trash tools, tarp, torches, shelter craftable from minute one; furnaces, machines, redstone and up are locked until learned. "You remember how to survive; you've forgotten how to build a civilization."
- **B. Deterministic study points; chance is only acceleration.** Each teardown advances that recipe (1/3, 2/3, learned); lucky insights grant double progress. No bad-streak misery; `scraps_required` models the threshold.
- **C. Knowledge is a physical schematic item.** Study completion makes the bench emit a schematic; right-click to learn permanently. Tradeable between players, storable (library showcase), and the SAME item knowledge caches drop (filing cabinets, time capsules) - one knowledge currency, two sources: study or excavate.
- **D. Team-shared by default** (FTB Teams), per-player via config.

**What learning means practically:** vanilla `doLimitedCrafting` + recipe book grants gate the crafting table; unlearned recipes produce nothing even with correct materials; JEI shows them greyed with the unlock hint ("salvage X to study this"). Learning migrates an item from the found economy (finite, scavenged) to the made economy (infinite, manufactured) - the arc of the pack is moving the whole catalog across that line. Tuning rule: found items must be common enough that studying never feels like burning your only copy.

## P1.5 - Garbage regions (locked 2026-07-14)

1. **Real biomes, not an overlay.** Hostility-by-region (P0.1) lives on biome spawn rules; biomes also buy tinting, ambience, structure placement, F3 debuggability, and biome-aware mod compat for free.
2. **Launch trio: household sprawl (peaceful; fiber/plastic/organics), scrapyard (mildly hostile; metal, appliance-dense), e-waste dump (hostile; the precious chain).** Two regions can't show a gradient. Slag field + hazmat quarantine in P2, hazmat last (its identity is the hard gate).
3. **Distance-banded distribution.** Spawn is always household; scrapyard within walking distance; e-waste further; slag/hazmat beyond a threshold. The map is the difficulty curve. Band radii config-tunable.
4. **One region = one datapack bundle** (mound density/silhouette, block mix, pull tables, mob rules, palette/fog, surprise table). Adding a region is a content afternoon, not code.
5. **Region identity readable from the horizon** - silhouette and palette do the telling. The art bar.
6. **Biome-specific garbage blocks** (amends P0.3.4): each region has its own garbage block with its own textures and pull table. The drop table travels with the BLOCK, not the biome - haul e-waste blocks home and they still pull e-scrap. Region gating stays (you went there to get them); processing is location-free. Randomized texture variants apply within each region's block; the P0 slice block is the household one.

## P1.6 + P1.7 - Mound regrowth + healed-land immunity (locked 2026-07-14)

**Supersedes the "garbage keeps coming / race against the tide" pressure loop.** Trash is never impending doom.

1. **Mounds regrow toward their original size and footprint - never beyond.** A mound is a renewable quarry; the mechanic exists so you never have to relocate for materials. No unbounded accretion, no new-mound seeding on cleared land.
2. **Regrowth only fills exposed coarse dirt within the original bounds.** Grass and any built/placed blocks stop it. Kill a mound, grass its footprint, and it is retired forever.
3. **The core tension this creates (locked):** a regrowing mound is income; healed land is permanent but retires that income. Healing the world shrinks your garbage economy, so full reclamation must become affordable somehow before the endgame - the mechanism that resolves this is OPEN (the circular economy that was going to carry it is cut; see P3.9). The tension itself stands. Endgame thesis: not "you beat the tide" but "you no longer need the dump."
4. **Trash wind and sky dumps demoted to optional flavor/farmable events** (config, conservative defaults; never threaten builds or cleared land). Wind = ambience + small scatter near existing mounds at most; dumps = opt-in late-game deliveries.
5. **Regrowth rate config-exposed;** default slow enough to feel like recovery, not respawn (visible across sessions, not minutes).
6. **Delivery: blocks fall from the top of the world,** as if deorbiting from space - falling-block entities spawn high above the mound and rain into place. Visible from afar (you can see which mounds are replenishing), reuses the garbage-block gravity from P0.3, and ties the lore together: the void-dumped garbage is still coming home.

## P1.8 - Dimension lockout (locked 2026-07-14)

Nether and End portals disabled by config default until each themed dimension ships. Decided within the Dimensions discussion below; nothing further to design here.

## P1.9 - Food, foraging, and the dead dump (locked 2026-07-14)

Minecraft ships a hunger bar, so the player will eat; the question is *what*, on a dead garbage plain with no farms or animals. This tier answers it **without** becoming a survival-pressure pack (see `concept.md` "not hunger bars") - food is provided and thematic, never weaponized as a grind. Water stays a resource / purification thread, **not** a thirst meter (a hardcore thirst toggle is a config option only, default off).

1. **The initial biome has NO ambient creature spawns - on purpose.** A silent garbage plain sells "dead world," and it makes the reclamation payoff land: the first animal, the first birdsong, the returning villagers all hit *because* their absence is the entire early game. So early food is forage + scavenge, never hunting. (Livestock and crops return only on healed land - the P2.4 payoff.) Vanilla mobs were considered and rejected: chickens read wrong (not gulls), spiders aren't edible - nothing fits, and nothing should yet.

2. **Scavenge - tin cans (the risk staple).** Cans drop from the sort / pull tables (garbage and bags). *(Amended 2026-07-15: "and especially appliances - the fridge = preserved food note in P0.3" is dropped with the appliance. If a fridge ever lands as a Bulky Waste line, preserved food comes back with it.)* A can is **sealed (closed model) -> opened (open model)**; opening is a deliberate step (via the scrap knife - ties a tool to food). **An opened can behaves like Suspicious Stew:** a random effect on eating, so every can is a gamble. That IS the "eating sketchy food out of a dump" beat, mechanical not narrated. Suspicious Stew's own risk moves onto cans; clean cooked food is the safe upgrade you earn.

3. **Forage - a first-party edible mushroom.** Fungi are the decomposers of a waste world. **Vanilla mushrooms are not edible raw** (and stew needs a bowl - no wood here), and globally patching vanilla food via `ModifyDefaultComponentsEvent` would leak into any world that loads Recompile - a bad standalone-mod smell. So ship our **own `dump_mushroom`**: a plant block whose item is both placeable *and* edible (low nutrition - the humble staple; the *risk* lives on cans, not here). It grows on **patches of plain vanilla `minecraft:mycelium` between mounds** - a growing substrate that lives in the terrain, not a portable resource (mycelium needs Silk Touch, so it is not a casual pickup). Worldgen scatters the patches + mushrooms; vanilla mushrooms are left untouched. Early food is limited and in-place. *(Revised 2026-07-15: a bespoke `garbage_mycelium` / `spore_crust` block was built and then removed - vanilla mycelium already reads as fungal crust and is safe here, because it only spreads onto plain `minecraft:dirt` and this world's surface is coarse dirt, so a patch stays a patch. First-party is for what vanilla lacks; the mushroom is the part vanilla lacks.)*

4. **Farm - a first-party planter, gated behind knowledge. DEFERRED (2026-07-14).** Drop Botany Pots; build a first-party **scrap planter** as the hero growing item. Its recipe is **recovered through teardown-as-knowledge (P1.4), not craftable from minute one** - food progression hangs off the spine. Substrate comes from **`organic_muck` -> compost**, which finally gives that sorted material a job and makes farmed food a *processing output* (fits the recycling identity), not just loot. Farmed mushrooms -> mushroom stew, the reliable staple once you can grow. **Deferred until the P1.4 knowledge system exists** so the gating is real rather than a stopgap recipe; compost + substrate come with it.

5. **Roaches - infestation, not spawns. DEFERRED (2026-07-14).** A silverfish reskin, but do NOT ambient-spawn them (that fights the dead-quiet). Reuse silverfish's real mechanic: some garbage blocks are **infested** - break one and roaches swarm out. Tension and a gamble on certain blocks; vermin, not food. Not in the first build. **Wrinkle to solve when it lands:** an infested garbage block must look **slightly** different from a regular one - a subtle visual tell - so the gamble is fair-play, not invisible (and not so obvious it reads as a separate block).

**The food arc mirrors the game:** forage wild mushrooms + scavenge risky cans (survive) -> recover the planter recipe, compost muck, farm mushrooms (stabilize) -> reclaimed land brings livestock and crops back (payoff). Food heals as the world heals.

**Ownership:** Recompile owns the tin-can items (sealed/opened, suspicious-stew effects), the `dump_mushroom` plant + item, the scrap planter + muck-compost substrate, and the infested-block/roach behavior. The **mycelium substrate is vanilla**, and vanilla's own mushrooms are left untouched. Reclaimed farming is the pack's job at the P2.4 payoff.

**Build status (2026-07-15):** the **survive** tier is **shipped** - tin cans (scavenged risk food) + dump mushrooms foraged from vanilla-mycelium patches. Mushroom density was tuned down ~5x after the first playtest (patches/chunk x patch area x per-cell chance compounded to ~38 per chunk, a mushroom field rather than a scavenge; now ~7). The **stabilize** tier (scrap planter + muck compost, point 4) is deferred until the P1.4 knowledge system, and roaches / infested blocks (point 5) are deferred - both recorded above.

## P1.10 - Water (locked 2026-07-15)

Water was a footnote under P1.9 ("a resource / purification thread, not a thirst meter"). It earns its own block because of a fact nobody had checked: **this world contains no water at all.**

1. **Verified 2026-07-15, in the shipped worldgen:** `noise_settings/garbage.json` sets `sea_level: -64` and `default_fluid: minecraft:air`. There is no ocean, no lake, no spring, nothing to put a bucket in. Meanwhile `household_sprawl` sets `has_precipitation: true` (downfall 0.4) - **it rains.** So rain is not *a* source of water. It is the **only** one, and until something collects it, water does not exist in this game.

2. **Water is NOT a survival mechanic. This is not reopened.** No thirst bar, no drinking (see `concept.md` "not hunger bars"; the hardcore thirst toggle stays a config option, default off). Water is a **processing input** - a thing you need to make other things work, never a meter you nurse.

3. **First water comes from a rain collector** - improvised, pre-iron: a scrap frame with a tarp stretched over it, filling when it rains. It borrows the sorting table's visual language on purpose; both are the same real object, a tarp on a salvaged frame.

4. **The ladder is already half vanilla.** `LayeredCauldronBlock.handlePrecipitation` means a vanilla cauldron *already* fills from rain, and a cauldron is 7 iron ingots - reachable only once you can smelt scrap. So:

   **rain collector** (scrap + tarp, pre-iron, slow) -> **cauldron** (vanilla, iron) -> **pumps** (machines, much later).

   Improvised -> found -> made. That is the same arc as the mattress (found mattress -> string -> a real bed) and the burn barrel (burn barrel -> repaired furnace). Three independent systems landing on the same shape is the pack's spine showing.

5. **Do not ship the collector before something drinks it.** Nothing in the mod consumes water today, so a rain collector now is a block with no job - exactly what the anti-bloat rule exists to stop. It lands *with* its first consumer.

6. **The first consumer should be washing salvage, not farmland.** Rinsing sorted plastic before it is worth anything is a real step in informal recycling - the same world the sorting table already borrows from. Water as the thing that turns dirty scrap into good scrap is native to this pack in a way that hydrating farmland is not. Farmland (the P1.9 planter tier) and Create/Mekanism are later consumers, not the first.

**Ownership:** Recompile owns the rain collector. The cauldron and every fluid above it are vanilla and the mods' own.

**Amendment (shipped 2026-07-16):** point 5 was overridden by the owner - the Rain Collector **ships standalone**, not gated on a consumer. Its job is producing **water bottles** (glass bottle in -> water bottle out) plus bucket/pipe transfer; washing salvage (point 6) stays the intended first *processing* consumer but is decoupled from shipping the block. It was built as a **real fluid tank** (26.1's new transfer `ResourceHandler` API, water-only), so it already plugs into the pump end of the ladder - and it is a 1x2x1 structure (solid base holding the tank + a draped tarp catching the rain). Open thread carried forward: water bottles have no vanilla consumer yet in this pack (brewing/thirst gated), so a downstream for water (washing, concrete-mixing, etc.) still needs picking.

## P1.11 - Bulky Waste (locked 2026-07-15)

**One block: something big is buried here. Break it to find out what.** Named for the real thing - municipalities run "bulky waste collection" for exactly this category, the stuff too big for the bag, and every single thing we want inside it (mattress, fridge, sofa, car panel) is literally bulky waste. It borrows the same informal-recycling vocabulary as the sorting table and the bulk sacks.

**Why this one survived every argument:** it is the first thing in the mod that is a **tell** - something you can *see* and *choose*, rather than a random number you wait on. It is the only idea on the table that passes the test in `concept.md` ("Why sifting garbage is fun"): the player is the filter, not the RNG. Everything below follows from protecting that.

1. **The appliance is DROPPED, not rolled in (supersedes the P1.1 appliance row).** "Known find vs unknown find" was a distinction that could not answer *why one bulky object gets its own block and the others do not* - and once that fell, the appliance had nothing left. It was a **vague abstraction sitting between the player and a specific thing**: "an appliance" is not a fridge or a washer or a motor, it is a placeholder for one. Bulky Waste drops concrete objects, so the placeholder has no job. The block, the item, and `appliance_end`/`appliance_side` (approved earlier the same day) all go. Its 5% worldgen slot is inherited by Bulky Waste, and P0.3's "mining also drops the appliance, so it can be relocated whole" dies with it.

   *(Fridges, washers and stoves are not gone as **fiction** - they are candidate lines in the Bulky Waste table, alongside the rest of the P0.3 buried-surprise brainstorm. What is gone is a generic item pretending to be all of them.)*

   **The table ships with exactly one entry: the mattress.** It gets populated as we go, which is the entire point of the design - a find is a table line. Shipping a one-entry table is not a stub, it is the system working.

2. **Sorting yields small things; digging yields big things.** Small manufactured stuff comes out of the pull tables, where you are picking through loose trash. Bulky stuff comes out of the ground, because that is where bulky stuff is. This also fixes a believability gap: pulling a mattress out of a 1m3 compressed cube is odd; digging out the corner of something big is exactly what a dump looks like.

3. **No worldgen seeding system is needed, and this is the point.** Worldgen only ever places **one block type**. The find does not become a mattress or an engine until it is an **item in your hand**, so there are no per-find world models, no structure templates, no multi-block placement, and no entity question. **Adding a find is a loot-table line.** This is what P1.5.4's "content afternoon, not code" actually looks like.

4. **Two rarity dials, and they do different jobs.**
   - **Block frequency** = how often the *"something big is buried here"* beat fires.
   - **Loot-table weights** = *which* thing it turns out to be.

   The rarity of any given find is the **product**. So set the block by how often you want the *moment*, and put all the real rarity in the table. **Do not touch worldgen:** the appliance's existing 5% core chance is already playtested as "an uncommon pocket find" - measured 2026-07-15 at ~2.41 per mound, ~12 per chunk, against ~48.5 core-eligible cells per mound. Most mounds have a couple, so tearing into one pays off. The mattress is a *slice* of that 5%, not a new worldgen number.

5. **The invariant: nothing enters the found economy without a teardown exit. Finds in, materials out.** If that holds, quantity stops mattering: 1,000 mattresses is 4,000 string, 1,000 doors is 2,000 scrap. A pile is not clutter, it is **unprocessed inventory** - which is what a scrapyard is. This retires two systems designed earlier the same day: knowledge-aware "curriculum" loot (which needed the player in the loot context, and an answer to "what does a machine know?"), and blueprints-as-flood-control (they may still exist, but they are no longer load-bearing).
   - **Enforce it at load.** A startup check that every item reachable from a finds table has a `recompile:teardown` recipe, failing loudly. Otherwise the invariant is a comment, someone adds a find with no exit, and the flood quietly returns.
   - **The exit must exist first.** The workbench is P1.4 and under review, so general finds wait for it. **The mattress is the exception** and can ship now: its exit is "break the placed block for string", which needs no bench.
   - **Known tension (see `concept.md` Open questions):** this rule fixes the flood and *also* flattens judgment. If every object is worth grabbing, there is no decision. It stands until "is sifting the price or the game?" is answered.

6. **Finds are blocks, never entities.** Settled on three independent grounds: **sleep is block-addressed** (`startSleepInBed(BlockPos)`, and `ServerPlayer` sets respawn from that same pos - an entity has no address in that system, so an entity mattress means reimplementing sleep and respawn validation); **gravity** (garbage blocks are `FallingBlock`s and mounds slump when quarried - an entity would hang in the air while the pile collapsed out from under it, so the objects in the world would stop obeying the world); and **rendering at dump scale** (5 mounds/chunk x ~3 finds = ~15/chunk, so ~6,600 entities in view at a 21-chunk render distance; blocks bake into the chunk mesh and cost nothing marginal).
   - **The rule is stricter than "block not entity": baked JSON model, no BlockEntityRenderer.** A BER is a per-object draw call - exactly what we are avoiding. BlockEntities are fine when the block must *hold* something (the Scrap Barrel), never for rendering. (Verified 2026-07-15: in 26.1 `BaseEntityBlock` no longer forces `RenderShape.INVISIBLE` as it did in older versions, so a BE block renders from its model for free. Two versions ago the barrel would have been invisible.)
   - **What we give up:** blockstates rotate models in 90-degree steps only, so no mattress flopped at 37 degrees. Chaos comes from **random model variants** instead - `garbage_block` already does this free (3 models x 4 rotations, picked per position by the blockstate).

7. **Multi-block finds use the vanilla bed trick, not entities.** A mattress is longer than one block; vanilla solved that for beds with two blocks (`FACING` + `PART`). That buys the silhouette, real sleep, real spawn and real gravity with zero surgery.

**Ownership:** Recompile owns the Bulky Waste block and its table. The mattress is the table's first entry (see the shelter thread); cars, filing cabinets, time capsules and the rest of the P0.3 buried-surprise brainstorm are later lines in the same table, not new code.

## P1.12 - Building blocks, the deliberate shelter tier (locked 2026-07-16)

The mattress (P1.11) is the bed; this is the *walls*. Crude shelter was already free - P0.3 makes the Block of Garbage buildable and the P1.4-option-A scope locks "shelter craftable from minute one" - so this is not "add shelter," it is refining scrap into blocks you would **choose** to build a home from. Shipped in Recompile 2026-07-16.

1. **Not defense - expression.** The starting biome is creature-free and P2's pressure loop is explicitly "never a threat to builds or cleared land," so shelter defends against nothing. It is the WALL-E move: rebuild a civilization from its own garbage. "You remember how to survive; you've forgotten how to build a civilization" (P1.4-A) is the frame.

2. **It is also the material sink.** Answers the "1,000 stacks of scrap" overflow worry directly: building consumes the bulk the sort produces. Every family maps to a base material stream, so each is a sink for what you already drown in.

3. **Tier-0 and ungated.** Crafted at the Scrap Crafting Table, no knowledge gate (shelter is free, tech is locked). Four full-kit families (block + slab + stairs + wall): **Pressed Junk** (the junk sink), **Scrap Plating**, **Corrugated Metal** (the iconic shanty aesthetic), **Plastic Panel** - plus **Cullet Glass** as **block + pane** only (glass has no honest slab or stairs form; vanilla ships neither).

4. **Hand-breakable, drop themselves.** No pickaxe exists (P1.2) and reclaiming your own walls must not be punishing; the prybar is only the *faster* tool on metal, never required. This is not a teardown input - it is crafted (made economy), so the "nothing enters the found economy without a teardown exit" invariant does not apply.

5. **Costs are first-pass** (4 material -> 1 base; vanilla slab/stairs/wall ratios); a balance pass comes once the tier is played. Corrugated is a 1:1 reshape of plating - a second aesthetic, not a second cost.

**Ownership:** Recompile owns all five families and their JSON. Region-specific building blocks (rebar concrete from C&D rubble, etc.) ride the regions system later; this is the household-tier starter set.

## P2.1 - The opening (locked 2026-07-14)

**Spawn is between mounds, not inside one** (the buried-spawn idea is dead - it fought garbage gravity and the walkable-world principle).

1. **Spawn in a natural clearing** in the household region: open coarse dirt, mounds on every horizon, a bag or two in reach, nearest mound within ~20 blocks. The place is the set piece.
2. **Opening spectacle: a scripted deorbit delivery** lands on a distant mound within the first minute - shows the signature visual, teaches "mounds replenish," zero danger. One-time; natural regrowth cadence takes over after.
3. **Quest book in inventory at spawn;** page one sells the exile lie ("they threw you away too"). "You arrived with the trash" survives as text/implication, not a playable burial.
4. **First-minutes flow** rides existing locks: hand-dig, discover pick-through, tarp within 15 minutes.
5. **Respawns are normal;** deorbit intro has a config skip for repeat players/servers.

## P2.2 - Tier 2 processing (locked 2026-07-14)

1. **Vanilla-first; custom only where vanilla has no verb.** Tier 2 adds one custom machine; everything else is vanilla stations (furnace, campfire, composter) unlocked via study - every unlock is recovering civilization, not learning a modded machine.
2. **The one custom station: the Burn Barrel.** Junk-fired, slow, inefficient, unlocked almost immediately. The real furnace is the mid-tier-2 upgrade - excavated broken and REPAIRED (find-and-fix as a main-quest beat). Burn barrel -> repaired furnace is the tier's arc.
3. **Fuel is junk** (+ plastic scrap). No trees, no coal; every worthless pull feeds the barrel. Organics compost, never burn.
4. **Purity as yield, not as parallel items.** Vanilla end products (iron, glass, bonemeal); the RATIO improves with tier (burn barrel 3 scrap -> 1 nugget; repaired furnace better; tier-4 machines approach lossless). No "reclaimed iron" item bloat. Identity lives in inputs/intermediates (scrap, cullet, muck, plastic sheet, rubber). Full material framework: [`material_economy.md`](material_economy.md).
5. **No energy at tier 2.** Fuel and hands only; electricity is a later tier's identity.

## P2.3 - Tier 3 logistics (locked 2026-07-14)

**Create is in the pack for belts (real MRFs run on belts); belts/transport are NOT part of the Recompile mod.**

1. **The seam rule: Recompile converts, Create moves.** Recompile machines turn garbage into components; Create (belts, funnels, brass tunnels, arms) routes them. The Recompile sorter has no internal filters - it dumps onto a belt and Create's filtering splits the stream.
2. **Recompile machines never REQUIRE Create** (standalone-mod constraint). Own simple power (fuel now, energy later); hopper/automation-compatible at this tier by design (unlike the tarp). Create integration is the pack's job via recipe gating; optional kinetic compat module only if demand exists.
3. **Two tier-3 machines: powered sorter** (automated pick-through, region tables intact) and **powered disassembler** (workbench successor; installed tool-heads replace the tool rack; still generates study progress - full vs reduced rate is a config, tune in playtest).
4. **Pack-tunes Create's leaks:** its crushing/washing chains route through our material streams, not around them. Create-spine materials (andesite, brass, zinc, copper) get bulk garbage streams - see the Create-spine section of [`material_economy.md`](material_economy.md) (found brass from fixtures; zinc from corrugated galvanized sheet; andesite from construction rubble/C&D debris).
5. **Create tech is locked until studied.** Your first belt segment is torn down from a conveyor found in the scrapyard.

## P2.4 - Reclamation chain (locked 2026-07-14)

1. **Healing is a recipe, not a right-click:** compost (from organic muck) + clean water + seed. Muck becomes the healing currency; leachate purification (clean water is made, not found) becomes load-bearing.
2. **Seeds are found, then made:** seed packets in household pulls, preserved pits from organics, rare intact saplings as cache-grade treasure; mid-tier greenhouse/nursery propagates recovered seed into self-sustaining lines.
3. **Scale ladder:** manual per-block first (the first grass patch is a monument), then the tier-4/5 irrigator/soil-spreader (radius conversion consuming compost + clean water - how mound footprints retire at scale), region-scale healing reserved for the final chapter.
4. **Green progression: grass -> crops -> trees.** Trees near-endgame (wood-as-treasure holds until tree farms); the first tree grown from recovered seed is a quest beat.
5. **Healing yields nothing but land.** No drops, no rewards beyond immunity, retirement, and the final chapter's payoffs - keeps quarry-vs-heal honest.

## P2.5 - Hazmat gating (locked 2026-07-14)

**Mekanism carries the systems; Recompile ships only content.** (Same lesson as belts: don't build what the lineup ships.)

1. **Hazard = Mekanism radiation**, emitted by radioactive debris seeded through the quarantine's mounds - including Mekanism's own radioactive waste barrels (which leak when broken - the chemical-drum idea, already implemented).
2. **Gate = Mekanism's hazmat suit**, their immunity rules and tuning. The gate sits at Mekanism-tier progression, which is right: uranium is endgame fuel; the region guarding it should require midgame chemistry to enter.
3. **Recompile's role: biome, garbage blocks, pull tables, caches.** Content, not systems. Standalone fallback (Recompile without Mekanism): config poison-on-contact block property, not a radiation engine.
4. **Sealed containers are the best knowledge caches in the game** - high-tier schematics survived BECAUSE the area was quarantined. The region's second treasure alongside uranium.

## P2.6 - E-waste recovery chains (locked 2026-07-14)

**Mekanism's chemical machinery is the recovery plant; Recompile ships inputs and tables.**

1. **Two-stage recovery, purity-as-yield:** crude board-smelting early (a little gold, a lot of loss); Mekanism dissolver/washer chains late (near-complete gold/silver/copper/rares from the same boards). Steepest yield curve in the pack - hoarding boards early pays off, an implicit lesson.
2. **The battery chain is its own mini-tree:** car/lead-acid, dry-cell, lithium pack - distinct teardowns (lead, zinc, lithium, nickel) feeding Mekanism chemistry. Carries a quest arc inside the e-waste region.
3. **Data recovery:** dead computers/TVs give e-scrap + schematic chance - the region's knowledge role, distinct from hazmat's sealed-container jackpots.
4. **Toxicity is flavor, not a system:** crude burning puffs smoke and brief nausea - a nudge toward the clean path. No new hazard systems.

## P2.7 - The quest line (locked 2026-07-14)

1. **Engine: FTB Quests.** NeoForge standard, datapack-driven, reward/unlock gating, and the quest-voice skill already targets it.
2. **Structure mirrors the tier spine - chapter per tier - titled in the exile fiction.** Not "Tier 2: Processing" but "The Way Home, Part II." Every chapter framed as a step toward the Overworld Gate; the quest book is the delivery vehicle for the surface lie (see the_twist.md).
3. **Quests teach, then get out of the way:** hand-holding early (pick-through, tarp, first study), tapering to loose objective lists by mid-game.
4. **The narrator is a character** (previous scavenger? automated system? last archivist?). Lock that quests HAVE a narrator persona; specific identity is a twist-adjacent open thread for the quest-writing phase (did they know?).
5. **The final chapter is authored against the_twist.md directly** - reveal beats + staged payoff. Playtesters who reach it need spoiler-safe feedback channels.

### Spoiler-safe hidden chapters (locked 2026-07-14)

Post-twist quests exist in the datapack but stay hidden until the reveal, using FTBQ chapter/quest visibility rules. Guardrails so hidden-in-FTBQ doesn't leak:

- **Gate at the content layer too, not just the visibility flag.** FTBQ hiding leaks via reward-item names in inventory, advancement toasts, JEI recipes for post-twist blocks, and quest-book search. So post-twist content (reclamation-scale blocks, villager-return triggers, final materials) is locked behind the Gate event itself - nothing to stumble on early.
- **The Gate activation is the single reveal switch** - one event unlocks the whole post-twist chapter tree at once.
- **The book should LOOK complete before the twist.** "The Way Home, Part VI" reads as the final chapter and clearly builds a Gate; a savvy player expects Gate-completion to end the pack. The existence of more chapters is itself the surprise - design intent for the quest writer.

## P2.8 - Cross-mod teardown tables at scale (locked 2026-07-14)

Content and process, not new mechanics.

1. **Budget it as content, forever.** Every mod added = a batch of teardown tables. A mod isn't "added" to the pack until its teardown tables exist - no craftable item should hit the workbench and get "no salvage value" (reads as broken, not authored).
2. **Tag-driven defaults do the heavy lifting.** Tables keyed on tags (`c:ingots/copper`, `c:storage_blocks/*`) cover thousands of items across all mods at once. Author tag rules once; per-item tables only for interesting exceptions. This is what makes scale tractable.
3. **Tiered generation:** tag rules cover the long tail; hand-authored tables for landmark items (a Create arm, a Mekanism machine) where yields and `teaches` unlocks are worth designing. Tags for coverage, handcraft for what players care about.
4. **A completeness check as a build step:** a script walks every pack item and flags craftables with no table and no matching tag rule - catches "no salvage value" gaps before players do. Keeps the compat promise honest as mods update.
5. **Community-extensible by design.** All datapack JSON (P0.5); the public schema lets pack users and addon authors add tables for untouched mods. Third-party teardown addons are a WANTED outcome, not a support burden.

**P2 is now fully specified (P2.1-P2.8).**

## P3.1 - Sky dumps - CUT/FOLDED (2026-07-14)

Not a separate feature. Sky dumps ARE the regrowth delivery already locked in P1.6.6: falling blocks spawn at the highest world level and fall into place in the mound. No beacon system, no supply-drop event, no opt-in toggle - it's simply how mounds refill. Technical details (spawn timing, entity handling) worked out at implementation.

## P3.2 - Field Manual (locked 2026-07-14)

1. **No custom guide book.** Use whatever guide-book mod is updated for MC 26.x at build time (Patchouli if available, else the current equivalent). Do NOT name-lock the mod or build a bespoke UI.
2. **The knowledge system does not depend on a custom book.** Study progress (the 2/3 in-progress states) surfaces through existing tools where possible; the guide book is lore + reference, not a required knowledge UI.
3. **The guide book is technical reference, NOT a lore vehicle.** Terse functional guidance (how to sort, study, process). Per the minimize-authored-prose principle, no ambient lore documents or archivist prose. Meaning is carried by environment and mechanics, not writing.

## P3.3 - Degraded recipes - CUT (2026-07-14)

Cut. "Crude first, better later" is already delivered by purity-as-yield (P2.2: lossy -> efficient conversion) and the burn-barrel -> repaired-furnace arc. Degraded item variants would violate the anti-bloat rule (parallel weaker blocks = JEI/ID clutter) and add a second progress axis on top of study points. Where a crude tier genuinely adds flavor, it's a separate cheap recipe unlocked first via the knowledge system (e.g. "scrap furnace" before "furnace") using normal items - a content pattern, not a stat-degradation system.

## P3.4 - Blueprint scraps - CUT (2026-07-14)

Dropped. Redundant: deterministic study points (P1.4.B, `scraps_required`) already give the collect-to-complete feel, and knowledge caches already drop full schematic items (P1.4.C). A third fractional-knowledge acquisition path adds nothing the system needs. Remove the "blueprint scraps" and `scraps_required`-as-fragments framing from the schema notes; keep study points and whole-schematic caches only.

## P3.5 - The themed Nether build (locked 2026-07-14)

Worldgen spec already locked (see Dimensions below: solid techno-organic waste roof to floor, lava pockets, embedded structures, vanilla mob rules - a dump you mine).

1. **A mid-game resource stop, not a parallel progression.** Go for what only it has, then leave. The overworld carries progression; no second tech tree down there.
2. **The reason to go: first RF power and osmium originate here** (plus netherite-analog from the compacted depths and nether-tier salvage). This is where the energy tier begins - before the Nether, no RF (fuel/manual only, consistent with "no energy at tier 2"). The Nether unlocks RF generation.
3. **It is solid, not mounds.** Do NOT think of the Nether in mound terms. Solid techno-organic fill with structure-voids; you tunnel through it. Different generation concept from the overworld's mounds-on-a-plain.

## P3.6 - The garbage End build (locked 2026-07-14)

Worldgen spec already locked (End-style islands of end-themed garbage, vanilla dragon/pillars/mobs, no liquid).

1. **Role: the late-game materials capstone - the endpoint of the found economy.** Holds what nothing else does: elytra (dragon reward), ender-tier materials, shulker boxes (the endgame storage payoff), chorus. The last found materials before everything becomes made.
2. **Access is earned per the locked bridge:** portal materials from high-tier recycling (obsidian made not found, eyes of ender from e-waste rare drops). End access naturally sits after the e-waste chain runs - you reach the End by having mastered recycling.
3. **The dragon stays vanilla** (fight, drop, open the gateway) - gives the pack its one real boss beat, framed as the old world's last guardian. No new systems.

**Twist tie-in (already true from worldgen):** the End being garbage too reinforces the reveal - nowhere pristine to escape to, not even here. Doesn't spoil it; a hindsight data point.

## P3.7 - Frogs return / Productive Frogs crossover - CUT (2026-07-14)

Dropped. The "life returns to healed land" payoff (twist doc) stays, but delivered with vanilla life, not a Productive Frogs integration. No cross-mod crossover in the pack.

## P3.8 - Win-condition tracking - CUT (2026-07-14)

Dropped entirely. **Progression is quest-based** - the FTB Quests line is the only progress system. No cleared-land metric, survey tool, scoreboard, or contiguous-area tracking. Endgame payoffs (including the twist's villager return) are gated by completing reclamation quests, not by a measured land total.

## P3.9 - Circular endgame - CUT, endgame REOPENED (2026-07-14)

The self-feeding-economy framing is dropped. **The pack needs a different endgame** (Jason's call - to be designed).

Dependencies this cut leaves OPEN (the circular economy was quietly carrying these - the replacement endgame must address them):
1. **The mechanical climax of the tech tree** - what is the peak the progression builds toward?
2. **The quarry-vs-heal resolution** - the circular economy was what made endgame healing affordable (once you manufacture inputs, retiring garbage quarries stops starving you). Without it, what makes full reclamation affordable rather than a permanent income sacrifice?
3. **The Gate-completion trigger** - completing the Overworld Gate triggers the twist. The Gate is still a big materials sink / final quest, but its "what you must achieve to build it" content is now open.

The twist, the final-chapter payoff, and the Gate-as-trigger all still stand (the_twist.md); what's open is the mechanical endgame that leads INTO the Gate.

## Dimensions - Nether and End (locked 2026-07-13, specs revised same day)

**Target: themed dimensions (Option 3).** Vanilla dimensions would leak free resources (quartz, gold, ancient debris) into a closed trash economy, so both get rebuilt to serve the fiction. Worldgen specs locked per-dimension below (four decisions each, mirroring P0.1).

### Nether - the compacted depths (working frame; "Incinerator" name under review)

1. **Profile:** solid techno-organic waste from bedrock roof to bedrock floor - fused machinery and organic refuse. You tunnel through it; the overworld is a dump you clear, the Nether is a dump you mine.
2. **Voids:** none, except possible embedded structures.
3. **Liquid:** random lava blocks/pockets seeded through the garbage, vanilla-Nether style.
4. **Mobs:** vanilla Nether mob spawning rules (mobs appear in tunnels and structure voids).

Mechanical role unchanged: the mid-game heat-and-energy tier, plus nether-tier salvage.

### End - the garbage End

1. **Profile:** floating End-style islands made of end-themed garbage. Vanilla dragon and obsidian pillars intact.
2. **Layout:** a lot like the vanilla End.
3. **Liquid:** none.
4. **Mobs:** vanilla End mobs.

**Supersedes the "Unspoiled World" idea** - even the void got trashed. The pristine-green payoff question is RESOLVED in [`the_twist.md`](the_twist.md) (full spoilers - the narrative frame, the final-chapter payoff, and the spoiler-discipline process rules live there).

**Interim + bridge:** portals are config-locked by default until each themed dimension ships. When they unlock, portal materials come out of high-tier recycling (obsidian is made, not found; eyes of ender from e-waste rare drops), so arrival is an earned event.

**Lore in one sentence:** a civilization that buried its overworld, compacted what wouldn't fit into the Nether, and threw the rest into the void.
