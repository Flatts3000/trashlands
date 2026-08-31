# Top-down pass: what a player expects a landfill to contain

**Written 2026-08-30, owner-prompted.** This mod was built bottom-up: teardown, reclamation, regions,
machines. Each system was designed and then dressed. The list below is the thing that was never made -
the one a top-down designer writes *first*, before any mechanic exists, by asking what a player pictures
when they hear the concept and then checking which of those the game actually delivers.

**The first attempt at this listed objects** - tyres, trolleys, wrecked cars - and missed entire axes,
including the one Amber and the Snack Cake already sit on. That failure is the reason this is organised
by **axis** rather than by object: an object list finds objects, and most of what a player expects from
"everything here was thrown away" is not an object at all.

Nothing here is decided. Graduating an entry means a numbered decision in `design_decisions.md`, the
same as `ideas.md`.

---

## The ten axes

### 1. Objects - what is physically in a dump

**Ships:** dirty mattress, fridge, washing machine, printer, filing cabinet, broken hydroponics bay,
bin bags, broken glass, rebar, reinforced concrete, e-scrap, kitty litter, oily rags, waste drums.

**Missing:** tyres (issue #155), shopping trolley, wrecked car, furniture, shoes, cardboard bales, a
television as an *object* rather than as e-scrap, a bicycle, a pram.

This axis is the best covered and the least interesting to extend. Another object is another loot entry.

### 2. Time and preservation - what survives, and what that says

**This is the axis the first pass missed, and it is the strongest one the mod already has.**

**Ships:** Amber, with a creature inside it and a species stamped on it, read by the Sequencer into a
spawn egg. The Snack Cake, the food that outlasts everything. Six recovered paintings. Pottery sherds.
A Worn Forging Die. An echo shard. Ancient Sculk. The turpentine chain, which is explicitly about
fossilisation being irreversible.

**Missing:**
- **Strata.** A real landfill is dated by depth - you know roughly when something was buried by how far
  down it is. The mounds have no layers and depth means nothing.
- **A time capsule**: something deliberately buried to be found later. The purest form of the trope, and
  the only find that would be *addressed to you*.
- **Obsolete media** - a cassette, a floppy disk, a vinyl record. Data you cannot read until you build
  the thing that reads it.
- Fossils and bones. A newspaper with a date on it. Photographs.

### 3. Decay - what does not survive

**Ships:** organic muck, rendered organics, the Compost Heap, leachate, dump mushrooms, mycelium.

**Missing:** anything that rots *while you hold it*. Food spoilage, maggots, a compost pile that is
visibly working. Decay is currently a material you collect rather than a process you watch.

### 4. Life that moves in

**Ships:** roaches, pigeons, dump mushrooms, mycelium, fireweed, slimes, sewer turtles and frogs,
Animal Bait with terrain-weighted draws.

**Missing:** rats (issue #306). Gulls, declined - not meaningfully different from pigeons. Crows,
foxes, nesting birds. Weeds cracking concrete, which fireweed half-covers.

### 5. Hazard and contamination

**Ships:** leachate (hunger, and it drowns you), the radioactive dump, waste drums, stained ground that
cannot be healed, techno-organic waste.

**Missing:**
- **Subsidence.** Old fill settles. Standing on a mound that has not been cleared could be genuinely
  unreliable, and it is the one hazard that would make *clearing* a dump feel like making it safe.
- Sharps. A dump fire that spreads and will not go out. Gas pockets that ignite (see issue #305).

### 6. The human trace - who lived here

**Ships:** paintings, the Puzzle Cube, toy car, present, gold coin, avocado, the radium dial clock, and
the narrative layer recorded separately in `the_twist.md`.

**Missing: almost nothing here is *personal*.** The finds are objects a person owned, not objects a
person can be inferred from. A collar with a pet's name. A child's drawing. A wedding ring. One named
thing does more for this axis than ten more appliances.

### 7. Reclamation - the dump becoming land again

**Ships:** the entire ladder - Grass Spreader, plant cover, farming, trees, animals - plus encroachment
pushing back at the frontier and mounds that regrow.

**Missing:** the *ceremony* of it. A capped cell. A park bench. The sign that says what this used to be.
This axis is mechanically complete and symbolically empty.

### 8. Scale and industry - the site as an operation

**Ships:** the machine tier, the demolition yard, compacted bales, the Scrap Network.

**Missing:** a weighbridge or gatehouse, chain-link fence, a bulldozer or compactor, a crane with an
electromagnet (Magnet Scrap already exists as an item), conveyors, the idea of a cell being filled.

### 9. Economy - what junk is worth

**Ships:** found-not-crafted as a rule, the Scrap Network, emeralds via a cured zombie villager.

**Missing:** deposit return. A buyer for scrap. Any sense that junk has a *price* rather than a use.

### 10. Atmosphere

**Ships:** windblown dust in the radioactive dump, per-biome fog and sky, leachate.

**Missing:** flies. The sound of a dump. Heat shimmer over the mounds. Smell was considered and
declined - an invisible stat that teaches nothing, and the leachate hunger ruling already covers "the
dump makes you ill".

---

## The five worth building

Ranked by how much they add that nothing else does, not by cost.

1. **Obsolete media, and a reader for it.** A cassette or a floppy disk is data you cannot use until you
   build the machine that reads it - which is the mod's own thesis, stated in an object. It is the
   Sequencer pattern applied to media instead of amber, and it lands on axis 2, the strongest axis the
   mod has, while reinforcing teardown-as-knowledge rather than sitting beside it.
2. **Strata.** Depth means age. Digging a mound deeper finds older things. This costs a loot change and
   a depth check rather than a system, and it turns the mounds from a resource into a timeline.
3. **Subsidence.** The one hazard that makes clearing the dump feel like making the ground safe.
4. **A time capsule.** One find, addressed to whoever digs it up. The purest version of the trope.
5. **A named personal object.** The cheapest possible fix for axis 6, which is the emptiest axis with
   the most thematic weight.

## What this pass says about the mod

Axes 1, 4 and 7 are strong. Axis 2 is strong and was *accidental* - Amber and the Snack Cake landed
there one idea at a time, without anyone naming the axis. Axes 6, 9 and 10 are thin, and 6 is thin in
the place where the theme is heaviest.
