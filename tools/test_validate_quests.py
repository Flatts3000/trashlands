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


def quest_with_inline_title(qid: str, task_id: str) -> str:
    """A quest carrying its title in the chapter file instead of the lang file.

    FTB does not render text authored here, and wipes it on the next save.
    """
    return (
        "    {\n"
        f'      id: "{qid}"\n'
        '      title: "written inline"\n'
        f'      tasks: [{{ id: "{task_id}", type: "item", item: "minecraft:stone" }}]\n'
        "    }\n"
    )


# Written as escapes on purpose. These are the two characters the house rule
# bans, and these are the fixtures that prove the linter fires on them. Spelled
# literally they invite a well-meaning cleanup pass to delete the evidence, and
# the tests would still pass while asserting nothing.
EM_DASH = "—"
EN_DASH = "–"
EM_DASH_COMMENT = f"// a {EM_DASH} b\n"
EN_DASH_LANG = '{ "x": "a ' + EN_DASH + ' b" }'


def titles_for(*quest_ids: str) -> str:
    """A lang file giving every quest a title.

    Not decoration: `check_lang` warns LANG-NO-TITLE for any quest without one,
    so a fixture that omits titles makes every single case noisy and hides what
    it is actually asserting.
    """
    body = ",\n".join(f'  "quest.{qid}.title": "T"' for qid in quest_ids)
    return "{\n" + body + "\n}\n"


def build_tree(root: pathlib.Path, *, chapters: str | None = None,
               data_file: bool = True, groups_file: bool = True,
               lang: str | None = None, titles: tuple[str, ...] = ()) -> None:
    """Lay out the minimum FTB Quests tree the validator walks."""
    quests = root / "pack" / "config" / "ftbquests" / "quests"
    (quests / "chapters").mkdir(parents=True, exist_ok=True)
    (quests / "lang" / "en_us").mkdir(parents=True, exist_ok=True)
    if chapters is not None:
        (quests / "chapters" / "welcome.json5").write_text(chapters, encoding="utf-8")
    if titles:
        (quests / "lang" / "en_us" / "chapters").mkdir(parents=True, exist_ok=True)
        (quests / "lang" / "en_us" / "chapters" / "welcome.json5").write_text(
            titles_for(*titles), encoding="utf-8")
    if data_file:
        (quests / "data.json5").write_text("{ title: \"Trashlands\" }\n", encoding="utf-8")
    if groups_file:
        (quests / "chapter_groups.json5").write_text("{ chapter_groups: [] }\n",
                                                     encoding="utf-8")
    if lang is not None:
        (quests / "lang" / "en_us" / "chapter.json5").write_text(lang, encoding="utf-8")


def codes_from(t, build) -> set:
    """Run every check over a throwaway tree; return `{(severity, code)}`.

    Severity is part of the result on purpose. Returning bare codes let a check
    be downgraded from ERROR to WARN with every case still green - and
    `validate_quests.main()` exits 0 on warnings, so CI would go green on a book
    with no `data.json5`, which is exactly the failure v0.2.0 and v0.3.0 shipped.
    A test that cannot see the difference between "reported" and "blocking" is
    not testing the thing that matters.
    """
    root = pathlib.Path(tempfile.mkdtemp(prefix="quests-test-"))
    saved = t.REPO
    try:
        build(root)
        t.set_root(root)
        out: list = []
        t.check_required_files(out)
        chapters = t.load_chapters()
        lang = t.load_lang()
        t.check_ids(chapters, out)
        t.check_dependencies(chapters, out)
        t.check_inline_text(chapters, out)
        t.check_lang(chapters, lang, out)
        t.check_images(chapters, out)
        t.check_dashes(out)
        return {(sev, code) for sev, code, _where, _msg in out}
    finally:
        t.set_root(saved)
        shutil.rmtree(root, ignore_errors=True)


def E(*codes):
    """Expected set of ERROR-severity codes."""
    return {("ERROR", c) for c in codes}


def cases(t):
    """Each case: (name, thunk -> {(severity, code)}, expected).

    `titles` is supplied everywhere because check_lang warns on any quest
    without one; leaving it out made every case carry a LANG-NO-TITLE it was
    not about.
    """
    T1, T2 = "0A55E0BA6E000010", "0A55E0BA6E000011"
    good = chapter(quest(Q1, task_id=T1) + quest(Q2, deps=f'"{Q1}"', task_id=T2))

    def run(**kw):
        kw.setdefault("chapters", good)
        kw.setdefault("titles", (Q1, Q2))
        return lambda: codes_from(t, lambda r: build_tree(r, **kw))

    def one(qid, **kw):
        """A single-quest chapter, titled, so only the id under test speaks."""
        kw.setdefault("chapters", chapter(quest(qid)))
        kw.setdefault("titles", (qid,))
        return lambda: codes_from(t, lambda r: build_tree(r, **kw))

    return [
        # The baseline. If this is not clean, nothing below means anything.
        ("a well-formed book reports nothing", run(), set()),

        # The failure that shipped twice, in v0.2.0 and v0.3.0. An empty book
        # with no in-game error and no log anyone reads.
        ("a missing data.json5 is a blocking ERROR",
         run(data_file=False), E("NO-DATA-FILE")),
        ("a missing chapter_groups.json5 is a blocking ERROR",
         run(groups_file=False), E("NO-GROUPS-FILE")),
        ("both missing at once are both reported",
         run(data_file=False, groups_file=False),
         E("NO-DATA-FILE", "NO-GROUPS-FILE")),

        # An id leading 8-F parses as a negative long; FTB regenerates it on
        # load and every dependency pointing at it is dropped, silently.
        ("an id leading 8-F is caught as negative",
         one("FA55E0BA6E000002"), E("Q-ID-POSITIVE")),
        ("the boundary digit 7 is accepted",
         one("7A55E0BA6E000002"), set()),
        ("the boundary digit 8 is rejected",
         one("8A55E0BA6E000002"), E("Q-ID-POSITIVE")),
        ("a chapter id leading 8-F is caught too",
         run(chapters=chapter(quest(Q1), chapter_id="8A55E0BA6E000001"),
             titles=(Q1,)),
         E("Q-ID-POSITIVE")),

        # A non-hex id breaks its own lang key too, which is worth asserting
        # rather than hiding: the key cannot match `<kind>.<hex id>.<field>`, so
        # it is flagged for shape AND the quest reads as untitled. The two
        # cases below stay clean because their ids are still hex.
        ("a malformed id is caught, and takes its lang key with it",
         one("not-an-id"),
         E("Q-ID-FORMAT") | {("WARN", "LANG-KEY-SHAPE"), ("WARN", "LANG-NO-TITLE")}),
        ("a lowercase id is caught", one("0a55e0ba6e000002"), E("Q-ID-FORMAT")),
        ("a too-short id is caught", one("0A55E0BA"), E("Q-ID-FORMAT")),

        # Two quests sharing an id: FTB keeps one and the other vanishes.
        ("a duplicate quest id is caught",
         run(chapters=chapter(quest(Q1, task_id=T1)
                              + quest(Q1, task_id=T2)), titles=(Q1,)),
         E("Q-ID-UNIQUE")),
        ("a duplicate TASK id is caught",
         run(chapters=chapter(quest(Q1, task_id=T1) + quest(Q2, task_id=T1))),
         E("Q-ID-UNIQUE")),
        ("a quest reusing its chapter's id is caught",
         one(CH_ID), E("Q-ID-UNIQUE")),

        # A dependency on a quest that does not exist orphans the quest: it
        # never unlocks, and the book gives no reason.
        ("a dangling dependency is caught",
         run(chapters=chapter(quest(Q1, deps='"0A55E0BA6EDEAD01"')),
             titles=(Q1,)),
         E("DEP-DANGLING")),
        ("a dependency on a real quest is fine", run(), set()),

        # A lang key for an id nothing defines never renders at all.
        ("a lang key for an unknown id is caught",
         run(lang='{ "quest.0A55E0BA6EDEAD01.title": "ghost" }'),
         E("LANG-ORPHAN")),
        ("a quest with no title warns rather than blocks",
         run(titles=(Q1,)), {("WARN", "LANG-NO-TITLE")}),

        # Text authored inline in a chapter instead of the lang file does not
        # render, and FTB wipes it on the next save.
        ("inline quest text is caught",
         run(chapters=chapter(quest_with_inline_title(Q1, T1)), titles=(Q1,)),
         E("LANG-INLINE")),

        # The house rule, enforced in CI: ASCII punctuation only. The dash goes
        # in a comment so this case tests check_dashes and nothing else - an
        # earlier draft put it in a chapter-level `title:`, which check_inline_text
        # would also have flagged once it was wired in.
        ("an em-dash in a chapter file is caught",
         run(chapters=EM_DASH_COMMENT + good), E("DASH")),
        ("an en-dash in a lang file is caught",
         run(lang=EN_DASH_LANG),
         E("DASH") | {("WARN", "LANG-KEY-SHAPE")}),
        ("a plain hyphen is not a dash violation",
         run(lang='{ "x": "a - b" }'), {("WARN", "LANG-KEY-SHAPE")}),

        # No chapters at all is not a crash - load_chapters returns [].
        ("an empty chapters dir does not crash the validator",
         run(chapters=None, titles=()), set()),
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
