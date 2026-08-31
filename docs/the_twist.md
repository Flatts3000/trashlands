# THE TWIST - full spoilers. Do not summarize elsewhere.

**This file is the only place in the repo that states the twist plainly.** Everything player-facing (quest text, changelogs, CurseForge page, README) maintains the surface fiction. If you are writing pack copy, read this once, then never reference it directly.

---

## The twist

The pack's stated goal, from minute one, is to **get back to the overworld.** The quest fiction says you were dumped in a waste dimension. The tech tree is framed as escape infrastructure, culminating in the **Overworld Gate**.

The last chapter reveals: **there is no overworld to return to. This IS the overworld.** The garbage plain is the old world - buried, abandoned, still catching its own deorbiting trash. You were never exiled. You're standing on home.

## The surface fiction (what the player is told)

- The quest book claims exile: dumped in "the Heap" (quest-voice name TBD) by parties unknown.
- The long arc is building the Overworld Gate - every tier has a diegetic escape reason.
- Chapter titles sell it: "The Way Home," parts one through six.

## Fair-play breadcrumbs (never hinted at, only legible in hindsight)

**All breadcrumbs are environmental or mechanical - NOT written lore** (per the minimize-authored-prose principle). The twist must land without prose documents.

1. **The buried world uses your recipes.** Recovered schematics are for ordinary vanilla/modded items - because this civilization was yours. Mechanical, no text needed.
2. **Environmental set-dressing is evidence:** buried roads, street lamps, bus stops, signage, preserved food in fridges. The old world's skeleton, in plain sight, for the entire playthrough. Built from blocks, not readables.
3. **A time capsule** containing a child's drawing (an image/painting item) of green hills whose silhouette matches the local terrain. Visual, not prose.
4. **The garbage falls from space.** Someone threw it from somewhere. Shown, never narrated.
5. **F3 says `minecraft:overworld` the whole time.** We deliberately keep the real dimension ID. The technically-minded have the answer from second one and won't believe it. This is a feature; do not "fix" it with a custom dimension ID.

## The reveal

The Overworld Gate completes at the end of the tech tree. It activates - and **opens onto coarse dirt and garbage mounds.** The environment carries the reveal: a gate to the overworld goes *here*. The player understands before any words.

The confirmation is a single quest beat (quests are a sanctioned writing surface), kept to a few punchy lines, not a lore dump - e.g. the destination readout resolving to `Site designation: Overworld`. Minimal text; the gut-punch is the Gate opening onto the same garbage you started in.

There is no way home. **There is only home.**

## The new payoff (the rug pull must hand over a bigger one)

A twist that only subtracts the goal deflates the pack. Two design moves prevent that:

**1. Nothing you built was wasted.** The Gate does not fail; it repurposes. The escape infrastructure (mass recycling, terraforming-grade materials, energy) was exactly the restoration infrastructure this world needed. The escape project WAS the reclamation project under its real name. The reveal recontextualizes the player's factory instead of invalidating it.

**2. The replacement payoff is bigger and SHOWN, staged across a playable final chapter:**

1. **The sky clears.** Retiring mounds stops the deorbit rain over that land; fully healed regions get open blue sky and stars - the first time in the playthrough garbage isn't falling somewhere on screen. "You stopped the rain."
2. **Life returns in waves:** grass, trees, then animals - vanilla life returning to land that was garbage.
3. **People return.** Completing the reclamation quest line triggers villagers to arrive and settle the healed land - the "no longer need the dump" win condition made visible as a living village. (Quest-gated, not metric-gated - progression is quest-based.)
4. **The dead Gate stays standing as a monument** in the middle of the green. Final image: a village under a clear sky on land that was garbage. You didn't go home. You made it.

The pack's promise ("get back to the overworld") is kept literally: the overworld comes back.

## The conglomerate (added 2026-08-30)

**The scrap buyer answers breadcrumb 4.** "The garbage falls from space. Someone threw it from
somewhere" has never had a *who*. The conglomerate is the who, and the market block is how that lands
mechanically instead of as written lore.

### The loop, stated plainly

You sell the planet's remains back to the people who buried it, and they pay you in tokens that are
only good with them. Then you spend those tokens buying back the recipes your own civilization wrote.

Every part of that is already in the design for other reasons, which is why it fits:

- **The recipes went in the bin, and somebody owns them now.** Buying Blueprints from the conglomerate
  is buying back your own culture from the company that threw it away. Breadcrumb 1 says the recovered
  schematics are yours *because this civilization was yours* - the market is that same fact, with a
  price on it.
- **Company scrip** - tokens issued by the company, redeemable only at the company store, worthless
  everywhere else - is a real and grim piece of industrial history. It is also the exact shape of the
  relationship: you cannot bank what they pay you, you can only spend it back.

### The breadcrumb, and it is fair play

**The freight goes up.** Garbage falls out of the sky for the entire playthrough; the scrap you sell
leaves the same way, in the opposite direction. Nothing says so. A player who notices that the outbound
route and the inbound rain are the same route has the twist in hand, and - exactly like the F3
dimension ID - will not believe it.

The second one is quieter and better: **the surface fiction says you were dumped here by parties
unknown, and you have been doing business with them since the first hour.** That is never hinted. In
hindsight it is the whole game.

### What it does at the reveal

The market does not break; it **inverts**. Before the Gate it is a useful shop. After, it is what you
have been doing: feeding a dead world to the party that killed it, for scrip.

This is the same move the Gate makes - nothing you built was wasted, it means something else now - so
the market needs no special handling at the reveal beyond the player understanding it.

### The post-twist payoff, which the rug pull owes

Consistent with the existing epilogue rather than competing with it:

- **Their want-list empties as you heal.** They only ever wanted what they dumped. A cleared region has
  nothing they will buy, so **the market going quiet is the reclamation metric made visible** - the
  same job the clearing sky does in payoff 1, on the economic axis instead of the environmental one.
- **The freight route repurposes rather than shutting down.** The escape infrastructure became the
  restoration infrastructure; the trade route is the last piece of that pattern. What comes *down* it
  at the end is the open question, and "people" is the obvious answer given payoff 3.

### Engine and pack split - this is what keeps the spoiler safe

The market block is **Recompile** (a system), the meaning is **Trashlands** (curation and quests). That
is not only the standing architectural rule, it is the spoiler discipline:

- **The engine's market carries no lore.** It buys scrap, it pays scrip, its destination is "off-site"
  and nothing more. Recompile ships standalone and a player using the mod alone gets a shop.
- **The pack supplies the party, the framing and the reveal.** Issue Flatts3000/recompile#311 is the
  engine half and must stay lore-free - that repo is public and its issues are the most visible surface
  there is. Rule 2 above permits naming this file, and nothing more.

## What the twist resolves

- **The pristine-payoff open question** (design_decisions.md, Dimensions section): the green world is not a place you reach; it is the thing you make after the reveal. The final chapter pivots escape -> reclamation: heal the mounds, retire the quarries, life returns. The quarry-vs-heal tension (P1.6) is the epilogue's gameplay.
- **Why the End is garbage too:** they threw it into the void. Even the "way out" dimensions are part of the burial.

## Process rules (spoiler discipline)

1. Quest text, changelogs, README, CurseForge description: **maintain the exile fiction.** Marketing pitches the pack as "escape the dump and get back to the overworld."
2. No other doc in this repo states or hints at the twist. Cross-reference this file by name only ("see the_twist.md").
3. Quest-voice work on the final chapter happens against this file directly.
4. Playtester builds that include the final chapter need spoiler-safe feedback channels.
5. **Post-twist quests are hidden in FTB Quests until the Gate activates** (single reveal switch). But FTBQ visibility alone leaks - close every edge: post-twist content must ALSO be gated at the content layer (behind the Gate event), so reward-item names, advancement toasts, JEI recipes, and quest-book search can't surface it early. The book should read as complete at "The Way Home, Part VI" - the existence of more chapters is the surprise.
