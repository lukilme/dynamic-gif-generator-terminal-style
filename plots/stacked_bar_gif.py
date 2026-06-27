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

def make_stacked_bar_gif(
    categories: list[str],
    groups: list[str],
    matrix: list[list[float]],
    title: str = ">> STACKED BAR",
    subtitle: str = "",
    footer: str = "",
    colors: list | None = None,
    out_path: str = "stacked.gif",
    n_frames: int = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {}
) -> list[Image.Image]:

    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [7, 14, 21, 28, 35]
    colors = colors or [Palette.for_lang(g, i) for i, g in enumerate(groups)]

    def text_width(draw, text, font):
        box = draw.textbbox((0, 0), text, font=font)
        return box[2] - box[0]

    def fit_text(draw, text, font, max_width):
        if text_width(draw, text, font) <= max_width:
            return text
        ell = "..."
        if text_width(draw, ell, font) > max_width:
            return ""
        s = text
        while s and text_width(draw, s + ell, font) > max_width:
            s = s[:-1]
        return s + ell

    def wrap_two_lines(draw, text, font, max_width):
        words = text.split()
        if not words:
            return [""]
        if len(words) == 1:
            return [fit_text(draw, words[0], font, max_width)]

        line1 = words[0]
        i = 1
        while i < len(words):
            candidate = line1 + " " + words[i]
            if text_width(draw, candidate, font) <= max_width:
                line1 = candidate
                i += 1
            else:
                break

        rest = " ".join(words[i:]).strip()
        if not rest:
            return [fit_text(draw, line1, font, max_width)]

        line2 = fit_text(draw, rest, font, max_width)
        return [fit_text(draw, line1, font, max_width), line2]

    def paginate(items, page_size):
        return [items[i:i + page_size] for i in range(0, len(items), page_size)]

    n_cats = len(categories)
    if n_cats == 0:
        fr = canvas.new_frame()
        canvas.draw_header(fr.draw, title, subtitle)
        canvas.draw_footer(fr.draw, footer)
        frames = [canvas.finish_frame(fr)]
        save_gif(out_path, frames, canvas=canvas)
        return frames

    max_bars_per_page = max(1, (canvas.W - 120) // 110)
    pages_idx = list(range(n_cats))
    pages = paginate(pages_idx, max_bars_per_page)

    frames: list[Image.Image] = []

    for page_no, idxs in enumerate(pages, start=1):
        page_categories = [categories[i] for i in idxs]
        page_matrix = [matrix[i] for i in idxs]

        page_n = len(page_categories)

        bar_w = max(36, min(90, (canvas.W - 120) // max(1, page_n) - 14))
        gap = max(10, (canvas.W - 100 - page_n * bar_w) // (page_n + 1))
        x0 = gap

        header_h = 70
        footer_h = 24
        label_h = 34

        legend_font = FONTS["small"]
        legend_rows = []
        cur_row = []
        cur_w = 0
        max_legend_w = canvas.W - 40
        item_gap = 18

        for j, grp in enumerate(groups):
            swatch_w = 10
            txt = grp
            item_w = swatch_w + 6 + text_width(canvas.new_frame().draw, txt, legend_font) + item_gap
            if cur_row and cur_w + item_w > max_legend_w:
                legend_rows.append(cur_row)
                cur_row = []
                cur_w = 0
            cur_row.append(j)
            cur_w += item_w
        if cur_row:
            legend_rows.append(cur_row)

        legend_h = max(18, len(legend_rows) * 16 + 8)

        y_base = canvas.H - footer_h - legend_h - label_h - 8
        chart_h = y_base - header_h

        totals = [sum(row) or 1 for row in page_matrix]
        normed = [[v / totals[i] * 100 for v in row] for i, row in enumerate(page_matrix)]

        for f in range(n_frames):
            fr = canvas.new_frame()
            prog = min(1.0, f / (n_frames * 0.55))

            page_subtitle = subtitle
            if subtitle:
                page_subtitle += "  •  "
            page_subtitle += f"página {page_no}/{len(pages)}"

            canvas.draw_header(fr.draw, title, page_subtitle)

            fr.draw.line([(x0 - 6, header_h - 5), (x0 - 6, y_base)], fill=Palette.WHITE, width=2)
            fr.draw.line([(x0 - 6, y_base), (canvas.W - 20, y_base)], fill=Palette.WHITE, width=2)

            for pct_lbl in [0, 25, 50, 75, 100]:
                yy = y_base - int(chart_h * pct_lbl / 100)
                fr.draw.line([(x0 - 10, yy), (x0 - 6, yy)], fill=Palette.WHITE)
                fr.draw.text((4, yy - 6), f"{pct_lbl}%", font=FONTS["small"], fill=Palette.WHITE)

            for i, (cat, row) in enumerate(zip(page_categories, normed)):
                bx = x0 + i * (bar_w + gap)
                y_cur = y_base

                for j, pct in enumerate(row):
                    seg_h = int(chart_h * (pct / 100) * prog)
                    if seg_h <= 0:
                        continue

                    col = colors[j % len(colors)]

                    for by in range(0, seg_h, 6):
                        shade = tuple(max(0, c - random.randint(0, 40)) for c in col)
                        fr.draw.rectangle([bx, y_cur - by - 6, bx + bar_w, y_cur - by], fill=shade)

                    fr.draw.rectangle([bx, y_cur - seg_h, bx + bar_w, y_cur], outline=col, width=1)
                    y_cur -= seg_h

                max_label_w = bar_w + 10
                lines = wrap_two_lines(fr.draw, cat, FONTS["small"], max_label_w)
                if len(lines) > 2:
                    lines = lines[:2]

                if len(lines) == 1:
                    tx = bx + (bar_w // 2) - (text_width(fr.draw, lines[0], FONTS["small"]) // 2)
                    fr.draw.text((tx, y_base + 4), lines[0], font=FONTS["small"], fill=Palette.CYAN)
                else:
                    line1, line2 = lines[0], lines[1]
                    tx1 = bx + (bar_w // 2) - (text_width(fr.draw, line1, FONTS["small"]) // 2)
                    tx2 = bx + (bar_w // 2) - (text_width(fr.draw, line2, FONTS["small"]) // 2)
                    fr.draw.text((tx1, y_base + 2), line1, font=FONTS["small"], fill=Palette.CYAN)
                    fr.draw.text((tx2, y_base + 13), line2, font=FONTS["small"], fill=Palette.CYAN)

            ly = canvas.H - footer_h - legend_h + 2
            row_x = 20
            for row in legend_rows:
                row_x = 20
                for j in row:
                    grp = groups[j]
                    col = colors[j % len(colors)]
                    txt = fit_text(fr.draw, grp, legend_font, 120)

                    item_w = 10 + 6 + text_width(fr.draw, txt, legend_font) + item_gap
                    if row_x + item_w > canvas.W - 20:
                        break

                    fr.draw.rectangle([row_x, ly + 3, row_x + 10, ly + 13], fill=col)
                    fr.draw.text((row_x + 16, ly + 1), txt, font=legend_font, fill=col)
                    row_x += item_w
                ly += 16

            canvas.draw_footer(fr.draw, footer)

            frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))

    save_gif(out_path, frames, canvas=canvas)
    return frames