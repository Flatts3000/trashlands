#!/usr/bin/env python3
"""Report what a generated world's level.dat says about its generator.

Used by the release workflow's server boot smoke test. The server pack sets
``level-type=recompile:garbage`` in server.properties, and an unknown level-type
does not crash - Minecraft resolves it against the WORLD_PRESET registry and
falls back to ``minecraft:normal``. So a renamed or misspelled preset would hand
every server an ordinary overworld while CI stayed green, which is the failure
this exists to make visible.

**This reports; it does not assert.** The first attempt at the check was a single
``zcat world/level.dat | grep -q recompile:region`` in the workflow, and it failed
a release whose pack was fine while being unable to say why: that one pipeline
conflates "the preset did not apply", "level.dat has not been written yet" and
"the file could not be decompressed". Exactly where MC 26.1 records the resolved
generator has not been established here, so this prints the namespaced ids it can
actually find and leaves the judgement to a person reading the log. Once the log
shows what a correct world looks like, this can grow a real exit code.

Usage:
    python tools/inspect_level_dat.py world/level.dat
"""
from __future__ import annotations

import gzip
import pathlib
import re
import sys

GZIP_MAGIC = bytes([0x1F, 0x8B])
ID_RE = re.compile(rb"[a-z0-9_]+:[a-z0-9_/.-]+")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: inspect_level_dat.py <path to level.dat>")
        return 2
    path = pathlib.Path(sys.argv[1])

    if not path.is_file():
        print(f"::warning::{path} does not exist - the world type could not be verified.")
        parent = path.parent
        if parent.is_dir():
            print(f"contents of {parent}:")
            for p in sorted(parent.iterdir())[:20]:
                print("   ", p.name)
        else:
            print(f"({parent} does not exist either - no world was written)")
        return 0

    raw = path.read_bytes()
    try:
        data = gzip.decompress(raw) if raw[:2] == GZIP_MAGIC else raw
    except OSError as e:
        print(f"::warning::could not decompress {path}: {e}")
        return 0

    print(f"{path}: {len(raw)} bytes on disk, {len(data)} decompressed")

    ids = sorted({m.decode("ascii", "replace") for m in ID_RE.findall(data)})
    ours = [i for i in ids if i.startswith("recompile:")]

    if ours:
        print("recompile ids are present, so the garbage preset applied:")
        for i in ours:
            print("   ", i)
        return 0

    print("::warning::no recompile: id found in level.dat - the preset may not have applied.")
    print("namespaced ids actually present, to write a real assertion from:")
    for i in ids[:40]:
        print("   ", i)
    if len(ids) > 40:
        print(f"    ... and {len(ids) - 40} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
