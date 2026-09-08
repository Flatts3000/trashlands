#!/usr/bin/env python3
"""Tests for `import_quests.py`, which writes to shipped player-facing copy.

This is the most dangerous tool in the repo. Everything else here reads, reports
or validates; this one rewrites the quest book from a document that has been
round-tripped through a word processor. `export_quests.py` argues in its own
docstring that the export should stay one-way because the failure mode of an
importer is *silent text loss* in a book that has already shipped empty twice.
That objection was not withdrawn when the importer was written, it was turned
into requirements, and these are the tests for those requirements.

The two that matter most:

  * **An unedited round trip must be a no-op.** Export, import, zero changes. If
    that ever fails, the tool is rewriting bodies nobody touched and the git
    diff of a real review becomes unreadable.
  * **Colour codes must survive.** Four bodies carry `&a`/`&e`/`&r`, the prose
    export strips them, and a naive import would delete them permanently with
    nothing to say so.

`splice` is tested directly because it edits JSON5 by text rather than by
reparsing, to keep the diff local. That is the right call for reviewability and
the wrong call for safety unless the bracket scan is correct, so the scan gets
its own cases including a string containing a bracket.
"""

from __future__ import annotations

import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import import_quests as iq  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SAMPLE = '''{
  "quest.7A55E0BA6E000010.title": "Welcome",
  "quest.7A55E0BA6E000010.quest_desc": [
    "First line.",
    "",
    "Second line."
  ],
  "quest.7A55E0BA6E000011.quest_desc": [
    "Untouched [not an array end] body."
  ],
}
'''


def parse(text: str):
    import tempfile
    fd, p = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    try:
        return iq.parse_prose(pathlib.Path(p))
    finally:
        os.unlink(p)


def cases():
    out = []

    # ---------------------------------------------------------------- parsing
    doc = "# Title\n\npreamble text\n\n## Welcome\n\n### One\n\nAlpha.\n\nBeta.\n\n### Two\n\nGamma.\n"
    got = parse(doc)
    out.append(("chapters and quests are found",
                [(c[0], [q[0] for q in c[1]]) for c in got],
                [("Welcome", ["One", "Two"])]))
    out.append(("blank lines separate paragraphs",
                got[0][1][0][1], ["Alpha.", "Beta."]))
    out.append(("preamble under the H1 is not copy",
                len(got[0][1]), 2))

    wrapped = "## C\n\n### Q\n\nA line that was\nsoft wrapped by the editor.\n"
    out.append(("a soft-wrapped paragraph rejoins into one",
                parse(wrapped)[0][1][0][1],
                ["A line that was soft wrapped by the editor."]))

    out.append(("a document with no chapters parses to nothing",
                parse("# Just a title\n\nsome text\n"), []))

    # ------------------------------------------------- heading-level detection
    # The two export shapes differ only in whether a document title is present,
    # and the first detection rule got the whole-book case backwards: it picked
    # the "# Trashlands quest copy" title as the chapter level, so every real
    # chapter parsed as a quest. --split then could not be read by the importer
    # at all, which is the shape a reviewer is actually handed.
    whole = ["# Doc title", "## Chapter", "### Quest", "### Quest Two"]
    split = ["# Chapter", "## Quest", "## Quest Two"]
    out.append(("three heading depths: the shallowest is a title",
                iq.heading_levels(whole), (2, 3)))
    out.append(("two heading depths: the shallowest is a chapter",
                iq.heading_levels(split), (1, 2)))
    out.append(("no headings at all falls back",
                iq.heading_levels(["just text"]), (2, 3)))
    out.append(("one heading depth falls back rather than guessing",
                iq.heading_levels(["# A", "# B"]), (2, 3)))

    split_doc = "# Welcome\n\n## One\n\nAlpha.\n\n## Two\n\nBeta.\n"
    out.append(("a split-shaped document parses as one chapter",
                [(c[0], [q[0] for q in c[1]]) for c in parse(split_doc)],
                [("Welcome", ["One", "Two"])]))

    whole_doc = ("# Book\n\n## Welcome\n\n### One\n\nAlpha.\n\n"
                 "## Salvage\n\n### Two\n\nBeta.\n")
    out.append(("a whole-book document parses as two chapters",
                [(c[0], [q[0] for q in c[1]]) for c in parse(whole_doc)],
                [("Welcome", ["One"]), ("Salvage", ["Two"])]))

    # ----------------------------------------------------------------- render
    out.append(("paragraphs render with a blank separator",
                iq.render_array(["A.", "B."], "  ", "    "),
                '[\n    "A.",\n    "",\n    "B.",\n  ]'))
    out.append(("a quote is escaped",
                iq.render_array(['He said "no".'], "  ", "    "),
                '[\n    "He said \\"no\\".",\n  ]'))
    out.append(("a backslash is escaped",
                iq.render_array(["a\\b"], "  ", "    "),
                '[\n    "a\\\\b",\n  ]'))

    # ------------------------------------------------------ punctuation guard
    # From the first real review pass: 16 curly apostrophes and one em-dash came
    # back from the editor. The author typed neither.
    out.append(("curly apostrophes fold to ASCII",
                iq.normalise_punctuation("You’ll need it"), "You'll need it"))
    out.append(("curly quotes fold to ASCII",
                iq.normalise_punctuation("“no”"), '"no"'))
    out.append(("an ellipsis folds to three dots",
                iq.normalise_punctuation("wait…"), "wait..."))
    out.append(("a non-breaking space folds to a space",
                iq.normalise_punctuation("a b"), "a b"))
    out.append(("ASCII text is left alone",
                iq.normalise_punctuation("plain 'text' here"), "plain 'text' here"))
    out.append(("an em-dash is NOT auto-fixed, because no fix is safe",
                iq.normalise_punctuation("a—b"), "a—b"))
    out.append(("both banned dashes are known",
                sorted(iq.DASHES), sorted(["—", "–"])))

    # ------------------------------------------------- full-export detection
    # Both exports use the same heading depths, so heading detection cannot tell
    # them apart. Feeding the full one in appended "<sub>46 words</sub>" and a
    # raw id/shape/tasks line into player-facing copy, silently, exit 0. It
    # aborted only by accident, because The Depths has four bodiless quests and
    # the counts happened to disagree.
    out.append(("a <sub> tag marks the full export",
                iq.looks_like_full_export(["## Welcome", "<sub>46 words</sub>"]), True))
    out.append(("an id bullet marks the full export",
                iq.looks_like_full_export(["- id `7A55E0BA6E000010`, shape `hexagon`"]), True))
    out.append(("a tasks bullet marks the full export",
                iq.looks_like_full_export(["- tasks: checkmark"]), True))
    out.append(("prose is not mistaken for the full export",
                iq.looks_like_full_export(
                    ["# Welcome", "## One", "A coarse dirt plain, no trees on it."]), False))
    out.append(("an ordinary dash bullet is not a marker",
                iq.looks_like_full_export(["- a normal markdown list item"]), False))

    # ------------------------------------------------- substitution counting
    # zip(input, output) misaligns the moment a substitution changes length, so
    # one ellipsis reported about twenty normalisations. The number appears in
    # the line announcing a silent mutation of shipped copy.
    out.append(("one ellipsis counts as one substitution",
                iq.count_substitutions("wait… for it"), 1))
    out.append(("three apostrophes count as three",
                iq.count_substitutions("it’s a can’t won’t"), 3))
    out.append(("clean ASCII counts zero",
                iq.count_substitutions("plain text"), 0))

    # ----------------------------------------------------------------- splice
    spliced = iq.splice(SAMPLE, "7A55E0BA6E000010", ["Only line."])
    out.append(("splice replaces the target body",
                '"Only line.",' in spliced, True))
    out.append(("splice removes the old body",
                "First line." in spliced, False))
    out.append(("splice leaves the neighbouring quest alone",
                "Untouched [not an array end] body." in spliced, True))
    out.append(("splice leaves the title alone",
                '"quest.7A55E0BA6E000010.title": "Welcome",' in spliced, True))
    out.append(("a bracket inside a string does not end the array",
                iq.splice(SAMPLE, "7A55E0BA6E000011", ["New."]).count("["),
                SAMPLE.count("[") - 1))

    try:
        iq.splice(SAMPLE, "DEADBEEFDEADBEEF", ["x"])
        got = "no error"
    except iq.Abort:
        got = "Abort"
    out.append(("splicing an absent quest aborts", got, "Abort"))

    not_array = '{\n  "quest.7A55E0BA6E000010.quest_desc": "a plain string",\n}\n'
    try:
        iq.splice(not_array, "7A55E0BA6E000010", ["x"])
        got = "no error"
    except iq.Abort:
        got = "Abort"
    out.append(("refusing to rewrite a non-array body", got, "Abort"))

    # ------------------------------------------------- the live round trip
    # The real book, exported and reparsed. This is the no-op guarantee.
    import export_quests as ex
    text = ex.build(prose_only=True)
    reparsed = parse(text)
    book = iq.current_book()
    out.append(("round trip preserves the chapter count",
                len(reparsed), len(book)))
    out.append(("round trip preserves every quest count",
                [len(c[1]) for c in reparsed], [len(c[1]) for c in book]))

    mismatched = []
    for (etitle, equests), (btitle, bquests) in zip(reparsed, book):
        for (eq_title, eq_paras), (qid, bq_title, bq_desc) in zip(equests, bquests):
            old = [p for p in (ex.strip_codes(x) for x in bq_desc) if p.strip()]
            new = [p for p in eq_paras if p.strip()]
            if old != new:
                mismatched.append(qid)
    out.append(("round trip changes no body at all", mismatched, []))

    coded = [qid for _c, qs in book for qid, _t, d in qs
             if any(iq.COLOUR_RE.search(x) for x in d)]
    out.append(("the colour-coded bodies are still there to protect",
                len(coded) > 0, True))

    return out


def main() -> int:
    failures = 0
    all_cases = cases()
    for name, got, want in all_cases:
        ok = got == want
        failures += not ok
        print("  {}  {}".format("ok  " if ok else "FAIL", name))
        if not ok:
            print("          got {!r}\n          want {!r}".format(got, want))
    print("\n{} case(s), {} failure(s)".format(len(all_cases), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
