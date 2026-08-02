#!/usr/bin/env python3
"""Composite the pack logo: a Minecraft Title Generator wordmark over a backdrop.

Mirrors how Sky Frogs' logo was built (`../sky-frogs/docs/branding.md`): the
wordmark is a real 3D render from the Minecraft Title Generator Blockbench
plugin, and this script only places it. Nothing here is AI-generated art, which
is the maintainer rule - the render comes from the plugin, the backdrop is an
in-game screenshot, and the composite is deterministic.

Render the wordmark first (see docs/branding.md for the exact settings):
    Blockbench > Minecraft Title Generator > two text rows, "TRASH" / "LANDS"
    > font Minecraft Ten > 2k render > antialiasing on > Save render

Then:
    python tools/make_logo.py --wordmark branding/wordmark_two_row.png

Outputs `branding/logo.png` (512 master) and `pack/icon.png` (the CurseForge
logo). CurseForge rejects a logo over 500 KB, so the icon is emitted at the
largest size that stays under the ceiling, and the script says which size it
picked and why.

A two-row wordmark must be RENDERED as two rows, not sliced out of a one-row
render - slicing warps the per-word perspective, which is why Sky Frogs keeps a
separate `wordmark_two_row.png`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python -m pip install Pillow")

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
CF_LOGO_MAX_BYTES = 500 * 1024


def square_crop(img: Image.Image, anchor: float) -> Image.Image:
    """Center-weighted square crop. `anchor` is 0.0 (top) to 1.0 (bottom)."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = int(round((h - side) * anchor))
    return img.crop((left, top, left + side, top + side))


def build(background: Path, wordmark: Path, size: int,
          width_pct: float, bottom_pct: float, anchor: float) -> Image.Image:
    bg = Image.open(background).convert("RGBA")
    bg = square_crop(bg, anchor).resize((size, size), Image.LANCZOS)

    wm = Image.open(wordmark).convert("RGBA")
    # Trim transparent padding so placement is driven by the glyphs, not by
    # whatever canvas the renderer happened to emit.
    bbox = wm.getbbox()
    if bbox:
        wm = wm.crop(bbox)

    target_w = int(size * width_pct)
    scale = target_w / wm.width
    wm = wm.resize((target_w, max(1, int(round(wm.height * scale)))), Image.LANCZOS)

    x = (size - wm.width) // 2
    y = size - wm.height - int(size * bottom_pct)
    if y < 0:
        print(f"  note: wordmark is taller than the space; clamping to top "
              f"(try a smaller --width-pct than {width_pct})")
        y = 0

    out = bg.copy()
    out.alpha_composite(wm, (x, y))
    return out


def save_under_ceiling(img: Image.Image, path: Path, sizes: list[int]) -> None:
    """Write the largest of `sizes` that stays under CurseForge's 500 KB logo cap."""
    for candidate in sizes:
        resized = img.resize((candidate, candidate), Image.LANCZOS).convert("RGB")
        path.parent.mkdir(parents=True, exist_ok=True)
        resized.save(path, optimize=True)
        n = path.stat().st_size
        if n <= CF_LOGO_MAX_BYTES:
            print(f"  wrote {path.relative_to(REPO)}  {candidate}x{candidate}  {n // 1024} KB")
            return
        print(f"  {candidate}x{candidate} is {n // 1024} KB, over the 500 KB CurseForge cap; "
              f"trying smaller")
    sys.exit(f"could not get {path.name} under {CF_LOGO_MAX_BYTES // 1024} KB at any size")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--wordmark", default="branding/wordmark_two_row.png",
                   help="transparent PNG from the Minecraft Title Generator")
    p.add_argument("--background", default="branding/backdrop.jpg",
                   help="backdrop image (an in-game screenshot)")
    p.add_argument("--master", default="branding/logo.png", help="512 master output")
    p.add_argument("--icon", default="pack/icon.png", help="CurseForge logo output")
    p.add_argument("--width-pct", type=float, default=0.90,
                   help="wordmark width as a fraction of the canvas (default 0.90)")
    p.add_argument("--bottom-pct", type=float, default=0.06,
                   help="gap below the wordmark as a fraction of the canvas (default 0.06)")
    p.add_argument("--anchor", type=float, default=0.5,
                   help="vertical crop anchor of the backdrop, 0 top to 1 bottom (default 0.5)")
    args = p.parse_args()

    wordmark = (REPO / args.wordmark).resolve()
    background = (REPO / args.background).resolve()
    for label, path in (("wordmark", wordmark), ("background", background)):
        if not path.is_file():
            sys.exit(f"{label} not found: {path}\nSee docs/branding.md for how to produce it.")

    composed = build(background, wordmark, 512,
                     args.width_pct, args.bottom_pct, args.anchor)

    master = REPO / args.master
    master.parent.mkdir(parents=True, exist_ok=True)
    # Flatten to RGB. The backdrop is opaque, so the composite's alpha channel is
    # uniformly 255 - it carries no information and costs ~40 KB in a committed asset.
    composed.convert("RGB").save(master, optimize=True)
    print(f"  wrote {master.relative_to(REPO)}  512x512  {master.stat().st_size // 1024} KB")

    save_under_ceiling(composed, REPO / args.icon, [512, 400, 320, 256, 192])

    print("\nRemember to run `python tools/pack_refresh.py` - pack/icon.png is indexed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
