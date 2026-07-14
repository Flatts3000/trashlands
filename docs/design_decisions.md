# Design decisions log

Running log of locked per-feature decisions from the feature-by-feature walkthrough of [`feature_matrix.md`](feature_matrix.md). One section per feature, in walkthrough order. "Locked" means design intent is settled; everything still ships config-gated per the architecture principle.

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

### Buried-surprise candidates (brainstorm 2026-07-13)

- **Loot pinatas:** appliances (fridge = preserved food, early food source; washer, stove - prybar targets), crushed cars (metal + battery chance), tire stacks, pipe bundles, wire spools.
- **Knowledge caches:** filing cabinets / briefcases (documents teach recipes), dead computers and TVs (e-waste + data recovery), time capsules (rare; lore + a guaranteed full recipe). Blueprint scraps live here, not only in teardown machines.
- **Utility finds:** broken machines repairable into working ones (find-and-fix beats craft for the fantasy - your first furnace might be excavated), dumpsters as working storage, mattresses as field respawn points.
- **Hazards:** rusty chemical-waste barrels (leak if broken carelessly, but are chemical-tier inputs), pocketed garbage gas (fire/poison puff on careless digging).
- **Lore set-dressing:** buried road segments, street lamps, bus stops, signage - the old world's skeleton.

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

**Supersedes the "Unspoiled World" idea** - even the void got trashed. OPEN QUESTION: the pristine-green emotional payoff no longer has a dimension to live in; leading candidate is that the healed overworld itself is the payoff (the green place is the one you made). Decide in its own turn.

**Interim + bridge:** portals are config-locked by default until each themed dimension ships. When they unlock, portal materials come out of high-tier recycling (obsidian is made, not found; eyes of ender from e-waste rare drops), so arrival is an earned event.

**Lore in one sentence:** a civilization that buried its overworld, compacted what wouldn't fit into the Nether, and threw the rest into the void.
