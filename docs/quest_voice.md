# Quest voice

How Trashlands quest text is written. This is the pack-specific layer only.

**Canonical spec:** `F:\minecraft-repos\mc-pack-toolkit\quest-voice\voice_spec.md`, applied via the
`quest-voice` skill. Read it before a writing pass. Everything there binds here; this page does not
repeat it, it adds what is specific to this pack and records why.

---

## The job

A quest description does two things: **teach a player who may be new to Minecraft entirely**, and
**guide a player who already knows the conventions**. That is all of it.

It is not there to sell the pack, and it is not there to entertain. The gameplay is the product; copy
that hypes it is both redundant and the loudest tell that a marketer wrote it. Copy that reaches for
a joke is competing with the game for the fun job and losing.

The test on every sentence: **is this teaching a new player or guiding an experienced one? If it is
neither, cut it.**

## This world's register

**Flat and practical. Not dry wit.**

Sky Frogs earned a dry, wry voice honestly: its premise (frogs replace mining) is absurd, and a
narrator who finds nothing odd about it is genuinely funny. That voice does not transfer. Trashlands'
premise is not absurd, it is grim and ordinary: you are picking through a dump because there is
nothing else. A wry narrator on top of that is a copywriter performing, and it will read as exactly
that.

So bodies are flat. Say what the thing is, how to get it, and the one gotcha. Stop.

**Personality lives in titles, and it is optional.** A title may be plain. Most should be. The
sanctioned-subtitle slot from the spec is deliberately under-used here: this pack does not need 60
kickers in a row, and Sky Frogs proved what happens when it has them.

**Vernacular is the register, not jargon.** Use the words a player reaches for reflexively - mob cap,
spawn-proof, silk touch, tick, despawn, hopper it in. The point is not to stuff them in; it is that a
real player has them available and a marketer does not.

## The failure this pack is avoiding

Sky Frogs shipped roughly 750 quests with 249 descriptions and players said the copy "looks like AI."
It was not badly written. It had already been through an editorial pass that made it punchy, and that
polish, applied in the same shape every time, was the problem.

Measured on 2026-06-29, before the rewrite:

| Signal | Count |
|---|---|
| ` - ` dash-as-reveal | 301 across 245 described quests |
| Subtitles in identical 3-5 word kicker form | 245 of 245 |
| Bodies on one "earnest setup, snappy button" arc | pervasive |
| Rhetorical-question openers | ~12 |

The fix took a full rewrite across 23 chapters, over two releases, and **still did not finish**: 47
dash-reveals survive, subtitles are still mostly kickers, and whether players read it as AI was never
settled.

**The root cause was register, not surface tells.** It sounded like it was written by a PR firm that
had never played Minecraft. Fixing tells on top of PR-voice copy still reads as PR-voice copy.

What that costs this pack, in rules:

1. **Most quests get no description.** A task widget that already says "collect 8 rebar" is not
   improved by a sentence saying so. Bare is normal and correct, not a gap to fill.
2. **Vary by need, never by template.** Some quests earn two plain sentences, some one fragment, most
   nothing. Uneven density is the single strongest human signal.
3. **Let quests be boring.** Relentless wit is the trying-too-hard tell.
4. **No shape repeats its neighbour.** If two adjacent descriptions have the same arc, one is wrong.
5. **Write by decomposition, not by drafting.** Name the teach payload and the guide payload, write
   only those, stop. Reaching for a nice sentence, or imitating an example, is what produces
   performed copy.

## Accuracy is half of it

Confident-but-wrong is itself an AI signal, and it compounds the impression. Every mechanic claim is
checked before it ships, against:

- [`progression_gates.md`](progression_gates.md) - the traced gate order, and the answer to "can the
  player have this yet". It exists because that question kept getting answered wrong from memory.
- [`material_economy.md`](material_economy.md) - what each material is for.
- `../recompile/` - the code and the specs. The design docs describe the intended end state, which is
  not the same as what ships. Check the roadmap phase status and the source.

**Check the version the pack PINS, not `../recompile/` as it sits.** That sibling repo is a live
working tree: it runs ahead of the last release, another session may be part-way through an edit in
it, and neither state is what a player has. Read the pinned tag - `git show v0.8.0:path/to/file` -
and only then the working tree, to see what is coming.

_This is not hypothetical. On 2026-08-11 the bucket's drop rate was read out of an uncommitted
rebalance in that repo and shipped as "roughly one pull in fourteen hundred". The pinned build had it
at one in fifty-two; the finished rebalance landed on one in twenty-five hundred. Three different
numbers, and the one that reached players matched neither._

**Do not quote a drop rate as "one in N".** Recompile #174 diagnosed exactly this in its own docs: a
rate in that form reads as rare and was never converted into anything a person experiences. Sorting
runs about five pulls a second, so "one pull in fourteen hundred" is roughly five minutes, not a
grind. Either give the number in time a player feels, or give no number - and prefer no number while
a system is being balanced, because it will be wrong again by the next release.

Three rules that come out of this directly, all now in the canonical spec:

- **Do not recite the recipe.** JEI is one keypress away and the task widget already names the item,
  so listing ingredients spends the only paragraph on the one thing a player can look up instantly.
  Answer the four questions nothing in the UI answers: **what it does, where it goes, how it goes
  together with other blocks, and when you would want it.** "Stack the funnel on the collector; on its
  own it holds water but gathers none" cannot be looked up. "A Water Tank with a Copper Pipe over it"
  is JEI read aloud. The carve-out is a recipe fact that is a *mechanic* - fitting the 2x2 inventory
  grid is a gate, one nugget per scrap is a rate. Gates and rates stay.

- **Do not personify.** Blocks and the world do not want, fight, or take. "Coarse dirt reverts grass
  at the frontier", not "the junkyard takes it back". Beyond register, it misleads: the second one
  implies a pressure the code does not apply.
- **Only verbs the game has.** You do not pour anything: you use a bottle, empty a bucket, place a
  fluid. In a recipe step this sends a new player looking for something that is not there.

## Spoiler discipline

`the_twist.md` governs. Quest text maintains the exile fiction without exception, the twist is never
hinted at in copy, and post-reveal chapters are gated at the content layer rather than only hidden in
the book. Read that file before writing any chapter; never restate its contents anywhere else.

## Chapters

Structure follows [`progression_gates.md`](progression_gates.md), which is already the traced order.

**A chapter ends on an object the player can hold, not on a tier boundary.** Salvage
runs to a Bucket of Water because that is one thing that required both halves of the
chapter - scrap smelted into copper on one side, a found Pump and collected rain on
the other. Tiers are a design vocabulary; they do not mean anything to someone
reading the book.
Classification decides how much copy each chapter earns (see `quest-voice/review_protocol.md`).

| Chapter | Covers | Class | State |
|---|---|---|---|
| Welcome | Orientation, the no-trees gotcha, the guidebook handoff | TEACH-heavy | written |
| Salvage | Everything up to your first Bucket of Water: trash tools, Bulky Waste, food, storage, the Sorting Tarp, the Workbench, the Pump and Rain Collector, the Burn Barrel and copper | TEACH-heavy | written |
| (network) | The Scrap Network and the storage tier - issue #11 | TEACH-heavy | |
| (the yard) | Demolition yard, rubble and stone, steel piles, Cutting Torch, concrete | PIVOT | |
| (iron) | Cupola Furnace and iron, blueprints | TEACH-heavy | |
| (gem tier) | Mechanical Waste, the Separator, power | PIVOT | |
| (reclamation) | The ladder, Hydroponics Bay | PIVOT | |

TEACH-heavy chapters get full decomposition and a line-by-line read. PIVOT chapters get a
hand-written opener and templated steps. A pure checklist family gets titles only.

**Chapter names are operational, not `The Way Home, Part I..VI`, and that is deliberate for now.**
The escape framing in [`the_twist.md`](the_twist.md) needs somewhere to go, and the endgame is
reopened with the postgame parked, so the arc currently has no destination. Sky Bees Reborn's corpus
entry is flagged for exactly this: it opens on a "looming over the void" fiction and drops it after
the welcome screen. Renaming chapters is a one-line change in `lang/en_us/chapter.json5` whenever the
ending exists; rewriting bodies written to the wrong frame is not.

## Mechanics

- **Text lives in `pack/config/ftbquests/quests/lang/en_us.snbt`**, keyed by quest id. Structure
  lives in `chapters/*.snbt`. Inline text in a chapter file does not render and gets wiped on load.
- **Quest, chapter, and task ids must be positive longs** - the first hex digit is 0-7. An id leading
  8-F gets silently regenerated on load, which drops dependencies.
- **ASCII punctuation only.** No em-dashes, no en-dashes, no emoji.
- **FTB Quests colour codes** (`&a`, `&e`) sparingly, on key nouns, never as decoration.

## Checks

```sh
python tools/validate_quests.py
python "F:/minecraft-repos/mc-pack-toolkit/quest-voice/lint_quest_voice.py" pack/config/ftbquests/quests/lang/en_us.snbt
python tools/score_quest_voice.py --check
python tools/pack_refresh.py      # stage index.toml and pack.toml in the same commit
```

A clean lint is necessary and not sufficient. It catches surface tells; it cannot judge register,
personification, or whether a line teaches anything. That read is human, and quest content stays on a
branch until it has been playtested.
