# Ideas backlog

**Status:** unlocked ideas, captured as they come. This is the holding pen - nothing here is
decided. An idea graduates to a numbered decision in [`design_decisions.md`](design_decisions.md)
(and a row in [`feature_matrix.md`](feature_matrix.md)) once its shape is locked. Each entry is
faithful to the original pitch, plus a few sharp notes and the open questions to resolve before
it can be built. Numbered `I-N` so they can be referenced.

---

## I-1: Junk Cooler (auto-feeder curio)

**Idea:** a **Junk Cooler** that holds **only food** and **automatically feeds you** when you
get hungry. Gets **its own Curios slot**.

**Fit / notes:**
- Sits in the food tier (P1.9). Thematically a salvaged mini-fridge/cooler dug out of the dump -
  on-brand (WALL-E salvage), and it quietly reconnects the "fridge = preserved food" fiction that
  was dropped when the appliance was cut (see P1.11). A cooler is a natural **Bulky Waste find**
  candidate, or crafted from scrap + a cooling element.
- Pure QoL: removes hunger micromanagement. Aligns with "not a survival-pressure pack" (no thirst,
  no grind) - it makes the already-low survival friction lower, it does not add pressure.
- **Its own Curios slot** (a dedicated "cooler" slot type, not competing with other trinkets) is
  the right call so it is an always-on utility, not a slot-cost trade-off.

**Depends on:**
- **Curios API** - a **new dependency**; the lineup so far is Create + Mekanism only. Curios is
  light and widely used, but adding it is a pack-level decision (affects every future trinket-style
  item too, so it may be worth it beyond just this one). Flag before committing.

**Open questions:**
- **What does it auto-eat, and when?** Threshold (eat when hunger drops below N), and which food
  first - worst-first to clear risky stock, or best-first for saturation?
- **Does it auto-eat the risky tin cans** (random-effect food)? Auto-eating a gamble can is funny
  and dangerous - a deliberate design lever (maybe it only auto-eats "safe" food, or maybe the risk
  is the point and you curate what you load).
- **Powered or passive?** Passive fits the food/early tier. If food spoilage ever exists, a
  Mekanism-energy "keeps it cold" version becomes meaningful; no spoilage today, so passive.
- **Found or crafted (or both)?** Bulky Waste find vs. a scrap recipe - or found broken, repaired
  like the furnace (find-and-fix beat).
- **Capacity** and whether it feeds from its own inventory only or also the hotbar.
