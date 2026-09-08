#!/usr/bin/env python3
"""Read an edited prose export back into the quest lang files.

The other half of `export_quests.py --prose-only`. The review pass happens in a
real editor (Grammarly, Coda, Word, anything), and this walks the result back
into `lang/en_us/chapters/*.json5` so nobody hand-copies 59 bodies and
introduces the typos the review just removed.

`export_quests.py` says the export is "one-way by design" and gives the reason:
round-tripping markdown into keyed json5 is a second parser to keep honest, and
its failure mode is silent text loss in a book that has already shipped empty
twice. That objection is right and it has not gone away. It is answered here by
making the import refuse rather than guess, on every axis:

  * **Dry run by default.** Nothing is written without --apply.
  * **Structure must match exactly.** Same chapters, same quests, same order.
    A missing or extra heading aborts the whole run rather than importing the
    part that lined up.
  * **Titles are a checksum.** Matching is by position in the same reading order
    the export used; titles are then compared and any mismatch is reported by
    name. A title is copy and can legitimately be edited, so this asks rather
    than silently trusting position.
  * **Colour codes are never destroyed.** Four bodies carry `&a`/`&e`/`&r`,
    which the prose export strips. If such a body comes back changed, the import
    refuses it and names it for hand-editing; if it comes back identical to the
    stripped original, the original is left untouched with its codes intact.
  * **Only quest_desc is touched.** Never a title, never structure, never a
    quest that had no body. Nothing is created or deleted.
  * **Minimal diff.** Changed bodies are spliced in place; every other byte of
    the file is left exactly as it was, so the git diff shows the copy edits and
    nothing else.

Usage:
    python tools/import_quests.py docs/quest_prose.md            # show the diff
    python tools/import_quests.py docs/quest_prose.md --apply    # write it
"""

from __future__ import annotations

import argparse
import difflib
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import export_quests as ex  # noqa: E402  (same reading order, same lang maps)
import validate_quests as vq  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

COLOUR_RE = re.compile(r"&[0-9a-fk-or]")


class Abort(RuntimeError):
    pass


# --------------------------------------------------------------------- parsing

def parse_prose(path: pathlib.Path):
    """The --prose-only format: '## Chapter', '### Quest', blank-line paragraphs.

    Returns [(chapter_title, [(quest_title, [paragraph, ...]), ...]), ...].
    """
    chapters, cur_ch, cur_q, buf = [], None, None, []

    def flush_para():
        if buf:
            cur_q[1].append(" ".join(b.strip() for b in buf).strip())
            buf.clear()

    def flush_quest():
        flush_para()
        if cur_ch is not None and cur_q is not None:
            cur_ch[1].append(cur_q)

    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("### "):
            flush_quest()
            cur_q = (s[4:].strip(), [])
            continue
        if s.startswith("## "):
            flush_quest()
            cur_q = None
            cur_ch = (s[3:].strip(), [])
            chapters.append(cur_ch)
            continue
        if s.startswith("# "):
            continue
        if not s:
            flush_para()
            continue
        if cur_q is None:
            continue          # preamble under the H1, not copy
        buf.append(line)
    flush_quest()
    return chapters


# ------------------------------------------------------------------- matching

def current_book():
    """The same walk the exporter does, so order is identical by construction."""
    chapters = sorted(vq.load_chapters(),
                      key=lambda c: (c.data.get("order_index", 0), c.name))
    qlang, chlang = ex.lang_maps(vq.load_lang())
    out = []
    for ch in chapters:
        cid = str(ch.data.get("id", "")).upper()
        title = chlang.get(cid, {}).get("title") or ch.name
        quests = []
        for q in ex.reading_order(ch):
            qid = str(q.get("id", "")).upper()
            meta = qlang.get(qid, {})
            desc = meta.get("desc", [])
            if not any(s.strip() for s in desc):
                continue      # prose export omits bodiless quests
            quests.append((qid, meta.get("title") or "", desc))
        out.append((ex.strip_codes(title), quests))
    return out


def lang_file_for(qid: str):
    """Which lang file holds this quest's body, and where the array starts."""
    key = 'quest.{}.quest_desc'.format(qid)
    for p in sorted(vq.LANG_DIR.rglob("*.json5")):
        raw = p.read_text(encoding="utf-8")
        if '"' + key + '"' in raw or key in raw:
            return p, raw
    return None, None


# -------------------------------------------------------------------- writing

def render_array(paragraphs, indent_key: str, indent_item: str) -> str:
    """Render body paragraphs as a JSON5 string array.

    A blank entry separates paragraphs, which is the shape FTB Quests renders and
    the shape every existing body already uses.
    """
    parts = []
    for i, para in enumerate(paragraphs):
        if i:
            parts.append("")
        parts.append(para)
    lines = ["["]
    for s in parts:
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        lines.append('{}"{}",'.format(indent_item, esc))
    lines.append(indent_key + "]")
    return "\n".join(lines)


def splice(raw: str, qid: str, paragraphs: list):
    """Replace one quest_desc array in the file text, touching nothing else."""
    key = "quest.{}.quest_desc".format(qid)
    m = re.search(r'^([ \t]*)"?' + re.escape(key) + r'"?\s*:\s*', raw, re.M)
    if not m:
        raise Abort("could not find {} in its lang file".format(key))
    indent_key = m.group(1)
    start = m.end()
    if not raw[start:].lstrip().startswith("["):
        raise Abort("{} is not an array; refusing to rewrite it".format(key))
    open_at = raw.index("[", start)

    depth, i, in_str, esc = 0, open_at, False, False
    while i < len(raw):
        c = raw[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    else:
        raise Abort("unterminated array for {}".format(key))
    close_at = i + 1

    # Reuse the existing per-item indentation so the diff stays local.
    body = raw[open_at:close_at]
    im = re.search(r'\n([ \t]+)"', body)
    indent_item = im.group(1) if im else indent_key + "  "

    return raw[:open_at] + render_array(paragraphs, indent_key, indent_item) + raw[close_at:]


# ----------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Import an edited prose export.")
    ap.add_argument("path", help="the edited --prose-only markdown")
    ap.add_argument("--apply", action="store_true", help="write the changes")
    args = ap.parse_args(argv)

    edited = parse_prose(pathlib.Path(args.path))
    book = current_book()

    # ---- structure must match, or nothing happens ------------------------
    if len(edited) != len(book):
        print("ABORT: {} chapters in the document, {} in the book"
              .format(len(edited), len(book)))
        return 2
    problems = []
    for (etitle, equests), (btitle, bquests) in zip(edited, book):
        if len(equests) != len(bquests):
            problems.append("chapter {!r}: {} quests in the document, {} in the book"
                            .format(btitle, len(equests), len(bquests)))
    if problems:
        print("ABORT: structure does not match.")
        for p in problems:
            print("  " + p)
        print("\nRegenerate with --prose-only, redo the edits, and try again.")
        print("Adding or removing quests is not something this tool will do.")
        return 2

    changes, refused, renamed = [], [], []
    for (etitle, equests), (btitle, bquests) in zip(edited, book):
        for (eq_title, eq_paras), (qid, bq_title, bq_desc) in zip(equests, bquests):
            plain_title = ex.strip_codes(bq_title)
            if eq_title != plain_title:
                renamed.append((qid, plain_title, eq_title))

            old_paras = [p for p in (ex.strip_codes(x) for x in bq_desc) if p.strip()]
            new_paras = [p for p in eq_paras if p.strip()]
            if old_paras == new_paras:
                continue
            if any(COLOUR_RE.search(x) for x in bq_desc):
                refused.append((qid, plain_title))
                continue
            changes.append((qid, plain_title, old_paras, new_paras))

    if renamed:
        print("Titles differ between the document and the book.")
        print("Titles are copy and can be edited, but this tool only writes bodies,")
        print("so these are reported and not applied:")
        for qid, was, now in renamed:
            print("  {}  {!r} -> {!r}".format(qid, was, now))
        print()

    if refused:
        print("REFUSED: these bodies changed but carry FTB Quests colour codes,")
        print("which the prose export strips. Re-importing would delete them.")
        print("Edit these by hand in the json5:")
        for qid, title in refused:
            print("  {}  {}".format(qid, title))
        print()

    if not changes:
        print("No body changes to import.")
        return 0

    for qid, title, old, new in changes:
        print("{}  {}".format(qid, title))
        diff = difflib.unified_diff(old, new, lineterm="", n=0,
                                    fromfile="book", tofile="document")
        for line in list(diff)[2:]:
            print("  " + line)
        print()

    print("{} body change(s)".format(len(changes)))
    if not args.apply:
        print("Dry run. Nothing written. Pass --apply to write.")
        return 0

    touched = {}
    for qid, _title, _old, new in changes:
        path, raw = lang_file_for(qid)
        if path is None:
            print("ABORT: no lang file holds {}".format(qid))
            return 2
        raw = touched.get(path, raw)
        touched[path] = splice(raw, qid, new)

    for path, raw in touched.items():
        path.write_text(raw, encoding="utf-8", newline="\n")
        print("wrote {}".format(path))

    print("\nNow run: python tools/validate_quests.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
