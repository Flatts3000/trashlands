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
- [x] **Pack filled out** - 43 mods pinned via `packwiz curseforge add`.
- [x] **Icon** - `pack/icon.png`, 512x512, 316 KB. The TRASH / LANDS wordmark; see
  [`branding.md`](./branding.md).
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

## The server pack

`tools/build_server.py` builds `dist/trashlands-server-<version>.zip`, and `release.yml` runs it on
every tag: the zip is attached to the GitHub release and uploaded to CurseForge as a `parentFileID`
child of the client file.

**The mod list comes from the `side` tags.** packwiz-installer runs with `-s server`, taking
`both` and `server` and skipping `client`, so what a server gets is decided entirely by
`side =` in `pack/mods/*.pw.toml`. Ten mods are `client` today; the other 37 go to servers. A
client-only mod mistagged `both` reaches a dedicated server and can crash boot, which is why the
release does three things about it. A guard reads `side =` out of `pack/mods/*.pw.toml` and fails if
any client-tagged mod's recorded `filename` turns up in `build/server/mods/`, so a client mod added
later is covered with no edit and the check cannot drift from the jars. `check_pack_deps.py` then
runs a second time against the installed server set, because its normal pass resolves `-s both` and
so cannot see a break caused by the split itself. Last, a **boot smoke test** installs NeoForge,
waits for `Done (`, and then **asserts the generated terrain actually came from the garbage
preset**, via `tools/inspect_world_terrain.py`. Booting alone proves nothing about the world type,
since an unknown `level-type` falls back to `minecraft:normal` without erroring.

That check reads the region files, not `level.dat`. Three earlier attempts read `level.dat` and all
three were looking in the wrong file: the v0.8.0 release log showed it holding 2436 bytes and a
single namespaced id, `minecraft:overworld`, with no generator id of any namespace - and a vanilla
world would have to record its generator somewhere too, so that absence proved nothing either way.
The terrain check looks for any `recompile:` id in the chunk data, which hits the per-section biome
palette and therefore appears in **every** generated chunk rather than only where a garbage mound
happened to spawn. Verified both ways against real worlds on disk before it went in: a Trashlands
save reports `recompile:household_sprawl` and friends, an unrelated modded save reports none.

**A wrong world now fails the release.** A world it cannot read does not - "I could not tell" exits
2 and warns, because conflating that with "it failed" is exactly what killed a release whose pack
was fine (#32).

**It ran for the first time in the v0.9.0 release, and it passed**, which is the answer #32 had been
after since 2026-08-18 and failed to get three times:

```
save confirmed in boot.log
--- world type check ---
4 region file(s), 529 chunk(s) read, 529 with a biome palette
the preset applied. recompile: ids in the terrain:
    1176  recompile:household_sprawl
     159  recompile:mound_ground
```

A server world does generate as Trashlands. Note the middle line: every one of the 529 chunks had a
biome palette, which is what makes the absence of a `recompile:` id meaningful rather than merely
unobserved. The clean `stop` is load-bearing - `kill` on the wrapper orphans the JVM, no save runs,
and there would be no region files to read at all.

**The world type is set here, not by a mod.** Default World Type is client-only, so the server pack
ships `level-type=recompile:garbage` in `server.properties`. Without that line a server generates an
ordinary overworld, and because world generation is decided once at creation, the only fix is
deleting `world/` and starting again.

**Typing it as a Server Pack is manual, every release.** CurseForge's upload API cannot set the flag:
`upload-file` accepts changelog, changelogType, displayName, parentFileID, gameVersions, releaseType,
isMarkedForManualRelease and relations, and an `isServerPack` field is silently ignored
(henkelmax/upload-curseforge-modpack-action#1, confirmed by CF support). Uploading with
`parentFileID` makes the zip an *additional file*, which is visible and downloadable but is not the
same thing. Host one-click deploys - BisectHosting, Nodecraft, Pterodactyl eggs,
itzg/docker-minecraft-server `AUTO_CURSEFORGE` - read `isServerPack`/`serverPackFileId` from the Core
API and cannot see an untyped file.

So after every release: Authors Console -> Trashlands -> Files -> the client file -> the attached
server file -> **Additional File Info** -> `Server Pack`. The release run prints this as a warning
and a step-summary reminder. Verify with `python tools/check_server_pack_flag.py`, which reads the
website's v1 API and reports any attached-but-untyped file. Sky Frogs shipped 29 untyped files before
anyone noticed, which is why the checker exists rather than a note in someone's head.

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
