# Feature matrix - priority x feasibility

**Status:** brainstorm capture (2026-07-13). Nothing here is committed-to except P0. Every feature is config-gated per the architecture principle; priority here is about build order and what the pack's identity actually depends on.

**Feasibility scale:**
- **Easy** - datapack/JSON or a well-worn modding pattern (block registration, loot tables, world preset).
- **Medium** - custom code, but known techniques (block-tick spread, weather events, simple machines).
- **Hard** - novel system, UI work, or cross-mod introspection. Schedule risk lives here.

---

## P0 - the feasibility slice (build first; proves the thesis)

| Feature | Feasibility | Notes |
|---|---|---|
| Custom flat world preset (coarse-dirt substrate) | Easy | World preset datapack. |
| Garbage surface layer (piles/mounds horizon-to-horizon) | Medium | Custom surface rules + mound placement. The brand; must *feel* right or the pack dies here. |
| Block of Garbage (one basic block) | Easy | Block + loot table. |
| Mixed trash -> hand-sort into components | Easy | Item + loot-table-driven extraction. |
| One hand-authored teardown table (JSON) | Easy | Proves the data-driven schema end to end. |

**Slice exit test:** spawn, dig garbage, sort it, get sorted materials. If the world doesn't feel like an endless dump, stop and rethink before any P1 work.

## P1 - core identity (the pack isn't Trashlands without these)

| Feature | Feasibility | Notes |
|---|---|---|
| Garbage block variants (bags, bales, appliances) | Easy | Different break-tools gate early game instead of biomes. |
| Trash-tier tools (scrap knife, rebar sticks, prybar) | Easy | No trees, so tools must come from trash. Wood is a recovered treasure. |
| Sorting Tarp (first station, manual sorting) | Medium | Ex Nihilo sieve shape, garbage flavor. |
| Teardown machine (feed item -> components) | Medium | The Salvage mod's centerpiece block. |
| Teardown-as-knowledge (recover recipes) | **Hard** | THE distinct axis and THE schedule risk. De-risk: v1 is hand-authored JSON unlock tables (item -> recipe it can teach), NOT automatic recipe introspection. Auto-derivation from recipe trees is a later upgrade if ever. |
| Garbage regions (household / scrapyard / e-waste / slag / hazmat) | Medium | Region noise or custom biome source. Start with 2 (household + scrapyard); add the rest as content. |
| Creep (garbage spreads onto exposed coarse dirt) | Medium | Sculk-like block-tick spread. The baseline pressure. |
| Healed-land immunity (grass can't be re-buried) | Easy | One rule, but it IS the progression banking mechanic. Ships with creep. |

## P2 - the full loop (makes it a complete pack)

| Feature | Feasibility | Notes |
|---|---|---|
| Spawn-buried opening (dig up toward light) | Medium | Best first impression; needs safe-spawn logic. Slice can fake it manually first. |
| Trash wind (weather event drops garbage + region loot) | Medium | The periodic threat that is also a delivery. |
| Tier 2 processing (melt plastic, smelt scrap, compost, crush glass) | Easy-Medium | Mix of Salvage machines and curated existing mods. |
| Tier 3 logistics (conveyors/filters, hands-off sorting) | Easy | Pack curation - existing mods (Create et al.), not custom code. |
| Reclamation chain (coarse dirt -> grass -> trees) | Medium | The visible win state. Needs a deliberate mechanic, not just bonemeal. |
| Hazmat gating (protection gear unlocks the quarantine region) | Easy-Medium | Armor tag check. The hard gate for the rare-materials zone. |
| E-waste recovery chains (gold from boards, lithium from batteries) | Easy | JSON content on existing machines. |
| Quest line (FTB Quests, quest-voice spec) | Easy | Content work, large surface. Gate on tier spine being stable. |
| Cross-mod teardown tables at pack scale | Easy per entry | The compat surface is the content; grows forever. Budget it like content, not code. |

## P3 - polish and delight (after the pack is playable end to end)

| Feature | Feasibility | Notes |
|---|---|---|
| Sky dumps (telegraphed mass garbage drop, farmable late) | Medium-Hard | Default-off until midgame or quest-unlocked. |
| Field Manual (knowledge book UI that fills in) | Medium-Hard | v1 can be advancement toasts + quest book; dedicated UI later. |
| Degraded recipes (jury-rigged variants, re-refine later) | Medium-Hard | Gives Upcycle tier meaning; adds recipe-variant complexity. |
| Blueprint scraps (partial recipes, collect 3 to complete) | Medium | Collection meta on top of knowledge system; only after knowledge v1 proves fun. |
| Frogs return to healed land (Productive Frogs integration) | Easy | One-line spawn condition, signature moment, cross-promo. |
| Win-condition tracking (cleared-land metric, district map) | Medium | Nice scoreboard; not load-bearing. |
| Circular endgame (self-feeding economy) | Medium | Mostly recipe/quest design, not new systems. |

## Parked (not in this pack unless the plan changes)

| Feature | Notes |
|---|---|
| Magnetism (magnetic/eddy-current sorting tier) | Standalone-mod candidate in the shortlist. |
| Superposition (garbage block as probability cloud) | Standalone-mod candidate in the shortlist. |

---

## Reading the matrix

- **The one Hard item in P1 is the distinct axis.** Teardown-as-knowledge is why this pack exists, and it is the riskiest build. The de-risk is explicit: hand-authored JSON unlock tables first, automatic recipe introspection maybe never. If the hand-authored version isn't fun, the auto version won't save it.
- **Everything in P0 is Easy/Medium.** The thesis can be tested in a week without touching anything hard.
- **P2/P3 lean on curation.** Tiers 3-5 are mostly existing mods + JSON; custom code stays concentrated in worldgen, pressure, and knowledge.
