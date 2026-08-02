#!/usr/bin/env python3
"""Prove the pinned pack can actually load: dependency and loader-range audit.

Why this exists
---------------
A mod that declares `neoforge [X,)` above the pack's pin does NOT warn. It
refuses to load, and the pack boots without it. Nothing in packwiz checks this,
because packwiz only resolves files - it never opens a jar.

That is not hypothetical. The first Trashlands lineup pinned NeoForge 26.1.2.76
while JEI required [26.1.2.81,) and Balm required [26.1.2.93,). JEI is core to
the pack, and it would have shipped silently absent. Sky Frogs hit the same
class of bug twice, both times via Apotheosis, and its checklist carries the
audit as a heredoc a human is supposed to remember to paste. This is that check,
made a real tool and wired into CI.

What it checks, per jar in the resolved pack:
  1. Every REQUIRED dependency modId is present somewhere in the pack.
  2. No required `neoforge` range has a lower bound above pack.toml's pin.
  3. No required `minecraft` range excludes pack.toml's Minecraft version.

Optional dependencies are ignored - that is what optional means.

How it gets the jars
--------------------
`pack/mods/*.pw.toml` holds metadata, not jars, so the jars have to be resolved
first. By default this drives the canonical tool chain - `packwiz serve` plus
packwiz-installer - into a temp directory, then audits it and cleans up. Pass
--mods-dir to audit a directory that already has jars (a live instance, or a
CI step that installed them).

The default port is the one registered for this project (see ~/.claude/port_registry.yaml).

Usage:
    python tools/check_pack_deps.py
    python tools/check_pack_deps.py --mods-dir "C:/.../instance/mods"
    python tools/check_pack_deps.py --port 8603

Exit codes: 0 = the pack can load, 1 = a blocker was found, 2 = the audit could
not run (no java, no packwiz, download failure). Non-zero is the point.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
import urllib.request
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
PACK = REPO / "pack"
BOOTSTRAP = REPO / "tools" / "packwiz-installer-bootstrap.jar"
DEFAULT_PORT = 8603

# Supplied by the loader itself; never separate jars, so never "missing".
BUILTIN = {"neoforge", "minecraft", "forge", "java", "fml", "neoforge_test"}


def version_tuple(text: str) -> tuple[int, ...]:
    return tuple(int(p) for p in re.findall(r"\d+", text))


def lower_bound(version_range: str) -> tuple[int, ...] | None:
    """Lower bound of a Maven range like `[26.1.2.93,)`. None if unparseable."""
    m = re.match(r"^\s*[\[(]\s*([0-9.]+)", version_range or "")
    return version_tuple(m.group(1)) if m else None


def pack_pins() -> tuple[str, str]:
    data = tomllib.loads((PACK / "pack.toml").read_text(encoding="utf-8"))
    versions = data.get("versions", {})
    if "neoforge" not in versions or "minecraft" not in versions:
        sys.exit("2: pack.toml [versions] is missing minecraft or neoforge")
    return versions["minecraft"], versions["neoforge"]


def resolve_jars(port: int, dest: Path) -> None:
    """Drive `packwiz serve` + packwiz-installer to download the pinned jars."""
    for tool in ("packwiz", "java"):
        if shutil.which(tool) is None:
            sys.exit(f"2: `{tool}` not on PATH; cannot resolve the pack's jars")
    if not BOOTSTRAP.is_file():
        sys.exit(f"2: packwiz-installer bootstrap not found at {BOOTSTRAP}")

    serve = subprocess.Popen(
        ["packwiz", "serve", "--port", str(port)],
        cwd=PACK, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        url = f"http://localhost:{port}/pack.toml"
        for _ in range(30):                       # up to ~15s for the server to bind
            try:
                urllib.request.urlopen(url, timeout=1).read()
                break
            except Exception:
                time.sleep(0.5)
        else:
            sys.exit(f"2: `packwiz serve` did not come up on port {port}")

        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(BOOTSTRAP, dest / BOOTSTRAP.name)
        run = subprocess.run(
            ["java", "-jar", BOOTSTRAP.name, "-g", "-s", "both", url],
            cwd=dest, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if run.returncode != 0:
            print(run.stdout[-3000:])
            print(run.stderr[-3000:], file=sys.stderr)
            sys.exit("2: packwiz-installer failed to resolve the pack's jars")
    finally:
        serve.terminate()
        try:
            serve.wait(timeout=10)
        except subprocess.TimeoutExpired:
            serve.kill()


def read_jars(mods_dir: Path):
    """Return {jar_name: (mod_ids, dependencies)} for every readable mod jar."""
    out, unreadable = {}, []
    for jar in sorted(mods_dir.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as z:
                data = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8"))
        except Exception as exc:
            unreadable.append(f"{jar.name}: {exc}")
            continue
        out[jar.name] = ([m["modId"] for m in data.get("mods", [])],
                         data.get("dependencies", {}))
    return out, unreadable


def audit(mods_dir: Path) -> int:
    mc_pin, loader_pin = pack_pins()
    loader_pin_t, mc_pin_t = version_tuple(loader_pin), version_tuple(mc_pin)

    meta, unreadable = read_jars(mods_dir)
    if not meta:
        sys.exit(f"2: no readable mod jars in {mods_dir}")
    present = {mid for ids, _ in meta.values() for mid in ids}

    missing, loader_blocks, mc_blocks = [], [], []
    for jar, (_ids, deps) in meta.items():
        for _owner, dep_list in deps.items():
            for dep in dep_list:
                mod_id = dep.get("modId")
                kind = str(dep.get("type", dep.get("mandatory", ""))).lower()
                if kind in ("optional", "false"):
                    continue
                rng = dep.get("versionRange") or ""
                if mod_id == "neoforge":
                    bound = lower_bound(rng)
                    if bound and loader_pin_t < bound:
                        loader_blocks.append(f"{jar} needs neoforge {rng}")
                elif mod_id == "minecraft":
                    bound = lower_bound(rng)
                    if bound and mc_pin_t < bound:
                        mc_blocks.append(f"{jar} needs minecraft {rng}")
                elif mod_id not in BUILTIN and mod_id not in present:
                    missing.append(f"{jar} requires '{mod_id}' {rng}")

    print(f"pack pins   : Minecraft {mc_pin}, NeoForge {loader_pin}")
    print(f"jars audited: {len(meta)}   mod ids present: {len(present)}\n")

    failed = False
    for title, rows, hint in (
        ("MISSING REQUIRED DEPENDENCIES", missing,
         "add the missing mod with `packwiz curseforge add`"),
        ("LOADER PIN TOO LOW", loader_blocks,
         "raise [versions] neoforge in pack/pack.toml to the highest bound listed"),
        ("MINECRAFT PIN TOO LOW", mc_blocks,
         "raise [versions] minecraft in pack/pack.toml"),
    ):
        if rows:
            failed = True
            print(f"=== {title} ===")
            for row in rows:
                print(f"  {row}")
            print(f"  -> {hint}\n")

    if unreadable:
        # Not fatal: coremods and some libraries legitimately ship without the file.
        print("=== NOT AUDITED (no readable neoforge.mods.toml) ===")
        for row in unreadable:
            print(f"  {row}")
        print()

    if failed:
        print("FAIL - this pack would boot with mods silently absent.")
        return 1
    print("OK - every required dependency is present and every pin is high enough.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mods-dir", help="audit an existing mods dir instead of resolving one")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"port for `packwiz serve` (default {DEFAULT_PORT}, the registered one)")
    parser.add_argument("--keep", action="store_true", help="keep the resolved jars for inspection")
    args = parser.parse_args()

    if args.mods_dir:
        return audit(Path(args.mods_dir))

    work = Path(tempfile.mkdtemp(prefix="trashlands-audit-"))
    try:
        print(f"resolving pinned jars into {work} ...")
        resolve_jars(args.port, work)
        return audit(work / "mods")
    finally:
        if args.keep:
            print(f"\nresolved jars kept at {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
