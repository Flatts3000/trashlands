#!/usr/bin/env python3
"""Score quest copy for mechanical AI-tells, and measure shape uniformity.

Two jobs, and the second is the one that matters here.

**Per-quest tells** rank individual descriptions. Formula below, documented so the
ranking is reproducible rather than a black box.

**Shape uniformity** is the aggregate. Sky Frogs' scorer had only the per-quest half,
and per-quest scores never showed the actual defect: 245 of 245 subtitles in the same
3-5 word kicker form. Every one of those scored the same modest 1.5 and nothing added
them up. The uniformity block is what would have made that visible while it was still
6 quests instead of 245.

Neither number judges register, personification, or whether a line teaches anything.
A human does that (docs/quest_voice.md).

  Per-quest scoring
  -----------------
  dash-as-reveal ` - `     1.5 each  spaced hyphen doing em-dash work
  long body (>=100 words)   2.5      one-shot; supersedes "wordy"
  wordy body (60-99 words)  1.5      one-shot
  fragment subtitle         1.5      subtitle of <=5 words (the kicker formula)
  rhetorical opener         1.5      desc opens with a question-word clause ending "?"
  non-MC verb 'pour'        1.0      names an action MC lacks; human confirms metaphor
  em/en-dash                2.0      house-rule violation (validate_quests blocks it)

  Bands: HIGH >=8 | MED 4-7.5 | LOW 0.5-3.5 | CLEAN 0

Usage:
    python tools/score_quest_voice.py            # print the report
    python tools/score_quest_voice.py --json     # machine-readable
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_quests as vq  # noqa: E402  (reuse the SNBT parser and paths)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STR_RE = r'"((?:[^"\\]|\\.)*)"'
RHETORICAL_RE = re.compile(
    r'^\s*(?:tired|done|want|need|ever|why|ready|sick|got|had enough|looking)\b[^"]*\?',
    re.I,
)
POUR_RE = re.compile(r"\bpour(?:s|ed|ing)?\b", re.I)
EMDASH_RE = re.compile(r"[–—]")
DASH_REVEAL_RE = re.compile(r"\S - \S")


def load_lang_text():
    """quest id -> title / subtitle / description, from the committed lang file."""
    if not vq.LANG_FILE.is_file():
        return {}, {}, {}
    text = vq.LANG_FILE.read_text(encoding="utf-8")
    titles, subs, descs = {}, {}, {}
    for m in re.finditer(r"quest\.([0-9A-F]+)\.title: " + STR_RE, text):
        titles[m.group(1)] = m.group(2)
    for m in re.finditer(r"quest\.([0-9A-F]+)\.quest_subtitle: " + STR_RE, text):
        subs[m.group(1)] = m.group(2)
    # quest_desc is an array of quoted strings, written multi-line or single-line.
    # Match the run of quoted strings between brackets so both shapes parse and a
    # "]" inside a string cannot end the match early.
    desc_re = re.compile(r"quest\.([0-9A-F]+)\.quest_desc: \[((?:\s*" + STR_RE + r")*\s*)\]")
    for m in desc_re.finditer(text):
        parts = re.findall(STR_RE, m.group(2))
        descs[m.group(1)] = " ".join(p for p in parts if p != "")
    return titles, subs, descs


def quest_chapter_map():
    out = {}
    for ch in vq.load_chapters():
        stem = ch.name[:-5] if ch.name.endswith(".snbt") else ch.name
        for q in ch.quests:
            qid = q.get("id")
            if isinstance(qid, str) and re.fullmatch(r"[0-9A-Fa-f]{16}", qid):
                out[qid.upper()] = stem
    return out


def strip_codes(s: str) -> str:
    return re.sub(r"&[0-9a-fk-or]", "", s)


def word_count(s: str) -> int:
    return len(strip_codes(s).split())


def score_quest(desc: str, sub: str):
    tells, score = [], 0.0
    plain = strip_codes(desc)

    n_dash = len(DASH_REVEAL_RE.findall(plain))
    if n_dash:
        score += 1.5 * n_dash
        tells.append(f"{n_dash}x dash-reveal")

    wc = word_count(desc)
    if wc >= 100:
        score += 2.5
        tells.append(f"long ({wc}w)")
    elif wc >= 60:
        score += 1.5
        tells.append(f"wordy ({wc}w)")

    if sub and word_count(sub) <= 5:
        score += 1.5
        tells.append("fragment subtitle")

    if RHETORICAL_RE.match(plain):
        score += 1.5
        tells.append("rhetorical opener")

    if POUR_RE.search(plain):
        score += 1.0
        tells.append("'pour' verb")

    if EMDASH_RE.search(desc) or EMDASH_RE.search(sub):
        score += 2.0
        tells.append("em/en-dash")

    return round(score, 2), tells


def band(score: float) -> str:
    if score >= 8:
        return "HIGH"
    if score >= 4:
        return "MED"
    if score > 0:
        return "LOW"
    return "CLEAN"


def uniformity(quest_ids, subs, descs) -> dict:
    """The aggregate the per-quest score cannot see.

    Sky Frogs' numbers on 2026-06-29, for calibration: 100% of described quests
    carried a subtitle and 100% of those were fragments. That is the shape a reader
    registers as machine-written, and no single quest looks wrong.
    """
    total = len(quest_ids)
    described = [q for q in quest_ids if descs.get(q, "").strip()]
    subtitled = [q for q in quest_ids if subs.get(q, "").strip()]
    fragments = [q for q in subtitled if word_count(subs[q]) <= 5]
    lengths = [word_count(descs[q]) for q in described]

    return {
        "quests": total,
        "described": len(described),
        "described_pct": round(100 * len(described) / total, 1) if total else 0.0,
        "subtitled": len(subtitled),
        "subtitled_pct": round(100 * len(subtitled) / total, 1) if total else 0.0,
        "fragment_subtitles": len(fragments),
        "fragment_pct": round(100 * len(fragments) / len(subtitled), 1) if subtitled else 0.0,
        "desc_words_mean": round(statistics.mean(lengths), 1) if lengths else 0.0,
        "desc_words_stdev": round(statistics.stdev(lengths), 1) if len(lengths) > 1 else 0.0,
        "desc_words_min": min(lengths) if lengths else 0,
        "desc_words_max": max(lengths) if lengths else 0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--check", action="store_true",
                    help="accepted for symmetry with the Sky Frogs tool; this "
                         "script never writes files")
    args = ap.parse_args()

    titles, subs, descs = load_lang_text()
    chapters = quest_chapter_map()
    quest_ids = sorted(chapters)

    if not quest_ids:
        print("no quests found - nothing to score")
        return 0

    rows = []
    for qid in quest_ids:
        desc, sub = descs.get(qid, ""), subs.get(qid, "")
        score, tells = score_quest(desc, sub)
        rows.append({
            "id": qid,
            "chapter": chapters.get(qid, "?"),
            "title": titles.get(qid, ""),
            "score": score,
            "band": band(score),
            "tells": tells,
        })
    rows.sort(key=lambda r: -r["score"])

    uni = uniformity(quest_ids, subs, descs)
    counts = {b: sum(1 for r in rows if r["band"] == b)
              for b in ("HIGH", "MED", "LOW", "CLEAN")}

    if args.json:
        print(json.dumps({"uniformity": uni, "bands": counts, "quests": rows}, indent=2))
        return 0

    print("Per-quest tells")
    flagged = [r for r in rows if r["score"] > 0]
    if not flagged:
        print("  none")
    for r in flagged:
        print(f"  {r['band']:5} {r['score']:5}  {r['chapter']:18} "
              f"{r['title'][:34]:34}  {', '.join(r['tells'])}")
    print(f"\n  {counts['HIGH']} HIGH / {counts['MED']} MED / "
          f"{counts['LOW']} LOW / {counts['CLEAN']} CLEAN")

    print("\nShape uniformity")
    print(f"  quests                {uni['quests']}")
    print(f"  with a description    {uni['described']} ({uni['described_pct']}%)")
    print(f"  with a subtitle       {uni['subtitled']} ({uni['subtitled_pct']}%)")
    print(f"  fragment subtitles    {uni['fragment_subtitles']} "
          f"({uni['fragment_pct']}% of subtitled)")
    print(f"  description words     mean {uni['desc_words_mean']}, "
          f"stdev {uni['desc_words_stdev']}, range {uni['desc_words_min']}-{uni['desc_words_max']}")
    print("\n  Watch: description rate near 100%, fragment rate near 100%, or a low")
    print("  stdev all mean the copy has one shape. That is the Sky Frogs failure,")
    print("  and no individual quest looks wrong when it happens.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
