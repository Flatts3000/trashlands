# Discoverability, and what the quest book is allowed to say

Research note, 2026-09-08. Written because the quest book has to teach and guide, and every
sentence that teaches is a sentence that closes something the player could have found out.
That is a real cost, not a rhetorical one, and this is the attempt to price it.

---

## Two words that were being used as one

**Discoverability** is a usability property: *can a player find out that a thing exists and
how it works, if they go looking.* Low discoverability is a defect.

**Discovery** is a design pleasure: *the player finds out for themselves.* Spending it is a
cost.

They pull opposite ways only if there is one place to put information. This pack has two,
which is the whole resolution and is dealt with at the bottom.

## What the research says

**Learning is the pleasure, so spending it is not free.** Raph Koster's *A Theory of Fun*
argues that fun in games comes out of mastery: "It is the act of solving puzzles that makes
games fun. In other words, with games, **learning is the drug.**" A game keeps being fun for
as long as it keeps supplying patterns the brain has not yet learned. On that account, a
quest book that hands over the solved pattern has removed the thing it was there to serve.

**Curiosity needs a gap the player can see.** George Loewenstein's information-gap theory
(1994) is the standard psychological account: curiosity arises when attention is drawn to a
gap between what one knows and what one wants to know, and the awareness of the gap produces
a feeling of deprivation that motivates closing it.

The part that matters here is the direction of the effect: **the more a person knows about a
domain, the more aware they are of their gaps, and the more curious they become.** Knowledge
does not straightforwardly destroy curiosity. It is what makes curiosity possible. A player
who does not know tire dumps exist cannot be curious about rubber.

**Gaps are not free either.** A 2023 study in *Organizational Behavior and Human Decision
Processes* is titled, in full, "(Don't) mind the gap? Information gaps compound curiosity yet
also feed frustration at work" - the finding is in the title, and it is the counterweight to
the two above. An unclosed gap generates curiosity and frustration together. Which one
dominates is not automatic.

So the shape is a curve rather than a slope. Too little and no gap is visible, which is not
mystery but confusion. Too much and there is no gap left. The target is a gap that is
**salient and closable**, and that is a narrower target than "say less".

## The genre this pack is actually in

Minecraft and Terraria are openly "wiki games": the community accepts that a large part of
the documentation lives outside the client, and Terraria's own player base argues that for
Terraria this is a feature rather than a defect.

Modded Minecraft is a harder case, and the difference is worth being precise about. Vanilla
Minecraft withholds information *by choice*. **A mod withholds it by accident** - it ships a
machine with no in-game explanation because writing one is work nobody budgeted. That is a
discoverability defect, not a design decision, and **quest books exist to repair it.**

This matters for what the book owes the player. When the quest book explains a Recompile
machine it is not spending discovery that was designed; it is closing a hole that was never
designed at all.

## The resolution, and it is structural

**The Salvager's Manual guarantees discoverability. That frees the quest book to preserve
discovery.**

Recompile ships 190 entries across 11 categories, and the player is handed the book as the
reward for quest one. Every mechanic in the mod is therefore *findable* whatever the quest
book does. So anything the quest book leaves out is not lost. It is one keypress away.

Most packs have a single book and must choose between the two properties. This pack does not
have to, and that is an asset it has not been using: the quest book has been writing the
Manual's paragraphs a second time and slightly worse.

**The book's job is to make gaps salient, not to fill them.** That is Loewenstein applied
directly. "Nothing else on this world gives rubber" opens a gap and hands the player a reason
to go looking. "One tire yields three rubber at a bench" closes it.

## The test

Tell it only when not knowing it is **unrecoverable** or **invisible**. Otherwise make the
gap salient and stop.

| Category | Example | Why | Verdict |
|---|---|---|---|
| **Unrecoverable** | Tire dumps do not regrow, and the field cut pays a third of the bench | Failure is permanent and there is no signal beforehand. This is Loewenstein's frustration side, not his curiosity side | **tell** |
| **Invisible** | Four cardboard makes a block in the 2x2 grid | Nothing in the game would ever prompt the attempt, so no gap can become salient. Not mystery, absence | **tell** |
| **Discoverable** | A burning tire heap goes out if you throw water at it | The player sees a fire, tries the obvious thing, and gets Koster's pattern-match. Low stakes, and the Manual holds it if they want certainty | **make the gap salient, do not close it** |
| **Already shown** | "Some heaps are alight" - they are visibly on fire | The world has said it. Text repeating the world is pure loss | **never** |

The fourth row is "do not recite the recipe" generalised. Do not recite the world either.

**Applied to The Sprawl**, the test cut the chapter from 222 words to 187 while *adding* the
two unrecoverable facts it was missing. It cuts more than it adds, which is the sign that it
is doing work rather than licensing.

## What this does not license

It is not an argument for terseness. A body has as much copy as its facts earn, and three of
the four categories above still say "tell". The claim is narrower: **the book stops paying
for facts the Manual already holds and the player would have enjoyed finding.**

Nor is it an argument for mystery as an aesthetic. A gap that cannot be closed is frustration
with better branding, and that is the 2023 finding above. If the book opens a gap, something
reachable has to close it.

## Sources

- Raph Koster, *A Theory of Fun for Game Design* (2005) - fun as mastery, "learning is the
  drug". [lostgarden review](https://lostgarden.com/2005/05/08/book-raph-kosters-theory-of-fun-for-game-design/),
  [O'Reilly, 2nd ed.](https://www.oreilly.com/library/view/theory-of-fun/9781449363208/)
- George Loewenstein, "The Psychology of Curiosity: A Review and Reinterpretation" (1994) -
  information-gap theory. [summary](https://psychologyfanatic.com/information-gap-theory/)
- "(Don't) mind the gap? Information gaps compound curiosity yet also feed frustration at
  work", *Organizational Behavior and Human Decision Processes* (2023).
  [abstract](https://www.sciencedirect.com/science/article/abs/pii/S0749597823000523) -
  **title and framing only; the full text is paywalled and was not read.**
- Terraria as a wiki game, community argument.
  [Steam discussion](https://steamcommunity.com/app/105600/discussions/0/594021734614586387)
