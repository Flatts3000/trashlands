# Branding

How the Trashlands logo is made, and how to remake it. Mirrors the Sky Frogs process
(`../sky-frogs/docs/branding.md`), which is the house pattern for pack logos.

**Maintainer rule: no AI-generated art.** Everything here comes from a real render or a real in-game
screenshot; the only automated step is a deterministic Pillow composite.

## The logo

`branding/logo.png` (512 master) and `pack/icon.png` (the CurseForge project logo) are the same
image: a two-row **TRASH / LANDS** wordmark over an in-game shot of the garbage world.

| Asset | What it is |
|---|---|
| `branding/wordmark_two_row.png` | 2048x1068 transparent PNG, straight from the Minecraft Title Generator |
| `branding/backdrop.jpg` | 1920x1027 in-game screenshot, no HUD. Same capture as the mod's gallery shot `01-garbage-world.jpg` |
| `branding/logo.png` | 512x512 composite, the master |
| `pack/icon.png` | The CurseForge logo. Emitted at the largest size that stays under CF's 500 KB cap |

Rebuild both from source with:

```sh
python tools/make_logo.py
python tools/pack_refresh.py     # pack/icon.png is indexed, so the hash has to be updated
```

## Rendering the wordmark

Tool: the [Minecraft Title Generator](https://ewanhowell.com/plugins/minecraft-title-generator/)
Blockbench plugin by Ewan Howell (renders are free to use). Same tool Sky Frogs used.

One-click install and open: <https://web.blockbench.net/?plugins=minecraft_title_generator>

Settings used for the shipped wordmark:

| Setting | Value |
|---|---|
| Text | Two texts: `TRASH` and `LANDS` |
| Font | **Minecraft Ten** (the authentic vanilla title font) |
| Text Type / Angle | **Top** for both. Not Top/Bottom - see below |
| Text Row | `TRASH` on row **1**, `LANDS` on row **0** |
| Texture | **Copper** > variant **Oxidised Copper** |
| Overlay | None |
| Camera | Position camera (the plugin's automatic angle) |
| Resolution | **2k** |
| Antialiasing | on |

Then Render > the preview dialog > **Save render**.

**Why Oxidised Copper.** Sky Frogs picked Mangrove because the Wild Update added frogs, so the
texture said something about the pack. Oxidised copper is weathered scrap metal, which is what this
pack is about, and its teal-green is the only option in the set that separates cleanly from the
brown-grey backdrop. Copper (raw) and Mud were both closer to the backdrop's own colour family and
would go muddy at thumbnail size.

**Both rows are type `Top`, on different rows.** The lower row renders larger purely from the
camera's perspective, which is the effect you see in Sky Frogs' wordmark too. `Bottom` is the
smaller "update text" style from the real Minecraft logo and is not what either pack uses.

**Render the two rows as two rows.** Do not render one row and slice it - slicing warps the
per-word perspective, because each row sits at a different depth from the camera.

## A note on the Minecraft EULA

Blockbench shows a one-time **Minecraft EULA** prompt the first time a feature pulls in Minecraft
assets (the font and block textures). It is Blockbench's gate, not the plugin's, and acceptance is
stored per browser profile as `StateMemory.minecraft_eula_accepted` in `localStorage`. A fresh
browser profile will ask again even if you have accepted it before on the same machine.

## Composition

`tools/make_logo.py` does the placement, and only the placement:

1. Square-crops the backdrop (centred by default, `--anchor` shifts it vertically).
2. Trims transparent padding off the wordmark, so placement follows the glyphs rather than whatever
   canvas the renderer emitted.
3. Scales the wordmark to `--width-pct` of the canvas (default 0.90) and centres it horizontally,
   sitting `--bottom-pct` (default 0.06) above the bottom edge.
4. Writes the 512 master, then the CF icon at the largest size under 500 KB.

Tunables if the framing needs to change:

```sh
python tools/make_logo.py --width-pct 0.86 --bottom-pct 0.08 --anchor 0.35
```

## The title screen

FancyMenu takes over `net.minecraft.client.gui.screens.TitleScreen`, configured under
`pack/config/fancymenu/`:

| Path | What |
|---|---|
| `customization/trashlands_title.txt` | the layout, ported from Sky Frogs' `sky_frogs_title.txt` |
| `assets/wordmark.png` | the pack wordmark, currently a copy of `branding/wordmark_two_row.png` |
| `assets/discord_{gray,color}.png`, `github_{gray,color}.png` | the two link buttons, hover pairs |
| `customizablemenus.txt`, `options.txt` | which screens FancyMenu owns, and `modpack_mode` |

Layout, all positions in FancyMenu's anchor space:

- **wordmark** - `top-centered`, 240x125 at (-120, 18)
- **Discord** and **GitHub** buttons - `bottom-right`, 96x23 at (-106, -68) and (-106, -40)
- **the vanilla Minecraft logo** - pushed to `y = -9999` with `stay_on_screen = false`, so it does
  not sit on top of the wordmark. FancyMenu clamps an off-screen element back into view unless
  `stay_on_screen` is off, so both changes are needed.

**The wordmark box is sized for the two-row render, not Sky Frogs'.** Sky Frogs uses a 308x56 box,
which is 5.5:1, matching its single-row 2048x373 wordmark. Ours is `wordmark_two_row.png` at
2048x1068, or 1.918:1, so the box is 240x125 instead. Dropping the two-row image into a 5.5:1 box
squashes it flat.

**A single-row `TRASHLANDS` render would suit a title screen better** and would let the layout use
Sky Frogs' proportions directly. Same tool and settings as above, one text row. Not done yet, and
the two-row version is a reasonable stand-in until it is - do not slice it out of the two-row render.

## Still open

- **CurseForge banner** (512x288) and a **hero shot** (1280x720) are not made. The CF page currently
  runs on the logo plus the gallery screenshots.
- **Title-screen background** - the layout has no custom background, so the vanilla panorama shows
  through. `branding.md` lists a proper panorama as a v1.x item; a static background is the cheaper
  first pass.
- The gallery shots live in the mod's repo (`../recompile/docs/cf image gallery/`). The pack borrows
  them; it does not own a gallery of its own yet.
