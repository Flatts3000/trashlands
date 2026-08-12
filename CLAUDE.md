# Trashlands - Claude Code context

**What this is:** a Minecraft **modpack**, named **Trashlands** (locked 2026-08-02 - the CurseForge slug is claimed, so the name is no longer up for grabs). An endless coarse-dirt plain crowded with mounds of **Blocks of Garbage** that regrow to their original size - renewable quarries raining back down from space, never impending doom. No ore, no trees; everything you build comes out of the trash. Rebuild, and eventually heal, a ruined world from its own garbage - healing a mound's footprint retires it forever, trading the mineral economy for the biological one the healed land produces (P2.4-R). But the junkyard fights back: healed ground erodes from its edge inward until the reclamation ladder locks it (P1.7-R).

**Status: alpha, shipping (v0.5.0, 2026-08-12).** The pack is **assembled and pinned** - 47 mods, MC 26.1.2 / NeoForge 26.1.2.94 - and the tag-driven release pipeline is in (`.github/workflows/release.yml` -> GitHub release + CurseForge upload). CurseForge project **`1636627`**, slug `trashlands`; `CF_PROJECT_ID` and `CF_API_TOKEN` are set on the repo. Recompile is at v0.9.0 and released on CurseForge (project `1625740`).

On the design side: walkthrough complete except the parked endgame/postgame cluster (2026-07-14). P0-P2 and most of P3 are fully specified; the endgame is reopened and postgame/final-chapter is parked - see the bookmark in `docs/design_decisions.md`.

## Read first
- [`docs/concept.md`](docs/concept.md) - the full design (vision, worldgen, mound regrowth, tier spine, prior-art pass, open questions). **Start here.**
- [`docs/feature_matrix.md`](docs/feature_matrix.md) - every feature by priority (P0 slice -> P3 polish) and feasibility. The build order.
- [`docs/design_decisions.md`](docs/design_decisions.md) - the per-feature locked-decisions log + **the session bookmark** (walkthrough status, what to resume next).
- `docs/the_twist.md` - **FULL SPOILERS.** The hidden narrative layer. Read before writing any quest text or player-facing copy; never reference its contents anywhere else.
- [`docs/quest_voice.md`](docs/quest_voice.md) - how quest text is written here, and the Sky Frogs failure it exists to avoid. Read before authoring any player-facing copy.
- [`docs/pack_setup.md`](docs/pack_setup.md) - the locked mod lineup, packwiz commands, and how to stand up a test instance.
- [`docs/distribution.md`](docs/distribution.md) + [`docs/release_checklist.md`](docs/release_checklist.md) - how releases ship, and the CurseForge API traps (game-version ids are resolved, never hardcoded).
- [`docs/curseforge_page.md`](docs/curseforge_page.md) - the CurseForge listing copy. Edit here, paste to CF.
- [`README.md`](README.md) - the one-paragraph pitch.
- `F:\minecraft-repos\next-mod-concepts.md` - the parent mod shortlist and the design rules (DNA criteria, "prior art informs, doesn't veto").

## The core (what to actually build)
Garbage + recycling. A **Recompile** loop: dig Blocks of Garbage (they drop themselves) -> sort (hand pick-through -> Sorting Tarp -> machines) -> tear down found items at the Recompile Workbench -> materials **plus schematics** (teardown-as-knowledge is the distinct axis; survival crafts free, technology locked until learned). Cross-mod teardown = the compat surface is the content. **Magnetism and Superposition are noted as OPTIONAL, not explored - do not build them into the pack** unless the plan changes.

## Architecture (decided 2026-07-13)
**One mod + one pack, more mods later if earned.** A single fresh companion mod, **Recompile** (NeoForge / MC 26.1, standalone/world-agnostic - the Productive Frogs role; this pack is its showcase), owns all custom systems to start: garbage worldgen, Blocks of Garbage, teardown-as-knowledge, and mound regrowth. Recompile lives in its own sibling repo (`../recompile`, GitHub `Flatts3000/recompile`); this repo (`trashlands`) is the pack. The pack owns curation, quests, tuning, and cross-mod teardown tables (JSON). Keep internal seams clean so systems can split into their own mods later. Not building on Create Recycle Everything (it may appear in the pack as mid-tier automation, not the foundation). **Features are config-gated** with tunable rates - playtesting picks winners, but the pack ships one opinionated default experience; defaults are the design.

Prior-art pass is done (see concept.md): the near-exact mod, **Dumpster Diving**, is abandoned on MC 1.12.2 (2018-2020). Niche is open - this is the Productive Bees -> Productive Frogs move (rebuild a beloved-but-dead concept modern).

## The alpha mod lineup (locked 2026-08-02)
**47 mods.** Core six: **Recompile** (1625740) plus the four it actually integrates with - **JEI** (Recompile ships a JEI plugin), **Jade** (15 providers), **Modonomicon** (the guidebook engine), **Pipez** (the automation policy is written and tested against it) - and **Spawn Detective** (1621450, ours, `../spawn-detective`), which names the rule blocking a mob from spawning at a given block; the animals rung of the reclamation ladder is exactly that question. Then a **QoL layer** ported from the Sky Frogs stack and filtered to what has a 26.1.2 CurseForge build (inventory/UI, performance, GraveStone, Simple Backups, sound muffling), the **FTB stack** (Library, Quests, Teams, Chunks, Essentials, XMod Compat for JEI-in-the-book), a **tech and gadget layer** (Powah for FE, plus the Direwolf20 gadgets), **world-type enforcement** (Default World Type), **FancyMenu** for the title screen, and the auto-pulled libraries. Full table and the considered-but-cut list are in `docs/pack_setup.md`.

**One consequence of the FTB stack.** It is CurseForge-exclusive, so **Modrinth is closed to this pack** (`docs/distribution.md`).

**Quest content** is `pack/config/ftbquests/quests/` - **JSON5, not SNBT**: chapters in `chapters/*.json5`, text in `lang/en_us/` (chapter titles in `chapter.json5`, quest text in `chapters/<name>.json5`), plus `data.json5` and `chapter_groups.json5` at the root. FTB Quests on MC 26.x reads no `.snbt` at all, and a missing `data.json5` makes the whole book load empty with no in-game error - which is how v0.2.0 and v0.3.0 both shipped a Welcome chapter no player could see. Sky Frogs is a **voice** reference and **not** a format one; it is a major version behind. Today: **Welcome** and **Salvage**, 22 quests, shipped in v0.5.0. Salvage runs to a Bucket of Water; a chapter ends on an object the player can hold, not a tier boundary. Chapter names are operational; the `The Way Home` spine (per `the_twist.md`) is deferred until the endgame exists. **Read [`docs/quest_voice.md`](docs/quest_voice.md) before writing any quest text**, and use the `quest-voice` skill - the pack doc carries this world's register (flat and practical, not Sky Frogs' dry wit) and the failure it is avoiding.

Cut on purpose: **Sophisticated Storage** (would make Recompile's Scrap Network dead content), **Waystones** (travel cost may be pacing), **Forgiving Void** (skyblock baggage - this world seals the void under bedrock).

**Create and Mekanism are dead on 26.1.2** - neither has a NeoForge build past 1.21.1 (checked, `../recompile/docs/hydroponics_spec.md`). Any doc still planning them is stale. Energy mods (Powah, AE2) interoperate for free via `Capabilities.Energy.BLOCK` but are deliberately out of the alpha: *when* the player gets power is a pack decision that has not been made.

**Never `packwiz modrinth add`** for this pack. Modrinth-sourced mods get inlined into the CurseForge export as real jars, which is a redistribution violation. Use `packwiz curseforge add`; the release workflow greps the export for `.jar` and fails the run.

## Next actions
1. **Chapter three** - the Scrap Network and storage (issue #11). The adjacency rule itself is taught inside Salvage as of v0.5.0, so what is left is the tier the barrel does not cover: Scrap Bins and binding a bin to one material, the Filing Cabinet, and the payoff of crafting straight out of the cluster.
2. **Paste the CurseForge description** from `docs/curseforge_page.md` and upload the gallery. The live page is behind the repo copy.
3. **Design the endgame** (reopened - circular economy cut). Then the postgame/final chapter (against `the_twist.md`). Bookmark in `docs/design_decisions.md` has the three seed directions.
4. **Toward 1.0:** the knowledge half of teardown, the `The Way Home` quest spine, and one balance pass across all loot tables and recipes together. Gate list in `docs/release_checklist.md`.

## Conventions (this machine / Jason's mod work)
- Target **NeoForge / MC 26.1** to match the Productive Frogs 2.x line (siblings: `../productive-frogs`, `../sky-frogs` - the proven pack+mod pattern to mirror).
- Data-driven first (JSON content: garbage-block loot/teardown tables), shippable in small increments.
- **No em-dashes or en-dashes, no emoji** in any authored text (Jason's hard rule). ASCII punctuation only.
- **Minimize authored prose.** Only two sanctioned writing surfaces: quests and technical guidance. No ambient lore documents, archivist notes, or readable flavor text - players distrust AI writing. Carry meaning through environment and mechanics, not prose.
- Pack-authored text (quests, changelogs, guides) uses the `quest-voice` skill + spec in `../mc-pack-toolkit`.
- Docs in `/docs` are snake_case.
