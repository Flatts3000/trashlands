# CurseForge submission checklist

One-time guide for the first Trashlands project submission. Once the slug is claimed and the project
is approved, releases ship automatically via [`.github/workflows/release.yml`](../.github/workflows/release.yml)
and this doc goes quiet.

Cross-references: page copy is in [`curseforge_page.md`](./curseforge_page.md); the channel decision
and versioning policy are in [`distribution.md`](./distribution.md); the per-release do-list is
[`release_checklist.md`](./release_checklist.md).

## Before you start

- [x] **Pack icon ready** - `pack/icon.png`, 400x400 RGB PNG, 335 KB. Under CurseForge's 500 KB
  ceiling. Cropped from `../recompile/docs/cf image gallery/01-garbage-world.jpg` (an in-game
  screenshot with no HUD), so it is not AI-generated and carries no trademarked asset. **It is a
  placeholder** - a real logo with a wordmark would serve the listing better; swap it in whenever
  one exists, the file path does not change.
- [x] **`pack/pack.toml` version = `0.1.0`** - the manifest version CurseForge reads.
- [x] **Export builds clean** - `packwiz refresh && packwiz curseforge export` from `pack/` produces
  `Trashlands-0.1.0.zip`, ~1 KB, manifest + modlist only. **No `.jar` anywhere in the zip** - the
  five mods are CurseForge project/file references. `release.yml` asserts this.
- [ ] **CurseForge account** in good standing (no active project bans).

## Step 1 - Create the project

<https://www.curseforge.com/dashboard/projects/create>

Fields are in [`curseforge_page.md`](./curseforge_page.md) under "Project creation form" - name,
summary, class, categories, social links - and the Description body is everything below that doc's
`PASTE MARKER` comment. Paste it as-is; it needs no editing.

Submit for review. CurseForge moderation is typically 1-3 business days.

## Step 2 - Wire the project id into CI  *(DONE)*

The project is **`1636627`** ([Authors Console](https://authors.curseforge.com/#/projects/1636627/files)).
Both repo settings are already set:

```sh
gh variable set CF_PROJECT_ID --body "1636627"
grep '^CURSEFORGE_API_KEY=' ../recompile/.env | cut -d= -f2- | tr -d '\r\n' | gh secret set CF_API_TOKEN
```

The upload token is the same one in `../recompile/.env` as `CURSEFORGE_API_KEY` - same author
account, and it works for any project that account owns. Piping it via stdin keeps it out of the
shell history and the terminal.

Until `CF_PROJECT_ID` is set, `release.yml` ships the GitHub release and prints a job-summary notice
explaining the skip. That was the intended degraded state; it no longer applies.

## Step 3 - Upload the first file

Tag-driven is the normal path (see [`release_checklist.md`](./release_checklist.md)):

```sh
git tag v0.1.0 && git push origin v0.1.0
```

If the project is still in moderation, or CI is unavailable, upload by hand:

```sh
python tools/cf_release.py --zip "pack/Trashlands-0.1.0.zip" --project <id> \
    --display-name "Trashlands 0.1.0" --release-type alpha --changelog-file release_notes.md
```

**Release type is `alpha` for the 0.x line.** Mark it explicitly so players arrive with the right
expectations - the pack has no quest book and its balance numbers are first-pass.

The web-form fallback, if both of the above fail:

| Field | Value |
|---|---|
| File | `pack/Trashlands-0.1.0.zip` |
| Display name | `Trashlands 0.1.0` |
| Release type | **Alpha** |
| Game version | `26.1.2` (pick by name; the web form resolves the id for you) |
| Mod loader | `NeoForge` (`26.1.2.94`) |
| Java version | Skip. The modpack class takes no Java selector and the API rejects one. |

## Step 4 - After approval

- [ ] **Gallery** - the shots already exist at `../recompile/docs/cf image gallery/` (garbage world,
  Bulky Waste finds, scrap bins, machines on reclaimed grass, tree nursery, compost heap, demolition
  yard, cutting torch, reinforced concrete, cupola furnace, collectibles). They were captured for the
  mod's page and show the same content the pack ships.
- [ ] **Cross-link from the Recompile mod page** - "Featured in the Trashlands modpack", pointing at
  the new slug. Recompile is project `1625740`.
- [ ] **Update `docs/distribution.md`** with the live slug and project id.

## What CurseForge bounces you for

- **Missing icon.** The single most common rejection. Do not submit without one.
- **Short or placeholder description.** Moderators want to know what the pack is; the
  `curseforge_page.md` body is well past that bar.
- **Bundled mod jars.** A modpack manifest references mods by `projectID` / `fileID`, never by
  bundled jar. `packwiz curseforge export` does this correctly as long as every mod was added with
  `packwiz curseforge add`. A mod added from Modrinth gets inlined into `overrides/mods/` as a real
  jar, and that is a redistribution violation. `release.yml`'s export step greps the zip for `.jar`
  and fails the run if it finds one.
- **License mismatch.** The project license, the manifest `author` field, and bundled-mod
  attribution have to agree. Trashlands is MIT for pack content, with the per-mod disclaimer already
  in the page copy.

## Troubleshooting

- **"Project name already exists"** - someone holds `trashlands`. The internal pack name in
  `pack.toml` can stay `Trashlands`; only the CurseForge URL slug would change.
- **"File rejected: invalid manifest"** - usually a mod with a missing or mismatched `projectID`.
  Run `python tools/pack_refresh.py`, then re-export.
- **`errorCode 1009: Invalid game version ID`** - a game-version id from the wrong type was sent.
  `26.1.2` exists three times in CurseForge's version list (id `16082` under type `83806`
  `minecraft-26-1`, id `16085` under type `1`, id `16130` under type `615` `addons`) and only
  `16082` is valid here. `release.yml` resolves this by filtering on type slug; see the comment on
  its "Build CurseForge metadata" step.
- **Recompile shows a download error during a reviewer's test install** - check whether Recompile's
  CurseForge project has third-party API distribution enabled. The CurseForge launcher (first-party)
  downloads it either way, but `packwiz-installer` and other third-party tools cannot fetch a
  project that opted out.
