# Design decisions log

Running log of locked per-feature decisions from the feature-by-feature walkthrough of [`feature_matrix.md`](feature_matrix.md). One section per feature, in walkthrough order. "Locked" means design intent is settled; everything still ships config-gated per the architecture principle.

---

## Walkthrough status (the bookmark - update every session)

**As of 2026-07-14:** P0 fully locked (P0.1-P0.5). P1 fully locked (P1.1-P1.8). **P2 fully locked (P2.1-P2.8).** Dimensions, the knowledge system, mound regrowth, the material economy ([`material_economy.md`](material_economy.md)), and the narrative layer ([`the_twist.md`](the_twist.md), spoilers) are locked. Mod lineup so far: Create (belts/logistics), Mekanism (chemical/radiation endgame), Productive Frogs (reclamation crossover).

**Resume here - P3 walkthrough, in matrix order:**
1. Sky dumps (opt-in late farmable deliveries)
2. Field Manual (knowledge book UI)
3. Degraded recipes (jury-rigged variants, re-refine)
4. Blueprint scraps (partial recipes, collect-3)
5. The Incinerator / themed Nether build
6. The garbage End build
7. Frogs return to healed land (Productive Frogs)
8. Win-condition tracking (cleared-land metric)
9. Circular endgame (self-feeding economy)
10. The final chapter (narrative frame + staged payoff - author vs the_twist.md)

**Open threads not on the matrix:** pack name (working: Trashlands), Nether theme name ("compacted depths" placeholder), the quest-narrator question (who wrote the quest book - see the_twist.md), where construction rubble lives (see material_economy.md).

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
- **Knowledge caches:** filing cabinets / briefcases (documents teach recipes), dead computers and TVs (e-waste + data recovery), time capsules (rare; lore + a guaranteed full recipe). Blueprint scraps live here, not only in teardown machines.
- **Utility finds:** broken machines repairable into working ones (find-and-fix beats craft for the fantasy - your first furnace might be excavated), dumpsters as working storage, mattresses as field respawn points.
- **Hazards:** rusty chemical-waste barrels (leak if broken carelessly, but are chemical-tier inputs), pocketed garbage gas (fire/poison puff on careless digging).
- **Lore set-dressing:** buried road segments, street lamps, bus stops, signage - the old world's skeleton.

## P0.3 - The Block of Garbage (locked 2026-07-14)

1. **Drops itself.** The block is the unit of mixed trash: carry it, stack it, build with it (trash walls as first shelter), feed it whole into sorting stations. Loose mixed-trash items still exist (from bags, loot) but the block stays whole when dug.
2. **Hand-breakable but slow; shovel-class fast.** Zero-barrier start. Tougher variants needing prybar/knife arrive in P1.
3. **Gravity on, config-gated.** Gravel-style falling. Mounds slump when quarried; digging into a tall mound's base can bury you. Foreshadows the pressure system.
4. **One block, randomized texture/model variants** (protruding bag, jutting pipe, compressed face) so mounds read as heterogeneous junk without multiplying block IDs. Region palettes come with the regions system.

## P0.4 - Mixed trash and hand-sorting (locked 2026-07-14)

1. **Tier-zero sorting = picking through a placed block.** Right-click a placed garbage block with an empty hand; each pull yields one drop from its table; after 4-6 pulls the block is exhausted and crumbles. No UI, no station. The Sorting Tarp (P1) is the batch version, machines the automated version - same verb at three speeds.
2. **Base material vocabulary (7):** scrap metal, plastic scrap, glass shards, organic muck, fiber scrap, e-scrap (rare), junk (filler majority). Every machine tier speaks this language; keep the set small and stable.
3. **Junk is fuel, not worthless.** Burns poorly, compacts back into buildable trash blocks. Nothing is worthless; some things are barely worth anything - the pack's moral stance as an item.
4. **Region-weighted pull tables from day one.** JSON per region; slice ships one (household). Scrapyard skews metal, e-waste skews e-scrap - regions gate materials.

## P0.5 - Teardown table schema (locked 2026-07-14)

1. **Two systems, two formats.** Garbage-block pulls use vanilla loot tables (free tooling, modder familiarity). Teardown gets a custom recipe type (`salvage:teardown`). One format is not forced to do both jobs.
2. **Output shape: fixed core + weighted extras.** Deterministic bones (plan an economy around it) plus chance-weighted bonuses (stays interesting).
3. **`teaches` field in the schema from day one** even though the knowledge mechanic is P1: recipe(s) revealed, chance, `scraps_required` for the blueprint-scraps hook. The distinct axis is not retrofitted into a shipped schema.
4. **`station` field for tier gating** (hand / tarp / machine / advanced) - one format covers the whole progression; pack authors gate cross-mod teardowns with one string.

Reference sketch:

```json
{
  "type": "salvage:teardown",
  "input": "minecraft:iron_door",
  "station": "salvage:workbench",
  "results": [ { "item": "salvage:scrap_metal", "count": 2 } ],
  "extras": [ { "item": "salvage:hinge", "chance": 0.35 } ],
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
| Appliance | Prybar | Deterministic guts; ideal teardown input |

1. **Starter tool trio from tier-zero materials:** scrap knife (bales, fiber), prybar (appliances, weak weapon), junk shovel (digs garbage fast). No pickaxe in the starter set - nothing to mine, and its absence tells the player that.
2. **Rebar is the universal handle** (drops from scrap-metal pulls). Wood recovery stays a mid-tier treasure, not a tool gate.
3. **Bags/bales feed sorting (random pulls); appliances feed teardown (deterministic + teaches chance).** Appliances are the on-ramp to the knowledge system.
4. **Generation:** bags on mound surfaces, bales in mound cores (mound shape does the depth-reward work), appliances uncommon pocket finds. Region palettes reweight all three.

## P1.3 - Sorting Tarp (locked 2026-07-14)

The batch tier of the sorting verb, designed with sifting's (Ex Nihilo lineage) lessons baked in:

1. **Form:** single flat block, tarp-with-junk-heap model. No multiblock ceremony at tier one.
2. **Interaction:** small UI (input slots for garbage/bags/bales, outputs accumulate) - the interface pattern later machines inherit. **Hold-to-sort, never click-spam** (sieving's RSI lesson, fixed preemptively). One operation sorts one whole block vs 4-6 hand pulls.
3. **Screen slot (mesh-tier lesson):** screens change *what*, not *how much* - a metal screen skews pulls toward scrap metal, an organics screen toward muck. Player-chosen filtering, no raw-value inflation; richer odds stay the machine tier's selling point.
4. **Bales batch (compression lesson):** sorting a bale is one operation yielding 2-3 blocks' worth. Knife -> bale pipeline is the anti-tedium upgrade.
5. **Recipe:** fiber scrap + rebar, pure tier-zero, buildable in the first 15 minutes.
6. **Drop tables visible in JEI/EMI from day one.** Non-negotiable.
7. **In-world charm:** the junk heap on the tarp visibly shrinks as you sort.
8. **Hopper compatibility off at this tier** (config-gated) - the tarp is manual by identity.

## P1.4 - Salvage Workbench + teardown-as-knowledge (locked 2026-07-14)

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
3. **The core tension this creates:** a regrowing mound is income; healed land is permanent but retires that income. Healing the world shrinks your garbage economy - full reclamation becomes affordable only when the circular economy (recycling your own outputs) can replace scavenging. Endgame thesis: not "you beat the tide" but "you no longer need the dump."
4. **Trash wind and sky dumps demoted to optional flavor/farmable events** (config, conservative defaults; never threaten builds or cleared land). Wind = ambience + small scatter near existing mounds at most; dumps = opt-in late-game deliveries.
5. **Regrowth rate config-exposed;** default slow enough to feel like recovery, not respawn (visible across sessions, not minutes).
6. **Delivery: blocks fall from the top of the world,** as if deorbiting from space - falling-block entities spawn high above the mound and rain into place. Visible from afar (you can see which mounds are replenishing), reuses the garbage-block gravity from P0.3, and ties the lore together: the void-dumped garbage is still coming home.

## P1.8 - Dimension lockout (locked 2026-07-14)

Nether and End portals disabled by config default until each themed dimension ships. Decided within the Dimensions discussion below; nothing further to design here.

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

**Create is in the pack for belts (real MRFs run on belts); belts/transport are NOT part of the Salvage mod.**

1. **The seam rule: Salvage converts, Create moves.** Salvage machines turn garbage into components; Create (belts, funnels, brass tunnels, arms) routes them. The Salvage sorter has no internal filters - it dumps onto a belt and Create's filtering splits the stream.
2. **Salvage machines never REQUIRE Create** (standalone-mod constraint). Own simple power (fuel now, energy later); hopper/automation-compatible at this tier by design (unlike the tarp). Create integration is the pack's job via recipe gating; optional kinetic compat module only if demand exists.
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

**Mekanism carries the systems; Salvage ships only content.** (Same lesson as belts: don't build what the lineup ships.)

1. **Hazard = Mekanism radiation**, emitted by radioactive debris seeded through the quarantine's mounds - including Mekanism's own radioactive waste barrels (which leak when broken - the chemical-drum idea, already implemented).
2. **Gate = Mekanism's hazmat suit**, their immunity rules and tuning. The gate sits at Mekanism-tier progression, which is right: uranium is endgame fuel; the region guarding it should require midgame chemistry to enter.
3. **Salvage's role: biome, garbage blocks, pull tables, caches.** Content, not systems. Standalone fallback (Salvage without Mekanism): config poison-on-contact block property, not a radiation engine.
4. **Sealed containers are the best knowledge caches in the game** - high-tier schematics survived BECAUSE the area was quarantined. The region's second treasure alongside uranium.

## P2.6 - E-waste recovery chains (locked 2026-07-14)

**Mekanism's chemical machinery is the recovery plant; Salvage ships inputs and tables.**

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

1. **Budget it as content, forever.** Every mod added = a batch of teardown tables. A mod isn't "added" to the pack until its salvage tables exist - no craftable item should hit the workbench and get "no salvage value" (reads as broken, not authored).
2. **Tag-driven defaults do the heavy lifting.** Tables keyed on tags (`c:ingots/copper`, `c:storage_blocks/*`) cover thousands of items across all mods at once. Author tag rules once; per-item tables only for interesting exceptions. This is what makes scale tractable.
3. **Tiered generation:** tag rules cover the long tail; hand-authored tables for landmark items (a Create arm, a Mekanism machine) where yields and `teaches` unlocks are worth designing. Tags for coverage, handcraft for what players care about.
4. **A completeness check as a build step:** a script walks every pack item and flags craftables with no table and no matching tag rule - catches "no salvage value" gaps before players do. Keeps the compat promise honest as mods update.
5. **Community-extensible by design.** All datapack JSON (P0.5); the public schema lets pack users and addon authors add tables for untouched mods. Third-party teardown addons are a WANTED outcome, not a support burden.

**P2 is now fully specified (P2.1-P2.8).**

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
