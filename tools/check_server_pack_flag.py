#!/usr/bin/env python3
"""Audit whether Trashlands' CurseForge files are typed as Server Packs.

Every release attaches `trashlands-server-<version>.zip` to its client file via the
upload API's `parentFileID` (see `.github/workflows/release.yml`). That makes the zip
public under "Additional Files" - but it does NOT make CurseForge treat it as a
*Server Pack*. Those are two different things:

  additional file  -> visible on the file page, downloadable by humans
  server pack      -> the above, PLUS `serverPackFileId` / `isServerPack` set in CF's
                      Core API, which is what server hosts and launcher "create a
                      server" flows read (BisectHosting, Akliz, Nodecraft, Pterodactyl
                      eggs, itzg/docker-minecraft-server AUTO_CURSEFORGE).

The CurseForge **upload API cannot set that flag** - `upload-file` accepts only
changelog / changelogType / displayName / parentFileID / gameVersions /
gameVersionNames / releaseType / isMarkedForManualRelease / relations, and
`update-file` is the same minus parentFileID. CF support confirmed there is no
documented way (henkelmax/upload-curseforge-modpack-action#1, where sending
`isServerPack: true` in the metadata was tested and silently ignored). So the flag is
a MANUAL step in the Authors Console, once per release:

    Authors Console -> Trashlands -> Files -> click the client file
      -> the attached server file -> set "Additional File Info" to "Server Pack"
         (default is "None")

This script is the verification half of that manual step. It reads the website's own
undocumented v1 API - no API key needed:

    GET https://www.curseforge.com/api/v1/mods/<projectId>/files?pageIndex=&pageSize=

Each file carries `hasServerPack` (bool) and `additionalServerPackFilesCount` (int)
alongside `additionalFilesCount`. A correctly-typed release reads
additionalFilesCount >= 1 AND hasServerPack true. Undocumented, so it could change; if
the fields disappear, fall back to the file page (the same values are embedded in its
Next.js payload).

Usage:
    python tools/check_server_pack_flag.py              # latest 5 files
    python tools/check_server_pack_flag.py --all
    python tools/check_server_pack_flag.py --project 1636627
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

PROJECT_ID = 1636627  # Trashlands on CurseForge
API = "https://www.curseforge.com/api/v1/mods/{pid}/files?pageIndex=0&pageSize={n}"
UA = "Mozilla/5.0 (trashlands check_server_pack_flag.py)"


def fetch(project_id: int, count: int) -> list[dict]:
    req = urllib.request.Request(API.format(pid=project_id, n=count),
                                 headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"CurseForge returned HTTP {e.code}. The undocumented v1 API may have moved.")
    except Exception as e:  # noqa: BLE001
        sys.exit(f"could not reach CurseForge: {e}")
    data = payload.get("data")
    if data is None:
        sys.exit("unexpected response shape - no 'data' key. The v1 API may have changed.")
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="Check the Server Pack flag on CurseForge files.")
    ap.add_argument("--project", type=int, default=PROJECT_ID)
    ap.add_argument("--all", action="store_true", help="check every file, not just the latest 5")
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    files = fetch(args.project, 200 if args.all else 5)
    if not files:
        print("no files on the project yet.")
        return 0

    bad = 0
    print(f"{'file':<34} {'addl':>4} {'srvpack':>8}  status")
    for f in files:
        name = (f.get("displayName") or f.get("fileName") or "?")[:33]
        addl = f.get("additionalFilesCount", 0) or 0
        has = bool(f.get("hasServerPack"))
        # A file with no attachment at all is not a failure: releases before the
        # server pack existed legitimately have none.
        if addl == 0:
            status = "no attachment"
        elif has:
            status = "OK - typed"
        else:
            status = "NOT TYPED - fix in Authors Console"
            bad += 1
        print(f"{name:<34} {addl:>4} {str(has):>8}  {status}")

    if bad:
        print(f"\n{bad} file(s) have an attached server pack that is NOT typed as a Server Pack.")
        print("Authors Console -> Trashlands -> Files -> the file -> the attached server file")
        print("  -> Additional File Info -> Server Pack")
        print("\nUntil that is set, host one-click deploys cannot see the server pack.")
        return 1
    print("\nevery attached server pack is typed correctly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
