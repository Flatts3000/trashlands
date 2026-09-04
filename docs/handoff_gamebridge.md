# Handoff: wiring gamebridge / devbridge into Trashlands

**Written 2026-08-04 from the Recompile session that built these.** Everything below is verified on
Recompile unless it says otherwise. This is a task brief, not a design doc: the design is
`F:\devbridge\SPEC.md` and `F:\devbridge\gamebridge\README.md`.

**Paths corrected 2026-09-04.** This doc pointed at `mc-pack-toolkit\gamebridge`, which does not
exist - `mc-pack-toolkit\devbridge\` exists but is empty. Both tools live under `F:\devbridge`.

## What the tools are

**`gamebridge`** is a Python CLI that talks to a **running** Minecraft instance, so something placed in
the world can be **verified** instead of eyeballed. It speaks two transports.

**RCON**, against any dedicated server. Needs no mod at all.

**devbridge**, a dev-only NeoForge mod at `F:\devbridge`, for the two things RCON structurally cannot
do: reach a **singleplayer** world (whose integrated server listens on nothing) and take a
**screenshot** (which a dedicated server has no framebuffer for).

```bash
pip install -e F:/devbridge/gamebridge

gamebridge cmd "function trashlands:whatever"          # RCON, default
gamebridge check "block 6 125 0 recompile:garbage_block"   # exits non-zero when false
gamebridge --devbridge 25580 shot progression_step_3       # devbridge only
```

## The warning, first, because a pack is not a mod

**A pack ships its mods folder. That is the whole difference.**

In a mod repo devbridge lives in `run/mods/`, which is gitignored and never published. In a pack repo
`pack/mods/` **is the deliverable**. If devbridge ends up there, every player who installs Trashlands
gets a socket that executes arbitrary commands.

So:

- devbridge goes in the **test instance's** `mods/` folder, by hand.
- It never goes in `pack/mods/`, and it never gets a `packwiz` index entry.
- Check before any release that `pack/index.toml` has no devbridge line.

It binds loopback only and is inert without `-Ddevbridge.port`, so the realistic worst case is small.
Do not rely on that. The rule is simply that it is not part of the pack.

## Version compatibility - **verify this first**

| | Version |
| --- | --- |
| Trashlands | MC 26.1.2, NeoForge **26.1.2.100** (`pack/pack.toml`) |
| devbridge jar as built | MC 26.1.2, NeoForge **26.1.2.76** |

**Same MC and the same NeoForge minor, and the mod declares a loader range of `[4,)`, so it should
load - but nobody has run it on .100.** (**Corrected 2026-09-04:** this said .94, four lines under a
table that already said .100. The table was swept forward and the prose was not.) Confirm before building anything on top of it. If it refuses,
the fix is one line: change `neoforge_version` in `F:\devbridge\gradle.properties` and rebuild with

```bash
JAVA_HOME="/c/Program Files/Java/jdk-25" ./gradlew build
```

`gamebridge` is plain Python and does not care about either version.

## What this is actually worth here

Recompile uses it to place and verify screenshot scenes. **A pack's use is different and probably
bigger: progression.** Trashlands is a curated gate chain, and the questions that matter are exactly
the ones a command can answer and a screenshot cannot.

- **Gate assertions.** `docs/progression_gates.md` claims things like "iron needs the Cupola" and "lapis
  comes from a Printer teardown". Those are testable now: give a test player the inputs, run the
  crafting, assert the output exists. A gate that quietly broke because a mod updated is the failure
  mode this catches.
- **Quest verification.** FTB Quests tasks reference item ids. An id that no longer resolves fails
  silently and leaves a quest nobody can complete. `gamebridge check` over the quest item list would
  catch a whole class of that.
- **Screenshots for quests and the CurseForge page**, reproducibly, via devbridge. The pack page and the
  quest book both want images that stay current as the mod's textures change, and they change often.

## Suggested build order

1. **RCON against a test server.** Enable `enable-rcon` and `rcon.password` in the test server's
   `server.properties`, `gamebridge wait`, then one real assertion. Needs no mod and proves the loop.
2. **A `tools/verify_gates.sh`**, modelled on `F:\minecraft-repos\recompile\tools\verify_showcase.sh`.
   Start with two or three gates from `progression_gates.md` that you would actually be upset to see
   break.
3. **devbridge in the test instance**, only once 1 and 2 are useful, and only if you want screenshots.

## Four things that will bite

**Chunks unload with nobody standing in them.** A playerless server answers `data get block` with
"That position is not loaded" and otherwise behaves as though it worked. `forceload add` first. This is
the single likeliest reason a command that should work appears to do nothing.

**A failed RCON login returns request id -1, not an error.** A wrong password looks exactly like a
working connection until commands silently do nothing.

**Commands run as the console**, so `@s` matches nothing and `~` is spawn-relative. Anything needing a
player context needs a real player, or the `run as player` option that devbridge does not have yet
(tracked in its SPEC's Open section).

**The HUD is in devbridge screenshots** - hotbar, crosshair, held item. Not yet suppressible. Fine for
verification, not yet fine for a gallery image.

## Where things live

| Thing | Path |
| --- | --- |
| CLI source and README | `F:\minecraft-repos\mc-pack-toolkit\gamebridge\` |
| devbridge mod, spec, own repo | `F:\devbridge\` |
| A worked verification script | `F:\minecraft-repos\recompile\tools\verify_showcase.sh` |
| How Recompile wires its dev run | `F:\minecraft-repos\recompile\build.gradle`, the `client` run block |
