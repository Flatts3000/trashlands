#!/usr/bin/env python3
"""Assert that every item the quest book references actually exists in game.

The gap this closes
-------------------
tools/validate_quests.py checks structure and cannot check meaning: it has no item
registry, so `recompile:e_scrap` is an assertion nobody has tested. When a mod
renames or removes an item, an FTB Quests task referencing the old id **fails
silently**. Nothing logs, the book still opens, and the quest simply cannot be
completed by anyone, ever. Only the game knows what is registered.

Why devbridge and not RCON
--------------------------
This runs against the singleplayer test instance. A singleplayer world has no RCON
and cannot get one: its integrated server listens on nothing, so there is no remote
command interface to connect to. Reaching one needs mod code inside the game, which
is what devbridge is.

Setup, once:

  1. Copy F:/devbridge/build/libs/devbridge-*.jar into the INSTANCE's mods folder.
     Never into pack/mods - that directory is shipped to players, and this mod
     opens a socket that executes arbitrary commands. check_pack_deps.py fails the
     build if it ever appears in the pack index.
  2. In the CurseForge app, Instance settings -> Java, add:  -Ddevbridge.port=8604
     Without that property the mod opens no socket at all.
  3. Launch the instance and load a world.

How an id is tested
-------------------
By handing it to the command parser and asking devbridge whether it ran. An
unknown id is a *parse* error, so the command never executes; a live id parses,
runs, and reports that the selector matched nobody:

    give @a[tag=...] recompile:e_scrap   ->  executed=True   id is live
    give @a[tag=...] recompile:nonsense  ->  executed=False  id is dead

No output is read. Wording can change between versions; whether a command ran
cannot.

**The selector matches nobody on purpose.** In singleplayer there is a real player
connected, so a bare `@a` would actually hand them every item in the quest book.
A tag nothing carries keeps the check side-effect free, which is what makes it
safe to run against a world you care about rather than a scratch one.

What this does and does not cover
---------------------------------
Measured against a running game, not assumed:

    bad item id        recompile:not_a_real_item                    CAUGHT
    bad component key  modonomicon:modonomicon[nosuch:x="y"]        CAUGHT
    bad component VALUE modonomicon:modonomicon[book_id="nope:no"]  NOT CAUGHT

A wrong component *value* parses fine, because the value is just a string and the
parser has no idea which strings name a real book. So the Salvager's Manual task
is verified as far as "that item and that component exist" and no further - if
`recompile:guide` were renamed, this tool would still say ok and the quest would
be uncompletable.

An earlier version of this file claimed component filters were covered "in
exactly the way a wrong item id is". They are not, and a check that overstates
its reach is worse than one that admits a gap.

Usage
-----
    python tools/verify_quests.py
    python tools/verify_quests.py --port 8604

Exit codes: 0 = every id resolved, 1 = at least one did not, 2 = could not connect.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_quests as vq  # noqa: E402  (JSON5 parser + chapter loading)

GAMEBRIDGE_INSTALL = ('  pip install "gamebridge @ '
                      'git+https://github.com/Flatts3000/devbridge.git#subdirectory=gamebridge"')

try:
    from gamebridge.devbridge import DevBridge, DevBridgeError
except ImportError:  # noqa: BLE001
    sys.exit("gamebridge is not installed. Run:\n" + GAMEBRIDGE_INSTALL)

# `run` arrived with devbridge 0.5.0. `command` alone returns only the output text,
# which cannot distinguish a command that failed to parse from one that ran and
# matched nothing - and that distinction is the entire basis of the check below.
# Without this guard the failure is a bare AttributeError from inside the loop,
# which says nothing about the cause.
if not hasattr(DevBridge, "run"):
    sys.exit("this needs gamebridge from devbridge 0.5.0 or later: DevBridge.run is\n"
             "missing, so a dead item id cannot be told from a live one. Reinstall:\n"
             + GAMEBRIDGE_INSTALL.replace("pip install", "pip install --force-reinstall"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Claimed for this project: `ports claim Trashlands --service devbridge --band tool`.
# NOT devbridge's own default of 25580, and that is the point. The port is baked
# into the mod as a default, so every project using it lands on the same number -
# the Recompile repo's gradle dev client holds 25580 on this machine, and the first
# run of this tool connected to that and reported a clean pass about the wrong game.
#
# Worth knowing: `ports check` will not catch a repeat. devbridge binds the JVM's
# loopback address, which is ::1 here, and the ports helper only sees IPv4
# listeners - it reports 25580 as free while a game is listening on it. The
# sentinel check below is the real guard; the claimed port just stops the clash
# happening in the first place.
DEFAULT_PORT = 8604

# A tag no entity carries, so the selector is always empty. The command still
# parses fully, which is the whole point - parsing is what validates the item.
NOBODY = "@a[tag=trashlands_verify_nobody]"

# Proof that the game on the other end is THIS pack. devbridge listens on a fixed
# port, and more than one Minecraft on this machine can have it: the Recompile mod
# repo's gradle dev client runs devbridge on the same 25580. Connecting to that one
# and reporting a clean pass is a real failure mode - it happened on the first run
# of this tool, and every id in the Welcome chapter resolved there, because that
# world has Recompile and Modonomicon loaded too.
#
# FTB Quests is in the pack and not in the mod dev run, so its book item
# distinguishes them. Any pack-only item would do; this one is certain to stay,
# since a pack without FTB Quests has no quest book to verify.
SENTINEL = "ftbquests:book"

# devbridge 0.5.0 reports whether a command ran, so this no longer reads English.
#
# `executed` is the whole test. An unknown item id fails to PARSE, so the command
# never runs and executed is false. A live id parses, runs, finds no player behind
# the selector, and reports failure - executed true, success false. Two different
# things that produced identical-looking prose before.
#
# The string matching this replaces was the weakest part of the tool: a reworded
# vanilla message would have turned a real failure into a silent pass, which is
# the exact fault it existed to catch. devbridge removed the same pattern from its
# own `check` verb in #56.


def item_argument(item: dict) -> str:
    """Render an FTB Quests item spec as a Minecraft item argument.

    1.20.5+ syntax: `namespace:id[component=value,...]`. Values are quoted, which
    is valid for the string components used here; a component holding a compound
    would need more, and gets a visible note rather than a wrong pass.
    """
    ident = item.get("id")
    if not isinstance(ident, str):
        return ""
    components = item.get("components")
    if isinstance(components, dict) and components:
        parts = [f'{k}="{v}"' for k, v in components.items() if isinstance(v, str)]
        if len(parts) == len(components):
            return f"{ident}[{','.join(parts)}]"
        print(f"  note: {ident} has a non-string component; checking the id only")
    return ident


def collect_items(chapters) -> list[tuple[str, str]]:
    """Every distinct (item argument, where it came from) in the book.

    Icons count. A quest whose icon item was removed renders as a missing-texture
    square in the book, which is not fatal but every player sees it.
    """
    found: dict[str, str] = {}

    def add(item, where):
        if isinstance(item, dict):
            arg = item_argument(item)
            if arg:
                found.setdefault(arg, where)

    for ch in chapters:
        add(ch.data.get("icon"), f"{ch.name} chapter icon")
        for q in ch.quests:
            qid = q.get("id", "?")
            add(q.get("icon"), f"{ch.name} quest {qid} icon")
            for t in q.get("tasks", []) or []:
                add(t.get("item"), f"{ch.name} quest {qid} task {t.get('id', '?')}")
            for r in q.get("rewards", []) or []:
                add(r.get("item"), f"{ch.name} quest {qid} reward {r.get('id', '?')}")
    return sorted(found.items())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT,
                    help=f"devbridge port (default {DEFAULT_PORT}; must match "
                         f"-Ddevbridge.port on the instance)")
    # "localhost", not the v4 literal: the mod binds the JVM's loopback address,
    # which is ::1 when the JVM prefers IPv6, and dialling 127.0.0.1 then gets
    # "connection refused" from a socket that is up and healthy.
    ap.add_argument("--host", default="localhost")
    args = ap.parse_args()

    chapters = vq.load_chapters()
    if not chapters:
        print("no chapters found - nothing to verify")
        return 0
    items = collect_items(chapters)
    if not items:
        print("no item references in the quest book - nothing to verify")
        return 0

    bridge = DevBridge(host=args.host, port=args.port, timeout=30.0)
    try:
        bridge.connect()
    except (DevBridgeError, OSError) as exc:
        print(f"could not reach devbridge on {args.host}:{args.port} - {exc}\n\n"
              "Check, in order:\n"
              "  1. the instance is running and a world is loaded\n"
              "  2. devbridge-*.jar is in the INSTANCE's mods folder (not pack/mods)\n"
              "  3. -Ddevbridge.port=%d is set in the CurseForge app's Java args\n"
              "     (without it the mod opens no socket)" % args.port)
        return 2

    bad = []
    with bridge:
        if not bridge.run(f"give {NOBODY} {SENTINEL}").get("executed"):
            print(f"connected on port {args.port}, but {SENTINEL} is not registered "
                  f"there.\n\nThat game is not this pack. The likeliest cause is the "
                  f"Recompile mod repo's\ngradle dev client, which runs devbridge on "
                  f"the same port. Close it, or point\nthis at the pack instance with "
                  f"--port.\n\nRefusing to report a pass from the wrong game.")
            return 2

        print(f"checking {len(items)} item reference(s)\n")
        for arg, where in items:
            reply = bridge.run(f"give {NOBODY} {arg}")
            ok = bool(reply.get("executed"))
            print(f"  {'ok  ' if ok else 'FAIL'}  {arg}")
            if not ok:
                bad.append((arg, where, str(reply.get("output", "")).strip()))

    if bad:
        print(f"\n{len(bad)} unresolved reference(s):")
        for arg, where, reply in bad:
            print(f"  {arg}\n    used by: {where}\n    game:    {reply}")
        return 1

    print(f"\nall {len(items)} item reference(s) resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
