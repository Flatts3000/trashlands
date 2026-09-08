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

   **Then read the mod's changelog for new content in a dimension the book already documents, and
   check the chapter still covers it.** This is not hypothetical housekeeping: three releases running
   added to the compacted depths after The Depths was written. 0.13.0 added the Worn Forging Die,
   caught in review and folded in before it shipped; 0.14.0 added Ancient Sculk, which was not, and
   needed #51 afterwards. A chapter documenting a dimension that is still being built goes stale by
   default, and nothing else in this list would notice.

   **In the same read, check whether any dimension has gained amethyst geodes.** Recompile owns every
   dimension in this pack, so it owns this risk. `flattsthings:silk_touch_budding_amethyst` is pinned
   **on** in `pack/config/flattsthings-common.toml`, and it is safe only because no geode generates
   anywhere - the four biomes carry explicit feature lists and the mod contains no `geode` reference
   at all. The day one does, silk touch takes budding amethyst, amethyst becomes renewable, and that
   walks around the Separator chain `../recompile/docs/gem_tier_spec.md` calls "the proving material"
   for the whole gem tier. **Turn that switch off in the same commit that takes the pin.** The
   Flatts's Things check in step 3 will not catch this: the feature lives in that mod, but the
   condition that makes it safe lives in this one.

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

   **When the Flatts's Things pin moves, diff its feature list against
   `pack/config/flattsthings-common.toml`.** Every feature in that mod ships ON, and NeoForge's
   `ModConfigSpec.correct()` writes any *missing* key with its spec default - so a feature added
   upstream arrives switched on in this pack no matter what that config lists. The pin bump is the
   only moment anyone would notice. Read the mod's changelog, add the new keys, and decide each one
   rather than inheriting it. Same trap as the Recompile changelog check in step 1, and for the same
   reason: a mod that is still being built goes stale against the pack by default.

   **Do not read that config out of an instance to see what the pack set.** Correction also fires on
   a comment mismatch alone, and it rewrites and saves the whole file, replacing every pack-authored
   comment with the mod's own. An instance copy tells you the values and nothing else. The repo copy
   and `pack_setup.md` are the record.

4. **Things this list cannot check. All of them need a client launch.**

   The Better Advanced Tooltips pin is **not** one of them any more: it is registered in
   `HELD_PINS` in `check_pack_deps.py`, so moving or deleting it fails `validate-pack.yml` on every
   PR. That is the pin the whole KubeJS reintroduction rests on, and it now has automated cover.

   What still needs eyes:

   - **KubeJS must reach the title screen.** It is a **beta** build, and it is the mod that crashed
     this pack on 2026-08-02. The held pin proves the right *file* is present; it cannot prove the
     game boots.
   - **FTB Ultimine must not vein-mine the garbage.** The exclusion lives in a tag at
     `pack/kubejs/data/ftbultimine/tags/block/excluded_blocks.json`, and a tag is invisible to the
     dep check. **If KubeJS fails to load for any reason, the tag silently does not apply** and the
     mod becomes a vein-miner pointed at the core loop, with no error anywhere. In game: hold the
     Ultimine key on a Block of Garbage and confirm only the block under the crosshair highlights,
     then on deepslate two blocks under the plain and confirm it does not chain either, then on a
     grown tree and confirm the whole trunk *does*. That last one is the positive control: without it
     a totally unloaded tag looks identical to a working one. **In the Compacted Depths nothing at
     all should chain** - every solid block down there is sortable garbage or the sculk seam. Both
     bulk blocks were left chaining by earlier passes and excluded on owner call, so a test written
     against either old position would pass on a broken tag.
   - **Settle whether `enchanted_golden_apple` is live or dead content.** Flatts's Things pins it on,
     and it hooks `PlayerEnchantItemEvent` from the vanilla enchanting table - which Apothic
     Enchanting replaces. Put a golden apple in a table and see whether the offer appears. If it
     does, it is a live route to a vanilla loot-only item in a world that gates gold and apples, and
     it wants pricing. If it does not, it is dead content and should be pinned off rather than left
     looking supported.
   - **Decide the right-click question while you are in there.** `excluded_blocks` governs breaking
     only. Ultimine's area hoe and shovel read `ftbultimine:farmland_tillable` and
     `ftbultimine:shovel_flattenable`, which ship containing `minecraft:coarse_dirt` and are not
     overridden. Mass-tilling the plain may be fine, or even wanted for the reclamation ladder. Try
     it and rule.

   **Sequencing.** Consider not shipping Ultimine in the same release that reintroduces KubeJS. One
   playtest miss hands players an unguarded vein-miner aimed at the core loop, and the two changes
   are independent. If they do ship together, the two checks above are mandatory, not optional.

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

Steps: version guard -> index guard -> CF export (+ no-jar assertion) -> **server pack build ->
client-mod guard -> server boot smoke test** -> changelog extract -> GitHub release -> CurseForge
metadata (game-version ids resolved from the API) -> CurseForge upload -> **server pack upload as a
child file**.

The boot test installs NeoForge and waits for `Done (`, so a release takes a few minutes longer than
it used to. That is the only check that proves the `side` tags are right, and a mistagged mod is
otherwise found by whoever first runs a server.

## 3. Verify

- [ ] GitHub release `vX.Y.Z` exists with `Trashlands-X.Y.Z.zip` attached.
- [ ] CurseForge shows the new file, typed **Alpha** for the `0.x` line.
- [ ] The CurseForge changelog matches the CHANGELOG section (not the bare "Release X.Y.Z" fallback -
      that string means the regex missed and the heading shape is wrong).
- [ ] **Type the server pack.** Authors Console -> Files -> the client file -> the attached server
      file -> Additional File Info -> `Server Pack`. **The API cannot do this**, so it is manual every
      single release, and an untyped server pack is invisible to host one-click deploys. The release
      run leaves a warning saying so. Then confirm with `python tools/check_server_pack_flag.py`
      - **which currently exits 2, meaning unverified, not fine.** It cannot confirm the typing
      while the v1 listing has no files for this project; see #55. Do the console step anyway.
      **A 3 is a different thing and must not be waved off as the known 2:** it means the listing
      was read fine and no file carries an attachment at all, so the release workflow failed to
      attach the server pack. 1 means attached but untyped, which is the console step.

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
- **Java 25, not 21.** NeoForge 26.1 is compiled for Java 25 (class file 69). A Java 21 runtime dies
  with `UnsupportedClassVersionError` before a single mod loads, which is what failed the first
  v0.7.0 attempt. Both workflows and the server pack's `INSTALL.md` say 25; the dev instance has been
  on jdk-25 all along. If a boot ever fails instantly with a class-version error, this is it.
- **`packwiz` in CI is pinned, not `@latest`.** Upstream commit `9066bf8` (#407, 2026-09-02) added
  a `replace` directive to packwiz's `go.mod`, and `go install pkg@version` refuses any module whose
  go.mod carries one ("contains one or more replace directives"). Both workflows broke the moment it
  landed upstream, with nothing in this repo changed - it failed PR #58 before this release. They now
  pin `v0.0.0-20260218225342-dfd8b68a4796`, the commit immediately before it, which is itself
  "Support neoforge for 26.1 and above" (#386). **Move the pin only to a commit whose `go.mod` has no
  replace directive**; check with
  `gh api "repos/packwiz/packwiz/contents/go.mod?ref=<sha>" --jq .content | base64 -d | grep replace`.
- **`packwiz-installer-bootstrap` used to call the GitHub API anonymously** to look up its own
  latest release, and got a **403** when the runner's shared IP was rate-limited. It hit PR CI on
  2026-08-18 and again on PR #33 on 2026-08-20, and the release drives that bootstrap three times, so
  the odds compounded. **Fixed 2026-08-20 (#31).** `tools/packwiz-installer.jar` is vendored at
  v0.5.14 and both callers pass `--bootstrap-no-update --bootstrap-main-jar`, so no API call happens
  at all - in CI or locally. If resolution ever fails now, it is the jar itself: see
  [`../tools/README_packwiz_installer.md`](../tools/README_packwiz_installer.md). Do not restore the
  update check.

---

# The 1.0 gate

`1.0.0` is the promise that the pack is finished enough for a broad audience. Not a routine tag.

- [ ] **The knowledge half of teardown shipped.** Recovering a recipe off a torn-down item is the
      mod's distinct axis. Until it exists, the pack's own pitch is only half true.
- [ ] **Quest content.** The engine is in and the book is no longer empty - a **Welcome** chapter
      a **Salvage**, a **Groundwork** and a **The Depths** chapter all ship: 63 quests from the first
      Block of Garbage to a piece of coal. What is missing is the spine: `The Way Home`, parts one to six, per `the_twist.md`. Write it against the
      `quest-voice` spec; the twist means the final chapters are authored against that file directly.
- [ ] **One balance pass across all loot tables and recipes together** - the standing gate in
      `../recompile/docs/roadmap.md`. Every drop rate and recipe cost shipped so far is a first-pass
      placeholder chosen to prove a mechanic. Tuning is pack responsibility even though the numbers
      live in the mod's JSON.
- [ ] **No soft-locks.** A fresh world plays start to finish with no dead ends.
- [ ] **A real logo.** The current `pack/icon.png` is a screenshot crop.
- [ ] **Server pack playtested.** It has built, booted and shipped on every release since v0.7.0,
      but **nobody has actually played a multiplayer world on it**. The world *type* is no longer in
      doubt - since #32 the release asserts the generated terrain came from the garbage preset and a
      wrong world fails the release. What is untested is play: a second person, joining, over time.
      See [`distribution.md`](./distribution.md#the-server-pack).
- [ ] **License audit.** Every bundled mod's license permits redistribution in a CurseForge pack.
