from __future__ import annotations

import os
import random

from PIL import Image, ImageFont

from .gif_canvas import GifCanvas


def save_gif(
    path: str,
    frames: list[Image.Image],
    duration: int = 80,
    loop: int = 0,
    hold_last: int = 8,
    canvas: GifCanvas | None = None,
    glitch_hold: bool = True,
):

    all_frames = list(frames)
    last = frames[-1]
    for _ in range(hold_last):
        if glitch_hold and canvas and random.random() < 0.4:
            all_frames.append(canvas.apply_glitch(last, intensity=0.04))
        else:
            all_frames.append(last)

    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    all_frames[0].save(
        path,
        save_all=True,
        append_images=all_frames[1:],
        loop=loop,
        duration=duration,
    )
    print(f"{path}  ({len(all_frames)} frames)")


def load_fonts() -> dict:
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
    ]
    bold = next((p for p in paths[::2] if os.path.exists(p)), None)
    reg = next((p for p in paths[1::2] if os.path.exists(p)), None) or bold

    def _f(path, size):
        try:
            return ImageFont.truetype(path, size) if path else ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()

    return {
        "big": _f(bold, 18),
        "med": _f(bold, 13),
        "small": _f(reg, 11),
    }
