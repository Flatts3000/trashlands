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
`additionalServerPackFilesCount >= 1` AND `hasServerPack` true. The all-attachments
count is deliberately not the signal: a file can carry a typed server pack plus some
other attachment, and a pre-server-pack release can carry an attachment that was never
meant to be one. Undocumented, so it could change; if the fields disappear, fall back
to the file page (the same values are embedded in its Next.js payload).

An empty listing is NOT a pass, which is what this script used to treat it as. On
2026-08-30 it printed "no files on the project yet." and exited 0 for a project that
had just taken its tenth release, and `release_checklist.md` step 3 says to confirm the
manual typing with this script - so the check had been reporting success without ever
running. The files were not missing: `www.curseforge.com/api/v1/mods/1636627/files`
returns `totalCount: 0` for both this project and Recompile (1625740) while returning
real data for JEI (238222) through the identical call, and packwiz resolves Recompile
by numeric id off the Core API and downloads the file released the same day. So the
files exist and serve; they are absent from THIS listing surface. Slug lookup on the
Core API fails for our projects too and succeeds for third-party ones, so it is the
name-and-listing surfaces that do not have them, not the file store.

That is why an empty result now runs a CONTROL probe against a third-party project
before saying anything. If the control returns files and the target does not, the
endpoint works and the target is absent from it. If neither returns files, the endpoint
or the WAF in front of it is the problem and this script cannot tell you anything. Both
are exit 2 - unverified - and neither is a pass.

Usage:
    python tools/check_server_pack_flag.py              # latest 5 files
    python tools/check_server_pack_flag.py --all
    python tools/check_server_pack_flag.py --project 1636627
    python tools/check_server_pack_flag.py --control 238222

Exit codes: 0 = every attached server pack is typed, 1 = one or more is not,
2 = could not verify (empty listing, unreachable API, unexpected shape),
3 = files listed but NONE carries an attachment at all.

3 is deliberately not 2. A 2 means this script could not see anything; a 3 means it saw
the files clearly and the server pack was never attached, which points at the release
workflow rather than at CurseForge. While #55 keeps 2 as the everyday result, folding
them together would let a real 3 be waved off as the known cosmetic failure.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request

PROJECT_ID = 1636627  # Trashlands on CurseForge
# A busy third-party project, used only to prove the endpoint answers at all. Any
# project with files would do; JEI is in this pack and is never going to go quiet.
CONTROL_ID = 238222   # Just Enough Items
API = "https://www.curseforge.com/api/v1/mods/{pid}/files?pageIndex=0&pageSize={n}"
UA = "Mozilla/5.0 (trashlands check_server_pack_flag.py)"


def fetch(project_id: int, count: int) -> list[dict] | None:
    """The project's files, or None if the endpoint could not be read.

    None and [] mean different things and the caller has to tell them apart: None is
    "the API did not answer", [] is "the API answered and named no files". Returning
    None rather than exiting lets the control probe run either way.
    """
    req = urllib.request.Request(API.format(pid=project_id, n=count),
                                 headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"CurseForge returned HTTP {e.code} for project {project_id}. "
              "The undocumented v1 API may have moved.")
        return None
    except Exception as e:  # noqa: BLE001
        print(f"could not reach CurseForge for project {project_id}: {e}")
        return None
    data = payload.get("data")
    if data is None:
        print(f"unexpected response shape for project {project_id} - no 'data' key. "
              "The v1 API may have changed.")
        return None
    return data


def explain_empty(project_id: int, files: list[dict] | None, control_id: int) -> int:
    """Say WHY there were no files to check, using a control project. Never returns 0.

    `files` is None when the target listing could not be READ and [] when it answered
    and named nothing. Those are different findings and the whole point of the control
    probe is to tell them apart, so neither this function nor its caller may collapse
    them - an unreadable target reported as "absent from the listing" asserts a fact
    nobody observed, which is what this script was fixed for in the first place.
    """
    unreadable = files is None
    if unreadable:
        print(f"could not read the v1 listing for project {project_id}.")
    else:
        print(f"the v1 listing answered for project {project_id} and named no files.")

    if control_id == project_id:
        # Probing a project against itself proves nothing: the second request is
        # byte-identical to the first. Say so rather than draw a conclusion from it.
        print(f"control is the same project ({control_id}), so there is nothing to compare "
              "against.")
        print("Pass a different --control to get a diagnosis.")
        print()
        print("UNVERIFIED - the Server Pack typing was not checked. This is not a pass.")
        return 2

    print(f"probing control project {control_id} to see whether the endpoint answers at all...")
    control = fetch(control_id, 1)
    print()
    if control:
        print(f"  control {control_id}: {len(control)} file(s) -> the endpoint works.")
        if unreadable:
            print(f"  project {project_id}: unreadable -> that one request failed while the")
            print("  endpoint itself is fine. A transient block or rate limit fits; being absent")
            print("  from the listing does not, because absence answers rather than fails.")
        else:
            print(f"  project {project_id}: 0 files -> this project is absent from THIS listing.")
            print()
            print("That is not the same as having no files. The Core API serves these files by")
            print("numeric id even while this listing is empty - packwiz resolves them that way -")
            print("so check the Authors Console.")
    elif control is None:
        print(f"  control {control_id}: unreadable too -> the endpoint, or the WAF in front of")
        print("  it, is the problem rather than this project. Nothing can be concluded about")
        print("  the files at all.")
    else:
        # Control answered with an empty list. Readable, and empty for a project that
        # is known to have files - so the listing surface is returning nothing to
        # anybody. Stronger and different from "unreachable".
        print(f"  control {control_id}: answered with 0 files -> the endpoint is readable and")
        print("  is listing nothing for a project that certainly has files. The listing surface")
        print("  is empty for everyone, not just this project.")
    print()
    print("UNVERIFIED - the Server Pack typing was not checked. This is not a pass.")
    return 2


def main() -> int:
    ap = argparse.ArgumentParser(description="Check the Server Pack flag on CurseForge files.")
    ap.add_argument("--project", type=int, default=PROJECT_ID)
    ap.add_argument("--all", action="store_true", help="check every file, not just the latest 5")
    ap.add_argument("--control", type=int, default=CONTROL_ID,
                    help=f"project used to prove the endpoint answers (default {CONTROL_ID})")
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    files = fetch(args.project, 200 if args.all else 5)
    if not files:
        # None (unreadable) and [] (answered, named nothing) both land here and both are
        # failures, but they are DIFFERENT failures - explain_empty is handed the state
        # rather than a truthiness test so it can say which one happened.
        return explain_empty(args.project, files, args.control)

    bad = 0
    print(f"{'file':<34} {'addl':>4} {'srvpack':>8}  status")
    for f in files:
        name = (f.get("displayName") or f.get("fileName") or "?")[:33]
        addl = f.get("additionalFilesCount", 0) or 0
        typed = f.get("additionalServerPackFilesCount", 0) or 0
        has = bool(f.get("hasServerPack"))
        # Key off the server-pack counter, not the attachment counter. A release can
        # carry attachments that are not server packs, and a client file with one of
        # those plus nothing else is not a failure - it is a release from before the
        # server pack existed. Conversely a file can carry a typed pack AND an
        # untyped extra, which the all-attachments count cannot tell apart.
        if addl == 0:
            status = "no attachment"
        elif typed >= 1 and has:
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
    attached = sum(1 for f in files if (f.get("additionalFilesCount", 0) or 0) > 0)
    if attached == 0:
        # Vacuous truth is the same defect this script was fixed for: "every attached
        # server pack is typed" is trivially true when nothing is attached, and every
        # release since v0.7.0 attaches one. Say what was actually seen.
        print(f"\nnone of the {len(files)} file(s) listed carries an attachment at all, "
              "so there was nothing to check.")
        print("Every release since v0.7.0 attaches a server pack, so this is a finding, "
              "not a pass.")
        print("This is exit 3, not 2: the listing was read fine and the attachment is missing,")
        print("which points at the release workflow rather than at CurseForge.")
        return 3
    print(f"\nevery attached server pack is typed correctly ({attached} of {len(files)} "
          "file(s) carried one).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
