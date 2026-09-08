# Quest format

The technical half of authoring the quest book: where files live, what FTB Quests will
silently refuse, and how copy gets in and out for review.

**There is no voice document, and that is deliberate.** This pack started from zero voice
rules on 2026-09-08. The voice is [`handbook.md`](handbook.md) - the company's personnel
handbook, written as a handbook, from which quest copy is extracted. A list of rules
describing how the operator sounds is a lossy summary of a document that already exists, and
a slot that rules accrete back into. If you want to know how a quest body should read, read
the handbook.

What was thrown out, and why, is at the bottom.

---

## The method

Copy is **extracted from the handbook**, not composed per quest. Sixty-five bodies written
independently come out the same shape as each other; a document has structure of its own, and
extracts inherit it.

The handbook never ships. It is longer than what comes out of it, which is what makes an
extract read like one. Its extraction log records which section fed which quest - keep it
current, because a body that came from nowhere is one nobody can trace.

Who is speaking, and in which chapter, is a design decision rather than a style guide:
`design_decisions.md` P2.7-R and P2.7-R2.

## Where things live

- **Structure**: `pack/config/ftbquests/quests/chapters/*.json5`, with `data.json5` and
  `chapter_groups.json5` at the root of `quests/`.
- **Text**: `pack/config/ftbquests/quests/lang/en_us/`. Chapter and chapter-group titles in
  `chapter.json5`; quest bodies in `chapters/<name>.json5`, keyed by quest id.
- Inline text in a chapter file **does not render and is wiped on load**.

## What FTB Quests will not tell you

Every one of these fails silently. That is why the validator exists.

- **JSON5, not SNBT.** FTB Quests on MC 26.x reads no `.snbt` at all.
- **A missing `data.json5` loads the whole book empty**, with no in-game error. This shipped
  twice, in v0.2.0 and v0.3.0, as a Welcome chapter no player could see.
- **Ids must be positive longs** - first hex digit 0-7. An id leading 8-F is silently
  regenerated on load, dropping every dependency that pointed at it.
- **A chapter whose `group` names an undeclared group** renders under no heading at all.
- **An icon that is not an item** renders as the Missing Item placeholder. Blocks without a
  BlockItem are the trap: `recompile:mound_ground` has a block lang key and no item model,
  and reached review on PR #75 as the icon of a quest.
- **Numbers must not be quoted.** `count: "1"` and `xp: "10"` are decoded with integer
  codecs. A round trip through a JSON5 reader that stringifies scalars will produce them.
- **Dict keys containing a colon must be quoted**, or the file does not parse. The
  Modonomicon reward carries `"modonomicon:book_id"`.

## What the book is allowed to say

The book teaches and guides. It also spends discovery every time it does, and
[`discoverability.md`](discoverability.md) prices that: Koster's fun-is-learning, Loewenstein's
information-gap theory, and the finding that unclosed gaps produce frustration as readily as
curiosity.

The resolution is structural rather than stylistic. **The Salvager's Manual guarantees
discoverability - 190 entries, handed over at quest one - which frees the book to preserve
discovery.** Anything the book omits is one keypress away, not lost. Most packs have one book and
must choose; this one does not.

**Tell it only when not knowing it is unrecoverable or invisible.**

| | Verdict |
|---|---|
| **Unrecoverable** - tire dumps do not regrow, the field cut pays a third | tell |
| **Invisible** - four cardboard makes a block in the 2x2 grid | tell |
| **Discoverable** - water puts out a burning heap | make the gap salient, do not close it |
| **Already shown** - "some heaps are alight", when they are visibly alight | never |

The last row is "do not recite the recipe" generalised. Do not recite the world either.

This is not a licence to be terse: three of the four still say tell, and a body has as much copy
as its facts earn.

## Correctness

Not a style matter. A wrong mechanic is a bug that ships.

**Check the version the pack PINS, not the sibling working tree.** That repo runs ahead of
its last release, another session may be mid-edit in it, and neither state is what a player
has. Read the pinned tag first: `git show v0.20.0:path/to/file`.

Twice this has gone wrong. On 2026-08-11 a drop rate was read out of an uncommitted rebalance
and shipped as "roughly one pull in fourteen hundred"; the pinned build had it at one in
fifty-two. On 2026-09-08 a handbook draft said recovered material could be sold back at the
posted rate, and the Sell Terminal refuses raw salvage outright - the first thing a player
would try.

**Do not quote a drop rate as "one in N".** It reads as rare and was never converted into
anything a person experiences. Give it in time a player feels, or give no number, and prefer
no number while a system is being balanced.

## Two things that are not style rules

- **The world is never named.** No designation, no code, no number, anywhere. The readout at
  the Gate is the first and only naming. `the_twist.md` carries why.
- **ASCII punctuation only.** No em-dashes, en-dashes, smart quotes or emoji. House rule,
  repo-wide. `import_quests.py` normalises smart quotes and refuses dashes by name.

`the_twist.md` governs spoilers. Its requirement that breadcrumbs be environmental and
mechanical rather than written stands on its own footing, and is why the handbook does not
ship.

## Chapters

| Chapter | Covers | Speaking |
|---|---|---|
| **Welcome to the Dump** (group) | | |
| - Start Here | The premise, the guidebook handoff, the alpha notice, Discord | the pack |
| - The Ground | Induction, mounds coming back, picking through garbage | the operator |
| - The Sprawl | Leachate, tire piles, cardboard | the operator |
| - Living Here | Water, what spawns | the operator |
| Salvage | Everything up to a Bucket of Water | the operator |
| Groundwork | The reclamation ladder, grass through animal baits | the operator |
| The Depths | The Nether: slag, obsidian, terrain from shards, coal | the operator |
| (the yard) | Demolition yard, rubble, steel, Cutting Torch, concrete | unwritten |
| (iron) | Cupola Furnace, iron, blueprints | unwritten |
| (gem tier) | Mechanical Waste, the Separator, power | unwritten |

Order follows [`progression_gates.md`](progression_gates.md), the traced gate order.

**A chapter ends on an object the player can hold, not a tier boundary.** Salvage runs to a
Bucket of Water because that is the one thing needing both halves of it.

**Chapter names stay operational.** `The Way Home, Part I..VI` commits to a part count, and
four chapters are unwritten. Renaming is one line each in `chapter.json5`.

## The review loop

```sh
python tools/export_quests.py --prose-only --out docs/quest_prose.md   # whole book
python tools/export_quests.py --split docs/quest_prose/                # per chapter
#   ... review in a real editor ...
python tools/import_quests.py docs/quest_prose.md                      # show the diff
python tools/import_quests.py docs/quest_prose.md --apply              # write it
python tools/validate_quests.py
python tools/test_import_quests.py
python tools/pack_refresh.py
```

Export prose, never the full book: `quest_book.md` is 60% metadata by non-blank line, and a
checker handed that spends its attention proofreading `recompile:garbage_block`. Split by
chapter for anything scored, because a whole-book figure averages 65 quests into one number
that moves for reasons nobody can locate.

The import refuses rather than guesses. Dry run by default; exact structure match or it
aborts; titles are a blocking checksum, because quests match by position and a reordered
section would otherwise write a body onto the wrong quest; only `quest_desc` is ever written;
and a body returning with fewer paragraphs than it left with is flagged above the diff.

## What was thrown out

On 2026-09-08 this pack started from zero voice rules. `docs/quest_voice.md` is deleted. All
of the following came from Sky Frogs' 2026-06-29 postmortem rather than from here, and the
section that listed them said so in its own words: *"What that costs this pack, in rules."*

| Thrown out | Why |
|---|---|
| "Teach or guide; if neither, cut it" | Could not tell flavour that informs from flavour that performs, so it banned both |
| "It is not there to entertain" | The same rule restated |
| "Most quests get no description" | A coverage target derived from another pack shipping 249 on 750 |
| "Vary by need, never by template" | A counter-measure to composing bodies independently, which is no longer the method |
| "Let quests be boring" | Aimed at relentless wit this pack never had |
| "No shape repeats its neighbour" | The same |
| "Write by decomposition, not by drafting" | Contradicted outright by the handbook, which was drafted, deliberately |
| "Personality lives in titles only" | Superseded by having a narrator |
| "Flat and practical, not dry wit" | A description of the voice, and the handbook is a better one |
| The ~30-passage budget | Invented under the rules above. There is no cap |
| TEACH-heavy / PIVOT chapter classes | From the shared `review_protocol.md`, stood down |
| The whole shared `voice_spec.md` | Stood down for this pack |
| Minimize-authored-prose | Obsoleted. Its stated reason - "players distrust AI writing; every prose surface is a liability" - is a hedge against bad writing, not a design position |

The shared toolkit at `mc-pack-toolkit/quest-voice/` and `tools/score_quest_voice.py` are
**kept and unused.** Nothing was deleted; none of it is the standard here.

**The Sky Frogs failure is still worth knowing**, as history rather than as rules: 750
quests, 249 descriptions, 301 dash-reveals, 245 of 245 subtitles in a single form, and
players said it looked like AI. The diagnosis survives and the prescription does not. The
root cause was register, and the answer here is a narrator with a reason to sound like
itself, not a list of prohibitions.
