#!/usr/bin/env python3
"""Stand up a local dedicated server for this pack, with RCON on, so the world can
be driven and asserted against by `gamebridge`.

Why a dedicated server at all
-----------------------------
A singleplayer world cannot be driven remotely: its integrated server listens on
nothing, so there is no command interface to connect to. Reaching one needs mod
code running inside the game (that is what `devbridge` is for). A dedicated server
has RCON natively and needs no mod, so it is the cheap path to a verifiable world -
and it is the one the gamebridge handoff recommends starting from.

This is NOT a distributable server pack. Sky Frogs' tools/build_server.py builds
one of those, zip and INSTALL.md and all, because hosts run it. Nothing here is
meant to leave this machine, so it stays a fraction of the size.

What it does
------------
1. Downloads the NeoForge installer for the version pinned in pack/pack.toml and
   runs `--installServer`.
2. Serves the working-tree pack over HTTP and drives packwiz-installer with
   `-s server`, so `side = "client"` mods (Sodium, FancyMenu, ...) never land.
3. Writes server.properties with RCON enabled and the level-type set to the
   garbage world preset, because a server that generates vanilla terrain tests
   nothing about this pack.

Usage
-----
    python tools/dev_server.py --accept-eula     # install (first run)
    python tools/dev_server.py --run             # start it
    gamebridge wait && gamebridge cmd "list"     # from anywhere under the repo
"""
from __future__ import annotations

import argparse
import os
import secrets
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_instance as si  # noqa: E402  (packwiz-serve helpers; do not duplicate them)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DIR = REPO / "build" / "server"
NEOFORGE_INSTALLER = ("https://maven.neoforged.net/releases/net/neoforged/neoforge/"
                      "{v}/neoforge-{v}-installer.jar")

# The pack forces this world preset at world creation (see
# pack/config/defaultworldtype/client-config.toml). A dedicated server ignores that
# client config entirely, so without level-type here the server generates ordinary
# overworld terrain and every progression assertion runs against the wrong world.
LEVEL_TYPE = "recompile:garbage"

# packwiz serve needs a port that is not the one sync_instance.py uses, so a server
# build and an instance sync cannot collide. 8603 is this project's registered port.
SERVE_PORT = 8604


def server_properties(rcon_password: str) -> str:
    return "\n".join([
        "# Written by tools/dev_server.py. Local verification server only.",
        "enable-rcon=true",
        f"rcon.password={rcon_password}",
        "rcon.port=25575",
        f"level-type={LEVEL_TYPE}",
        "level-name=devworld",
        "online-mode=false",
        "gamemode=creative",
        "difficulty=peaceful",
        # A playerless server unloads chunks, and gamebridge assertions then fail
        # with "not loaded" rather than saying anything true. Keeping spawn loaded
        # removes the commonest cause of a command that appears to do nothing.
        "spawn-protection=0",
        "max-tick-time=-1",
        "sync-chunk-writes=false",
        "view-distance=8",
        "",
    ])


def install_neoforge(target: Path, version: str) -> None:
    jar = target / f"neoforge-{version}-installer.jar"
    if not (target / "libraries").is_dir():
        target.mkdir(parents=True, exist_ok=True)
        if not jar.is_file():
            url = NEOFORGE_INSTALLER.format(v=version)
            print(f"downloading NeoForge {version} installer ...")
            req = urllib.request.Request(url, headers={"User-Agent": si.UA})
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    jar.write_bytes(resp.read())
            except Exception as exc:  # noqa: BLE001
                sys.exit(f"could not download the NeoForge installer: {exc}\n{url}")
        print("running --installServer ...")
        rc = subprocess.run(["java", "-jar", str(jar), "--installServer", str(target)],
                            cwd=target).returncode
        if rc != 0:
            sys.exit(f"NeoForge installer exited {rc}")
    else:
        print(f"NeoForge already installed in {target}")


def install_mods(target: Path) -> None:
    """Serve the working-tree pack and install its SERVER-side mods into `target`."""
    si.ensure_bootstrap()
    print("\nnormalizing line endings + packwiz refresh ...")
    if subprocess.run([sys.executable, str(REPO / "tools" / "pack_refresh.py")]).returncode != 0:
        sys.exit("tools/pack_refresh.py failed")

    url = f"http://127.0.0.1:{SERVE_PORT}/pack.toml"
    print(f"serving pack on 127.0.0.1:{SERVE_PORT} ...")
    serve = subprocess.Popen(
        ["packwiz", "serve", "--port", str(SERVE_PORT), "--refresh=false"],
        cwd=REPO / "pack", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        body = si.wait_for_serve(url, serve)
        if body is None:
            sys.exit(f"`packwiz serve` did not come up on :{SERVE_PORT}")
        pack_name, _, _ = si.pack_pins()
        if pack_name and pack_name not in body:
            sys.exit(f"server on :{SERVE_PORT} is not pack '{pack_name}' - aborting")
        print("running packwiz-installer (side=server) ...\n")
        rc = subprocess.run(["java", "-jar", str(si.BOOTSTRAP), "-g", "-s", "server", url],
                            cwd=target).returncode
    finally:
        serve.terminate()
        try:
            serve.wait(timeout=10)
        except subprocess.TimeoutExpired:
            serve.kill()
    if rc != 0:
        sys.exit(f"packwiz-installer exited {rc}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR,
                    help=f"where to install (default {DEFAULT_DIR}, gitignored)")
    ap.add_argument("--accept-eula", action="store_true",
                    help="write eula=true. Only you can accept Mojang's EULA; this "
                         "flag is how you say you have.")
    ap.add_argument("--run", action="store_true", help="start the server (installs first if needed)")
    args = ap.parse_args()

    for tool in ("packwiz", "java"):
        if not si.shutil.which(tool):
            sys.exit(f"`{tool}` not found on PATH")

    _, mc_pin, loader_pin = si.pack_pins()
    target = args.dir.resolve()
    print(f"pack pins : Minecraft {mc_pin}, NeoForge {loader_pin}")
    print(f"server dir: {target}\n")

    install_neoforge(target, loader_pin)
    install_mods(target)

    eula = target / "eula.txt"
    if args.accept_eula:
        eula.write_text("eula=true\n", encoding="utf-8")
    elif not eula.is_file():
        eula.write_text("eula=false\n", encoding="utf-8")

    props = target / "server.properties"
    if not props.is_file():
        password = secrets.token_hex(12)
        props.write_text(server_properties(password), encoding="utf-8")
        print(f"\nwrote server.properties (rcon.password generated, level-type={LEVEL_TYPE})")
    else:
        print("\nserver.properties already exists - left alone")
        if "enable-rcon=true" not in props.read_text(encoding="utf-8"):
            print("  WARNING: enable-rcon is not true in it, so gamebridge cannot connect.")

    if not args.accept_eula and eula.read_text(encoding="utf-8").strip() != "eula=true":
        print("\neula.txt says eula=false. Re-run with --accept-eula once you have read\n"
              "https://aka.ms/MinecraftEULA . The server will refuse to start until then.")
        return 0

    print(f"\nready. Start it with:\n  cd {target} && ./run.sh      (or run.bat)")
    print(f"Then, from anywhere under {REPO}:\n"
          f"  gamebridge wait\n"
          f"  python tools/verify_quests.py")

    if args.run:
        script = target / ("run.bat" if os.name == "nt" else "run.sh")
        if not script.is_file():
            sys.exit(f"{script.name} not found - did --installServer succeed?")
        print(f"\nstarting {script.name} ...\n")
        return subprocess.run([str(script), "nogui"], cwd=target).returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
