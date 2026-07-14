# Design decisions log

Running log of locked per-feature decisions from the feature-by-feature walkthrough of [`feature_matrix.md`](feature_matrix.md). One section per feature, in walkthrough order. "Locked" means design intent is settled; everything still ships config-gated per the architecture principle.

---

## P0.1 - Custom world preset (locked 2026-07-13)

1. **Vertical profile:** a few layers of coarse dirt, then several layers of deepslate, then a single bedrock layer. Solid all the way down - no caves, no voids, no ores. Digging down is pointless by design and the player discovers it fast.
2. **Terrain:** gently rolling, low-amplitude noise. Reads as buried plains, not a debug superflat.
3. **Water:** scattered pools of leachate (murky, mildly harmful, later a chemical-tier input). Clean water is made, not found.
4. **Mobs:** peaceful biomes and hostile biomes - hostility is a regional property, so safety is geography (starter regions calm, deeper regions dangerous). Vanilla mobs only for now; custom mobs possible later.
