#!/usr/bin/env python3
"""Build the Trashlands dedicated-server pack: trashlands-server-<version>.zip.

What it produces
----------------
A self-contained server directory (then zipped) that a host unzips and runs:

    <out>/
      mods/               server+both-side jars, resolved by packwiz-installer
      config/             the pack's data, copied from pack/
      setup.sh setup.bat  NeoForge-installer bootstrap scripts
      user_jvm_args.txt   JVM args (host edits RAM here)
      eula.txt            eula=false (the host must accept it)
      server.properties   level-type=recompile:garbage
      INSTALL.md          what to do with the zip

The mod jars come from packwiz-installer with ``-s server`` - it pulls every mod
tagged ``side = "server"`` or ``side = "both"`` and SKIPS ``side = "client"``
ones, so Sodium, FancyMenu and the rest never reach the server. That makes the
per-mod ``side`` tags in ``pack/mods/*.pw.toml`` load-bearing: a client-only mod
mistagged ``both`` ships to the server and can crash boot. The boot smoke test in
release.yml is what proves the tags are right on every release.

**The world type is this pack's whole premise, and on a server it is set here.**
Default World Type is a client mod: it preselects ``recompile:garbage`` in the
create-world screen and does nothing on a dedicated server. So the server gets
``level-type=recompile:garbage`` in server.properties instead. Without it a
server generates a vanilla overworld, which is not Trashlands in any sense.

Usage
-----
    python tools/build_server.py                       # -> dist/trashlands-server-<ver>.zip
    python tools/build_server.py --out build/server    # install dir (kept, for boot tests)
    python tools/build_server.py --no-zip              # install only, skip the zip
    python tools/build_server.py --neoforge 26.1.2.94  # override the NeoForge version
"""
from __future__ import annotations

import argparse
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACK = REPO / "pack"
TOOLS = REPO / "tools"
BOOTSTRAP = TOOLS / "packwiz-installer-bootstrap.jar"
BOOTSTRAP_URL = ("https://github.com/packwiz/packwiz-installer-bootstrap/"
                 "releases/latest/download/packwiz-installer-bootstrap.jar")
UA = "Mozilla/5.0 (trashlands build_server.py)"

# The world preset the pack is built around. Client-side this is chosen by
# Default World Type (config/defaultworldtype/client-config.toml); a dedicated
# server has no such screen, so it goes in server.properties.
LEVEL_TYPE = "recompile:garbage"

# Data dirs copied verbatim into the server pack (packwiz-installer fetches only
# mods; the pack's own config lives in the repo working tree). Missing ones are
# skipped, so this list can name dirs the pack does not have yet.
DATA_DIRS = ("config", "defaultconfigs")


def read_pack_field(field: str) -> str:
    for line in (PACK / "pack.toml").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith(field):
            return line.split("=", 1)[1].strip().strip('"')
    return ""


def ensure_bootstrap() -> None:
    if BOOTSTRAP.is_file() and BOOTSTRAP.stat().st_size > 1024:
        return
    print(f"fetching packwiz-installer-bootstrap.jar -> {BOOTSTRAP} ...")
    req = urllib.request.Request(BOOTSTRAP_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    if len(data) < 1024:
        sys.exit("bootstrap download looks wrong (too small); aborting")
    BOOTSTRAP.write_bytes(data)


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_serve(url: str, proc: subprocess.Popen, timeout: float = 30.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            return None
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    return resp.read().decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            time.sleep(0.4)
    return None


def install_mods(out: Path, port: int) -> None:
    """Serve the pack and run packwiz-installer -s server into out/."""
    ensure_bootstrap()
    expected = read_pack_field("name")
    url = f"http://127.0.0.1:{port}/pack.toml"
    print(f"serving pack on 127.0.0.1:{port} ...")
    serve = subprocess.Popen(["packwiz", "serve", "--port", str(port), "--refresh=false"],
                             cwd=PACK, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        body = wait_for_serve(url, serve)
        if body is None:
            sys.exit(f"`packwiz serve` did not come up on :{port} (port in use? try --port).")
        if expected and expected not in body:
            sys.exit(f"server on :{port} is not pack '{expected}' - aborting.")
        out.mkdir(parents=True, exist_ok=True)
        print(f"running packwiz-installer (side=server) into {out} ...\n")
        rc = subprocess.run(["java", "-jar", str(BOOTSTRAP), "-g", "-s", "server", url],
                            cwd=out).returncode
    finally:
        serve.terminate()
        try:
            serve.wait(timeout=10)
        except subprocess.TimeoutExpired:
            serve.kill()
    if rc != 0:
        sys.exit(f"packwiz-installer exited {rc}; see its output above.")


def copy_data(out: Path) -> None:
    for d in DATA_DIRS:
        src = PACK / d
        if not src.is_dir():
            continue
        dst = out / d
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
            ".ruff_cache", "__pycache__", ".gitkeep"))
        print(f"copied {d}/")


def write_launchers(out: Path, neoforge: str, mc: str) -> None:
    installer = f"neoforge-{neoforge}-installer.jar"
    nf_url = (f"https://maven.neoforged.net/releases/net/neoforged/neoforge/"
              f"{neoforge}/{installer}")

    (out / "user_jvm_args.txt").write_text(
        "# Trashlands dedicated server JVM args. Edit -Xmx to your host's RAM.\n"
        "# 4G is a sane floor for this pack; 6G is comfortable.\n"
        "-Xmx4G\n", encoding="utf-8", newline="\n")

    (out / "eula.txt").write_text(
        "# Change to true to accept the Minecraft EULA "
        "(https://aka.ms/MinecraftEULA).\neula=false\n",
        encoding="utf-8", newline="\n")

    # level-type is the whole point. Default World Type is a client mod and does
    # nothing here, so without this line the server makes a vanilla overworld.
    (out / "server.properties").write_text(
        f"level-type={LEVEL_TYPE}\n"
        "max-tick-time=180000\n"
        "motd=Trashlands\n",
        encoding="utf-8", newline="\n")

    setup_sh = (
        "#!/usr/bin/env bash\n"
        "# Trashlands dedicated server. First run installs NeoForge, then boots.\n"
        "set -e\n"
        f'NEOFORGE="{neoforge}"\n'
        f'INSTALLER="{installer}"\n'
        'if [ ! -d "libraries" ]; then\n'
        '  if [ ! -f "$INSTALLER" ]; then\n'
        '    echo "Downloading NeoForge $NEOFORGE installer ..."\n'
        f'    curl -fL -o "$INSTALLER" "{nf_url}"\n'
        "  fi\n"
        '  echo "Installing NeoForge server ..."\n'
        '  java -jar "$INSTALLER" --installServer\n'
        "fi\n"
        "# NeoForge's --installServer writes its own run.sh; hand off to it.\n"
        'echo "Starting server ..."\n'
        "bash run.sh nogui\n"
    )
    (out / "setup.sh").write_text(setup_sh, encoding="utf-8", newline="\n")

    setup_bat = (
        "@echo off\r\n"
        "REM Trashlands dedicated server. First run installs NeoForge, then boots.\r\n"
        f"set NEOFORGE={neoforge}\r\n"
        f"set INSTALLER={installer}\r\n"
        "if not exist libraries (\r\n"
        '  if not exist "%INSTALLER%" (\r\n'
        "    echo Downloading NeoForge %NEOFORGE% installer ...\r\n"
        f'    curl -fL -o "%INSTALLER%" "{nf_url}"\r\n'
        "  )\r\n"
        "  echo Installing NeoForge server ...\r\n"
        '  java -jar "%INSTALLER%" --installServer\r\n'
        ")\r\n"
        "REM NeoForge's --installServer writes run.bat. If it is missing the install\r\n"
        "REM failed, and falling through would exit 0 having done nothing.\r\n"
        "if not exist run.bat (\r\n"
        "  echo NeoForge install failed - run.bat was never written.\r\n"
        "  exit /b 1\r\n"
        ")\r\n"
        "call run.bat nogui\r\n"
    )
    (out / "setup.bat").write_text(setup_bat, encoding="utf-8", newline="\r\n")

    # POSIX build machines get the real bit too, so `bash setup.sh` works straight
    # out of build/server without unzipping. make_zip forces it in the archive.
    try:
        (out / "setup.sh").chmod(0o755)
    except (OSError, NotImplementedError):
        pass  # Windows has no exec bit; the zip carries the mode regardless

    (out / "INSTALL.md").write_text(
        f"# Trashlands dedicated server ({mc} / NeoForge {neoforge})\n\n"
        "1. Unzip everything into your server directory.\n"
        "2. Accept the EULA: edit `eula.txt`, set `eula=true`.\n"
        "3. Adjust RAM in `user_jvm_args.txt` if needed (default `-Xmx4G`).\n"
        "4. Run `setup.sh` (Linux/Mac) or `setup.bat` (Windows). The first run "
        "downloads and installs NeoForge, then boots the server; later runs boot "
        "directly through NeoForge's own `run.sh` / `run.bat`.\n\n"
        "Java 25 is required. NeoForge 26.1 is compiled for it, and a Java 21 runtime "
        "dies at startup with UnsupportedClassVersionError before a single mod loads.\n\n"
        "## The world type matters, and it is already set\n\n"
        f"`server.properties` ships with `level-type={LEVEL_TYPE}`. That is the "
        "garbage world the whole pack is built on. Default World Type, which picks "
        "it for you in single player, is a client mod and does nothing on a server, "
        "so this line is the only thing making a server world Trashlands.\n\n"
        "## If you get an ordinary world instead of the dump\n\n"
        "The world was generated before that line was in place. World generation is "
        "decided once, at creation, and never re-evaluated, so changing "
        "`server.properties` afterwards does nothing to a world that already exists.\n\n"
        "Stop the server, delete the `world/` directory, and start it again. That is "
        "the only fix.\n\n"
        "## Client mods are not in here\n\n"
        "Sodium, FancyMenu and the rest of the client-side mods are deliberately "
        "absent; a dedicated server does not run them. Players still install the "
        "full client pack from CurseForge as normal.\n",
        encoding="utf-8", newline="\n")
    print("wrote launch scripts + INSTALL.md")


# packwiz-installer drops its own runtime artifacts into the working dir; they are
# not part of the server and should not ship. NeoForge boot-test leftovers
# (world/, libraries/, logs) are excluded too, in case --out was reused.
ZIP_EXCLUDE_NAMES = {"packwiz.json", "packwiz-installer.jar",
                     "packwiz-installer-bootstrap.jar",
                     # Client-side pack files. packwiz-installer fetches these
                     # because plain index entries carry no side, unlike mods.
                     # A server ignores them; they are dropped to keep the zip
                     # honest about what a server actually uses.
                     "options.txt", "icon.png"}
ZIP_EXCLUDE_TOPDIRS = {"world", "libraries", "logs", "crash-reports",
                       "dynamic-data-pack-cache", "versions", "resourcepacks"}
# Boot-test scratch, matched at the install root ONLY. Matching "boot*" anywhere
# would quietly drop a config file like config/<mod>/bootstrap.json from the
# server pack, and nothing compares the zip's config/ against pack/config/.
ZIP_EXCLUDE_ROOT_PREFIXES = ("boot", "install")
# Stored with the executable bit set. Zip preserves whatever mode the file has on
# disk, and Windows cannot set an exec bit at all, so the mode is forced here
# rather than left to the build machine. Without it INSTALL.md's "run setup.sh"
# is a permission error on every Linux host.
EXECUTABLE_NAMES = {"setup.sh"}


def make_zip(out: Path, version: str) -> Path:
    dist = REPO / "dist"
    dist.mkdir(exist_ok=True)
    zip_path = dist / f"trashlands-server-{version}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(out)
            if rel.name in ZIP_EXCLUDE_NAMES or rel.parts[0] in ZIP_EXCLUDE_TOPDIRS:
                continue
            if rel.suffix == ".log":
                continue
            if len(rel.parts) == 1 and rel.name.startswith(ZIP_EXCLUDE_ROOT_PREFIXES):
                continue
            info = zipfile.ZipInfo.from_file(p, rel.as_posix())
            info.compress_type = zipfile.ZIP_DEFLATED
            if rel.name in EXECUTABLE_NAMES:
                # 0o100755, not 0o755: the high bits are the full st_mode and must
                # keep S_IFREG, or the entry has no file type and strict unzip
                # implementations do not treat it as a regular file.
                info.external_attr = (0o100755 << 16) | (info.external_attr & 0xFFFF)
            zf.writestr(info, p.read_bytes())
    print(f"\nbuilt {zip_path}  ({zip_path.stat().st_size // 1024} KiB)")
    return zip_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the Trashlands dedicated-server pack.")
    ap.add_argument("--out", type=Path, default=REPO / "build" / "server",
                    help="install directory (default: build/server)")
    ap.add_argument("--neoforge", default="", help="NeoForge version (default: from pack.toml)")
    ap.add_argument("--port", type=int, default=0, help="packwiz serve port (default: auto)")
    ap.add_argument("--no-zip", action="store_true", help="install only; do not zip")
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    if not (PACK / "pack.toml").is_file():
        sys.exit(f"pack not found at {PACK}")
    for tool in ("packwiz", "java"):
        if shutil.which(tool) is None:
            sys.exit(f"`{tool}` not found on PATH.")

    version = read_pack_field("version")
    mc = read_pack_field("minecraft")
    neoforge = args.neoforge or read_pack_field("neoforge")
    if not (version and neoforge):
        sys.exit("could not read version/neoforge from pack.toml")
    port = args.port or free_port()

    print("refreshing index (tools/pack_refresh.py) ...")
    if subprocess.run([sys.executable, str(TOOLS / "pack_refresh.py")]).returncode != 0:
        sys.exit("tools/pack_refresh.py failed")

    out = args.out.resolve()
    if out.exists():
        shutil.rmtree(out)
    install_mods(out, port)
    copy_data(out)
    write_launchers(out, neoforge, mc)

    n_mods = len(list((out / "mods").glob("*.jar"))) if (out / "mods").is_dir() else 0
    print(f"\nserver install ready in {out}  ({n_mods} mod jars)")
    if n_mods == 0:
        sys.exit("no mod jars were installed - check the side tags in pack/mods/")
    if not args.no_zip:
        make_zip(out, version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
