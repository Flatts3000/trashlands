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
  2. In the CurseForge app, Instance settings -> Java, add:  -Ddevbridge.port=25580
     Without that property the mod opens no socket at all.
  3. Launch the instance and load a world.

How an id is tested
-------------------
By handing it to the command parser and reading what comes back. `give` takes an
item argument, and an unknown id is a *parse* error, reported before the command
looks for anything to give to:

    give @a[tag=...] recompile:e_scrap   ->  "No player was found"      id is live
    give @a[tag=...] recompile:nonsense  ->  "Unknown item '...'"       id is dead

**The selector matches nobody on purpose.** In singleplayer there is a real player
connected, so a bare `@a` would actually hand them every item in the quest book.
A tag nothing carries keeps the check side-effect free, which is what makes it
safe to run against a world you care about rather than a scratch one.

Component filters go through the same path. The Salvager's Manual task matches
`modonomicon:modonomicon` carrying a `modonomicon:book_id` component, and a wrong
component key is uncompletable in exactly the way a wrong item id is.

Usage
-----
    python tools/verify_quests.py
    python tools/verify_quests.py --port 25580

Exit codes: 0 = every id resolved, 1 = at least one did not, 2 = could not connect.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_quests as vq  # noqa: E402  (JSON5 parser + chapter loading)

try:
    from gamebridge.devbridge import DevBridge, DevBridgeError
except ImportError:  # noqa: BLE001
    sys.exit("gamebridge is not installed. Run:\n"
             "  pip install -e F:/minecraft-repos/mc-pack-toolkit/gamebridge")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_PORT = 25580

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

# The parser's way of saying an id is not registered. Matched case-insensitively
# against the whole reply, so wording drift across versions is less likely to turn
# a real failure into a silent pass.
UNKNOWN_MARKERS = ("unknown item", "unknown registry", "can't find element",
                   "unknown data component", "did you mean")


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
        probe = str(bridge.command(f"give {NOBODY} {SENTINEL}")).lower()
        if any(m in probe for m in UNKNOWN_MARKERS):
            print(f"connected on port {args.port}, but {SENTINEL} is not registered "
                  f"there.\n\nThat game is not this pack. The likeliest cause is the "
                  f"Recompile mod repo's\ngradle dev client, which runs devbridge on "
                  f"the same port. Close it, or point\nthis at the pack instance with "
                  f"--port.\n\nRefusing to report a pass from the wrong game.")
            return 2

        print(f"checking {len(items)} item reference(s)\n")
        for arg, where in items:
            reply = bridge.command(f"give {NOBODY} {arg}")
            low = str(reply).lower()
            ok = not any(m in low for m in UNKNOWN_MARKERS)
            print(f"  {'ok  ' if ok else 'FAIL'}  {arg}")
            if not ok:
                bad.append((arg, where, str(reply).strip()))

    if bad:
        print(f"\n{len(bad)} unresolved reference(s):")
        for arg, where, reply in bad:
            print(f"  {arg}\n    used by: {where}\n    game:    {reply}")
        return 1

    print(f"\nall {len(items)} item reference(s) resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
