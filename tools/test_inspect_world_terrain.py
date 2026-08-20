#!/usr/bin/env python3
"""Exit-code tests for `inspect_world_terrain.py`, the release's world-type gate.

Why this file exists
--------------------
That tool decides whether a release ships. Nothing else exercised it, and its
whole value is returning the *right* code: exit 1 blocks a release, exit 2 lets
one through with a warning. Getting either wrong is worse than having no check -
the first blocks a good release, the second is a gate that silently always
passes.

Every case below is a way this tool got it wrong at least once while it was being
written. The `.mcc` one in particular: Anvil sets bit 0x80 on the compression
byte for chunks stored in a sidecar, and treating that as unreadable meant one
oversized chunk anywhere in the world downgraded a genuinely wrong world from
fatal to a warning.

Run:
    python tools/test_inspect_world_terrain.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import shutil
import struct
import sys
import tempfile
import zlib

HERE = pathlib.Path(__file__).resolve().parent
SECTOR = 4096
ZLIB = 2
EXTERNAL = 0x80
NUL = b"\x00"


def load_tool():
    spec = importlib.util.spec_from_file_location(
        "inspect_world_terrain", HERE / "inspect_world_terrain.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def nbt(payload: bytes) -> bytes:
    """A compound-tag header plus arbitrary bytes - enough for an id regex scan."""
    return zlib.compress(b"\x0a" + NUL + NUL + payload)


OURS = nbt(b" biomes recompile:household_sprawl")
THEIRS = nbt(b" biomes minecraft:plains")
NO_BIOME = nbt(b" minecraft:air proto chunk with no palette")


def write_region(root: pathlib.Path, name: str, entries) -> pathlib.Path:
    """entries: [(header_index, raw_compression_byte, payload_bytes)]"""
    region = root / "region"
    region.mkdir(parents=True, exist_ok=True)
    header = bytearray(SECTOR * 2)
    body, sector = b"", 2
    for idx, raw_scheme, payload in entries:
        struct.pack_into(">I", header, idx * 4, (sector << 8) | 1)
        blob = struct.pack(">I", len(payload) + 1) + bytes([raw_scheme]) + payload
        blob += NUL * (-len(blob) % SECTOR)
        body += blob
        sector += len(blob) // SECTOR
    (region / name).write_bytes(bytes(header) + body)
    return region


# Each case builds a world and states the exit code it must produce.
def c_ours(root):
    write_region(root, "r.0.0.mca", [(0, ZLIB, OURS)])


def c_foreign(root):
    write_region(root, "r.0.0.mca", [(0, ZLIB, THEIRS)])


def c_no_region_dir(root):
    (root / "data").mkdir()


def c_corrupt(root):
    write_region(root, "r.0.0.mca", [(0, ZLIB, b"\xff" * 40)])


def c_no_biome(root):
    write_region(root, "r.0.0.mca", [(0, ZLIB, NO_BIOME)])


def c_partial(root):
    write_region(root, "r.0.0.mca", [(0, ZLIB, THEIRS), (1, ZLIB, b"\xff" * 40)])


def c_empty_region_is_normal(root):
    region = write_region(root, "r.0.0.mca", [(0, ZLIB, THEIRS)])
    (region / "r.9.9.mca").write_bytes(b"")


def c_truncated_region(root):
    region = write_region(root, "r.0.0.mca", [(0, ZLIB, THEIRS)])
    (region / "r.9.9.mca").write_bytes(NUL * 100)


def c_external_present(root):
    region = write_region(root, "r.0.0.mca", [(0, EXTERNAL | ZLIB, b"")])
    (region / "c.0.0.mcc").write_bytes(OURS)


def c_external_missing(root):
    write_region(root, "r.0.0.mca", [(0, EXTERNAL | ZLIB, b"")])


def c_modern_layout(root):
    write_region(root / "dimensions" / "minecraft" / "overworld",
                 "r.0.0.mca", [(0, ZLIB, OURS)])


CASES = [
    ("our terrain is recognised", 0, c_ours),
    ("a foreign world fails the release", 1, c_foreign),
    ("no region dir cannot judge", 2, c_no_region_dir),
    ("a corrupt chunk cannot judge", 2, c_corrupt),
    ("chunks with no biome palette cannot judge", 2, c_no_biome),
    ("partial evidence withholds the verdict", 2, c_partial),
    ("an empty region file is normal, not a gap", 1, c_empty_region_is_normal),
    ("a truncated region file IS a gap", 2, c_truncated_region),
    ("an external .mcc chunk is read, not skipped", 0, c_external_present),
    ("a missing .mcc is a gap", 2, c_external_missing),
    ("the 26.1 dimensions/ layout is found", 0, c_modern_layout),
]


def main() -> int:
    tool = load_tool()
    failures = 0
    for name, expect, build in CASES:
        root = pathlib.Path(tempfile.mkdtemp(prefix="terrain-test-"))
        saved = sys.argv
        try:
            build(root)
            sys.argv = ["inspect_world_terrain.py", str(root)]
            got = tool.main()
        finally:
            sys.argv = saved
            shutil.rmtree(root, ignore_errors=True)
        ok = got == expect
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  exit {got} (want {expect})  {name}")
    print(f"\n{len(CASES)} case(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
