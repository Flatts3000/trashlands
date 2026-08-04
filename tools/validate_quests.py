#!/usr/bin/env python3
"""Static validator for the Trashlands FTB Quests content.

Catches the authoring/data class of quest bug - the ones that are silent in game,
where the book simply renders wrong or a dependency quietly vanishes. It does not
verify FTB's runtime behaviour; that needs the game (see docs/quest_voice.md).

Every check below encodes a failure that actually happened on Sky Frogs. This is a
deliberately small subset of that pack's validator (tools/validate_quests.py there,
1418 lines): most of its bulk is Productive Frogs jar introspection, coil ladders,
and census-generator reconciliation, none of which exist here. Checks get added when
this pack earns them, not by copying.

Usage:
    python tools/validate_quests.py [--strict]

Exit codes: 0 = clean (or warnings only), 1 = at least one ERROR,
            2 = warnings only AND --strict was passed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent


def set_root(repo: Path) -> None:
    """Point every path at `repo`. Overridable so the checks can be exercised
    against a throwaway tree - a validator nobody has seen fail is not evidence."""
    global REPO, QUESTS, CHAPTERS_DIR, LANG_DIR, DATA_FILE, GROUPS_FILE, RESOURCEPACKS
    REPO = repo
    QUESTS = REPO / "pack" / "config" / "ftbquests" / "quests"
    CHAPTERS_DIR = QUESTS / "chapters"
    LANG_DIR = QUESTS / "lang" / "en_us"
    DATA_FILE = QUESTS / "data.json5"
    GROUPS_FILE = QUESTS / "chapter_groups.json5"
    RESOURCEPACKS = REPO / "pack" / "resourcepacks"


set_root(REPO)

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
HEX_POSITIVE = set("01234567")
HEX_ID = re.compile(r"^[0-9A-F]{16}$")
EM_EN_DASH = re.compile(r"[—–]")

# Text that FTB extracts into the lang file on world load. Authoring any of these
# inline in a chapter file is a silent data-loss bug: it renders as a raw key or
# gets wiped on the next save.
INLINE_TEXT_KEYS = ("title", "subtitle", "description")


# --------------------------------------------------------------------------- #
# Minimal JSON5 parser
# --------------------------------------------------------------------------- #
# FTB Quests on MC 26.x stores quests as JSON5 (de.marhali.json5): unquoted keys,
# trailing commas, // and /* */ comments, no type suffixes on numbers. There is no
# .snbt string anywhere in the 26.1.2.3 jar - SNBT belongs to the previous major
# version, and Sky Frogs is not a format reference for this pack.
#
# The tolerant reader below started as that pack's SNBT parser, which is close
# enough to JSON5 to keep: both allow unquoted keys and treat commas as
# separators. Comment skipping is the addition. Only structure matters here, so
# scalars stay raw strings.
class SNBTError(Exception):
    pass


class SNBT:
    def __init__(self, s: str):
        self.s = s
        self.i = 0
        self.n = len(s)

    def parse(self):
        self._ws()
        return self._value()

    def _ws(self):
        """Skip whitespace, commas, and JSON5 comments."""
        while self.i < self.n:
            c = self.s[self.i]
            if c in " \t\r\n,":
                self.i += 1
            elif c == "/" and self.i + 1 < self.n:
                nxt = self.s[self.i + 1]
                if nxt == "/":
                    end = self.s.find("\n", self.i)
                    self.i = self.n if end < 0 else end + 1
                elif nxt == "*":
                    end = self.s.find("*/", self.i + 2)
                    self.i = self.n if end < 0 else end + 2
                else:
                    return
            else:
                return

    def _value(self):
        self._ws()
        if self.i >= self.n:
            raise SNBTError("unexpected end of input")
        c = self.s[self.i]
        if c == "{":
            return self._obj()
        if c == "[":
            return self._arr()
        if c == '"':
            return self._string()
        return self._scalar()

    def _obj(self) -> dict:
        self.i += 1
        d: dict = {}
        while True:
            self._ws()
            if self.i >= self.n:
                raise SNBTError("unterminated object")
            if self.s[self.i] == "}":
                self.i += 1
                return d
            key = self._key()
            self._ws()
            if self.i >= self.n or self.s[self.i] != ":":
                raise SNBTError(f"expected ':' after key {key!r}")
            self.i += 1
            d[key] = self._value()

    def _arr(self) -> list:
        self.i += 1
        a: list = []
        while True:
            self._ws()
            if self.i >= self.n:
                raise SNBTError("unterminated array")
            if self.s[self.i] == "]":
                self.i += 1
                return a
            a.append(self._value())

    def _key(self) -> str:
        self._ws()
        if self.s[self.i] in "\"'":
            return self._string()
        j = self.i
        while self.i < self.n and self.s[self.i] not in " \t\r\n:":
            self.i += 1
        return self.s[j:self.i]

    def _string(self) -> str:
        self.i += 1
        out = []
        while self.i < self.n:
            c = self.s[self.i]
            if c == "\\":
                self.i += 1
                out.append(self.s[self.i] if self.i < self.n else "")
            elif c == '"':
                self.i += 1
                return "".join(out)
            else:
                out.append(c)
            self.i += 1
        raise SNBTError("unterminated string")

    def _scalar(self) -> str:
        j = self.i
        while self.i < self.n and self.s[self.i] not in " \t\r\n,}]":
            self.i += 1
        return self.s[j:self.i]


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
class Chapter:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.raw = path.read_text(encoding="utf-8")
        self.data = SNBT(self.raw).parse()
        self.quests = self.data.get("quests", []) or []
        self.images = self.data.get("images", []) or []

    def line_of(self, token: str) -> int:
        """1-based line of the first occurrence of `token`, or 0."""
        idx = self.raw.find(token)
        return self.raw.count("\n", 0, idx) + 1 if idx >= 0 else 0


def load_chapters() -> list[Chapter]:
    if not CHAPTERS_DIR.is_dir():
        return []
    return [Chapter(p) for p in sorted(CHAPTERS_DIR.glob("*.json5"))]


def load_lang() -> dict:
    """Merge every lang file under lang/en_us/ into one key -> value map.

    26.x splits translations across chapter.json5, chapter_group.json5,
    file.json5, reward_table.json5, and one file per chapter under chapters/.
    Which file a key lives in does not matter to any check here; that a key
    resolves to a real object does.
    """
    out: dict = {}
    if not LANG_DIR.is_dir():
        return out
    for p in sorted(LANG_DIR.rglob("*.json5")):
        try:
            data = SNBT(p.read_text(encoding="utf-8")).parse()
        except SNBTError as e:
            raise SNBTError(f"{p.name}: {e}") from e
        if isinstance(data, dict):
            out.update(data)
    return out


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #
def check_ids(chapters, out):
    """IDs must be 16 hex digits leading 0-7, and unique across everything.

    FTB stores these as signed longs. An id whose first hex digit is 8-F parses
    negative, and FTB silently regenerates it on load - which drops every
    dependency pointing at it. Nothing warns; the book just loses its ordering.
    """
    seen: dict[str, str] = {}

    def one(value, kind, ch):
        if not isinstance(value, str):
            return
        where = f"{ch.name}:{ch.line_of(value)}"
        if not HEX_ID.match(value):
            out.append((ERROR, "Q-ID-FORMAT", where,
                        f"{kind} id {value!r} is not 16 uppercase hex digits"))
            return
        if value[0] not in HEX_POSITIVE:
            out.append((ERROR, "Q-ID-POSITIVE", where,
                        f"{kind} id {value} leads with {value[0]}, so it parses as a "
                        f"negative long. FTB regenerates it on load and drops any "
                        f"dependency on it. Use a leading 0-7."))
        if value in seen:
            out.append((ERROR, "Q-ID-UNIQUE", where,
                        f"{kind} id {value} already used by {seen[value]}"))
        else:
            seen[value] = f"{kind} in {ch.name}"

    for ch in chapters:
        one(ch.data.get("id"), "chapter", ch)
        for q in ch.quests:
            one(q.get("id"), "quest", ch)
            for t in q.get("tasks", []) or []:
                one(t.get("id"), "task", ch)
            for r in q.get("rewards", []) or []:
                one(r.get("id"), "reward", ch)
    return seen


def check_dependencies(chapters, out):
    """Every dependency must resolve to a quest that exists."""
    quest_ids = {q.get("id") for ch in chapters for q in ch.quests}
    for ch in chapters:
        for q in ch.quests:
            for dep in q.get("dependencies", []) or []:
                if dep not in quest_ids:
                    out.append((ERROR, "DEP-DANGLING", f"{ch.name}:{ch.line_of(dep)}",
                                f"quest {q.get('id')} depends on {dep}, which is not "
                                f"a quest in any chapter"))


def check_required_files(out):
    """data.json5 and chapter_groups.json5 must exist.

    Without data.json5, readDataFull throws FileNotFoundException before a single
    chapter is read and the book loads completely empty. This repo shipped v0.2.0
    and v0.3.0 with no data file at all, so the Welcome chapter those releases
    advertised has never been visible to a player. Nothing else catches it: the
    pack builds, the export is valid, and the only evidence is a stack trace in
    the client log.
    """
    if not DATA_FILE.is_file():
        out.append((ERROR, "NO-DATA-FILE", DATA_FILE.name,
                    "quests/data.json5 is missing. FTB Quests fails to load the "
                    "whole file and the book renders empty, with no in-game error."))
    if not GROUPS_FILE.is_file():
        out.append((ERROR, "NO-GROUPS-FILE", GROUPS_FILE.name,
                    "quests/chapter_groups.json5 is missing"))


def check_inline_text(chapters, out):
    """Text authored in a chapter file instead of the lang files.

    Titles, subtitles, and descriptions are translation keys resolved out of
    lang/<locale>/. Text left inline in a chapter is not read.
    """
    for ch in chapters:
        for key in INLINE_TEXT_KEYS:
            if key in ch.data:
                out.append((ERROR, "LANG-INLINE", f"{ch.name}:{ch.line_of(key)}",
                            f"chapter carries inline {key!r}; author it in "
                            f"lang/en_us/chapter.json5 as "
                            f"chapter.{ch.data.get('id')}.{key}"))
        for q in ch.quests:
            for key in INLINE_TEXT_KEYS:
                if key in q:
                    out.append((ERROR, "LANG-INLINE", f"{ch.name}:{ch.line_of(key)}",
                                f"quest {q.get('id')} carries inline {key!r}; "
                                f"author it in lang/en_us/chapters/{ch.name}"))


def check_lang(chapters, lang, out):
    """Lang keys must point at something real, and every quest wants a title.

    A description is optional and often correct to omit (docs/quest_voice.md: most
    quests earn no prose). A missing title is different - the book falls back to
    the raw task name.
    """
    known = {ch.data.get("id") for ch in chapters}
    known |= {q.get("id") for ch in chapters for q in ch.quests}

    titled = set()
    for key in lang:
        m = re.match(r"^(chapter|quest|task|reward|chapter_group|reward_table)"
                     r"\.([0-9A-Fa-f]+)\.(\w+)$", key)
        if not m:
            out.append((WARN, "LANG-KEY-SHAPE", "lang/en_us",
                        f"key {key!r} does not look like <chapter|quest>.<id>.<field>"))
            continue
        _kind, qid, field = m.groups()
        if qid not in known:
            out.append((ERROR, "LANG-ORPHAN", "lang/en_us",
                        f"key {key!r} references id {qid}, which no chapter or quest "
                        f"defines. It will never render."))
        if field == "title":
            titled.add(qid)

    for ch in chapters:
        for q in ch.quests:
            if q.get("id") not in titled:
                out.append((WARN, "LANG-NO-TITLE", ch.name,
                            f"quest {q.get('id')} has no title in lang/en_us/"))


def check_dashes(out):
    """House rule: ASCII punctuation only, no em-dashes or en-dashes."""
    # Relative path, not just the name: a chapter and its lang file share a
    # basename (chapters/welcome.json5 and lang/en_us/chapters/welcome.json5),
    # so "welcome.json5:4" does not say which file to open.
    for path in sorted(QUESTS.rglob("*.json5")):
        rel = path.relative_to(QUESTS).as_posix()
        text = path.read_text(encoding="utf-8")
        for n, line in enumerate(text.splitlines(), 1):
            if EM_EN_DASH.search(line):
                out.append((ERROR, "DASH", f"{rel}:{n}",
                            "em-dash or en-dash; use a hyphen, comma, colon, or "
                            "restructure"))


def check_images(chapters, out):
    """Chapter images must resolve to a file in a bundled resource pack.

    A broken image path renders as a missing-texture square with no log line.
    """
    for ch in chapters:
        for img in ch.images:
            ref = img.get("image")
            if not isinstance(ref, str) or ":" not in ref:
                continue
            namespace, rel = ref.split(":", 1)
            hits = list(RESOURCEPACKS.glob(f"*/assets/{namespace}/{rel}"))
            if not hits:
                out.append((ERROR, "IMG-MISSING", f"{ch.name}:{ch.line_of(ref)}",
                            f"image {ref!r} has no file at "
                            f"pack/resourcepacks/*/assets/{namespace}/{rel}"))


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="exit 2 when there are warnings but no errors")
    ap.add_argument("--root", type=Path,
                    help="validate a different repo tree (used to self-test the checks)")
    args = ap.parse_args()

    if args.root:
        set_root(args.root.resolve())

    if not QUESTS.is_dir():
        print(f"no quest directory at {QUESTS} - nothing to validate")
        return 0

    try:
        chapters = load_chapters()
        lang = load_lang()
    except SNBTError as e:
        print(f"ERROR  SNBT-PARSE  {e}")
        return 1

    out: list[tuple[str, str, str, str]] = []
    check_required_files(out)
    check_ids(chapters, out)
    check_dependencies(chapters, out)
    check_inline_text(chapters, out)
    check_lang(chapters, lang, out)
    check_dashes(out)
    check_images(chapters, out)

    errors = [o for o in out if o[0] == ERROR]
    warns = [o for o in out if o[0] == WARN]

    for level, code, where, msg in out:
        print(f"{level:5}  {code:16}  {where:28}  {msg}")

    quests = sum(len(ch.quests) for ch in chapters)
    print(f"\n{len(chapters)} chapter(s), {quests} quest(s): "
          f"{len(errors)} error(s), {len(warns)} warning(s)")

    if errors:
        return 1
    if warns and args.strict:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
