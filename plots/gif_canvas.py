from __future__ import annotations
import math
import os
import random
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from  .constants import Palette

@dataclass
class Frame:
    img: Image.Image
    draw: ImageDraw.ImageDraw

class GifCanvas:
    def __init__(
        self,
        width: int = 640,
        height: int = 400,
        bg_color: tuple = Palette.BG,
        grid_color: tuple = Palette.GRID,
        grid_step: int = 20,
        scanline_alpha: int = 40,
        glitch_intensity: float = 0.18,
        fonts: dict = {}
    ):
        self.W = width
        self.H = height
        self.bg_color = bg_color
        self.grid_color = grid_color
        self.grid_step = grid_step
        self.glitch_intensity = glitch_intensity
        self.FONTS = fonts
        self._scanlines = (
            self._make_scanlines(scanline_alpha) if scanline_alpha else None
        )

    def _make_scanlines(self, alpha: int) -> Image.Image:
        ov = Image.new("RGBA", (self.W, self.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for y in range(0, self.H, 4):
            d.line([(0, y), (self.W, y)], fill=(0, 0, 0, alpha))
        return ov

    def _draw_grid(self, draw: ImageDraw.ImageDraw):
        if not self.grid_color:
            return
        # for x in range(0, self.W, self.grid_step):
        #     draw.line([(x, 0), (x, self.H)], fill=self.grid_color, width=0)
        # for y in range(0, self.H, self.grid_step):
        #     draw.line([(0, y), (self.W, y)], fill=self.grid_color, width=0)

    def new_frame(self) -> Frame:
        img = Image.new("RGB", (self.W, self.H), self.bg_color)
        draw = ImageDraw.Draw(img)
        self._draw_grid(draw)
        return Frame(img, draw)

    def apply_scanlines(self, img: Image.Image) -> Image.Image:
        if not self._scanlines:
            return img
        rgba = Image.alpha_composite(img.convert("RGBA"), self._scanlines)
        return rgba.convert("RGB")

    def apply_glitch(
        self, img: Image.Image, intensity: float | None = None
    ) -> Image.Image:
        intensity = intensity if intensity is not None else self.glitch_intensity
        arr = np.array(img)
        out = arr.copy()
        for _ in range(random.randint(3, 10)):
            y0 = random.randint(0, self.H - 1)
            h = random.randint(1, max(2, int(self.H * 0.06)))
            y1 = min(y0 + h, self.H)
            shift = random.randint(-int(self.W * intensity), int(self.W * intensity))
            out[y0:y1] = np.roll(arr[y0:y1], shift, axis=1)
        if random.random() < 0.5:
            ch = random.randint(0, 2)
            shift = random.randint(-6, 6)
            out[:, :, ch] = np.roll(out[:, :, ch], shift, axis=1)
        return Image.fromarray(out.astype(np.uint8))

    def finish_frame(
        self,
        frame: Frame,
        glitch: bool = False,
        glitch_intensity: float | None = None,
    ) -> Image.Image:
        img = self.apply_scanlines(frame.img)
        if glitch:
            img = self.apply_glitch(img, glitch_intensity)
        return img

    def draw_header(
        self,
        draw: ImageDraw.ImageDraw,
        title: str,
        sub: str = "",
        title_color: tuple = Palette.CYAN,
        sub_color: tuple = Palette.MAGENTA,
    ):
        draw.text((20, 14), title, font=self.FONTS["big"], fill=title_color)
        if sub:
            draw.text(
                (self.W - len(sub) * 8 - 20, 14), sub, font=self.FONTS["med"], fill=sub_color
            )

    def draw_footer(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        color: tuple = Palette.YELLOW,
        line_color: tuple = Palette.CYAN,
    ):
        draw.line([(0, self.H - 24), (self.W, self.H - 24)], fill=line_color, width=1)
        draw.text((20, self.H - 18), text, font=self.FONTS["small"], fill=color)

    def draw_pixelated_bar(
        self,
        draw: ImageDraw.ImageDraw,
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        fill: tuple,
        block_w: int = 8,
        noise: int = 30,
    ):
        for bx in range(x0, x1, block_w):
            shade = tuple(max(0, c - random.randint(0, noise)) for c in fill)
            draw.rectangle([bx, y0, min(bx + block_w - 1, x1), y1], fill=shade)
        if x1 > x0 + 3:
            draw.rectangle([x1 - 3, y0, x1, y1], fill=Palette.WHITE)