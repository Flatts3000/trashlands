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
| Teardown-as-knowledge (recover recipes) | **Medium** (v1) | THE distinct axis. v1 rides vanilla `doLimitedCrafting` + recipe book grants (~1-2 wks on top of the bench); risks are the JEI locked-recipe overlay and FTB Teams sync. The Hard version (auto recipe introspection, gating other mods' machine recipes) stays maybe-never. Hand-authored JSON unlock tables only. |
| Garbage regions (household / scrapyard / e-waste / slag / hazmat) | Medium | Region noise or custom biome source. Start with 2 (household + scrapyard); add the rest as content. |
| Mound regrowth (mounds regenerate to original footprint, blocks fall from the sky) | Medium | Renewable quarries, not doom. Falling-block delivery from world top (deorbiting garbage). Needs original-bounds memory per mound. |
| Healed-land immunity (grass + built blocks stop regrowth) | Easy | Grassing a mound's footprint retires it forever. The quarry-vs-heal tension is the pack's engine. |
| Dimension lockout (Nether + End portals disabled by default) | Easy | Config flags. Plugs the vanilla-resource leak until the themed dimensions ship. |

## P2 - the full loop (makes it a complete pack)

| Feature | Feasibility | Notes |
|---|---|---|
| Spawn-buried opening (dig up toward light) | Medium | Best first impression; needs safe-spawn logic. Slice can fake it manually first. |
| Trash wind (weather flavor event, small scatter near existing mounds) | Medium | Demoted from threat to ambience. Never touches builds or cleared land. Config, conservative default. |
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
| ~~Sky dumps~~ (CUT - folded into mound regrowth) | - | Not a separate feature; the falling-blocks-into-mound visual IS the regrowth delivery (P1.6.6). |
| Field Manual (knowledge book UI that fills in) | Medium-Hard | v1 can be advancement toasts + quest book; dedicated UI later. |
| Degraded recipes (jury-rigged variants, re-refine later) | Medium-Hard | Gives Upcycle tier meaning; adds recipe-variant complexity. |
| Blueprint scraps (partial recipes, collect 3 to complete) | Medium | Collection meta on top of knowledge system; only after knowledge v1 proves fun. |
| Themed Nether (solid techno-organic waste, roof to floor; heat/energy tier) | Hard | Spec locked (see design_decisions.md). May pull forward if the energy tier needs it. |
| Themed End (End-style islands of end-themed garbage, vanilla dragon) | Medium-Hard | Spec locked. Portal access earned through high-tier recycling. |
| Frogs return to healed land (Productive Frogs integration) | Easy | One-line spawn condition, signature moment, cross-promo. |
| Win-condition tracking (cleared-land metric, district map) | Medium | Nice scoreboard; not load-bearing. |
| Circular endgame (self-feeding economy) | Medium | Mostly recipe/quest design, not new systems. |
| The final chapter (narrative frame + staged payoff: sky clears, life waves, villagers settle, Gate monument) | Hard | Full spec in the_twist.md (spoilers). The Overworld Gate multiblock, deorbit-rain suppression over healed land, villager arrival are all real systems. |

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
