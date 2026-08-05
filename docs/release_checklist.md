# Release checklist

Step-by-step for cutting a Trashlands release. The narrative and the why live in
[`distribution.md`](./distribution.md); this is the do-list. Releases are **tag-driven** - pushing a
`vX.Y.Z` tag fires [`.github/workflows/release.yml`](../.github/workflows/release.yml), which builds
and publishes everything.

## 0. Pick the version

Pre-1.0 (see [`distribution.md`](./distribution.md#versioning-policy)):

- **patch** (`0.1.0 -> 0.1.1`): fixes, config tuning, a mod version bump.
- **minor** (`0.1.1 -> 0.2.0`): new content, a mod added or removed, a Recompile feature wave.

Only release what is already on `main`.

## 0.5. Check the pins

Two pins drift silently and both ship to every new downloader.

1. **Recompile.** The pack tracks the mod, and the mod moves fast. Check whether a newer release
   exists (`gh release list --repo Flatts3000/recompile --limit 3`) and whether it is on CurseForge
   yet - the pack can only pin a *published* CF file.

   ```sh
   cd pack && packwiz update recompile -y
   ```

2. **NeoForge.** Compare `pack/pack.toml`'s `[versions] neoforge` against the latest 26.1.x:

   ```sh
   curl -s https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml \
     | grep -oE "26\.1\.[0-9.]+" | sort -V | tail -3
   ```

   **The pack and Recompile must never drift apart on loader version.** If the mod's toolchain moves,
   move the pack with it. Sky Frogs shipped v1.5.3 with an untested loader because its dev instance
   was on a different build than the pack pinned - the launch test was worthless.

3. **Everything else.** `cd pack && packwiz update --all`, then:

   ```sh
   python tools/check_pack_deps.py     # must exit 0
   ```

   This downloads every pinned jar and reads its `neoforge.mods.toml`, failing if a required
   dependency is missing from the pack or if any mod needs a loader newer than the pin. **A mod
   declaring `neoforge [X,)` above the pin does not warn, it refuses to load**, so the pack boots
   looking correct with a mod silently absent. `v0.1.0`'s first lineup pinned `26.1.2.76` while JEI
   needed `[26.1.2.81,)` and Balm needed `[26.1.2.93,)`.

   The pin is the highest lower bound any bundled mod requires - not Recompile's build number. Raise
   `[versions] neoforge` in `pack/pack.toml` to whatever the tool names, then re-run
   `tools/pack_refresh.py`.

   The same check runs on every PR (`validate-pack.yml`) and as a release guard, so this step is
   belt-and-braces rather than the only line of defence.

## 1. Cut the release (on `main`, clean tree)

1. `git checkout main && git pull` - working tree clean.
2. **CHANGELOG.md**: rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add a one-line summary
   under the heading, and leave a fresh empty `## [Unreleased]` above it. The heading MUST be
   exactly `## [X.Y.Z]` - `release.yml` regex-extracts that section for the GitHub release notes and
   the CurseForge changelog. ASCII punctuation only.
3. **pack/pack.toml**: bump `version = "X.Y.Z"`. It MUST equal the tag; the workflow's guard step
   fails the release otherwise.
4. `python tools/pack_refresh.py` - LF-normalizes, regenerates `index.toml`, and updates pack.toml's
   `[index]` hash. **Stage `pack/index.toml` AND `pack/pack.toml` in the SAME commit** as the
   version bump. Nothing else catches a stale index until the workflow's guard rejects it.
5. Commit on `main`: `commit "chore: release vX.Y.Z" "<one-line body>"`.
6. `git push`
7. `git tag vX.Y.Z && git push origin vX.Y.Z`

## 2. Watch the pipeline

```sh
gh run watch $(gh run list --workflow release.yml --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status
```

Steps: version guard -> index guard -> CF export (+ no-jar assertion) -> changelog extract -> GitHub
release -> CurseForge metadata (game-version ids resolved from the API) -> CurseForge upload.

## 3. Verify

- [ ] GitHub release `vX.Y.Z` exists with `Trashlands-X.Y.Z.zip` attached.
- [ ] CurseForge shows the new file, typed **Alpha** for the `0.x` line.
- [ ] The CurseForge changelog matches the CHANGELOG section (not the bare "Release X.Y.Z" fallback -
      that string means the regex missed and the heading shape is wrong).

## Gotchas

- **Version must match the tag.** Bump `pack.toml` before tagging; the guard fails otherwise.
- **Stage index.toml and pack.toml together** after `pack_refresh.py`. A stale index ships hashes no
  committed file has, and packwiz-installer then rejects the very jars it just downloaded. The
  workflow's index guard catches this, but it costs you a re-tag.
- **CHANGELOG heading format is load-bearing.** `## [X.Y.Z]` exactly.
- **Never add a mod with `packwiz modrinth add`** for a pack that ships to CurseForge. Modrinth-added
  mods get inlined into the export as real jars, which is a redistribution violation. Use
  `packwiz curseforge add`. The workflow greps the export for `.jar` and fails the run if one appears.
- **Game-version ids are resolved, not hardcoded.** If CurseForge returns `errorCode 1009`, the
  resolver picked an id from the wrong version type; see
  [`distribution.md`](./distribution.md#curseforge-upload-api-quirks).
- **Secrets.** `CF_API_TOKEN` (secret) and `CF_PROJECT_ID` (variable). If either is unset the
  CurseForge steps warn-and-skip and the GitHub release still ships; upload with
  `python tools/cf_release.py` afterwards.
- **`actions/setup-java` and friends** - keep workflow actions on current Node majors. GitHub
  force-deprecates old ones and the failure is abrupt.

---

# The 1.0 gate

`1.0.0` is the promise that the pack is finished enough for a broad audience. Not a routine tag.

- [ ] **The knowledge half of teardown shipped.** Recovering a recipe off a torn-down item is the
      mod's distinct axis. Until it exists, the pack's own pitch is only half true.
- [ ] **Quest content.** The engine is in and the book is no longer empty - a **Welcome** chapter
      and a **Salvage** chapter ship as of v0.4.0: 21 quests from the first Block of Garbage to the
      first Bucket of Water. What is missing is the spine: `The Way Home`, parts one to six, per `the_twist.md`. Write it against the
      `quest-voice` spec; the twist means the final chapters are authored against that file directly.
- [ ] **One balance pass across all loot tables and recipes together** - the standing gate in
      `../recompile/docs/roadmap.md`. Every drop rate and recipe cost shipped so far is a first-pass
      placeholder chosen to prove a mechanic. Tuning is pack responsibility even though the numbers
      live in the mod's JSON.
- [ ] **No soft-locks.** A fresh world plays start to finish with no dead ends.
- [ ] **A real logo.** The current `pack/icon.png` is a screenshot crop.
- [ ] **Server pack**, if multiplayer is in scope for 1.0. See
      [`distribution.md`](./distribution.md#not-built-yet) - note the manual Server Pack typing step.
- [ ] **License audit.** Every bundled mod's license permits redistribution in a CurseForge pack.
