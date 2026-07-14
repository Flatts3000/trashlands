# Trashlands

*(working name - rename freely)*

A modpack concept: an **endless coarse-dirt plain crowded with mounds of Blocks of Garbage** - renewable quarries that regrow to their original size, raining back down from space. No ore, no trees - everything you build comes out of the trash. Rebuild, and eventually heal, a ruined world from its own garbage: grassing a mound's footprint retires it forever, so healing the world costs you your garbage income.

- **Status:** design walkthrough complete except the parked endgame/postgame (2026-07-14). No code yet. P0-P2 + most of P3 specified.
- **Full design:** [`docs/concept.md`](docs/concept.md); per-feature decisions + session bookmark: [`docs/design_decisions.md`](docs/design_decisions.md); material economy: [`docs/material_economy.md`](docs/material_economy.md).
- **What it showcases:** it's the intended showcase pack for the **Recompile** mod (garbage + recycling is the core). Pack lineup: Create (belts/logistics) and Mekanism (chemistry/radiation/energy) carry systems the Recompile mod deliberately doesn't build. **Magnetism** and **Superposition** stay parked as optional standalone-mod candidates. Mod shortlist: `F:\minecraft-repos\next-mod-concepts.md`.
- **The distinct hook:** teardown-as-knowledge (recover *recipes*, not just materials) on a world of **regrowing garbage mounds** - keep a mound as a renewable quarry, or heal its footprint and retire it forever. The endgame isn't beating a tide; it's no longer needing the dump.

Architecture (decided): **one companion mod + one pack** - a fresh Recompile mod (NeoForge / MC 26.1) owns the custom systems; more mods can split out later if earned. Prior-art pass is done (niche is open); next milestone is a one-week feasibility slice on the custom garbage worldgen.
