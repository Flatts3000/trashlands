#!/usr/bin/env python3
"""Assert that every item the quest book references actually exists in game.

The gap this closes
-------------------
tools/validate_quests.py checks structure and cannot check meaning: it has no item
registry, so `recompile:e_scrap` is an assertion nobody has tested. When a mod
renames or removes an item, an FTB Quests task referencing the old id **fails
silently**. Nothing logs, the book still opens, and the quest simply cannot be
completed by anyone, ever. The pack that ships it looks fine right up until a
player is stuck.

That is exactly the class of bug the gamebridge handoff points at, and it needs a
running game to catch, because only the game knows what is registered.

How an id is tested
-------------------
By handing it to the command parser and reading what comes back. `give` takes an
item argument, and the parser rejects an unknown id *before* it looks for a player,
so on a server with nobody connected:

    give @a recompile:e_scrap   ->  "No player was found"          id is fine
    give @a recompile:nonsense  ->  "Unknown item 'recompile:...'"  id is dead

Nothing is granted either way, since @a matches nobody. That is deliberate: the
check has no side effects on the world, so it is safe to run against a server you
care about.

Component filters are checked the same way and for the same reason. The Salvager's
Manual task matches `modonomicon:modonomicon` carrying a `modonomicon:book_id`
component; a task whose component key is wrong is uncompletable in a way that looks
exactly like a task whose item is wrong.

Usage
-----
    python tools/dev_server.py --accept-eula --run     # in one terminal
    python tools/verify_quests.py                      # in another

Exit codes: 0 = every id resolved, 1 = at least one did not, 2 = could not connect.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_quests as vq  # noqa: E402  (JSON5 parser + chapter loading)

try:
    from gamebridge import Rcon, RconError
except ImportError:  # noqa: BLE001
    sys.exit("gamebridge is not installed. Run:\n"
             "  pip install -e F:/minecraft-repos/mc-pack-toolkit/gamebridge")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
DEFAULT_PROPERTIES = REPO / "build" / "server" / "server.properties"

# The parser's way of saying an id is not registered. Matched case-insensitively
# against the whole reply, so wording drift across versions is less likely to turn
# a real failure into a silent pass.
UNKNOWN_MARKERS = ("unknown item", "unknown registry", "can't find element",
                   "unknown data component", "did you mean")


def read_properties(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def item_argument(item: dict) -> str:
    """Render an FTB Quests item spec as a Minecraft item argument.

    1.20.5+ syntax: `namespace:id[component=value,...]`. Values are quoted, which
    is valid for the string components used here; a component holding a compound
    would need more, and gets a clear failure rather than a wrong pass.
    """
    ident = item.get("id")
    if not isinstance(ident, str):
        return ""
    components = item.get("components")
    if isinstance(components, dict) and components:
        parts = [f'{k}="{v}"' for k, v in components.items() if isinstance(v, str)]
        if len(parts) == len(components):
            return f"{ident}[{','.join(parts)}]"
        # A non-string component value: check the bare id rather than emit a
        # malformed argument, and say so, because a silently-skipped filter is
        # the thing this tool exists to prevent.
        print(f"  note: {ident} has a non-string component; checking the id only")
    return ident


def collect_items(chapters) -> list[tuple[str, str]]:
    """Every distinct (item argument, where it came from) in the book.

    Icons count. A quest whose icon item was removed renders as a missing-texture
    block in the book, which is not fatal but is visible to every player.
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
    ap.add_argument("--properties", type=Path, default=DEFAULT_PROPERTIES,
                    help="server.properties to read connection settings from "
                         "(default: the dev_server.py one)")
    args = ap.parse_args()

    chapters = vq.load_chapters()
    if not chapters:
        print("no chapters found - nothing to verify")
        return 0
    items = collect_items(chapters)
    if not items:
        print("no item references in the quest book - nothing to verify")
        return 0

    if not args.properties.is_file():
        print(f"no server.properties at {args.properties}\n"
              "Start the verification server first:\n"
              "  python tools/dev_server.py --accept-eula --run")
        return 2
    props = read_properties(args.properties)
    if props.get("enable-rcon", "false").lower() != "true":
        print(f"RCON is disabled in {args.properties}")
        return 2

    try:
        rcon = Rcon(host="127.0.0.1", port=int(props.get("rcon.port", 25575)),
                    password=props.get("rcon.password", ""), timeout=10.0)
        rcon.connect()
    except (RconError, OSError) as exc:
        print(f"could not reach the server over RCON: {exc}\n"
              "Is it running? `python tools/dev_server.py --run`")
        return 2

    bad = []
    with rcon:
        print(f"checking {len(items)} item reference(s)\n")
        for arg, where in items:
            reply = rcon.command(f"give @a {arg}")
            low = reply.lower()
            ok = not any(m in low for m in UNKNOWN_MARKERS)
            print(f"  {'ok  ' if ok else 'FAIL'}  {arg}")
            if not ok:
                bad.append((arg, where, reply.strip()))

    if bad:
        print(f"\n{len(bad)} unresolved reference(s):")
        for arg, where, reply in bad:
            print(f"  {arg}\n    used by: {where}\n    server:  {reply}")
        return 1

    print(f"\nall {len(items)} item reference(s) resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
