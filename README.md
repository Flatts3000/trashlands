# Trashlands

A modpack for Minecraft 26.1.2 / NeoForge. An endless coarse-dirt plain crowded with mounds of
**Blocks of Garbage** - renewable quarries that regrow to their original size, raining back down
from space. No ore, no trees. Everything you build comes out of the trash.

Mine a mound and it grows back. Heal the ground underneath it and it is gone for good. That is the
tension the pack runs on: garbage is your only income, and the only way to make the world green is
to give that income up.

- **Status:** **alpha, released.** Latest is `v0.11.0` (2026-09-03), which brings in Recompile 0.16.0
  and 0.17.0 - cardboard you can build with on the first day, a cooling tower and smoking chimneys on
  the skyline, and a powered vacuum that clears a mound faster than a pickaxe
  - on [GitHub Releases](https://github.com/Flatts3000/trashlands/releases) and CurseForge (project
  `1636627`). The pack is 64 mods on Minecraft 26.1.2 / NeoForge 26.1.2.100. If you are hand-building
  an instance, match the loader to the release you downloaded rather than to this line; `v0.9.0` and
  earlier declare 26.1.2.94. Releases are tag-driven - see
  [`docs/release_checklist.md`](docs/release_checklist.md).
- **The engine:** [Recompile](https://github.com/Flatts3000/recompile), a standalone NeoForge mod
  that owns the garbage world, teardown, the machines, and the reclamation ladder. Trashlands is its
  showcase pack (the Productive Frogs -> Sky Frogs pattern).
- **The distinct hook:** teardown-as-knowledge - recover *recipes*, not just materials - on a world
  of regrowing garbage mounds. Keep a mound as a renewable quarry, or heal its footprint and retire
  it forever. The endgame is not beating a tide; it is no longer needing the dump. Both halves are built: teardown returns materials and Idea Fragments, and mounds regrow so the
  quarry-versus-heal choice is a real one.

## Docs

- [`docs/concept.md`](docs/concept.md) - the full design.
- [`docs/feature_matrix.md`](docs/feature_matrix.md) - every feature by priority, and the build order.
- [`docs/design_decisions.md`](docs/design_decisions.md) - the locked-decisions log and the session bookmark.
- [`docs/pack_setup.md`](docs/pack_setup.md) - the mod lineup, packwiz commands, test instances.
- [`docs/distribution.md`](docs/distribution.md) - channels, versioning, CurseForge API quirks.
- [`docs/release_checklist.md`](docs/release_checklist.md) - how to cut a release.
- [`docs/curseforge_page.md`](docs/curseforge_page.md) - the CurseForge listing copy.

## License

MIT for pack-authored content. Each bundled mod keeps its own license.
