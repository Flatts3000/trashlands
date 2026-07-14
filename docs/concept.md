# Trashlands - Concept

**Status:** concept / exploring (2026-07-13). No code. Working name "Trashlands" (rename freely - candidates: The Heap, Landfill Earth, Wasteworld).
**Relationship:** the showcase modpack for the **Salvage** mod. Garbage + recycling is the core to explore. Magnetism and Superposition are noted as optional, not explored (see the note below). Mod shortlist + design rules: `F:\minecraft-repos\next-mod-concepts.md`.

---

## The vision

An **infinite flat world of coarse dirt, buried horizon-to-horizon under piles of Blocks of Garbage.** You spawn into an endless dump. No ore below you, no trees. Everything you will ever build comes out of the trash. **Rebuild - and eventually heal - a ruined world from its own garbage.**

This replaces the skyblock framing. Skyblock is a genre; an endless coarse-dirt plain under garbage is a *place* you recognize the instant you spawn, and it makes the cleanup fantasy **spatial** - you watch coarse dirt reappear as you process the piles. Progress shows on the ground.

---

## The world is the signature feature

- **Custom flat world type:** coarse-dirt substrate + a procedurally generated surface of Blocks of Garbage piled over everything. Worldgen/datapack job; it is the whole brand.
- **Garbage regions (instead of biomes):** the piles vary by area, gating progression through the terrain -
  - **Household-refuse sprawl** - plastics, packaging, organics (starter).
  - **Scrapyard** - metal, appliances, ferrous scrap.
  - **E-waste dump** - circuit boards, batteries; the rare/precious-materials zone.
  - **Industrial slag field** - heavier processing.
  - **Hazmat quarantine** - untouchable until you have protection (a hard gate).
  - Where you settle decides what you can recover first.

---

## Dimensions (decided 2026-07-13)

Vanilla Nether/End would leak free resources into a closed trash economy, so both get themed (portals config-locked until each ships; portal materials ultimately come from high-tier recycling). Full specs: [`design_decisions.md`](design_decisions.md).

- **Nether:** solid techno-organic waste from bedrock roof to floor, lava pockets, embedded structures. The overworld is a dump you clear; the Nether is a dump you mine. Mid-game heat-and-energy tier.
- **End:** floating End-style islands of end-themed garbage, vanilla dragon and pillars. Even the void got trashed.

Open: the pristine-green emotional payoff needs a home; leading candidate is the healed overworld itself.

Lore in one sentence: a civilization that buried its overworld, compacted what wouldn't fit into the Nether, and threw the rest into the void.

---

## The core loop

Break a Block of Garbage -> **mixed trash** -> **sort** -> **tear down / recycle** -> materials + recovered **know-how** -> craft/rebuild -> (your output eventually becomes trash again).

The tech tree runs entirely on waste. Teardown doesn't just yield scrap - disassembling an unfamiliar item **teaches you how it was made** (the Salvage twist), so you reverse-engineer the old world by picking through its garbage.

---

## The distinct mechanic: the garbage keeps coming

An infinite world reframes the renewable-trash problem into something better than a generator block: the world is a **still-active dump.** Trash re-accumulates - wind-blown drifts, periodic dumps burying your borders - so the game is a **race to out-process the incoming tide.**

- Early game you're drowning in it.
- Mid game you break even.
- The **win** is when recycling finally outpaces accumulation and your cleared coarse-dirt frontier expands faster than it's buried.

This pressure loop is thematically perfect (a fight against entropy) and structurally different from Sky Frogs' contained, vertical progression - this one is **horizontal, expansionist**. This is the pack's candidate distinct axis; verify against prior art before claiming it.

---

## The core: garbage + recycling (Salvage)

Teardown-as-knowledge is the spine. Feed any item (or garbage block) into a reverse-rig; get components + a chance to learn its recipe and better variants. Factorio's Fulgora is the proven-fun reference; the distinct axis is **recovering recipes, not just materials**, plus **universal cross-mod teardown** (the compat surface is the content). The garbage-and-recycling design is where the real work goes.

### Optional, NOT explored: Magnetism and Superposition

Noted as possible later directions only - not part of this pack's explored design, not committed. Parked here so the synergy isn't lost:

- **Magnetism** could power the sorting tier (magnetic + eddy-current separation is literally how real plants sort waste). A natural fit if we ever want it - but out of scope for now.
- **Superposition** could frame advanced recovery (a sealed garbage block as a cloud of possible contents whose odds you engineer). A conceptual fit - parked, not developed.

Both stay in the mod shortlist (`F:\minecraft-repos\next-mod-concepts.md`) as standalone-mod candidates; Trashlands does not depend on either.

---

## Tier spine (each layer adds one verb)

1. **Scavenge** - hand-sort trash for scrap metal, plastic, glass, organics, e-waste.
2. **Break down** - basic machines: melt plastic, smelt scrap, compost organics, crush glass to cullet.
3. **Sort & automate** - conveyors/filters separate mixed trash hands-off. The logistics tier.
4. **Recover the good stuff** - gold from circuit boards, lithium from batteries, rare bits from e-waste; chemical recycling.
5. **Upcycle** - turn recovered materials into real tech, closing loops earlier tiers couldn't.
6. **Circular endgame + reclamation** - a self-feeding economy; the trash mountain visibly shrinks; **restore the land** (coarse dirt -> grass -> trees). Win by making the highest-tier tech from pure waste, and by carving a green clearing out of an endless dump.

---

## Why it fits Jason's proven pattern

- **It's the Salvage mod's Sky Frogs** - pack as vehicle, mod as engine; the same one-two that already shipped.
- **Cross-mod IS the content** - recycle any mod's items; the more mods in the pack, the bigger the teardown tree.
- **Data-driven** - garbage-block loot/teardown tables, magnetic properties, recovery odds are all JSON.
- **Proven format** - a tiered, quest-driven progression pack (Sky Frogs shape) on a memorable custom world.
- **A hook with a conscience** - "one man's trash," reclamation, healing a ruined world. Legible and shareable.

---

## Prior art (checked 2026-07-13) - theme validated, niche OPEN

- **Dumpster Diving** (CurseForge) - the near-exact core: dig **Garbage Blocks**, a **Landfill biome** with buried mounds, recycle scraps to resources (cans -> tin, tires -> rubber, circuit boards -> redstone). **But abandoned** - latest release is v1.3.3 for **MC 1.12.2, dated 2018-2020** (~6 years dead, ancient version). Proves the theme has appeal; leaves the niche empty on modern MC.
- **Scraps and Shards** / **Create Recycle Everything** / **Overly Complicated Garbage** - cover pieces (worldgen scrap piles; universal item recycling via Create - a *living* base worth considering; garbage production/disposal), not a dedicated garbage-world progression.
- Wasteland survival packs (Survive The Wasteland, Wastelands, Project X) - scarcity/scavenging theme, not garbage-block recycling. The "Garbage Disposal" / "Garbage Dump" packs read as casual/kitchen-sink.
- **Verdict:** the **Productive Bees -> Productive Frogs pattern** - a beloved-but-dead concept (Dumpster Diving) to rebuild modern and better. Don't build ON the corpse; either a fresh **Salvage mod** (MC 26.1, teardown-as-knowledge) or a pack on a *living* base (Create Recycle Everything). Our two distinct axes - **teardown-as-knowledge** and the **still-active self-burying dump** - are unclaimed by anything current.

## Architecture (decided 2026-07-13)

**One mod + one pack, more mods later if earned.** A single fresh companion mod (working name **Salvage**, NeoForge / MC 26.1) owns all custom systems to start: the garbage worldgen (coarse-dirt world preset, Blocks of Garbage and variants, garbage regions), the teardown-as-knowledge loop, and eventually the "garbage keeps coming" pressure system. The pack owns curation, quests, tuning, and the cross-mod teardown tables (JSON datapack territory, extendable without mod releases).

Keep internal seams clean so systems can split into their own mods later - candidates: the pressure system as a generic data-driven accumulation engine; Magnetism / Superposition stay parked in the shortlist. Don't pre-create repos for mods that don't exist. This supersedes the build-on-vs-new-mod question: not building on Create Recycle Everything (it can still appear in the pack as a mid-tier automation layer, not the foundation).

**Features are config-gated.** Every major system ships behind a config flag with tunable rates (pressure variants, region weights, knowledge odds). This lets playtesting pick winners instead of deciding on paper - e.g. build creep, trash wind, AND sky-dumps, then tune. Guardrail: flags are for tuning, not for avoiding decisions; the pack ships one opinionated default experience. Defaults are the design.

## Open questions

- **In-place vs frontier renewal:** is trash finite-per-chunk (expand outward) or does it actively re-bury a fixed base (the "garbage keeps coming" pressure)? Lean: the latter, but tune so it's pressure, not punishment.
- **Worldgen approach:** custom world-preset/dimension datapack for the coarse-dirt + garbage surface + regions.

## Next actions

1. Lock the "garbage keeps coming" mechanic (rate, wind-in vs dump, pressure tuning).
2. Sketch the tier-one loop end to end (spawn -> first sorted materials -> first machine).
3. One-week feasibility slice: the custom garbage worldgen + one garbage block that tears down into sorted materials. Throwaway if the world doesn't *feel* right.
