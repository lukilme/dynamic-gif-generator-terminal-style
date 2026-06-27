from __future__ import annotations
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


def make_bar_chart_gif(
    labels: list[str],
    values: list[float],
    title: str = ">> BAR CHART",
    subtitle: str = "",
    footer: str = "",
    colors: list | None = None,
    out_path: str = "bar_chart.gif",
    n_frames: int = 36,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {},
) -> list[Image.Image]:

    canvas = canvas or GifCanvas(fonts=FONTS)
    colors = colors or Palette.DEFAULT_CYCLE
    glitch_frames = glitch_frames or [6, 12, 18, 24, 30]

    max_val = max(values) or 1
    margin_l = 220
    margin_r = 50
    bar_area = canvas.W - margin_l - margin_r
    row_h = max(40, (canvas.H - 100) // len(labels))
    y_start = 60
    frames = []

    for f in range(n_frames):
        fr = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.5))

        canvas.draw_header(fr.draw, title, subtitle)

        for i, (lbl, val) in enumerate(zip(labels, values)):
            y = y_start + i * row_h
            col = colors[i % len(colors)]

            short = (lbl[:22] + "..") if len(lbl) > 24 else lbl
            fr.draw.text((18, y + 8), short, font=FONTS["small"], fill=Palette.WHITE)

            fr.draw.rectangle(
                [margin_l, y + 4, margin_l + bar_area, y + row_h - 8],
                outline=Palette.GRID,
                width=1,
            )

            bar_w = int(bar_area * (val / max_val) * prog)
            if bar_w > 0:
                canvas.draw_pixelated_bar(
                    fr.draw, margin_l, y + 5, margin_l + bar_w, y + row_h - 9, col
                )

            if prog > 0.3 and bar_w > 0:
                fr.draw.text(
                    (margin_l + bar_w + 6, y + 10),
                    f"{val:,.0f}",
                    font=FONTS["small"],
                    fill=col,
                )

        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))

    save_gif(out_path, frames, canvas=canvas)
    return frames