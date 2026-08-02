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
        have, want = version_tuple(effective), version_tuple(loader_pin)
        # Compare only the loader digits (drop a leading MC-derived prefix mismatch
        # by comparing the full tuples, which for NeoForge already encode MC).
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

    pack_name, mc_pin, loader_pin = pack_pins()
    if not check_loader(args.instance, mc_pin, loader_pin) and not args.force:
        sys.exit("\nABORT: instance does not match the pack's pins. Fix it in the "
                 "CurseForge app, or pass --force to sync anyway.")

    ensure_bootstrap()

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
        rc = subprocess.run(["java", "-jar", str(BOOTSTRAP), "-g", "-s", args.side, url],
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

    print("\nRelaunch the instance to load the new mods.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
