#!/usr/bin/env python3
"""Upload a packwiz-exported modpack zip to CurseForge as a new file.

This is the MANUAL path. The normal path is a tag push, which fires
`.github/workflows/release.yml`. Reach for this script when the project is still
in moderation, when CI is unavailable, or when a file needs re-uploading.

CurseForge's author upload API only uploads FILES - it cannot set the project
description (that is dashboard-only; the description's source of truth is
docs/curseforge_page.md, pasted by hand below its PASTE MARKER).

Game-version ids are RESOLVED FROM THE API, not hardcoded. A single Minecraft
version name exists several times in CurseForge's version list under different
types, and only one is valid for a modpack:

    26.1.2 -> id 16082 (type 83806, slug "minecraft-26-1")   <- correct
           -> id 16085 (type 1, the mod-class version)        -> errorCode 1009
           -> id 16130 (type 615, slug "addons")              -> errorCode 1009

Matching on name alone picks a wrong id about two times in three. The filter is
that the version's type slug starts with "minecraft-" (excluding snapshots),
which selects the release-series type and nothing else. A Java-version id must
NOT be sent for a modpack - CurseForge rejects it; Java is implied by the loader.

The token is read from CURSEFORGE_API_KEY, or from ../recompile/.env if unset
(same author account). It is never printed.

Ported from ../sky-frogs/tools/cf_release.py, which hardcodes its ids.

Usage:
    python tools/cf_release.py --zip "pack/Trashlands-0.1.0.zip" --project 1234567 \
        --display-name "Trashlands 0.1.0" \
        --release-type alpha \
        --changelog-file release_notes.md

    python tools/cf_release.py --zip ... --project ... --display-name ... --dry-run
"""
import argparse
import json
import os
import re
import sys
import uuid
from urllib import error, request

sys.stdout.reconfigure(encoding="utf-8")

UPLOAD_URL = "https://minecraft.curseforge.com/api/projects/%d/upload-file"
GAME_API = "https://minecraft.curseforge.com/api/game/%s"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK_TOML = os.path.join(REPO, "pack", "pack.toml")
# Same author account as this pack, so the same upload token works.
ENV_FALLBACK = os.path.join(os.path.dirname(REPO), "recompile", ".env")


def resolve_token():
    token = os.environ.get("CURSEFORGE_API_KEY")
    if token:
        return token.strip()
    if os.path.exists(ENV_FALLBACK):
        for line in open(ENV_FALLBACK, encoding="utf-8"):
            if line.startswith("CURSEFORGE_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("No CURSEFORGE_API_KEY in env or %s" % ENV_FALLBACK)


def api(path, token):
    req = request.Request(GAME_API % path, headers={"X-Api-Token": token})
    with request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def mc_version_from_pack():
    """Read the Minecraft version out of pack.toml so this never drifts from the pack."""
    text = open(PACK_TOML, encoding="utf-8").read()
    m = re.search(r'^minecraft\s*=\s*"([^"]+)"', text, re.M)
    if not m:
        sys.exit("could not read [versions] minecraft from %s" % PACK_TOML)
    return m.group(1)


def resolve_game_versions(token, mc_version):
    """Return [mc_id, neoforge_id] using the modpack-valid version types.

    Fails here rather than on the upload: CurseForge's 400 arrives after the whole
    zip has been transferred, and its errorCode does not say which id was bad.
    """
    types = api("version-types", token)
    versions = api("versions", token)

    # Snapshot types are excluded by substring, not exact slug: the slug carries the
    # series ("minecraft-26-snapshots"), so an equality check silently stops matching
    # on the next MC major.
    mc_type_ids = {t["id"] for t in types
                   if (t.get("slug") or "").startswith("minecraft-")
                   and "snapshot" not in (t.get("slug") or "")}
    loader_type_ids = {t["id"] for t in types if (t.get("slug") or "") == "modloader"}

    mc_id = next((v["id"] for v in versions
                  if v.get("name") == mc_version
                  and v.get("gameVersionTypeID") in mc_type_ids), None)
    loader_id = next((v["id"] for v in versions
                      if v.get("name") == "NeoForge"
                      and v.get("gameVersionTypeID") in loader_type_ids), None)

    if mc_id is None:
        sys.exit("no CurseForge modpack-class id for Minecraft %s" % mc_version)
    if loader_id is None:
        sys.exit("no CurseForge id resolved for the NeoForge modloader")

    print("resolved gameVersions: MC %s=%d, NeoForge=%d" % (mc_version, mc_id, loader_id))
    return [mc_id, loader_id]


def encode_multipart(metadata, zip_path):
    boundary = "----trashlands" + uuid.uuid4().hex
    crlf = b"\r\n"
    parts = []
    parts.append(b"--" + boundary.encode())
    parts.append(b'Content-Disposition: form-data; name="metadata"')
    parts.append(b"")
    parts.append(metadata.encode("utf-8"))
    parts.append(b"--" + boundary.encode())
    fname = os.path.basename(zip_path)
    parts.append(('Content-Disposition: form-data; name="file"; filename="%s"' % fname).encode())
    parts.append(b"Content-Type: application/zip")
    parts.append(b"")
    with open(zip_path, "rb") as handle:
        parts.append(handle.read())
    parts.append(b"--" + boundary.encode() + b"--")
    parts.append(b"")
    return boundary, crlf.join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, help="Path to the packwiz-exported CF zip")
    parser.add_argument("--project", type=int, required=True,
                        help="Numeric CurseForge project id (also stored as the CF_PROJECT_ID repo variable)")
    parser.add_argument("--display-name", required=True, help='Human file name, e.g. "Trashlands 0.1.0"')
    parser.add_argument("--release-type", default="alpha", choices=["alpha", "beta", "release"])
    parser.add_argument("--changelog-file", help="Path to a markdown changelog for this file")
    parser.add_argument("--changelog", default="", help="Inline changelog (ignored if --changelog-file given)")
    parser.add_argument("--dry-run", action="store_true", help="Build the request but do not POST")
    args = parser.parse_args()

    if not os.path.exists(args.zip):
        sys.exit("Zip not found: %s" % args.zip)

    # A manifest-only export has no jars in it. One appearing means a mod came from a
    # non-CurseForge source and packwiz inlined the jar into overrides/, which CF
    # rejects on redistribution grounds. Catch it before the upload, not in moderation.
    import zipfile
    with zipfile.ZipFile(args.zip) as z:
        jars = [n for n in z.namelist() if n.lower().endswith(".jar")]
    if jars:
        sys.exit("ABORT: the export contains %d .jar file(s):\n  %s\n"
                 "Every mod must be added with `packwiz curseforge add`."
                 % (len(jars), "\n  ".join(jars)))

    changelog = args.changelog
    if args.changelog_file:
        changelog = open(args.changelog_file, encoding="utf-8").read()

    token = resolve_token()
    metadata = json.dumps({
        "changelog": changelog,
        "changelogType": "markdown",
        "displayName": args.display_name,
        "gameVersions": resolve_game_versions(token, mc_version_from_pack()),
        "releaseType": args.release_type,
    })

    boundary, body = encode_multipart(metadata, args.zip)
    print("Uploading %s (%d bytes) as %s [%s] to project %d ..." % (
        os.path.basename(args.zip), os.path.getsize(args.zip),
        args.display_name, args.release_type, args.project))
    if args.dry_run:
        print("--dry-run: not sending. metadata=%s" % metadata)
        return

    req = request.Request(
        UPLOAD_URL % args.project,
        data=body,
        headers={
            "X-Api-Token": token,
            "Content-Type": "multipart/form-data; boundary=%s" % boundary,
            "User-Agent": "trashlands-release/1.0",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=120) as resp:
            payload = resp.read().decode("utf-8", "replace")
            print("HTTP %d: %s" % (resp.status, payload))
            try:
                file_id = json.loads(payload).get("id")
                if file_id:
                    print("Uploaded. File ID: %s" % file_id)
                    print("https://www.curseforge.com/minecraft/modpacks/trashlands/files/%s" % file_id)
            except (ValueError, AttributeError):
                pass
    except error.HTTPError as exc:
        sys.exit("Upload failed: HTTP %d\n%s" % (exc.code, exc.read().decode("utf-8", "replace")))
    except error.URLError as exc:
        sys.exit("Upload failed (network): %s" % exc.reason)


if __name__ == "__main__":
    main()
