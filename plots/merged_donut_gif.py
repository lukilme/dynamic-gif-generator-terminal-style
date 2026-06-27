from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from plots.util import load_fonts
from plots.gif_canvas import GifCanvas
from plots.constants import Palette
from plots.util import save_gif

def make_merged_donut_gif(
    repos:    list[dict],
    title:    str  = ">> LANGUAGES · ALL REPOS",
    subtitle: str  = "",
    footer:   str  = "",
    out_path: str  = "all_langs_merged.gif",
    n_frames: int  = 44,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {}
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32, 40]
 
    merged: dict[str, float] = {}
    for r in repos:
        for lang, pct in r["languages_percent"].items():
            merged[lang] = merged.get(lang, 0) + r["total_code_bytes"] * (pct / 100)
 
    merged = dict(sorted(merged.items(), key=lambda x: -x[1]))
    langs  = list(merged.keys())
    bytes_ = list(merged.values())
    total  = sum(bytes_)
    pcts   = [b / total * 100 for b in bytes_]
    colors = [Palette.for_lang(l, i) for i, l in enumerate(langs)]
 
    cx, cy = 200, 210
    R, r   = 155, 65
    frames = []
 
    for f in range(n_frames):
        fr   = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.55))
 
        canvas.draw_header(fr.draw, title, subtitle or f"repos: {len(repos)}",
                           title_color=Palette.YELLOW)
 
        angle = -90.0
        for i, (lang, pct) in enumerate(zip(langs, pcts)):
            sweep  = 360 * (pct / 100) * prog
            col    = colors[i]
            wobble = random.randint(-2, 2) if f % 6 == 0 else 0
            fr.draw.pieslice(
                [cx - R + wobble, cy - R, cx + R + wobble, cy + R],
                start=angle, end=angle + sweep,
                fill=tuple(max(0, c - 55) for c in col),
                outline=col, width=2,
            )
            angle += sweep
 
        fr.draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                        fill=canvas.bg_color, outline=Palette.GRID, width=2)
        if prog > 0.85:
            total_kb = total / 1024
            label = f"{total_kb:.1f}k" if total_kb < 1000 else f"{total_kb/1024:.1f}M"
            fr.draw.text((cx - 26, cy - 16), label,   font=FONTS["med"],   fill=Palette.WHITE)
            fr.draw.text((cx - 20, cy +  2), "bytes", font=FONTS["small"], fill=Palette.GRID)
 
        lx, ly  = 385, 55
        row_h   = max(30, min(38, (canvas.H - 90) // len(langs)))
        bar_max = canvas.W - lx - 60
 
        for i, (lang, pct, b) in enumerate(zip(langs, pcts, bytes_)):
            col = colors[i]
            iy  = ly + i * row_h
            if iy + row_h > canvas.H - 35:
                break
 
            fr.draw.rectangle([lx, iy, lx + 12, iy + 12], fill=col)
            fr.draw.text((lx + 18, iy), lang, font=FONTS["small"], fill=Palette.WHITE)
 
            bw = int(bar_max * (pct / max(pcts)) * prog)
            fr.draw.rectangle([lx + 18, iy + 15, lx + 18 + bar_max, iy + 22],
                               outline=Palette.GRID, width=1)
            if bw > 0:
                fr.draw.rectangle([lx + 18, iy + 16, lx + 18 + bw, iy + 21], fill=col)
 
            if prog > 0.4:
                fr.draw.text((lx + 18 + bar_max + 4, iy + 13),
                             f"{pct:.1f}%", font=FONTS["small"], fill=col)
 
        canvas.draw_footer(
            fr.draw,
            footer or f"{len(repos)} repos  ·  {int(total):,} bytes  ·  {len(langs)} languages",
            line_color=Palette.YELLOW,
        )
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))
 
    save_gif(out_path, frames, canvas=canvas)
    return frames