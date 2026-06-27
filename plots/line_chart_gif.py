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


def make_line_chart_gif(
    series:   dict[str, list[float]],
    x_labels: list[str] | None = None,
    title:    str  = ">> LINE CHART",
    subtitle: str  = "",
    footer:   str  = "",
    colors:   list | None = None,
    out_path: str  = "line_chart.gif",
    n_frames: int  = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS : dict = {}
) -> list[Image.Image]:

    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    colors = colors or Palette.DEFAULT_CYCLE

    all_vals = [v for vals in series.values() for v in vals]
    y_min, y_max = min(all_vals), max(all_vals)
    y_range  = (y_max - y_min) or 1
    n_points = max(len(v) for v in series.values())

    pad_l, pad_r = 60, 30
    pad_t, pad_b = 55, 60
    plot_w = canvas.W - pad_l - pad_r
    plot_h = canvas.H - pad_t - pad_b

    def to_xy(i: int, val: float) -> tuple[int, int]:
        x = pad_l + int(i / max(n_points - 1, 1) * plot_w)
        y = pad_t + plot_h - int((val - y_min) / y_range * plot_h)
        return x, y

    frames = []
    for f in range(n_frames):
        fr   = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.6))
        n_vis = max(1, int(n_points * prog))

        canvas.draw_header(fr.draw, title, subtitle)

        fr.draw.line([(pad_l, pad_t), (pad_l, pad_t + plot_h)], fill=Palette.WHITE, width=2)
        fr.draw.line([(pad_l, pad_t + plot_h), (pad_l + plot_w, pad_t + plot_h)], fill=Palette.WHITE, width=2)

        for step in range(5):
            yy  = pad_t + int(plot_h * step / 4)
            val = y_max - (y_max - y_min) * step / 4
            fr.draw.line([(pad_l, yy), (pad_l + plot_w, yy)], fill=Palette.GRID, width=1)
            fr.draw.text((4, yy - 6), f"{val:.0f}", font=FONTS["small"], fill=Palette.WHITE)

        if x_labels:
            step = max(1, n_points // 6)
            for i in range(0, n_points, step):
                x, _ = to_xy(i, y_min)
                fr.draw.text((x - 10, pad_t + plot_h + 4), str(x_labels[i])[:6],
                             font=FONTS["small"], fill=Palette.WHITE)

        for s_idx, (name, vals) in enumerate(series.items()):
            col  = colors[s_idx % len(colors)]
            pts  = [to_xy(i, v) for i, v in enumerate(vals[:n_vis])]
            for k in range(1, len(pts)):
                fr.draw.line([pts[k - 1], pts[k]], fill=col, width=2)
            for px, py in pts:
                fr.draw.rectangle([px - 3, py - 3, px + 3, py + 3], fill=col)

        ly = canvas.H - 22
        for s_idx, name in enumerate(series):
            col = colors[s_idx % len(colors)]
            lx2 = pad_l + s_idx * 120
            fr.draw.rectangle([lx2, ly, lx2 + 10, ly + 10], fill=col)
            fr.draw.text((lx2 + 14, ly), name[:14], font=FONTS["small"], fill=col)

        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))

    save_gif(out_path, frames, canvas=canvas)
    return frames