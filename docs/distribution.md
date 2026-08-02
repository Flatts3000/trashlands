# Distribution

How Trashlands ships, where players install it from, and how releases happen. The step-by-step
do-list is [`release_checklist.md`](./release_checklist.md); this is the narrative.

Modelled on `../sky-frogs/docs/distribution.md`, which is the proven pipeline. Where this differs,
the reason is stated.

## Channels

| Channel | URL pattern | Format | Primary? |
|---|---|---|---|
| **CurseForge** | `curseforge.com/minecraft/modpacks/trashlands` | manifest zip | Yes |
| **GitHub Releases** | `github.com/Flatts3000/trashlands/releases` | CF zip mirror | Artifact mirror, not an install path |

**CurseForge is the player-facing channel.** GitHub Releases mirrors each tag's zip for rollback and
source-of-truth artifact hosting.

### CurseForge only

**Closed 2026-08-02, when the FTB stack was added.** Modrinth is not an option, for exactly the
reason it is not one for Sky Frogs: the FTB utility mods are **CurseForge-exclusive**.
`packwiz modrinth export` inlines a CF-only mod into the zip as a real `overrides/mods/*.jar`, and
Modrinth's uploader rejects that on redistribution grounds.

This was briefly open. Until the FTB stack landed, every mod in the lineup was published on both
platforms and a Modrinth release was mechanically possible. FTB Quests is the design's named quest
engine and the narrative's vehicle, so the trade was made knowingly: the quest book is worth more
than the second storefront.

Reopening it would mean dropping FTB Library, Quests, Teams, Chunks, and Essentials and finding
non-FTB equivalents - a different quest engine and a standalone minimap. Not planned.

## Setup checklist (one-time, before v0.1.0)

- [x] **GitHub repo** - `Flatts3000/trashlands`, public.
- [x] **Pack fills out** - five mods pinned via `packwiz curseforge add`, `pack.toml` at `0.1.0`.
- [x] **Icon** - `pack/icon.png`, 400x400, 335 KB. Placeholder; see
  [`cf_submission_checklist.md`](./cf_submission_checklist.md).
- [x] **Release pipeline** - `.github/workflows/release.yml`, tag-driven.
- [x] **CurseForge project created** - project ID **`1636627`**
  ([Authors Console](https://authors.curseforge.com/#/projects/1636627/files)). Awaiting moderation
  at time of writing.
- [x] **Repo variable `CF_PROJECT_ID`** = `1636627`. Public, so a variable and not a secret.
- [x] **Repo secret `CF_API_TOKEN`** - the CurseForge upload token. Same value as
  `CURSEFORGE_API_KEY` in `../recompile/.env`; same author account, so it works for this project too.
- [ ] **Gallery** - upload shots to the CF project page.

### CurseForge upload API quirks

**Game-version ids must come from the right version type.** A Minecraft version name appears several
times in CurseForge's version list under different types, and only one is valid for a modpack:

| Name | id | type | Valid for a modpack? |
|---|---|---|---|
| `26.1.2` | **16082** | 83806 `minecraft-26-1` | **yes** |
| `26.1.2` | 16085 | 1 (mod-class) | no, `errorCode 1009` |
| `26.1.2` | 16130 | 615 `addons` | no, `errorCode 1009` |
| `NeoForge` | **10150** | 68441 `modloader` | **yes** |

Sky Frogs hardcodes its pair (`[11779, 10150]` for MC 1.21.1). We do not: both `release.yml` and
`tools/cf_release.py` resolve the ids from the API at release time, filtering on the type slug
(`minecraft-*`, excluding snapshots). Hardcoding is a landmine that goes off on the next MC bump,
and the resulting error arrives after the whole zip has uploaded.

**Do NOT send a Java-version id** in a modpack's `gameVersions`. CurseForge rejects it. Java is
implied by the loader. (Mod uploads are the opposite case - Recompile's `release.yml` does send one.)

**The environment group (Client / Server) is not required for modpacks.** It is for mods: Recompile
v0.4.0 came back `errorCode 1021: You must select at least one version from the environment group`
after its GitHub release had already shipped. Sky Frogs has published ~30 modpack files with only
`[MC, loader]`, so the modpack class does not demand it. If a future upload returns 1021, add the
Client (`9638`) and Server (`9639`) ids.

## Release workflow

Releases are a tag push:

```sh
git tag v0.1.0
git push origin v0.1.0
```

`.github/workflows/release.yml` then:

1. Asserts `pack/pack.toml`'s version matches the tag.
2. Asserts the committed `index.toml` is current (runs `packwiz refresh` and fails on any diff) - a
   stale index ships hashes no committed file has, and packwiz-installer rejects the jars it just
   downloaded.
3. Runs `packwiz curseforge export`, then greps the zip for `.jar` and fails if it finds one. A jar
   in the export means a mod was added from a non-CurseForge source and got inlined into
   `overrides/`, which is a redistribution violation CurseForge would bounce.
4. Extracts the matching `## [x.y.z]` section of `CHANGELOG.md`.
5. Creates a GitHub release with the zip attached, marked prerelease for `0.x`.
6. Resolves the CurseForge game-version ids and uploads, with `releaseType: alpha` for `0.x`.

Steps 6 is skipped with a job-summary notice if `CF_PROJECT_ID` (variable) or `CF_API_TOKEN`
(secret) is unset. The GitHub release still ships. That is the intended state until the CurseForge
project is approved.

Manual fallback: `python tools/cf_release.py --zip <path> --project <id> ...`.

## Versioning policy

Pre-1.0, so SemVer is not yet strict:

- **`v0.x.y`** - alpha. `x` for content milestones or a mod-lineup change, `y` for fixes and tuning.
- **`v1.0.0`** - the launch release, out of alpha. Gate on: the knowledge half of teardown shipped,
  a quest book, and one full balance pass across all loot tables and recipes together.
- **Post-1.0** - major = world-breaking, minor = new content, patch = fixes.

`releaseType` on CurseForge is derived from the version: `0.x` uploads as **alpha**, `1.x+` as
**release**.

## Changelog

`CHANGELOG.md` at repo root, [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. The
`## [X.Y.Z]` heading shape is load-bearing - `release.yml` regex-extracts that section for both the
GitHub release notes and the CurseForge changelog. ASCII punctuation only.

Write it player-facing: lead with what changed for the player, not the internal ticket.

## Not built yet

- **Server pack.** Sky Frogs ships `tools/build_server.py` and treats a client-only release as a
  failed release, with the server zip attached to the GitHub release and uploaded to CurseForge as a
  `parentFileID` child file. Trashlands has no server pack. It is worth having (a garbage world is a
  good multiplayer premise) but it needs pack `config/` to exist first, which the alpha does not have.
  Note for when it lands: CurseForge's upload API **cannot** flag a child file as a Server Pack, so
  typing it is a manual Authors Console step every release, and untyped server packs are invisible to
  host one-click deploys. Sky Frogs shipped 29 untyped files before noticing.
- **Config validation CI.** Sky Frogs' `validate-pack.yml` enforces that `pack/config/` and
  `pack/defaultconfigs/` stay byte-identical, because `config/` is per-instance state that NeoForge
  can recreate from `defaultconfigs/`. Earns its keep once the pack ships configs.
- **Dev instance sync.** Sky Frogs' `tools/sync_instance.py` drives packwiz-installer into a
  junction-linked CurseForge instance for playtesting. Recompile's own `run/` covers mod-side
  iteration today; port this when pack-side tuning starts.

## Issue reporting

- **Bugs and balance:** GitHub Issues at `github.com/Flatts3000/trashlands/issues`. Mod-side bugs
  belong on `github.com/Flatts3000/recompile/issues`; most alpha reports will be mod-side.

## License

MIT for pack-authored content. Each bundled mod keeps its own license - the CurseForge page carries
that disclaimer.
