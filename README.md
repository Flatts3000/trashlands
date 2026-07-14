# Trashlands

*(working name - rename freely)*

A modpack concept: an **infinite flat world of coarse dirt, buried horizon-to-horizon under piles of Blocks of Garbage.** You spawn into an endless, still-active dump with no ore and no trees - everything you build comes out of the trash. Rebuild, and eventually heal, a ruined world from its own garbage.

- **Status:** concept only (2026-07-13). No code yet.
- **Full design:** [`docs/concept.md`](docs/concept.md).
- **What it showcases:** it's the intended showcase pack for the **Salvage** mod (garbage + recycling is the core). **Magnetism** and **Superposition** are noted as optional, not explored - they could fit (magnetic separation is how real recycling sorts waste; a garbage block as a probability cloud) but the pack doesn't depend on either. Mod shortlist: `F:\minecraft-repos\next-mod-concepts.md`.
- **The distinct hook:** teardown-as-knowledge (recover *recipes*, not just materials) on a **still-active dump that keeps re-burying you** - the game is the race to out-process the incoming garbage until your cleared frontier grows faster than it's buried.

Architecture (decided): **one companion mod + one pack** - a fresh Salvage mod (NeoForge / MC 26.1) owns the custom systems; more mods can split out later if earned. Prior-art pass is done (niche is open); next milestone is a one-week feasibility slice on the custom garbage worldgen.
