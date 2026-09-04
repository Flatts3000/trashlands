#!/usr/bin/env python3
"""Tests for `validate_quests.py`, the quest book's CI gate.

Why this file exists
--------------------
Every failure this validator catches is silent in-game. FTB Quests does not
report a bad book; it loads a smaller one, or an empty one, and the only
evidence is a stack trace in a log nobody reads. Two of the checks below exist
because the failure already shipped:

  * **A missing `data.json5` loads the book completely empty.** v0.2.0 and
    v0.3.0 both shipped a Welcome chapter no player could ever see. The pack
    built, the export validated, and nothing anywhere said a word.
  * **An id whose first hex digit is 8-F parses as a negative long**, and FTB
    silently regenerates it on load, dropping every dependency that pointed at
    it. The book keeps working and quietly loses its ordering.

The validator's own `set_root()` exists so these can be run against a throwaway
tree - its docstring says "a validator nobody has seen fail is not evidence",
which is exactly right and is what this file supplies.

Run:
    python tools/test_validate_quests.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import shutil
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent

# A leading 0-7 keeps the id positive as a signed long. These are valid.
CH_ID = "0A55E0BA6E000001"
Q1 = "0A55E0BA6E000002"
Q2 = "0A55E0BA6E000003"
TASK = "0A55E0BA6E000004"


def load_tool():
    spec = importlib.util.spec_from_file_location(
        "validate_quests", HERE / "validate_quests.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def chapter(quests: str, chapter_id: str = CH_ID) -> str:
    return "{\n" + f'  id: "{chapter_id}"\n' + "  quests: [\n" + quests + "  ]\n}\n"


def quest(qid: str, deps: str = "", task_id: str = TASK) -> str:
    dep_line = f'      dependencies: [{deps}]\n' if deps else ""
    return (
        "    {\n"
        f'      id: "{qid}"\n'
        + dep_line +
        "      tasks: [{ "
        f'id: "{task_id}", type: "item", item: "minecraft:stone"'
        " }]\n"
        "    }\n"
    )


def build_tree(root: pathlib.Path, *, chapters: str | None = None,
               data_file: bool = True, groups_file: bool = True,
               lang: str | None = None) -> None:
    """Lay out the minimum FTB Quests tree the validator walks."""
    quests = root / "pack" / "config" / "ftbquests" / "quests"
    (quests / "chapters").mkdir(parents=True, exist_ok=True)
    (quests / "lang" / "en_us").mkdir(parents=True, exist_ok=True)
    if chapters is not None:
        (quests / "chapters" / "welcome.json5").write_text(chapters, encoding="utf-8")
    if data_file:
        (quests / "data.json5").write_text("{ title: \"Trashlands\" }\n", encoding="utf-8")
    if groups_file:
        (quests / "chapter_groups.json5").write_text("{ chapter_groups: [] }\n",
                                                     encoding="utf-8")
    if lang is not None:
        (quests / "lang" / "en_us" / "chapter.json5").write_text(lang, encoding="utf-8")


def codes_from(t, build) -> set:
    """Run every tree-reading check over a throwaway tree, return the codes."""
    root = pathlib.Path(tempfile.mkdtemp(prefix="quests-test-"))
    saved = t.REPO
    try:
        build(root)
        t.set_root(root)
        out: list = []
        t.check_required_files(out)
        chapters = t.load_chapters()
        t.check_ids(chapters, out)
        t.check_dependencies(chapters, out)
        t.check_dashes(out)
        return {code for _sev, code, _where, _msg in out}
    finally:
        t.set_root(saved)
        shutil.rmtree(root, ignore_errors=True)


def cases(t):
    # Every id in the tree has to be distinct, tasks included - which the first
    # draft of this fixture got wrong, and the validator correctly caught.
    good = chapter(quest(Q1, task_id="0A55E0BA6E000010")
                   + quest(Q2, deps=f'"{Q1}"', task_id="0A55E0BA6E000011"))

    return [
        # The baseline. If this is not clean, nothing below means anything.
        ("a well-formed book reports nothing",
         lambda: codes_from(t, lambda r: build_tree(r, chapters=good)),
         set()),

        # The failure that shipped twice, in v0.2.0 and v0.3.0.
        ("a missing data.json5 is caught",
         lambda: codes_from(t, lambda r: build_tree(r, chapters=good, data_file=False)),
         {"NO-DATA-FILE"}),
        ("a missing chapter_groups.json5 is caught",
         lambda: codes_from(t, lambda r: build_tree(r, chapters=good, groups_file=False)),
         {"NO-GROUPS-FILE"}),
        ("both missing at once are both reported",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=good, data_file=False, groups_file=False)),
         {"NO-DATA-FILE", "NO-GROUPS-FILE"}),

        # An id leading 8-F parses negative; FTB regenerates it and every
        # dependency pointing at it is dropped, with no error anywhere.
        ("an id leading 8-F is caught as negative",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest("FA55E0BA6E000002")))),
         {"Q-ID-POSITIVE"}),
        ("a chapter id leading 8-F is caught too",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest(Q1), chapter_id="8A55E0BA6E000001"))),
         {"Q-ID-POSITIVE"}),
        ("the boundary digit 7 is accepted",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest("7A55E0BA6E000002")))),
         set()),
        ("the boundary digit 8 is rejected",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest("8A55E0BA6E000002")))),
         {"Q-ID-POSITIVE"}),

        ("a malformed id is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest("not-an-id")))),
         {"Q-ID-FORMAT"}),
        ("a lowercase id is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest("0a55e0ba6e000002")))),
         {"Q-ID-FORMAT"}),
        ("a too-short id is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest("0A55E0BA")))),
         {"Q-ID-FORMAT"}),

        # Two quests sharing an id: FTB keeps one and the other vanishes.
        ("a duplicate id is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest(Q1) + quest(Q1, task_id="0A55E0BA6E000005")))),
         {"Q-ID-UNIQUE"}),
        ("a quest reusing its chapter's id is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest(CH_ID)))),
         {"Q-ID-UNIQUE"}),

        # A dependency on a quest that does not exist orphans the quest: it
        # never unlocks, and the book gives no reason.
        ("a dangling dependency is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=chapter(quest(Q1, deps='"0A55E0BA6EDEAD01"')))),
         {"DEP-DANGLING"}),
        ("a dependency on a real quest is fine",
         lambda: codes_from(t, lambda r: build_tree(r, chapters=good)),
         set()),

        # The house rule, enforced in CI: ASCII punctuation only.
        ("an em-dash in a chapter is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=good.replace('id: "', 'title: "a — b"\n  id: "', 1))),
         {"DASH"}),
        ("an en-dash in a lang file is caught",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=good, lang='{ "x": "a – b" }\n')),
         {"DASH"}),
        ("a plain hyphen is not a dash violation",
         lambda: codes_from(t, lambda r: build_tree(
             r, chapters=good, lang='{ "x": "a - b" }\n')),
         set()),

        # No chapters at all is not a crash - the required-files check is what
        # speaks, and load_chapters returns an empty list rather than raising.
        ("an empty chapters dir does not crash the validator",
         lambda: codes_from(t, lambda r: build_tree(r, chapters=None)),
         set()),
    ]


def main() -> int:
    t = load_tool()
    failures = 0
    all_cases = cases(t)
    for name, thunk, want in all_cases:
        try:
            got = thunk()
        except Exception as exc:
            got = f"{type(exc).__name__}: {exc}"
        ok = got == want
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"          got {got!r}, want {want!r}")
    print(f"\n{len(all_cases)} case(s), {failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
