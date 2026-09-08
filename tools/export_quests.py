#!/usr/bin/env python3
"""Export the quest book to one readable markdown document.

Why this exists
---------------
The book's copy is split across two directory trees on purpose: structure in
`chapters/*.json5`, text in `lang/en_us/chapters/*.json5`, joined only by a
16-digit hex id. That split is right for the game and useless for reading. There
is no way to sit down with the pack's writing and read it as writing, which is
exactly what a voice pass needs - `docs/quest_voice.md` says a clean lint is
"necessary and not sufficient" and that the remaining read is human.

This walks both trees, rejoins them, and writes the whole book in reading order
with the mechanical detail demoted underneath each body.

One-way by design. The export is a review surface, not a source: edits go back
into the json5 and the document is regenerated. Round-tripping markdown into
keyed json5 would be a second parser to keep honest, and its failure mode is
silent text loss in a book that has already shipped empty twice.

Usage:
    python tools/export_quests.py                 # write docs/quest_book.md
    python tools/export_quests.py --out -         # stdout
    python tools/export_quests.py --out FILE
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_quests as vq  # noqa: E402  (reuse the JSON5 parser and paths)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_OUT = "docs/quest_book.md"
CODE_RE = re.compile(r"&[0-9a-fk-or]")
QUEST_KEY_RE = re.compile(r"^quest\.([0-9A-Fa-f]{16})\.(title|quest_subtitle|quest_desc)$")
CHAPTER_KEY_RE = re.compile(r"^chapter\.([0-9A-Fa-f]{16})\.(title|subtitle)$")


def strip_codes(s: str) -> str:
    """Drop FTB Quests colour codes. They are formatting, not text."""
    return CODE_RE.sub("", s)


def words(s: str) -> int:
    return len(strip_codes(s).split())


def lang_maps(lang: dict):
    """Split the merged lang map into quest and chapter records."""
    quests: dict = {}
    chapters: dict = {}
    for key, value in lang.items():
        m = QUEST_KEY_RE.match(key)
        if m:
            rec = quests.setdefault(m.group(1).upper(), {})
            field = m.group(2)
            if field == "quest_desc":
                lines = value if isinstance(value, list) else [value]
                rec["desc"] = [v for v in lines if isinstance(v, str)]
            elif field == "quest_subtitle":
                rec["subtitle"] = value
            else:
                rec["title"] = value
            continue
        m = CHAPTER_KEY_RE.match(key)
        if m:
            chapters.setdefault(m.group(1).upper(), {})[m.group(2)] = value
    return quests, chapters


def item_of(obj) -> str:
    """Readable name for an icon, task item, or reward item."""
    if not isinstance(obj, dict):
        return str(obj) if obj else ""
    ident = obj.get("id") or obj.get("item")
    if isinstance(ident, dict):
        ident = ident.get("id")
    if not ident:
        return ""
    count = obj.get("count")
    return "{} x{}".format(ident, count) if isinstance(count, int) and count > 1 else str(ident)


def task_line(task: dict) -> str:
    kind = task.get("type", "?")
    if kind == "checkmark":
        return "checkmark"
    if kind == "item":
        return "item: " + (item_of(task.get("item")) or item_of(task))
    if kind == "advancement":
        return "advancement: " + str(task.get("advancement", "?"))
    if kind == "dimension":
        return "dimension: " + str(task.get("dimension", "?"))
    if kind == "stat":
        return "stat: " + str(task.get("stat", "?"))
    extra = item_of(task.get("item"))
    return kind + (": " + extra if extra else "")


def reward_line(rw: dict) -> str:
    kind = rw.get("type", "?")
    if kind == "xp":
        return "xp " + str(rw.get("xp", "?"))
    if kind == "item":
        return "item " + item_of(rw.get("item"))
    return str(kind)


def reading_order(chapter):
    """Dependency depth first, then page position.

    The json5 stores quests in edit order, which is the order someone happened to
    click them into the editor. Depth is the closest thing to the order a player
    meets them, and ties break by where they sit on the page.
    """
    by_id = {str(q.get("id", "")).upper(): q for q in chapter.quests}

    def depth(quest, seen=frozenset()):
        qid = str(quest.get("id", "")).upper()
        if qid in seen:
            return 0  # a cycle is the validator's problem, not this one's
        deps = [d.upper() for d in (quest.get("dependencies") or []) if isinstance(d, str)]
        inside = [by_id[d] for d in deps if d in by_id]
        if not inside:
            return 0
        return 1 + max(depth(d, seen | {qid}) for d in inside)

    return sorted(chapter.quests, key=lambda q: (depth(q), q.get("y", 0), q.get("x", 0)))


def build(prose_only: bool = False) -> str:
    chapters = sorted(vq.load_chapters(),
                      key=lambda c: (c.data.get("order_index", 0), c.name))
    qlang, chlang = lang_maps(vq.load_lang())

    title_of = {}
    for ch in chapters:
        for q in ch.quests:
            qid = str(q.get("id", "")).upper()
            if qid:
                title_of[qid] = qlang.get(qid, {}).get("title", "")

    total = sum(len(c.quests) for c in chapters)
    described = sum(
        1
        for c in chapters
        for q in c.quests
        if any(s.strip() for s in qlang.get(str(q.get("id", "")).upper(), {}).get("desc", []))
    )
    pct = round(100 * described / total, 1) if total else 0.0

    out: list = []
    add = out.append

    if prose_only:
        # Prose only, for a human or a checker to read as writing.
        #
        # The full export is 73% metadata by non-blank line: <sub> tags, code
        # spans, and id/after/tasks/rewards bullets. Handed to Grammarly that
        # dominates the document - it proofreads `recompile:garbage_block` and
        # `minecraft:paper`, reports "Add a space", and folds all of it into a
        # writing-quality score that is then mostly scoring markdown. Strip it
        # and the checker sees only the sentences.
        add("# Trashlands quest copy")
        add("")
        add("{} chapters, {} quests, {} with a body. Prose only: no ids, no tasks, no"
            .format(len(chapters), total, described))
        add("markup. Generated by tools/export_quests.py --prose-only; edit the json5.")
        add("")
        for ch in chapters:
            cid = str(ch.data.get("id", "")).upper()
            cmeta = chlang.get(cid, {})
            add("")
            add("## " + strip_codes(cmeta.get("title") or ch.name))
            add("")
            for q in reading_order(ch):
                meta = qlang.get(str(q.get("id", "")).upper(), {})
                desc = meta.get("desc", [])
                if not any(s.strip() for s in desc):
                    continue
                add("### " + strip_codes(meta.get("title") or "(untitled)"))
                add("")
                for line in desc:
                    add(strip_codes(line) if line.strip() else "")
                add("")
        return "\n".join(out).rstrip() + "\n"

    add("# The quest book")
    add("")
    add("**Generated by `tools/export_quests.py`. Do not edit this file.** Copy lives in")
    add("`pack/config/ftbquests/quests/lang/en_us/chapters/*.json5`, keyed by quest id, and")
    add("structure lives in `pack/config/ftbquests/quests/chapters/*.json5`. Edit those and")
    add("regenerate. This document exists so the writing can be read as writing, which is the")
    add("one check the linter and the scorer cannot make for you.")
    add("")
    add("Exported {} from {} chapters and {} quests, {} of them with a description ({}%).".format(
        _dt.date.today().isoformat(), len(chapters), total, described, pct))
    add("")
    add("`[no description]` marks an empty body. The pack's rule is that bare is normal and")
    add("correct (`docs/quest_voice.md` rule 1), so a low count there is not a gap to fill.")
    add("")
    add("---")
    add("")

    for ch in chapters:
        cid = str(ch.data.get("id", "")).upper()
        cmeta = chlang.get(cid, {})
        add("## " + strip_codes(cmeta.get("title") or ch.name))
        add("")
        if cmeta.get("subtitle"):
            add("*" + strip_codes(cmeta["subtitle"]) + "*")
            add("")
        bits = ["`" + ch.name + "`",
                "order_index " + str(ch.data.get("order_index", "?")),
                str(len(ch.quests)) + " quests"]
        if ch.data.get("group"):
            bits.append("group `" + str(ch.data["group"]) + "`")
        if ch.images:
            bits.append(str(len(ch.images)) + " image(s)")
        add("<sub>" + " | ".join(bits) + "</sub>")
        add("")

        for q in reading_order(ch):
            qid = str(q.get("id", "")).upper()
            meta = qlang.get(qid, {})
            add("### " + strip_codes(meta.get("title") or "(untitled)"))
            add("")
            if meta.get("subtitle"):
                add("*" + strip_codes(meta["subtitle"]) + "*")
                add("")

            desc = meta.get("desc", [])
            if any(s.strip() for s in desc):
                for line in desc:
                    add(strip_codes(line) if line.strip() else "")
                add("")
                add("<sub>" + str(words(" ".join(desc))) + " words</sub>")
            else:
                add("`[no description]`")
            add("")

            head = "- id `" + qid + "`"
            if q.get("shape"):
                head += ", shape `" + str(q["shape"]) + "`"
            if q.get("icon"):
                head += ", icon `" + item_of(q.get("icon")) + "`"
            if q.get("optional"):
                head += ", **optional**"
            add(head)

            deps = [d for d in (q.get("dependencies") or []) if isinstance(d, str)]
            names = [strip_codes(title_of.get(d.upper()) or "?") for d in deps]
            add("- after: " + (", ".join(names) if names else "none"))

            tasks = [task_line(t) for t in (q.get("tasks") or []) if isinstance(t, dict)]
            add("- tasks: " + ("; ".join(tasks) if tasks else "none"))

            rewards = [reward_line(r) for r in (q.get("rewards") or []) if isinstance(r, dict)]
            if rewards:
                add("- rewards: " + "; ".join(rewards))
            add("")

        add("---")
        add("")

    return "\n".join(out).rstrip() + "\n"


def write_split(out_dir: str) -> int:
    """One prose file per chapter.

    Review happens a chapter at a time, and Grammarly's own AI-detection and
    writing-quality scores are per document: run against the whole book they
    average 63 quests into one number that moves for reasons nobody can locate.
    Per chapter the number points somewhere.
    """
    import unicodedata

    chapters = sorted(vq.load_chapters(),
                      key=lambda c: (c.data.get("order_index", 0), c.name))
    qlang, chlang = lang_maps(vq.load_lang())
    d = pathlib.Path(out_dir)
    d.mkdir(parents=True, exist_ok=True)

    written = 0
    for ch in chapters:
        cid = str(ch.data.get("id", "")).upper()
        title = strip_codes(chlang.get(cid, {}).get("title") or ch.name)
        # Same heading depths as the whole-book export (H1 title, H2 chapter,
        # H3 quest) so both shapes parse identically on the way back in. The
        # first version of --split used H1/H2 and the importer could not read
        # its own output.
        lines = ["# Trashlands quest copy: " + title, "", "## " + title, ""]
        bodies = 0
        for q in reading_order(ch):
            meta = qlang.get(str(q.get("id", "")).upper(), {})
            desc = meta.get("desc", [])
            if not any(s.strip() for s in desc):
                continue
            lines.append("### " + strip_codes(meta.get("title") or "(untitled)"))
            lines.append("")
            for line in desc:
                lines.append(strip_codes(line) if line.strip() else "")
            lines.append("")
            bodies += 1
        slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
        slug = re.sub(r"[^a-z0-9]+", "_", slug.lower()).strip("_") or ch.name
        path = d / (slug + ".md")
        path.write_text("\n".join(lines).rstrip() + "\n",
                        encoding="utf-8", newline="\n")
        print("wrote {} ({} bodies)".format(path, bodies))
        written += 1
    print("{} chapter file(s)".format(written))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Export the quest book to readable markdown.")
    ap.add_argument("--split", metavar="DIR",
                    help="write one prose file per chapter into DIR; a whole-book "
                         "AI-detection score is diluted across 63 quests, a "
                         "chapter-sized one is readable and reviewable in a sitting")
    ap.add_argument("--prose-only", action="store_true",
                    help="titles and bodies only, for a human or a grammar checker")
    ap.add_argument("--out", default=DEFAULT_OUT,
                    help="output path, or - for stdout (default: " + DEFAULT_OUT + ")")
    args = ap.parse_args()

    if args.split:
        return write_split(args.split)

    text = build(prose_only=args.prose_only)
    if args.out == "-":
        sys.stdout.write(text)
        return 0
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote {} ({} lines)".format(args.out, len(text.splitlines())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
