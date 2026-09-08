# Quest voice

How Trashlands quest text is written. This is the pack-specific layer only.

**This page is the authority for Trashlands copy.** It used to defer to the shared spec at
`F:\minecraft-repos\mc-pack-toolkit\quest-voice\voice_spec.md` and the `quest-voice` skill; as of
2026-09-08 it does not. That spec and its tooling are stood down for this pack, and nothing has
been deleted - the last section says why. Read the shared spec as background on another pack's
failure if you want it. Read this before writing.

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

## The narrator

**The book is written by the site operator.** The conglomerate that runs this disposal ground
wrote the induction material the player is reading, and wrote it for a worker it has never met.
Identity locked 2026-09-08, closing the open thread left by `design_decisions.md` P2.7 item 4
("lock that quests HAVE a narrator persona; specific identity is a twist-adjacent open thread
for the quest-writing phase"). What the choice is worth narratively lives in
[`the_twist.md`](the_twist.md) and is deliberately not restated here.

Why this persona and not the other two P2.7 floated: **its natural register is already the
register this pack mandates.** A previous scavenger wants to be wry; a last archivist wants to be
elegiac. Both would fight the flat-and-practical rule on every line, and losing that fight is
precisely the Sky Frogs failure. Site documentation is flat because site documentation is flat.
This narrator costs no drift.

Note it does not conflict with the no-personification rule above. That rule says name the real
agent or none. An operator running a site is a real agent; a block that "wants" is not.

Rules, and they are tight:

1. **The narrator never teaches.** No mechanic, no recipe, no number. Teaching belongs to the
   other node type. A quest is one or the other, never both.
2. **The narrator is never funny.** Corporate satire is a worn seam (Aperture, Vault-Tec) and it
   invites exactly the performed wit this pack exists to avoid. A line that raises a smile is wrong.
3. **The narrator is never menacing.** A sinister undertone telegraphs, and there is nothing to
   telegraph yet. As far as the operator is concerned this is a routine posting at a routine site.
4. **Indifferent, not upbeat.** The default failure of a corporate voice is chirpiness. Write an
   induction packet, not an advert. No thanking, no congratulating, no exclamation.
5. **It is wrong about how hard the job is, and never notices.** That is the only place tension
   is allowed to live, and it is never remarked on by anyone.
6. **It does not address the player as a person.** Administrative second person and passive
   construction: "personnel", "recovery is permitted", "the assignment". It has never met you.

## Two node types, never blended

Prominence II is the corpus's only heavy-narrative pack, and what makes it work is not that it
writes more. It is that lore nodes and tutorial nodes are separated by node type and, in the
corpus reading, "never blended within a line." That is the model here.

| | Teaching nodes | Operator nodes |
|---|---|---|
| Voice | none, impersonal | the site operator |
| Job | teach the new player, guide the veteran | carry the narrative |
| Carries | mechanics, gotchas, the number that matters | no mechanic, no number, ever |
| Share of book | most of it | budgeted, see below |
| Shape | the existing shapes | `rsquare`, reserved and currently unused |

**Every body written before 2026-09-08 is a teaching node and stays exactly as it is.** The
narrative layer is added alongside them, never folded into them. That is what makes this frame
cheap to adopt: nothing already shipped was authored against the wrong frame, so nothing has to
be rewritten to accept a narrator.

## The narrative budget

**A hard cap, and it is the whole of the pack's authored story surface.**

| Slot | Per | Approx |
|---|---|---|
| Chapter opener | one per chapter | 10 |
| Chapter close, `hide_text_until_complete` | one per chapter | 10 |
| Act transition | one per chapter group | 4 |
| The reveal cluster | final chapter, authored against `the_twist.md` | 5 |

Roughly 30 short passages for the entire pack. Three things follow:

- **A budget is a ceiling, not a quota.** A chapter with nothing to say gets no opener. Filling
  the budget because it exists is how uniformity comes back.
- **`hide_text_until_complete` is this pack's best narrative slot and nothing uses it.** Text
  readable only after finishing is spoiler-safe by construction, which matters more here than in
  most packs. FTBQ carries the flag on quests and on chapters.
- **The strongest narrative beat in the design has no words in it at all.** The Gate opens onto
  coarse dirt and garbage mounds. Prose is the fallback surface, not the primary one.

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
it, and neither state is what a player has. Read the pinned tag - `git show v0.14.0:path/to/file` -
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
Classification decides how much copy each chapter earns. (This used to cite `quest-voice/review_protocol.md`; that toolkit is stood down, and the classes below stand on their own.)

| Chapter | Covers | Class | State |
|---|---|---|---|
| Welcome | Orientation, the no-trees gotcha, the guidebook handoff | TEACH-heavy | written |
| Salvage | Everything up to your first Bucket of Water: trash tools, Bulky Waste, food, storage, the Sorting Tarp, the Workbench, the Pump and Rain Collector, the Burn Barrel and copper, fuel, and the Scrap Network adjacency rule | TEACH-heavy | written |
| (network) | Scrap Bins and binding, the Filing Cabinet, and crafting straight out of the cluster - issue #11. Adjacency itself is already taught inside Salvage as of v0.5.0, so this chapter starts from a player who knows blocks touch | TEACH-heavy | |
| Groundwork | The whole reclamation ladder: Grass Spreader, Mound Ground and the quarry-versus-heal trade, the frontier, Compost Heap and Fertilizer, farmland, the Tree Nursery, and the animal baits. Ends on a rich bait, so the herd breeds without you | TEACH-heavy | written |
| The Depths | The Nether. Slag off the Cupola, the Slag Furnace, obsidian and so a portal, techno-organic waste and slag rubble, terrain crafted from shards, the machine chains for quartz, glowstone, wart and blaze powder, and lignite. Ends on a piece of coal, which this world had no other route to | TEACH-heavy | written |
| (the yard) | Demolition yard, rubble and stone, steel piles, Cutting Torch, concrete | PIVOT | |
| (iron) | Cupola Furnace and iron, blueprints | TEACH-heavy | |
| (gem tier) | Mechanical Waste, the Separator, power | PIVOT | |
| (reclamation) | The Hydroponics Bay. The whole rung ladder moved into Groundwork | PIVOT | |

TEACH-heavy chapters get full decomposition and a line-by-line read. PIVOT chapters get a
hand-written opener and templated steps. A pure checklist family gets titles only.

**Chapter names are still operational, not `The Way Home, Part I..VI`, but the old reason expired
and the new one is smaller. Corrected 2026-09-08.** This paragraph used to say the endgame was
reopened and the postgame parked, so the arc had no destination. P3.10 chose the endgame on
2026-09-06 (the freight ladder) and [`the_twist.md`](the_twist.md) records the final chapter as
unblocked the same day. The destination exists.

What actually holds the renaming now is arithmetic: `Part I..VI` commits to a part count, and four
of the planned chapters (the yard, iron, gem tier, reclamation) are unwritten, so the count is not
known. Name them when the chapter set is final. Sky Bees Reborn's corpus entry is flagged for the
failure this avoids: it opens on a "looming over the void" fiction and drops it after the welcome
screen. Renaming is a one-line change per chapter in `lang/en_us/chapter.json5`; rewriting bodies
authored to the wrong frame is not, which is why the frame is settled first and the labels last.

**Chapter groups are the act structure, and `chapter_groups.json5` is empty.** Groups are the
cheap, reversible half of the escape framing: they carry an act name without committing to a part
count. Deliberately left empty until there are enough chapters for acts to mean anything; building
one group around the current four would be a container, not a structure.

## Mechanics

- **Text lives under `pack/config/ftbquests/quests/lang/en_us/`**, keyed by quest id and split
  across files: chapter titles in `chapter.json5`, quest bodies in `chapters/<name>.json5`.
  Structure lives in `chapters/*.json5`, and `data.json5` plus `chapter_groups.json5` sit at the
  root of `quests/`. Inline text in a chapter file does not render and gets wiped on load.
- **JSON5, not SNBT.** FTB Quests on MC 26.x reads no `.snbt` at all - there is not a `.snbt` string
  anywhere in the 26.1.2.3 jar. SNBT belongs to the previous major, which is why Sky Frogs is a
  voice reference and never a format one.
- **Quest, chapter, and task ids must be positive longs** - the first hex digit is 0-7. An id leading
  8-F gets silently regenerated on load, which drops dependencies.
- **ASCII punctuation only.** No em-dashes, no en-dashes, no emoji.
- **FTB Quests colour codes** (`&a`, `&e`) sparingly, on key nouns, never as decoration.

## Checks

```sh
python tools/export_quests.py     # rebuild docs/quest_book.md, then read it
python tools/validate_quests.py
python tools/pack_refresh.py      # stage index.toml and pack.toml in the same commit
```

`validate_quests.py` is structural and stays mandatory: every failure it catches is silent in game,
and two of them already shipped.

**Read the book as a book before shipping copy.** `tools/export_quests.py` rejoins the two trees
(structure in `chapters/`, text in `lang/en_us/chapters/`, married only by a hex id) into
[`quest_book.md`](quest_book.md) in reading order. The split is right for the game and makes the
writing unreadable as writing, which is most of why the register read kept being skipped. The export
is one-way: edit the json5 and regenerate, never the markdown.

## The voice tooling is stood down (2026-09-08)

**Nothing is deleted.** `tools/score_quest_voice.py`, its advisory CI step, the `quest-voice` skill
and the shared toolkit at `mc-pack-toolkit/quest-voice/` (spec, AI-tell linter, 13-pack corpus) all
stay exactly where they are and may be updated later. They are simply **not the authority on this
pack's copy any more**, and no writing pass is gated on them.

The reason is that all of it is remediation for a failure that happened somewhere else. The corpus
was assembled to find what Sky Frogs was not, the linter catalogs the tells Sky Frogs shipped, and
the scorer measures the 245-of-245 subtitle shape Sky Frogs had. This pack has zero subtitles. Three
things follow, and the third is the one that matters:

1. **It is entirely prohibitive.** Nine files, none of which help produce a line. The apparatus
   answers "is this bad" and never "what goes here".
2. **It has no model of what is being written.** No narrator, no node types, no chapter arc, no
   player state; it scores detached strings. Since P2.7-R it would flag an operator node as wrong,
   because a narrative body looks like the padding it was built to kill.
3. **It automates the wrong half.** "Accuracy is half of it" above documents a drop rate that shipped
   as three different numbers, none matching the pinned build. There are three tools for style and
   none for truth, and truth is the half that reached players.

**The replacement is deliberately not designed yet.** The next chapters get written by hand with no
automated voice check at all, and the tooling gets built against the failures that actually show up
rather than the ones inherited from another pack's postmortem. Predicting the failure mode is what
produced the gates that spend their whole life below their own sample-size floor.

Everything above this section - the register, the narrator, the node split, the budget, the accuracy
rules - is unaffected. Those are the standards. What is stood down is the machinery that claimed to
measure them.
