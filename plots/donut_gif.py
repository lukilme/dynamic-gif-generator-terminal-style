import math
import os
import random
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .gif_canvas import GifCanvas
from .constants import Palette
from .util import save_gif

def make_donut_gif(
    labels:   list[str],
    values:   list[float],
    title:    str  = ">> DONUT CHART",
    subtitle: str  = "",
    footer:   str  = "",
    colors:   list | None = None,
    out_path: str  = "donut.gif",
    n_frames: int  = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {}
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    total  = sum(values)
    pcts   = [v / total * 100 for v in values]
    colors = colors or [Palette.for_lang(l, i) for i, l in enumerate(labels)]

    cx, cy = 210, 200
    R, r   = 148, 68
    frames = []

    for f in range(n_frames):
        fr   = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.6))

        canvas.draw_header(fr.draw, title, subtitle)

        angle = -90.0
        for i, (lbl, pct) in enumerate(zip(labels, pcts)):
            sweep  = 360 * (pct / 100) * prog
            col    = colors[i % len(colors)]
            wobble = random.randint(-2, 2) if f % 6 == 0 else 0
            fr.draw.pieslice(
                [cx - R + wobble, cy - R, cx + R + wobble, cy + R],
                start=angle, end=angle + sweep,
                fill=tuple(max(0, c - 60) for c in col), outline=col,
            )
            angle += sweep

        fr.draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=canvas.bg_color, outline=Palette.GRID)
        if prog > 0.8:
            fr.draw.text((cx - 28, cy - 10), f"{total:.0f}", font=FONTS["med"], fill=Palette.WHITE)

        lx, ly = 390, 70
        for i, (lbl, pct) in enumerate(zip(labels, pcts)):
            col = colors[i % len(colors)]
            iy  = ly + i * 38
            fr.draw.rectangle([lx, iy, lx + 14, iy + 14], fill=col)
            fr.draw.text((lx + 18, iy),      lbl[:12],         font=FONTS["small"], fill=Palette.WHITE)
            if prog > 0.5:
                fr.draw.text((lx + 18, iy + 14), f"{pct:.1f}%", font=FONTS["small"], fill=col)

        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))

    save_gif(out_path, frames, canvas=canvas)
    return frames