#!/usr/bin/env python3
"""Renders a light+dark color-swatch strip PNG per family into
swatches/<family>.png, for the READMEs of this repo and any consumer
repo (dotfiles) that wants a visual preview instead of just hex codes.
Re-run after any palette edit to keep the images in sync -- generated,
never hand-edited.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PALETTES_DIR = Path(__file__).parent / "palettes"
OUT_DIR = Path(__file__).parent / "swatches"

_KEYS = ("bg", "fg", "button_bg", "select_bg", "highlight_bg", "muted_fg")
_LABELS = {"bg": "bg", "fg": "fg", "button_bg": "button", "select_bg": "select",
           "highlight_bg": "highlt", "muted_fg": "muted"}
_SWATCH = 72
_LABEL_H = 18
_PAD = 8
_MODE_COL_W = 44


def _font():
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(path).exists():
            return ImageFont.truetype(path, 13)
    return ImageFont.load_default()


def render_family(family: str, data: dict) -> Image.Image:
    font = _font()
    modes = [m for m in ("light", "dark") if m in data]
    width = _MODE_COL_W + _PAD + len(_KEYS) * (_SWATCH + _PAD)
    row_h = _SWATCH + _LABEL_H + _PAD
    height = _PAD + len(modes) * row_h
    img = Image.new("RGB", (width, height), "#ffffff")
    draw = ImageDraw.Draw(img)

    for row, mode in enumerate(modes):
        palette = data[mode]
        y0 = _PAD + row * row_h
        mid_y = y0 + _SWATCH // 2
        draw.text((_PAD, mid_y - 6), mode, fill="#000000", font=font)
        for col, key in enumerate(_KEYS):
            x0 = _MODE_COL_W + _PAD + col * (_SWATCH + _PAD)
            hexval = palette.get(key, "#808080")
            draw.rectangle([x0, y0, x0 + _SWATCH, y0 + _SWATCH], fill=hexval, outline="#999999")
            draw.text((x0, y0 + _SWATCH + 2), _LABELS[key], fill="#333333", font=font)
    return img


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for json_path in sorted(PALETTES_DIR.glob("*.json")):
        family = json_path.stem
        data = json.loads(json_path.read_text())
        img = render_family(family, data)
        out_path = OUT_DIR / f"{family}.png"
        img.save(out_path)
        print(f"{json_path.name} -> {out_path.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()
