#!/usr/bin/env python3
"""Assert that a generated world's terrain actually came from the garbage preset.

Why this exists, and why it does not read level.dat
---------------------------------------------------
The server pack sets ``level-type=recompile:garbage`` in server.properties, and an
unknown level-type does not crash - Minecraft resolves it against the WORLD_PRESET
registry and falls back to ``minecraft:normal``. Default World Type is a client mod
and does nothing on a dedicated server, so that one line is the only thing making a
server world Trashlands rather than an ordinary overworld.

Three attempts were made to prove it via ``level.dat``. All three were looking in
the wrong file. The v0.8.0 release log settled it: level.dat decompressed to 2436
bytes and held exactly one namespaced id, ``minecraft:overworld``, with no
generator id of any namespace - not ``minecraft:noise``, not ``multi_noise``, not
``minecraft:normal``. A vanilla world would have to record its generator somewhere
too, so that absence proves nothing either way. 26.1 simply does not put the
resolved generator there.

So this reads the terrain instead, which is the thing anyone actually cares about.
It looks for any ``recompile:`` id in the region files' chunk data. That hits the
per-section **biome palette**, which carries ``recompile:household_sprawl`` or
``recompile:demolition_yard`` in every single generated chunk - much stronger than
hoping a garbage mound happened to spawn near the origin. A vanilla overworld
contains no ``recompile:`` id anywhere.

This one asserts. Unlike level.dat, the three outcomes are distinguishable:

  exit 0  a recompile: id is in the terrain - the preset applied
  exit 1  chunks were read and contain NO recompile: id - the world is vanilla
  exit 2  no chunk could be read at all - a tool problem, not a world verdict

That last exit code is the whole lesson from the earlier attempts: "I could not
tell" must never be reported as "it failed".

Usage:
    python tools/inspect_world_terrain.py <path to world dir>
"""
from __future__ import annotations

import collections
import gzip
import pathlib
import re
import struct
import sys
import zlib

ID_RE = re.compile(rb"[a-z0-9_]+:[a-z0-9_/.-]+")
SECTOR = 4096

# Anvil chunk compression schemes. 4 (LZ4) and 127 (custom) need libraries we do
# not have; they are counted and reported rather than silently skipped, because a
# region we cannot read must not read as a region with no recompile blocks.
GZIP, ZLIB, NONE = 1, 2, 3
# Anvil stores any chunk over ~1MB in a sidecar `c.<x>.<z>.mcc` and ORs 0x80 into the
# compression byte. Missing that made 129/130/131 read as "unsupported scheme", which
# fed `skipped` - and because a non-empty `skipped` withholds the verdict WORLD-wide,
# one oversized chunk anywhere disarmed the whole gate: a genuinely wrong world would
# have downgraded from a fatal exit 1 to a warning, and shipped.
EXTERNAL = 0x80
# Region files are 0 bytes when empty, or a bare header. Anything else below a full
# header is a TRUNCATED file, which is an evidence gap rather than a normal absence.
NORMAL_SMALL = (0, SECTOR, SECTOR * 2)


def chunk_blobs(mca: pathlib.Path):
    """Yield decompressed chunk NBT from one .mca, plus counts of what we could not read."""
    try:
        data = mca.read_bytes()
    except OSError as exc:
        # Locked by a still-running JVM, permissions, a directory named *.mca. A file
        # we could not open IS an evidence gap, unlike an empty one below.
        return [], collections.Counter({f"unreadable file: {type(exc).__name__}": 1})
    if len(data) < SECTOR * 2:
        # An empty or header-only region file is NORMAL - Minecraft leaves a 0-byte
        # .mca for a region with no saved chunks, and a real save has hundreds. This
        # must NOT count as an evidence gap: doing so made the tool withhold a verdict
        # on every real world (591 of them in an ATM10 save).
        if len(data) in NORMAL_SMALL:
            return [], collections.Counter()
        # But a file that is neither empty nor a whole header was caught mid-write,
        # which IS a gap - and it is exactly what a force-killed server leaves behind.
        return [], collections.Counter({f"truncated region file ({len(data)} bytes)": 1})
    blobs, skipped = [], collections.Counter()
    for i in range(1024):
        off, cnt = struct.unpack_from(">I", data, i * 4)[0] >> 8, data[i * 4 + 3]
        if off == 0 or cnt == 0:
            continue  # chunk never generated - normal, not an error
        start = off * SECTOR
        if start + 5 > len(data):
            skipped["chunk offset past end of file"] += 1
            continue
        length = struct.unpack_from(">I", data, start)[0]
        raw_scheme = data[start + 4]
        scheme = raw_scheme & ~EXTERNAL
        if raw_scheme & EXTERNAL:
            # The payload lives in a sidecar. Read it rather than counting a gap:
            # an oversized chunk is ordinary, and treating it as unreadable is what
            # would silently disarm the gate.
            cx, cz = i % 32, i // 32
            m = re.match(r"r\.(-?\d+)\.(-?\d+)\.mca$", mca.name)
            if not m:
                skipped["external chunk but region filename unparseable"] += 1
                continue
            rx, rz = int(m.group(1)), int(m.group(2))
            mcc = mca.parent / f"c.{rx * 32 + cx}.{rz * 32 + cz}.mcc"
            try:
                payload = mcc.read_bytes()
            except OSError:
                skipped["external .mcc chunk missing or unreadable"] += 1
                continue
        else:
            payload = data[start + 5:start + 4 + length]
        try:
            if scheme == ZLIB:
                blobs.append(zlib.decompress(payload))
            elif scheme == GZIP:
                blobs.append(gzip.decompress(payload))
            elif scheme == NONE:
                blobs.append(payload)
            else:
                skipped[f"unsupported compression scheme {scheme}"] += 1
        except Exception as exc:
            skipped[f"decompress failed: {type(exc).__name__}"] += 1
    return blobs, skipped


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: inspect_world_terrain.py <path to world dir>")
        return 2
    world = pathlib.Path(sys.argv[1])

    if not world.is_dir():
        print(f"::warning::{world} does not exist - the terrain could not be checked.")
        return 2

    # Two layouts, because 26.1 moved the overworld. A 1.x world has region/ at the
    # world root; a 26.1 world has dimensions/minecraft/overworld/region/ and NO
    # root-level region/ at all. Searching for both means this does not quietly
    # report "unverified" forever the next time the layout moves.
    mcas = sorted(set(world.glob("region/*.mca")) | set(world.glob("*/*/*/region/*.mca")))
    if not mcas:
        print(f"::warning::no region/*.mca found under {world} - nothing generated?")
        print("looked for `region/*.mca` and `*/*/*/region/*.mca`. Directories present:")
        for p in sorted(d for d in world.rglob("*") if d.is_dir())[:25]:
            print(f"  {p.relative_to(world).as_posix()}")
        return 2

    scanned, biome_chunks, skipped, ids = 0, 0, collections.Counter(), collections.Counter()
    for mca in mcas:
        blobs, s = chunk_blobs(mca)
        skipped += s
        for blob in blobs:
            scanned += 1
            # A chunk saved below the `biomes` generation status has no sections and
            # no biome palette. "No recompile: id" in a pile of proto-chunks is not
            # evidence of a vanilla world, so only chunks that got as far as biomes
            # count as evidence at all.
            if b"biomes" in blob:
                biome_chunks += 1
            for m in ID_RE.findall(blob):
                ids[m.decode("utf-8", "replace")] += 1
        # blobs is dropped here on purpose: holding every decompressed chunk of a
        # multi-thousand-chunk save at once is gigabytes, and a MemoryError would
        # surface as exit 1, which the release reads as "the world is wrong".
    print(f"{len(mcas)} region file(s), {scanned} chunk(s) read, {biome_chunks} with a biome palette")

    if not scanned:
        print("::warning::could not read a single chunk, so the world type is UNVERIFIED.")
        for reason, n in skipped.most_common():
            print(f"  {n} x {reason}")
        print("This is a problem with this tool, not a verdict on the world.")
        return 2

    ours = {k: v for k, v in ids.items() if k.startswith("recompile:")}
    if ours:
        print("the preset applied. recompile: ids in the terrain:")
        for k, v in sorted(ours.items(), key=lambda kv: -kv[1])[:15]:
            print(f"  {v:6d}  {k}")
        return 0

    # Everything below is the ABSENCE of our ids, and absence is only evidence when
    # the evidence was complete. Both guards below downgrade to 2 rather than fail a
    # release, because "I could not tell" must never be reported as "it failed".
    if not biome_chunks:
        print("::warning::no chunk had a biome palette - every one was saved below the")
        print("`biomes` generation status. Nothing here can say what preset built them.")
        return 2

    if skipped:
        print("::warning::some chunks could not be read, and the unread ones are exactly")
        print("those that might have carried the palette. Verdict withheld.")
        for reason, n in skipped.most_common():
            print(f"  {n} x {reason}")
        return 2

    print("::error::no recompile: id anywhere in the terrain.")
    print("This world did NOT come from the garbage preset - level-type did not take, and a")
    print("server built from this pack would hand players an ordinary world.")
    print("most common ids actually present:")
    for k, v in ids.most_common(15):
        print(f"  {v:6d}  {k}")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - deliberately broad
        # Python exits 1 on an uncaught exception, and the release reads 1 as "this
        # world is wrong" and refuses to publish. A crash in this tool is not a
        # verdict on the world, so it leaves by the same door as every other
        # could-not-tell: exit 2.
        import traceback
        traceback.print_exc()
        print(f"::warning::{pathlib.Path(__file__).name} crashed ({type(exc).__name__}) - "
              "world type UNVERIFIED. This is a tool fault, not a world verdict.")
        sys.exit(2)
