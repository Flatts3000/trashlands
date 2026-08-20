#!/usr/bin/env python3
"""Sync the local CurseForge dev instance's mods to the pack pins.

Why this exists
---------------
packwiz stores mod *metadata* (`pack/mods/*.pw.toml`), not jars, so
`packwiz curseforge add` / `update` never touch the instance. Mod changes have to
be pushed into it separately.

This drives the canonical tool chain - `packwiz serve` plus packwiz-installer -
to do that. packwiz-installer downloads each pinned mod straight from CurseForge,
hash-verifies it, and tracks `.packwiz-installer-manifest.json`, so add / update /
remove all happen cleanly.

Ported from ../sky-frogs/tools/sync_instance.py, plus two checks that repo learned
the hard way and kept in a separate script (or a checklist step):

  1. LOADER PIN. If the instance runs a different NeoForge build than the pack
     pins, the test is worthless - it either fails for an unrelated reason or
     passes on a loader you are not shipping. Sky Frogs shipped v1.5.3 with no
     valid launch test for exactly this reason. Checked here, before syncing.
  2. CAN IT LOAD. After the sync, the instance's jars are audited with
     check_pack_deps.py, so a mod that needs a newer loader than the instance has
     is named now rather than silently not loading in-game.

Safety
------
- Refuses to run while this instance's Minecraft is running (loaded jars are locked).
- Refuses if `packwiz serve` on the port is not serving THIS pack.
- Idempotent: a run where every jar is present and hash-matching downloads nothing.

Usage
-----
    python tools/sync_instance.py
    python tools/sync_instance.py --side both       # include server-only mods
    python tools/sync_instance.py --instance "C:\\...\\Instances\\Other"
    python tools/sync_instance.py --skip-audit
"""
from __future__ import annotations

import argparse
import json
import re
import os
import shutil
import subprocess
import sys
import time
import tomllib
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACK = REPO / "pack"
TOOLS = REPO / "tools"
BOOTSTRAP = TOOLS / "packwiz-installer-bootstrap.jar"
# Vendored: see tools/README_packwiz_installer.md. Without it the bootstrap makes an
# anonymous api.github.com call on every sync and self-downloads whatever `latest` is,
# which also drifts the dev instance off the installer version CI pins.
INSTALLER = TOOLS / "packwiz-installer.jar"
BOOTSTRAP_URL = ("https://github.com/packwiz/packwiz-installer-bootstrap/"
                 "releases/latest/download/packwiz-installer-bootstrap.jar")

CF_ROOT = Path.home() / "curseforge" / "minecraft"
DEFAULT_INSTANCE = CF_ROOT / "Instances" / "Trashlands"
# The app-level store. CurseForge keeps the loader in TWO places and this one wins
# on launch, so a check that reads only the instance's own json can be fooled.
APP_STORE = (Path.home() / "AppData" / "Local" / "Overwolf" / "Curse"
             / "GameInstances" / "MinecraftGameInstance.json")
# Registered for this project - see ~/.claude/port_registry.yaml.
DEFAULT_PORT = 8603
UA = "Mozilla/5.0 (trashlands sync_instance.py)"


def version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(p) for p in re.findall(r"\d+", text or ""))


def pack_pins() -> tuple[str, str, str]:
    data = tomllib.loads((PACK / "pack.toml").read_text(encoding="utf-8"))
    v = data.get("versions", {})
    return data.get("name", ""), v.get("minecraft", ""), v.get("neoforge", "")


def minecraft_running(instance: Path) -> bool:
    """Best-effort: is a java process running this instance? (Windows/PowerShell)."""
    needle = instance.name.replace("'", "''")
    ps = ("Get-CimInstance Win32_Process -Filter \"Name='java.exe' OR Name='javaw.exe'\" "
          f"| Where-Object {{ $_.CommandLine -like '*{needle}*' }} "
          "| Select-Object -First 1 -ExpandProperty ProcessId")
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                             capture_output=True, text=True, timeout=30)
        return bool(out.stdout.strip())
    except Exception:  # noqa: BLE001 - no PowerShell / odd env: do not block on the check
        return False


def instance_loader(instance: Path) -> tuple[str | None, str | None]:
    """(mc_version, loader_name) from the instance's own json, or (None, None)."""
    p = instance / "minecraftinstance.json"
    if not p.is_file():
        return None, None
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None, None
    return d.get("gameVersion"), (d.get("baseModLoader") or {}).get("name")


def app_store_loader(instance: Path) -> str | None:
    """Loader name the CurseForge app itself has recorded for this instance.

    This is the copy that wins at launch. If it disagrees with the instance's own
    json, the app's value is what actually runs.

    The file is a FLAT LIST of instance objects (not an object with an "instances"
    key). Instances are matched on resolved installPath, not on name: names are not
    unique enough - this machine has both "Sky Frogs" and "Sky Frogs (1)", and a
    substring match on the shorter one hits the longer one too.
    """
    if not APP_STORE.is_file():
        return None
    try:
        data = json.loads(APP_STORE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    # Tolerate either shape in case a future app version wraps the list.
    entries = data if isinstance(data, list) else (
        data.get("instances") or data.get("Instances") or [])

    try:
        want = instance.resolve()
    except OSError:
        want = instance

    for inst in entries:
        if not isinstance(inst, dict):
            continue
        raw = inst.get("installPath") or inst.get("InstallPath")
        if not raw:
            continue
        try:
            # installPath carries a trailing separator; Path normalizes it away.
            if Path(str(raw)).resolve() != want:
                continue
        except OSError:
            continue
        bml = inst.get("baseModLoader") or inst.get("BaseModLoader") or {}
        return bml.get("name") or bml.get("Name")
    return None


def check_loader(instance: Path, mc_pin: str, loader_pin: str) -> bool:
    """Warn loudly if the instance is not on the loader the pack pins. True = ok."""
    mc, loader = instance_loader(instance)
    app_loader = app_store_loader(instance)
    print(f"pack pins    : Minecraft {mc_pin}, NeoForge {loader_pin}")
    print(f"instance     : Minecraft {mc or '?'}, {loader or '?'}")
    if app_loader:
        print(f"app store    : {app_loader}")

    ok = True
    if mc and mc != mc_pin:
        print(f"\n  MISMATCH: instance Minecraft {mc} != pack {mc_pin}. "
              "The pack and the instance must be on the same Minecraft version.")
        ok = False

    effective = app_loader or loader
    if effective:
        # Check the loader FAMILY before comparing numbers. Version digits are not
        # comparable across families: forge-47.3.27 parses to (47, 3, 27), which is
        # numerically greater than the NeoForge pin (26, 1, 2, 94), so a Forge
        # instance would pass a purely numeric check. And a Fabric instance would be
        # reported as "NeoForge build too old", which is the wrong diagnosis.
        if not effective.lower().startswith("neoforge"):
            print(f"\n  MISMATCH: instance loader is {effective}, but this pack is "
                  "NeoForge.\n  Recreate the instance on NeoForge in the CurseForge app.")
            ok = False
        else:
            have, want = version_tuple(effective), version_tuple(loader_pin)
            if have and want and have < want:
                print(f"\n  MISMATCH: instance loader {effective} is BELOW the pack pin "
                      f"{loader_pin}.\n  Mods that require a newer loader will not load, and "
                      "NeoForge does not warn about it.\n  Fix the instance's loader in the "
                      "CurseForge app before trusting any test.")
                ok = False
    if app_loader and loader and app_loader != loader:
        print(f"\n  NOTE: the app store ({app_loader}) and the instance json ({loader}) "
              "disagree.\n  The app store is what launches. Set the version in the "
              "CurseForge app, not by editing json.")
    return ok


def ensure_installer() -> None:
    """The vendored packwiz-installer must be present; we never fetch it at runtime."""
    if not INSTALLER.is_file() or INSTALLER.stat().st_size < 1024:
        sys.exit(f"vendored packwiz-installer missing or truncated at {INSTALLER} - "
                 "see tools/README_packwiz_installer.md")


def ensure_bootstrap() -> None:
    if BOOTSTRAP.is_file() and BOOTSTRAP.stat().st_size > 1024:
        return
    print(f"fetching packwiz-installer-bootstrap.jar -> {BOOTSTRAP} ...")
    req = urllib.request.Request(BOOTSTRAP_URL, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"could not download packwiz-installer-bootstrap.jar: {exc}")
    if len(data) < 1024:
        sys.exit("bootstrap download looks wrong (too small); aborting")
    BOOTSTRAP.write_bytes(data)


def wait_for_serve(url: str, proc: subprocess.Popen, timeout: float = 30.0) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            return None
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return resp.read().decode("utf-8", "replace")
        except Exception:  # noqa: BLE001 - refused until the server binds
            time.sleep(0.4)
    return None


# ---------------------------------------------------------------------------
# Dev overlay: a locally built mod, in the pack, without a CurseForge release
# ---------------------------------------------------------------------------
#
# CurseForge moderates every file, so pinning a mod there means waiting on a queue
# before it can be tested next to the rest of the pack. That is fine for shipping and
# useless for iterating: the whole point of a change is to play it.
#
# packwiz-installer only ever fetches what the pins say, so the overlay runs AFTER the
# sync and simply replaces that mod's jar in the instance. It is deliberately NOT a pin
# change - the pack keeps pointing at the released file, so nothing here can leak into
# an export or a release, and the next plain sync puts the released jar back.

JDK = Path("C:/Program Files/Java/jdk-25")

# Marks an overlaid jar so a mods folder always says which jars are local builds.
DEV_SUFFIX = "-dev"


def build_mod(repo: Path) -> Path | None:
    """Build a sibling mod repo and hand back the jar it produced."""
    if not (repo / "gradlew.bat").is_file() and not (repo / "gradlew").is_file():
        print(f"  {repo} has no gradle wrapper - is that a mod repo?")
        return None
    env = dict(os.environ)
    # The machine's JAVA_HOME points at a JDK that is not there; every gradle call in
    # these repos overrides it, so do the same rather than failing in a confusing way.
    if JDK.is_dir():
        env["JAVA_HOME"] = str(JDK)
    print(f"  building {repo.name} ...")
    wrapper = repo / ("gradlew.bat" if os.name == "nt" else "gradlew")
    done = subprocess.run([str(wrapper), "build", "--console=plain", "-q"],
                          cwd=repo, env=env)
    if done.returncode != 0:
        print(f"  build FAILED ({done.returncode}) - not overlaying a stale jar")
        return None
    return newest_jar(repo / "build" / "libs")


def newest_jar(libs: Path) -> Path | None:
    """The mod jar in build/libs, ignoring the sources and javadoc siblings."""
    if not libs.is_dir():
        return None
    jars = [j for j in libs.glob("*.jar")
            if not j.name.endswith(("-sources.jar", "-javadoc.jar"))]
    if not jars:
        return None
    # Newest by mtime: build/libs keeps older versions around, and picking by name
    # sorts 0.10 before 0.9. The one just built is the one wanted.
    return max(jars, key=lambda j: j.stat().st_mtime)


def pinned_filename(artifact: str) -> str | None:
    """What the pack pins this mod's jar as, so the overlay replaces the right file."""
    for meta in sorted((PACK / "mods").glob("*.pw.toml")):
        for line in meta.read_text(encoding="utf-8").splitlines():
            if line.startswith("filename"):
                name = line.split("=", 1)[1].strip().strip('"')
                if name.startswith(artifact + "-"):
                    return name
    return None


def overlay_dev_jar(instance: Path, source: Path) -> bool:
    """Put a locally built jar into the instance in place of its pinned one."""
    jar = build_mod(source) if source.is_dir() else source
    if jar is None or not jar.is_file():
        print(f"  no jar to overlay from {source}")
        return False

    # "recompile-26.1.2-0.8.0.jar" -> "recompile". The pin and the build agree on this
    # prefix, which is what lets the released jar be found and removed.
    artifact = jar.name.split("-")[0]
    mods = instance / "mods"
    mods.mkdir(exist_ok=True)

    # LANDS UNDER A -dev NAME, ON PURPOSE. A local build usually carries the same version
    # as the release it came from, so copying it in under its own name leaves a mods folder
    # where nothing distinguishes "the released jar" from "whatever I last compiled" - and
    # the answer decides whether a bug report is worth anything. NeoForge reads the version
    # from the jar rather than the filename, so the suffix costs nothing.
    target = mods / (jar.stem + DEV_SUFFIX + ".jar")

    replaced = pinned_filename(artifact)
    for stale in mods.glob(artifact + "-*.jar"):
        if stale != target:
            stale.unlink()
            print(f"  removed {stale.name}")
    shutil.copy2(jar, target)
    print(f"  installed {target.name}  ({jar.stat().st_size // 1024} KiB)")
    if replaced:
        print(f"  (the pack still pins {replaced}; a plain sync restores it)")
    return True


def sweep_dev_overlays(instance: Path, keep: list[Path]) -> None:
    """Delete dev overlays that this run is not (re)installing.

    Without this the tool is a footgun rather than a convenience. packwiz-installer only
    manages the files in its own manifest, so a plain sync happily reinstalls the pinned
    jar and leaves an older -dev overlay sitting beside it - two jars, one mod id, and a
    crash on launch that looks nothing like its cause.
    """
    keeping = {p.name.split("-")[0] for p in keep}
    for overlay in sorted((instance / "mods").glob("*" + DEV_SUFFIX + ".jar")):
        if overlay.name.split("-")[0] not in keeping:
            overlay.unlink()
            print(f"  removed stale dev overlay {overlay.name}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--instance", type=Path, default=DEFAULT_INSTANCE)
    ap.add_argument("--side", choices=["client", "server", "both"], default="client",
                    help="which side's mods to install (default: client = client+both)")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT,
                    help=f"port for `packwiz serve` (default {DEFAULT_PORT}, the registered one)")
    ap.add_argument("--skip-audit", action="store_true",
                    help="skip the post-sync check_pack_deps.py audit")
    ap.add_argument("--force", action="store_true",
                    help="sync even if the instance's loader does not match the pack pin")
    ap.add_argument("--dev", type=Path, action="append", metavar="PATH", default=[],
                    help="overlay a locally built mod after syncing: a repo to build, or a "
                         ".jar to copy. Repeatable. Lets an unreleased build be played next "
                         "to the rest of the pack without a moderated CurseForge release.")
    ap.add_argument("--dev-only", action="store_true",
                    help="skip the packwiz sync and only re-overlay --dev mods. The fast loop "
                         "while iterating on a mod: the rest of the pack has not changed.")
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    if not (PACK / "pack.toml").is_file():
        sys.exit(f"pack not found at {PACK} (expected pack.toml)")
    if not args.instance.is_dir():
        sys.exit(f"instance dir not found: {args.instance}\n"
                 "Create it in the CurseForge app first (see docs/pack_setup.md).")
    for tool in ("packwiz", "java"):
        if shutil.which(tool) is None:
            sys.exit(f"`{tool}` not found on PATH - install it / add it to PATH and retry.")
    if minecraft_running(args.instance):
        sys.exit("ABORT: Minecraft appears to be running this instance. Close it first "
                 "(loaded jars are locked), then retry.")

    if args.dev_only:
        if not args.dev:
            sys.exit("--dev-only needs at least one --dev PATH to overlay.")
        print("dev overlay only - the pack itself is not being synced")
        sweep_dev_overlays(args.instance, args.dev)
        ok = all(overlay_dev_jar(args.instance, d) for d in args.dev)
        print("Relaunch the instance." if ok else "Overlay failed.")
        return 0 if ok else 1

    pack_name, mc_pin, loader_pin = pack_pins()
    if not check_loader(args.instance, mc_pin, loader_pin) and not args.force:
        sys.exit("\nABORT: instance does not match the pack's pins. Fix it in the "
                 "CurseForge app, or pass --force to sync anyway.")

    ensure_bootstrap()
    ensure_installer()

    print("\nnormalizing line endings + packwiz refresh ...")
    if subprocess.run([sys.executable, str(TOOLS / "pack_refresh.py")]).returncode != 0:
        sys.exit("tools/pack_refresh.py failed")

    url = f"http://127.0.0.1:{args.port}/pack.toml"
    print(f"serving pack on 127.0.0.1:{args.port} ...")
    # --refresh=false: pack_refresh.py already refreshed. Without it, serve re-hashes
    # the working tree per query and can re-record CRLF hashes we just normalized away.
    serve = subprocess.Popen(["packwiz", "serve", "--port", str(args.port), "--refresh=false"],
                             cwd=PACK, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        body = wait_for_serve(url, serve)
        if body is None:
            sys.exit(f"`packwiz serve` did not come up on :{args.port} "
                     "(port already in use? try --port).")
        # Confirm the responder is OUR pack, not some other server holding the port.
        if pack_name and pack_name not in body:
            sys.exit(f"server on :{args.port} is not pack '{pack_name}' - aborting rather "
                     "than risk syncing the instance to the wrong pack.")
        print(f"running packwiz-installer (side={args.side}) in {args.instance} ...\n")
        rc = subprocess.run(["java", "-jar", str(BOOTSTRAP),
                             "--bootstrap-no-update", "--bootstrap-main-jar", str(INSTALLER),
                             "-g", "-s", args.side, url],
                            cwd=args.instance).returncode
    finally:
        serve.terminate()
        try:
            serve.wait(timeout=10)
        except subprocess.TimeoutExpired:
            serve.kill()

    if rc != 0:
        print(f"\npackwiz-installer exited {rc}. Any mod it could not download "
              "automatically (e.g. CurseForge third-party downloads disabled) is named "
              "above - fetch those manually into the instance's mods/ folder.")
        return rc

    print("\nSync complete - the instance's mods now match the pack pins.")

    if not args.skip_audit:
        print("\nauditing the synced instance (tools/check_pack_deps.py) ...")
        rc = subprocess.run([sys.executable, str(TOOLS / "check_pack_deps.py"),
                             "--mods-dir", str(args.instance / "mods")]).returncode
        if rc != 0:
            print("\nThe instance would boot with mods silently absent. Fix before testing.")
            return rc

    if args.dev:
        print("\noverlaying locally built mods ...")
        if not all(overlay_dev_jar(args.instance, d) for d in args.dev):
            return 1
        print("\n*** This instance is NOT the shipped pack. *** One or more mods are local "
              "builds.\n    Re-run without --dev to put the released jars back.")

    print("\nRelaunch the instance to load the new mods.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
