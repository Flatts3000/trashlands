#!/usr/bin/env python3
"""Tests for `check_pack_deps.py`, the release's dependency and loader-pin guard.

Why this file exists
--------------------
This tool is the only thing standing between the pack and the worst failure it
has: a mod that declares a loader floor above the pack's pin. NeoForge does not
warn about that. It declines to load the mod, so the pack boots looking correct
with a mod silently absent, and the first person to notice is a player. v0.1.0
shipped pinned at 26.1.2.76 while JEI needed [26.1.2.81,) and Balm needed
[26.1.2.93,). Sky Frogs hit the same class of bug twice via Apotheosis.

Nothing exercised it. The tool runs on every PR and again at release, and its
whole value is a comparison between two version tuples - which is exactly the
kind of code that looks obviously right and is quietly wrong at one boundary.

Two of the cases below were failing bugs when this file was written, both found
by writing the case rather than by reading the code:

  * `(26.1.2.100,)` is an EXCLUSIVE lower bound - the mod needs strictly more
    than .100 - and the guard read it as inclusive and let a pin of exactly .100
    through. That is the precise failure this tool exists to prevent, arrived at
    from the other direction.
  * `in_range` returned False for a bare version range like `1.2.3`, which its
    own docstring says must return True. A dependency that is fine got reported
    as "present but too old", which fails a good release.

The network-dependent half (resolve_jars, read_jars, audit) is deliberately not
covered here: it downloads every pinned jar through packwiz. That is exercised
for real on every PR by validate-pack.yml, which is a better test than a mock.

Run:
    python tools/test_check_pack_deps.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import shutil
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent


def load_tool():
    spec = importlib.util.spec_from_file_location(
        "check_pack_deps", HERE / "check_pack_deps.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# Pure version logic. Each case is (name, callable -> actual, expected).
# --------------------------------------------------------------------------

def version_cases(t):
    """`t` is the loaded module. Returns [(name, thunk, expected)]."""
    return [
        # version_tuple - digits only, and numeric rather than lexical.
        ("version_tuple splits on dots",
         lambda: t.version_tuple("26.1.2.100"), (26, 1, 2, 100)),
        ("version_tuple ignores a suffix",
         lambda: t.version_tuple("1.0.0-beta.2"), (1, 0, 0, 2)),
        ("version_tuple of nothing is empty",
         lambda: t.version_tuple(""), ()),

        # lower_bound - returns (bound, inclusive) so the caller can tell
        # `[x,)` from `(x,)`. Getting this wrong ships a mod that cannot load.
        ("lower_bound reads an inclusive floor",
         lambda: t.lower_bound("[26.1.2.93,)"), ((26, 1, 2, 93), True)),
        ("lower_bound reads an EXCLUSIVE floor as exclusive",
         lambda: t.lower_bound("(26.1.2.100,)"), ((26, 1, 2, 100), False)),
        ("lower_bound reads a bare version as an inclusive floor",
         lambda: t.lower_bound("26.1.2.100"), ((26, 1, 2, 100), True)),
        ("lower_bound of an unparseable range is None",
         lambda: t.lower_bound("banana"), None),
        ("lower_bound of an empty range is None",
         lambda: t.lower_bound(""), None),

        # below_floor is the DECISION the shape above exists to make, and the
        # first draft of this file never called it - so reverting the exclusive
        # bound fix left every case green. The shape is not the behaviour.
        ("below_floor: a pin under an inclusive floor is blocked",
         lambda: t.below_floor((26, 1, 2, 98), "[26.1.2.99,)"), True),
        ("below_floor: a pin exactly on an inclusive floor is fine",
         lambda: t.below_floor((26, 1, 2, 99), "[26.1.2.99,)"), False),
        ("below_floor: a pin exactly on an EXCLUSIVE floor is BLOCKED",
         lambda: t.below_floor((26, 1, 2, 100), "(26.1.2.100,)"), True),
        ("below_floor: a pin above an exclusive floor is fine",
         lambda: t.below_floor((26, 1, 2, 101), "(26.1.2.100,)"), False),
        ("below_floor: a bare-version floor above the pin is blocked",
         lambda: t.below_floor((26, 1, 2, 100), "26.1.2.200"), True),
        ("below_floor: a bare-version floor below the pin is fine",
         lambda: t.below_floor((26, 1, 2, 100), "26.1.2.50"), False),
        ("below_floor: an unreadable range never blocks a release",
         lambda: t.below_floor((26, 1, 2, 100), "banana"), False),
        ("below_floor: an empty range never blocks a release",
         lambda: t.below_floor((26, 1, 2, 100), ""), False),
        ("below_floor is numeric, not lexical",
         lambda: t.below_floor((26, 1, 2, 9), "[26.1.2.10,)"), True),

        # in_range - the satisfied-dependency check.
        ("a version above the floor is in range",
         lambda: t.in_range("26.1.2.100", "[26.1.2.99,)"), True),
        ("a version below the floor is not",
         lambda: t.in_range("26.1.2.98", "[26.1.2.99,)"), False),
        ("exactly the inclusive floor is in range",
         lambda: t.in_range("26.1.2.99", "[26.1.2.99,)"), True),
        ("exactly an EXCLUSIVE floor is NOT in range",
         lambda: t.in_range("26.1.2.99", "(26.1.2.99,)"), False),
        # The bug a string compare would introduce: "9" > "10" lexically.
        ("comparison is numeric, not lexical",
         lambda: t.in_range("26.1.2.9", "[26.1.2.10,)"), False),
        ("an exclusive upper bound excludes its own value",
         lambda: t.in_range("2.0", "[1.0,2.0)"), False),
        ("an inclusive upper bound includes its own value",
         lambda: t.in_range("2.0", "[1.0,2.0]"), True),
        ("under an upper bound is in range",
         lambda: t.in_range("1.5", "[1.0,2.0)"), True),
        ("an exact single version matches itself",
         lambda: t.in_range("1.2.3", "[1.2.3]"), True),
        ("an exact single version rejects anything else",
         lambda: t.in_range("1.2.4", "[1.2.3]"), False),
        ("a multi-clause range matches the second clause",
         lambda: t.in_range("3.5", "[1.0,2.0),[3.0,4.0)"), True),
        ("a multi-clause range still rejects the gap between clauses",
         lambda: t.in_range("2.5", "[1.0,2.0),[3.0,4.0)"), False),

        # A bare version is a soft lower bound - ">= 1.2.3" - not junk. This has
        # been wrong in both directions: it fell through to False (a satisfied
        # dependency reported as too old, failing a good release), and then
        # returned True unconditionally (a genuinely outdated one passing
        # silently, which is the direction that actually ships a broken pack).
        ("a bare version range accepts its own version",
         lambda: t.in_range("1.2.3", "1.2.3"), True),
        ("a bare version range accepts a newer version",
         lambda: t.in_range("26.1.2.100", "26.1.2"), True),
        ("a bare version range REJECTS an older version",
         lambda: t.in_range("26.1.2.50", "26.1.2.100"), False),

        # The documented safe direction: anything unreadable must pass, so the
        # tool never fails a release over a range it simply could not parse.
        ("an empty range means any version",
         lambda: t.in_range("1.0", ""), True),
        ("a wildcard range means any version",
         lambda: t.in_range("1.0", "*"), True),
        ("an open range means any version",
         lambda: t.in_range("1.0", "[,)"), True),
        ("unparseable junk means any version",
         lambda: t.in_range("1.0", "banana"), True),
        ("a range of only punctuation means any version",
         lambda: t.in_range("1.0", "..."), True),
        ("an unknown version passes rather than failing the release",
         lambda: t.in_range("", "[9.9.9,)"), True),
    ]


# --------------------------------------------------------------------------
# The guards that read the pack tree. Each builds a throwaway pack/mods dir.
# --------------------------------------------------------------------------

PIN = """name = "Held Mod"
filename = "held-1.0.jar"
side = "client"

[download]
hash-format = "sha1"
hash = "deadbeef"
mode = "metadata:curseforge"

[update]
[update.curseforge]
file-id = {file_id}
project-id = 363363
"""


def write_pin(mods: pathlib.Path, name: str, file_id: int) -> None:
    mods.mkdir(parents=True, exist_ok=True)
    (mods / name).write_text(PIN.format(file_id=file_id), encoding="utf-8")


def quietly(fn):
    """Run `fn`, swallowing what it prints.

    The failure-path cases deliberately trip guards that shout - `=== HELD PIN
    MOVED ===`, `dev-only mod(s) indexed in the pack`. Left on stdout, a
    perfectly green run reads in an Actions log as though the release guard
    fired.
    """
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return fn()


def held_pin_cases(t):
    """check_held_pins: 0 when every held pin still points where it was held.

    Skipped rather than crashed when HELD_PINS is empty. That is not a
    hypothetical state: the only hold is Extreme Sound Muffler waiting on a
    stable 4.x, and the day it is released the entry goes away. An unguarded
    `next(iter(...))` here runs while the case list is being BUILT, so it takes
    the whole suite down with a bare StopIteration and no test report at all.
    """
    if not t.HELD_PINS:
        return [("HELD_PINS is empty, so there is nothing to hold", lambda: 0, 0)]
    held_name, (held_id, _why) = next(iter(t.HELD_PINS.items()))

    def run(build) -> int:
        root = pathlib.Path(tempfile.mkdtemp(prefix="deps-test-"))
        saved = t.PACK
        try:
            build(root / "pack" / "mods")
            t.PACK = root / "pack"
            return quietly(t.check_held_pins)
        finally:
            t.PACK = saved
            shutil.rmtree(root, ignore_errors=True)

    return [
        ("a held pin still on its file passes",
         lambda: run(lambda m: write_pin(m, held_name, held_id)), 0),
        # This is the case that matters: `packwiz update --all` takes the newest
        # file regardless of channel, so it offers the 4.x alpha every single
        # pass and a distracted revert is one keystroke away.
        ("a held pin moved by an update FAILS",
         lambda: run(lambda m: write_pin(m, held_name, held_id + 1)), 1),
        ("a held pin whose file was deleted FAILS",
         lambda: run(lambda m: m.mkdir(parents=True, exist_ok=True)), 1),
    ]


def dev_mod_cases(t):
    """check_no_dev_mods: a dev-only mod must never reach a release.

    This guard reads `pack/index.toml`, not the pin files - the index is what
    the CurseForge export and packwiz-installer actually walk, so it is the
    right thing to look at.

    Skipped rather than crashed when DEV_ONLY_MODS is empty, for the same reason
    as the held pins above: this runs while the case list is built, so an
    IndexError here takes the suite down before a single result is printed.
    """
    if not t.DEV_ONLY_MODS:
        return [("DEV_ONLY_MODS is empty, so there is nothing to exclude",
                 lambda: 0, 0)]

    def run(index_body) -> int:
        root = pathlib.Path(tempfile.mkdtemp(prefix="deps-test-"))
        saved = t.PACK
        try:
            pack = root / "pack"
            pack.mkdir(parents=True, exist_ok=True)
            if index_body is not None:
                (pack / "index.toml").write_text(index_body, encoding="utf-8")
            t.PACK = pack
            return quietly(t.check_no_dev_mods)
        finally:
            t.PACK = saved
            shutil.rmtree(root, ignore_errors=True)

    dev = t.DEV_ONLY_MODS[0]

    def index_for(mod_file: str) -> str:
        return f'[[files]]\nfile = "mods/{mod_file}"\nhash = "abc"\n'

    return [
        ("an ordinary lineup passes",
         lambda: run(index_for("jei.pw.toml")), 0),
        (f"an indexed {dev} FAILS the release",
         lambda: run(index_for(f"{dev}.pw.toml")), 1),
        (f"{dev} is matched case-insensitively",
         lambda: run(index_for(f"{dev.upper()}.pw.toml")), 1),
        # Documented behaviour, asserted so it stays deliberate: with no index
        # there is nothing to walk, so this guard abstains. The release's own
        # index guard is what catches a missing or stale index.
        ("no index.toml means this guard abstains rather than failing",
         lambda: run(None), 0),
    ]


def main() -> int:
    t = load_tool()
    cases = version_cases(t) + held_pin_cases(t) + dev_mod_cases(t)
    failures = 0
    for name, thunk, want in cases:
        try:
            got = thunk()
        except Exception as exc:                      # a raise is a failure
            got = f"{type(exc).__name__}: {exc}"
        ok = got == want
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"          got {got!r}, want {want!r}")
    print(f"\n{len(cases)} case(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
