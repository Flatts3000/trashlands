# Trashlands - Concept

**Status:** design walkthrough complete except the parked endgame/postgame cluster (updated 2026-07-14). P0-P2 + most of P3 fully specified in [`design_decisions.md`](design_decisions.md) (the per-feature log and session bookmark); [`feature_matrix.md`](feature_matrix.md) is the build order. Working name "Trashlands" (rename freely - candidates: The Heap, Landfill Earth, Wasteworld).

**Build status (2026-07-15):** the **pack** is not assembled. The **Recompile mod** is a playable alpha and has shipped the garbage world, the block family, the trash tools, the Sorting Tarp, the food tier and storage (see `../recompile/docs/roadmap.md`). First real playtests happened this day, and they moved two things from "designed" to "known": the early loop needed retuning against actual play, and **the core question of what makes sifting fun is now open** - see below, and the first entry under Open questions.
**Relationship:** the showcase modpack for the **Recompile** mod. Garbage + recycling is the core to explore. Magnetism and Superposition are noted as optional, not explored (see the note below). Mod shortlist + design rules: `F:\minecraft-repos\next-mod-concepts.md`.

---

## The vision

An **endless, gently rolling plain of coarse dirt, crowded to the horizon with mounds of Blocks of Garbage.** You spawn into an endless dump. No ore below you, no trees. Everything you will ever build comes out of the trash. **Rebuild - and eventually heal - a ruined world from its own garbage.**

This replaces the skyblock framing. Skyblock is a genre; an endless garbage-mound plain is a *place* you recognize the instant you spawn, and it makes the cleanup fantasy **spatial** - every mound you kill and grass over is land visibly, permanently healed. Progress shows on the ground.

---

## Why sifting garbage is fun (foundational + aspirational, 2026-07-15)

**Foundational:** every mechanic in this pack should be able to answer to one of these four. **Aspirational:** the build does not honour them yet, and the first one it fails is the one that matters most. Arrived at by asking what is actually fun about picking through a dump *in real life*, not what is fun about a loot table.

**1. You are the filter.** A mudlarker walks past ten thousand bottle caps and their eye stops on a Roman coin. A diver flips a lid and *sees* it in half a second. The junk is not the tedious part - the junk is **the field your attention crosses**, and crossing it is the skill. The pleasure is being **the one who spots it**: ninety-nine rejections a second, then *wait*.

This is why the ratio matters and why nobody wants a dumpster full of treasure. **The junk is load-bearing.** It is what makes the find mean anything. Take the junk away and the coin is just a coin.

**2. The score is asymmetric.** Not "I got a thing" - *someone paid for this, threw it away, everyone else walked past it, and I got it for the price of dirty hands.* Free ticket, real prize. There is a righteous edge to it: the world declared this worthless and you proved the world wrong. Divers describe the outrage and the delight in the same breath, because they are the same feeling.

**3. Trash is honest.** People curate what they show you; their garbage is what they actually did. Archaeologists dig middens for exactly this reason - a dump is the most truthful museum a culture leaves behind. Half the fascination is never the object's value. It is *who was this person, and what happened to them.*

**4. Resurrection.** The fridge only needed a relay. It was dead, and now it is not, and you did that. Scrappers rate this above the score.

### The failure this exists to prevent

**In real life you are the filter. In Ex Nihilo - and in what this pack has built so far - the RNG is the filter.** You click a box and wait to be told what you got. There is no scanning, no spotting, no moment of recognition, because there is nothing to *look at*: a Block of Garbage is an opaque cube that reveals nothing until a random number decides for you. Your attention is nowhere.

So the tedium in sieving was never "too much junk". **It was that the player was not the one doing the looking.** That is the diagnosis this pack has to keep in front of it, because the symptom (tedium) invites the wrong fix (tune the drop rates), and rates cannot fix "the player is not looking". `design_decisions.md` P1.3 already carried the lesson - *"hold-to-sort, never click-spam (sieving's RSI lesson, fixed preemptively)"* - and the implementation drifted back into it anyway, one reasonable tuning decision at a time. By 2026-07-15 hand-sorting a stack of garbage was ~64 seconds of held right-click, and a stack through the Sorting Tarp sprayed ~384 item entities on the ground to walk around hoovering.

### The test

Any mechanic that produces or processes garbage should be asked:

- **Is the player the filter, or is the RNG?** A *tell* - something visible you can spot and choose - beats a better drop table every time. Bulky waste survives every argument for this reason: it is the first thing in the mod you can *see* and *decide about*.
- **Does the junk make the find mean something,** or is it just volume?
- **Is the player looking, or waiting?**

**Consequence for the loop:** the pack is an *infinite* dump. You can never sort it all and were never meant to. The game is therefore not "process the garbage" - it is **"know what is worth your time."** An expert scavenger walks past 99% of a dump without slowing down. That is the fantasy, and infinity makes it literal rather than a balance number.

---

## The world is the signature feature

- **Custom flat world type:** a gently rolling coarse-dirt plain crowded with garbage mounds of every size - short flat spreads to tall trash hills - dense enough to crowd the horizon (no continuous burial; dirt shows between mounds). Clearing means removing mounds. Worldgen/datapack job; it is the whole brand. Full worldgen decisions: [`design_decisions.md`](design_decisions.md).
- **Garbage regions (real biomes, distance-banded from spawn):** each region has its own garbage blocks, textures, pull tables, and hostility; launch trio is household + scrapyard + e-waste -
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

The pristine-green payoff question is resolved - see [`the_twist.md`](the_twist.md) (**full spoilers**; player-facing copy must not reference its contents).

Lore in one sentence: a civilization that buried its overworld, compacted what wouldn't fit into the Nether, and threw the rest into the void.

---

## The core loop

Dig Blocks of Garbage (they drop themselves) -> **sort** (pick through by hand -> Sorting Tarp -> machines: same verb at three speeds) -> **tear down** found items at the Recompile Workbench -> materials + **schematics** (recovered recipes) -> craft/rebuild -> (your output eventually becomes trash again).

The tech tree runs entirely on waste. Teardown doesn't just yield scrap - studying an item **teaches you how it was made** (deterministic study points; knowledge is a physical, tradeable schematic), so you reverse-engineer the old world by picking through its garbage. Survival crafts are free; technology is locked until learned.

---

## The renewal mechanic: mounds grow back (revised 2026-07-14)

Trash is never impending doom. **Mounds regrow toward their original size and footprint - never beyond.** A mound is a **renewable quarry**; the mechanic exists so you never have to relocate for materials. Regrowth only fills exposed coarse dirt within the original bounds; grass and built blocks stop it, so killing a mound and grassing its footprint **retires it forever**.

The tension this creates is the pack's engine:

- A regrowing mound is **income**. Healed land is **permanent, but retires that income**.
- Healing the world shrinks your garbage economy - full reclamation must become affordable before the endgame (the resolving mechanism is currently open; see the P3.9 note in `design_decisions.md`).
- The endgame thesis: not "you beat the tide" but **"you no longer need the dump."**

**Delivery is the signature visual:** regrowth blocks fall from the top of the world into place, as if deorbiting - the void-dumped garbage of the old civilization still coming home. You can see which mounds are replenishing from across the map.

(Supersedes the earlier "still-active dump / race to out-process the tide" pressure loop. Trash wind and sky dumps survive only as optional flavor/farmable events, config-gated, never a threat to builds or cleared land.)

---

## The core: garbage + recycling (Recompile)

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
6. **Endgame + reclamation** - **restore the land** (coarse dirt -> grass -> crops -> trees), retiring garbage quarries permanently. The mechanical endgame (what you build toward, culminating in the Overworld Gate) is currently REOPENED - see the P3.9 note and bookmark in [`design_decisions.md`](design_decisions.md). The narrative endgame is spoiler-quarantined in `the_twist.md`.

---

## Why it fits Jason's proven pattern

- **It's the Recompile mod's Sky Frogs** - pack as vehicle, mod as engine; the same one-two that already shipped.
- **Cross-mod IS the content** - recycle any mod's items; the more mods in the pack, the bigger the teardown tree.
- **Data-driven** - garbage-block loot tables, teardown tables (with recipe-teaching), region weights, recovery odds are all JSON.
- **Proven format** - a tiered, quest-driven progression pack (Sky Frogs shape) on a memorable custom world.
- **A hook with a conscience** - "one man's trash," reclamation, healing a ruined world. Legible and shareable.

---

## Prior art (checked 2026-07-13) - theme validated, niche OPEN

- **Dumpster Diving** (CurseForge) - the near-exact core: dig **Garbage Blocks**, a **Landfill biome** with buried mounds, recycle scraps to resources (cans -> tin, tires -> rubber, circuit boards -> redstone). **But abandoned** - latest release is v1.3.3 for **MC 1.12.2, dated 2018-2020** (~6 years dead, ancient version). Proves the theme has appeal; leaves the niche empty on modern MC.
- **Scraps and Shards** / **Create Recycle Everything** / **Overly Complicated Garbage** - cover pieces (worldgen scrap piles; universal item recycling via Create - a *living* base worth considering; garbage production/disposal), not a dedicated garbage-world progression.
- Wasteland survival packs (Survive The Wasteland, Wastelands, Project X) - scarcity/scavenging theme, not garbage-block recycling. The "Garbage Disposal" / "Garbage Dump" packs read as casual/kitchen-sink.
- **Verdict:** the **Productive Bees -> Productive Frogs pattern** - a beloved-but-dead concept (Dumpster Diving) to rebuild modern and better. Don't build ON the corpse; a fresh **Recompile mod** (decided - see Architecture). Our two distinct axes - **teardown-as-knowledge** and **regrowing-mound quarries with the quarry-vs-heal tension** - are unclaimed by anything current.

## Cross-medium design influences (reviewed 2026-07-14)

Non-Minecraft games whose *proven-fun* loops map onto ours. Fulgora (above, line ~68) is one; **The Planet Crafter** (Miju Games, 1.0 April 2024) is the closest whole-game match and worth mining.

**What it is:** first-person survival + terraforming. Crash on a dead planet; raise a single global **Terraformation Index (Ti)** by running machines that pump out Oxygen/Heat/Pressure, then Biomass (plant/insect/animal). Ti climbs through named **stages** (Barren -> ... -> lush), and crossing thresholds both **unlocks new blueprint tiers** and **physically changes the world** (ice melts, lakes fill, grass and trees appear).

**Direct parallels + what to steal:**
1. **Blueprint microchips == teardown-as-knowledge, already shipped and validated.** You find microchips as loot in wrecks and spend them at a terminal to unlock recipes; they unlock in **tiers** (clear the whole current tier before the next opens; order within a tier is random). This is live proof that "find item -> gain recipe knowledge" carries a game. **Lesson:** tie knowledge gain to exploration + a deliberate station action, and let some recipes need multiple finds - a clean fit for our "study progress / 2-3 in-progress states."
2. **One global metric gates content AND heals the world.** Ti is a single legible number that unlocks tiers and makes the world visibly recover. Our mound-regrowth + reclamation endgame wants exactly this. **Lesson:** expose ONE north-star "reclamation index"; make the world change **diegetic** (blocks regrow/heal), not a menu unlock. Reinforces the "delivery is the signature visual" call (line 60).
3. **Recycler is materials-only.** PC breaks items into their base materials, full stop. That is precisely the axis we deliberately go *beyond* (recover the **recipe**, not just mats). **Lesson:** it confirms the differentiator - don't let teardown collapse into "just a recycler."
4. **Survival-early -> automation-late arc.** Hand-gather -> auto-extractors/crafters, gated by Ti. Mirrors our tier spine (hand-sort -> sort & automate). **Lesson:** gate automation behind the reclamation metric so early friction earns the payoff.
5. **Environmental storytelling for the ending.** PC hides its narrative in wrecks/logs and the finale recontextualizes everything - no exposition dumps. Direct support for our minimize-authored-prose rule and the `the_twist.md` quarantine: deliver the twist through the world.

**What NOT to copy:**
- **Survival meters (O2/water/food).** Trashlands is not a survival-pressure pack - the "still-active dump tide" pressure loop was already dropped (line 62). Keep tension in the quarry-vs-heal choice, not hunger bars.
- **Single linear planet.** PC is one biome-planet on a linear Ti track; we have **region bands + cross-mod teardown breadth**. Don't flatten that breadth into one linear meter.

**Open question it sharpens (feeds the reopened P3.9 reclamation decision in `design_decisions.md`):** is reclamation ONE global index (PC's Ti - maximally legible) or **per-region with a global roll-up** (fits our region bands)? Lean per-region + a headline global number, so a player both sees local progress and has one score to chase.

### WALL-E (Pixar, 2008) - the aesthetic + tonal anchor

**What to steal:**
1. **The cube-compactor visual is our block language, already proven iconic.** WALL-E's whole job is crushing trash into cubes and stacking them into towers. That is exactly our **Compacted Bale** block and the regrowing **mounds** - readable at a glance, stackable, memorable. Lean in: bales as a hero block, mound/tower silhouettes as the skyline.
2. **A whole world's story told nearly wordless.** The film's first act runs on almost no dialogue - the ruined world and its abandoned objects carry everything. Gold standard for our minimize-authored-prose principle: build meaning from placed blocks and found objects, not readables.
3. **Tone: melancholy + hope, not grimdark and not jokey.** A buried world whose throughline is care and restoration. Keeps us off both "gritty apocalypse" and "wacky trash," so the reclamation arc lands as earned and warm.

**Discipline:** keep this a note on look, block language, and storytelling craft only. Any narrative resonance is handled in `the_twist.md` (name-reference only, per its process rules) and the sanctioned quest surface - do not draw story parallels here.

## Architecture (decided 2026-07-13)

**One mod + one pack, more mods later if earned.** A single fresh companion mod (working name **Recompile**, NeoForge / MC 26.1) owns all custom systems to start: the garbage worldgen (coarse-dirt world preset, Blocks of Garbage and variants, garbage regions), the teardown-as-knowledge loop, and the mound-regrowth system. The pack owns curation, quests, tuning, and the cross-mod teardown tables (JSON datapack territory, extendable without mod releases).

Keep internal seams clean so systems can split into their own mods later - candidate: mound regrowth as a generic data-driven accumulation engine; Magnetism / Superposition stay parked in the shortlist. Don't pre-create repos for mods that don't exist. This supersedes the build-on-vs-new-mod question: not building on Create Recycle Everything (it can still appear in the pack as a mid-tier automation layer, not the foundation).

**Features are config-gated.** Every major system ships behind a config flag with tunable rates (regrowth rate, region band radii, knowledge odds). This lets playtesting pick winners instead of deciding on paper. Guardrail: flags are for tuning, not for avoiding decisions; the pack ships one opinionated default experience. Defaults are the design.

## Open questions

- **Is sifting the price, or is sifting the game? (opened 2026-07-15 - the big one.)** "Same verb at three speeds" (hand -> tarp -> machines) is a **ladder**, which says sifting is the *price* and the fun is buying your way out of it - Factorio's manual mining. That is a legitimate design, but it means the first hour must carry the whole fantasy and everything after is about escape, so sifting should be made *short*, never deep. The alternative is that sifting **is** the game, in which case it needs judgment back - and "everything found breaks down into materials", the rule that fixed the item-flood problem, has to go, because if every object is worth grabbing there is no decision left and sifting degrades into hoovering. Rarity, blueprints, the knowledge system and the flood all resolve differently depending on this answer. See "Why sifting garbage is fun" above.
- **Pack name** (working: Trashlands) and the Nether theme's name ("compacted depths" placeholder).
- **The quest-narrator question:** who wrote the quest book (see `the_twist.md` - spoilers).
- P2/P3 features not yet walked through - see the bookmark in [`design_decisions.md`](design_decisions.md).

## Next actions

1. Resume the feature-by-feature walkthrough at P2 (bookmark and ordered list: [`design_decisions.md`](design_decisions.md)).
2. One-week feasibility slice per the locked P0 spec. Throwaway if the world doesn't *feel* right.
