# Design decisions log

Running log of locked per-feature decisions from the feature-by-feature walkthrough of [`feature_matrix.md`](feature_matrix.md). One section per feature, in walkthrough order. "Locked" means design intent is settled; everything still ships config-gated per the architecture principle.

---

## P0.1 - Custom world preset (locked 2026-07-13)

1. **Vertical profile:** a few layers of coarse dirt, then several layers of deepslate, then a single bedrock layer. Solid all the way down - no caves, no voids, no ores. Digging down is pointless by design and the player discovers it fast.
2. **Terrain:** gently rolling, low-amplitude noise. Reads as buried plains, not a debug superflat.
3. **Water:** scattered pools of leachate (murky, mildly harmful, later a chemical-tier input). Clean water is made, not found.
4. **Mobs:** peaceful biomes and hostile biomes - hostility is a regional property, so safety is geography (starter regions calm, deeper regions dangerous). Vanilla mobs only for now; custom mobs possible later.

## Dimensions - Nether and End (locked 2026-07-13)

**Target: themed dimensions (Option 3).** Vanilla dimensions would leak free resources (quartz, gold, ancient debris, elytra) into a closed trash economy, so they get rebuilt to serve the fiction:

- **The Nether is the Incinerator.** A burning dump: ash wastes, slag flows, the place where garbage goes to burn. Mechanically the heat-and-energy tier - mid-game you go there for furnace-grade heat and combustion power the surface can't provide.
- **The End is the Unspoiled World.** The only pristine, green, untouched place in existence. Seeing it is the emotional payoff of the cleanup fantasy - it answers "why am I healing this world" with a destination. Elytra survives as pristine-world technology.

**Interim + bridge:** portals are config-locked by default until each themed dimension ships. When they unlock, portal materials come out of high-tier recycling (obsidian is made, not found; eyes of ender from e-waste rare drops), so arrival is an earned event.

**Lore in one sentence:** a civilization that buried its overworld and burned what it couldn't bury explains both dimensions.
