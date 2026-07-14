# Trashlands - Claude Code context

**What this is:** a Minecraft **modpack concept** (working name "Trashlands" - not final). An infinite flat world of coarse dirt buried horizon-to-horizon under piles of **Blocks of Garbage** - a still-active dump you race to out-process. No ore, no trees; everything you build comes out of the trash. Rebuild, and eventually heal, a ruined world from its own garbage.

**Status:** concept only (2026-07-13). **No code yet.** This repo is design docs.

## Read first
- [`docs/concept.md`](docs/concept.md) - the full design (vision, worldgen, the "garbage keeps coming" mechanic, tier spine, prior-art pass, open questions). **Start here.**
- [`README.md`](README.md) - the one-paragraph pitch.
- `F:\minecraft-repos\next-mod-concepts.md` - the parent mod shortlist and the design rules (DNA criteria, "prior art informs, doesn't veto").

## The core (what to actually build)
Garbage + recycling. A **Salvage** loop: dig a Block of Garbage -> mixed trash -> sort -> tear down / recycle -> materials **plus recovered recipes** (teardown-as-knowledge is the distinct axis). Cross-mod teardown = the compat surface is the content. **Magnetism and Superposition are noted as OPTIONAL, not explored - do not build them into the pack** unless the plan changes.

## Architecture (decided 2026-07-13)
**One mod + one pack, more mods later if earned.** A single fresh companion mod (working name **Salvage**, NeoForge / MC 26.1) owns all custom systems to start: garbage worldgen, Blocks of Garbage, teardown-as-knowledge, and later the pressure system. The pack owns curation, quests, tuning, and cross-mod teardown tables (JSON). Keep internal seams clean so systems can split into their own mods later; don't pre-create repos. Not building on Create Recycle Everything (it may appear in the pack as mid-tier automation, not the foundation).

Prior-art pass is done (see concept.md): the near-exact mod, **Dumpster Diving**, is abandoned on MC 1.12.2 (2018-2020). Niche is open - this is the Productive Bees -> Productive Frogs move (rebuild a beloved-but-dead concept modern).

## Next actions
1. Lock the "garbage keeps coming" mechanic (rate, wind-in vs dump, pressure not punishment).
2. Sketch the tier-one loop end to end (spawn -> first sorted materials -> first machine).
3. One-week feasibility slice: the custom garbage worldgen + one garbage block that tears down into sorted materials. Throwaway if the world doesn't *feel* right.

## Conventions (this machine / Jason's mod work)
- Target **NeoForge / MC 26.1** to match the Productive Frogs 2.x line (siblings: `../productive-frogs`, `../sky-frogs` - the proven pack+mod pattern to mirror).
- Data-driven first (JSON content: garbage-block loot/teardown tables), shippable in small increments.
- **No em-dashes or en-dashes, no emoji** in any authored text (Jason's hard rule). ASCII punctuation only.
- Pack-authored text (quests, changelogs, guides) uses the `quest-voice` skill + spec in `../mc-pack-toolkit`.
- Docs in `/docs` are snake_case.
