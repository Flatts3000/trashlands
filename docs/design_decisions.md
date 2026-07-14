# Design decisions log

Running log of locked per-feature decisions from the feature-by-feature walkthrough of [`feature_matrix.md`](feature_matrix.md). One section per feature, in walkthrough order. "Locked" means design intent is settled; everything still ships config-gated per the architecture principle.

---

## P0.1 - Custom world preset (locked 2026-07-13)

1. **Vertical profile:** a few layers of coarse dirt, then several layers of deepslate, then a single bedrock layer. Solid all the way down - no caves, no voids, no ores. Digging down is pointless by design and the player discovers it fast.
2. **Terrain:** gently rolling, low-amplitude noise. Reads as buried plains, not a debug superflat.
3. **Water:** scattered pools of leachate (murky, mildly harmful, later a chemical-tier input). Clean water is made, not found.
4. **Mobs:** peaceful biomes and hostile biomes - hostility is a regional property, so safety is geography (starter regions calm, deeper regions dangerous). Vanilla mobs only for now; custom mobs possible later.

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
