# Feature matrix - priority x feasibility

**Status:** build-order reference (updated 2026-07-17). The full feature-by-feature walkthrough is done except the parked endgame/postgame cluster; locked decisions and the session bookmark live in [`design_decisions.md`](design_decisions.md) - this matrix is the priority/feasibility view, that log is the source of truth for what's decided. Every feature is config-gated per the architecture principle. Per-feature **shipped status** is tracked in the Recompile roadmap (`../../recompile/docs/roadmap.md`); the notes below carry ship dates where a row has landed.

**Feasibility scale:**
- **Easy** - datapack/JSON or a well-worn modding pattern (block registration, loot tables, world preset).
- **Medium** - custom code, but known techniques (block-tick spread, weather events, simple machines).
- **Hard** - novel system, UI work, or cross-mod introspection. Schedule risk lives here.

---

## P0 - the feasibility slice (build first; proves the thesis)

| Feature | Feasibility | Notes |
|---|---|---|
| Custom flat world preset (coarse-dirt substrate) | Easy | World preset datapack. |
| Garbage surface layer (variable mounds on a coarse-dirt plain, no continuous burial) | Medium | Custom surface rules + mound placement. The brand; must *feel* right or the pack dies here. |
| Block of Garbage (one basic block; drops itself, gravity on) | Easy | Block + loot table. |
| Pick-through hand-sorting (right-click a placed block for components) | Easy | Loot-table-driven extraction; block crumbles after 4-6 pulls. |
| One hand-authored teardown table (JSON) | Easy | Proves the data-driven schema end to end. |

**Slice exit test:** spawn, dig garbage, sort it, get sorted materials. If the world doesn't feel like an endless dump, stop and rethink before any P1 work.

## P1 - core identity (the pack isn't Trashlands without these)

| Feature | Feasibility | Notes |
|---|---|---|
| Garbage block variants (bags, bales, Bulky Waste) | Easy | Different break-tools gate early game instead of biomes. Appliance dropped 2026-07-15; Bulky Waste (P1.11) took its worldgen slot. |
| Trash-tier tools (scrap knife, rebar sticks, prybar) | Easy | No trees, so tools must come from trash. Wood is a recovered treasure. |
| Building blocks from scrap (P1.12) | Easy | Shipped 2026-07-16. Four full-kit families (block/slab/stairs/wall): pressed junk, scrap plating, corrugated metal, plastic panel; plus cullet glass as block + pane only. Tier-0, ungated; the deliberate shelter tier and the bulk-scrap material sink. Not defense (nothing threatens builds). |
| Food, the survive tier (P1.9) | Easy-Medium | Shipped 2026-07-15. Creature-free biome; scavenged tin cans (Suspicious-Stew risk, knife-opened) + foraged dump mushrooms on vanilla mycelium. Planter/compost deferred to the knowledge tier. |
| Water, the Rain Collector (P1.10) | Medium | Shipped 2026-07-16. The world has no water; a scrap frame + tarp fills a real water tank from rain (26.1 transfer API), dispenses water bottles, moves water through pipes/buckets. Water survives break/replace (item component). |
| Lighting - Scrap Torch + Oily Rag (P1.4-A) | Easy | Shipped 2026-07-17. No wood/coal: Oily Rag (fiber + muck) is the "coal" fuel (charcoal parity); Scrap Torch = oily rag on rebar, a 1:1 vanilla-torch reskin. Refined lantern parked. |
| Sorting Tarp (first station, manual sorting) | Medium | Ex Nihilo sieve shape, garbage flavor. |
| Teardown machine (feed item -> components) | Medium | Shipped 2026-07-16 - the Recompile Workbench, materials-only and GUI-free (hold-to-disassemble; tools rest on the table). The knowledge axis is the next row. |
| Teardown-as-knowledge (recover recipes) | **Medium** (v1) | THE distinct axis. v1 rides vanilla `doLimitedCrafting` + recipe book grants (~1-2 wks on top of the bench); risks are the JEI locked-recipe overlay and FTB Teams sync. The Hard version (auto recipe introspection, gating other mods' machine recipes) stays maybe-never. Hand-authored JSON unlock tables only. |
| Garbage regions (household / scrapyard / e-waste / slag / hazmat) | Medium | Real biomes, distance-banded from spawn; per-biome garbage blocks. Launch trio: household + scrapyard + e-waste; slag + hazmat in P2. |
| Mound regrowth (mounds regenerate to original footprint, blocks fall from the sky) | Medium | Renewable quarries, not doom. Falling-block delivery from world top (deorbiting garbage). Original-bounds memory settled as a `mound_bed` blockstate carrying the cell's original height - no SavedData. Blocked on art. |
| ~~Healed-land immunity (grass + built blocks stop regrowth)~~ -> **Encroachment** | Easy | **Inverted and SHIPPED 2026-07-23** (P1.7-R): healed *surface* is contested, not immune. Coarse earth takes back soil bordering unhealed ground; the rung ladder is the defence (cover absorbs a hit, trees lock a border). Builds untouched, stops while you are away, wet farmland holds. **Mound retirement stays permanent** - only the green is a fight. |
| Dimension lockout (Nether + End portals disabled by default) | Easy | Config flags. Plugs the vanilla-resource leak until the themed dimensions ship. |

## P2 - the full loop (makes it a complete pack)

| Feature | Feasibility | Notes |
|---|---|---|
| Opening: clearing spawn + scripted deorbit spectacle | Medium | Spawn between mounds (buried-spawn cut, P2.1); distant sky-delivery in the first minute. |
| Trash wind (optional weather flavor event, small scatter near mounds) | Medium | Demoted to ambience. Never touches builds or cleared land. Config, conservative default. |
| Tier 2 processing (Burn Barrel + repaired furnace; purity-as-yield) | Easy-Medium | Burn Barrel **shipped 2026-07-17** (pulled ahead): a manual-only (non-automatable) vanilla-furnace reskin, `scrap -> copper nugget` (copper-first inversion). Repaired furnace + the metal-tier split remain. Fuel: Oily Rag + junk, no energy. |
| Tier 3 logistics (Create for belts; Recompile converts, Create moves) | Easy | Create in the pack; Recompile machines never require it. See material_economy.md Create spine. |
| Reclamation chain (grass -> crops -> trees) | Medium | One machine per rung (nothing renews on its own); the payout is the returning overworld - healed land is the second economy (P2.4-R). **Rung 1 is a *sprinkler* that consumes nothing (P2.4-R3)**, fed by an incorporated rain collector; the rungs are **multiblocks** built from a shared inert component vocabulary, and the framework is **shipped**. The Motor is teardown-only, so rung 1 sits behind the teardown spine. **Saplings are never obtainable as items (P2.4-R2, shipped)** - the tree planter is the only source of trees, so a tree farm is a running machine rather than hand-replanting. |
| Hazmat gating (Mekanism radiation + hazmat suit carry it) | Easy-Medium | Recompile ships biome + blocks + caches only; Mekanism owns the systems. |
| E-waste recovery chains (crude smelt early, Mekanism chemistry late) | Easy | Two-stage purity-as-yield; battery chain is its own mini-tree. |
| Quest line (FTB Quests, quest-voice spec; hidden post-twist chapters) | Easy | Titled in the exile fiction; the twist delivery vehicle. See the_twist.md. |
| Cross-mod teardown tables at pack scale (tag-driven + landmark handcraft) | Easy per entry | The compat surface is the content; grows forever. Budget it like content, not code. |

## P3 - polish and delight (after the pack is playable end to end)

| Feature | Feasibility | Notes |
|---|---|---|
| ~~Sky dumps~~ (CUT - folded into mound regrowth) | - | Not a separate feature; the falling-blocks-into-mound visual IS the regrowth delivery (P1.6.6). |
| Field Manual (technical reference, no custom book) | Easy | Use whatever guide-book mod is updated for 26.x; NOT a lore vehicle (minimize-prose principle). |
| ~~Degraded recipes~~ (CUT) | - | Redundant with purity-as-yield + burn-barrel arc; would violate anti-bloat. "Crude first" is a knowledge-unlock content pattern instead. |
| ~~Blueprint scraps~~ (CUT) | - | Redundant: study points already collect-to-complete; caches drop whole schematics. |
| Themed Nether (solid techno-organic waste, roof to floor) | Hard | Spec locked. First RF power + osmium originate here; a mid-game resource stop, not parallel progression. |
| Themed End (End-style islands of end-themed garbage, vanilla dragon) | Medium-Hard | Spec locked. The found-economy capstone; portal access earned through high-tier recycling. |
| ~~Frogs return to healed land (Productive Frogs integration)~~ (CUT) | - | Crossover dropped. Life-returns beat stays vanilla. |
| ~~Win-condition tracking (cleared-land metric, district map)~~ (CUT) | - | Progression is quest-based; no separate metric. |
| ~~Circular endgame (self-feeding economy)~~ (CUT) | - | Dropped; endgame REOPENED for redesign (see design_decisions P3.9). |
| The final chapter (narrative frame + staged payoff: sky clears, life waves, villagers settle, Gate monument) | Hard | **PARKED** - depends on the endgame redesign. Full spec in the_twist.md (spoilers). Overworld Gate multiblock, deorbit-rain suppression over healed land, quest-gated villager arrival are all real systems. |
| **Endgame redesign** (leads into the Gate; resolves quarry-vs-heal affordability) | TBD | **PARKED / OPEN** - circular economy cut. Three seed directions in design_decisions P3.9; not chosen. |

## Parked (not in this pack unless the plan changes)

| Feature | Notes |
|---|---|
| Magnetism (magnetic/eddy-current sorting tier) | Standalone-mod candidate in the shortlist. |
| Superposition (garbage block as probability cloud) | Standalone-mod candidate in the shortlist. |

---

## Reading the matrix

- **Teardown-as-knowledge is the distinct axis and the riskiest build**, though the walkthrough downgraded it P1-Hard -> Medium (it rides vanilla `doLimitedCrafting`). De-risk stays explicit: hand-authored JSON unlock tables first, automatic recipe introspection maybe never.
- **Everything in P0 is Easy/Medium.** The thesis can be tested in a week without touching anything hard.
- **The pack leans hard on curation.** Create carries logistics, Mekanism carries chemistry/radiation/energy; the Recompile mod deliberately doesn't build what the lineup ships. Custom code stays concentrated in worldgen, mound regrowth, and the knowledge system.
- **P3 shrank in the walkthrough:** five features cut (sky dumps, degraded recipes, blueprint scraps, frogs crossover, win-tracking) as redundant or over-built; the endgame was reopened. The systems locked in P0-P2 already covered most of what P3 originally promised.
