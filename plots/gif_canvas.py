from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

from .constants import Palette


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
        fonts: dict = {},
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
        self._matrix_enabled = True
        self._matrix_cycle = 32
        self._matrix_step = 0
        self._matrix_speed = 1
        self._matrix_density = 1.0
        self._matrix_glow = 1.0
        self._matrix_seed = 7
        self._matrix_columns = self._build_matrix_columns()

    def configure_matrix(
        self,
        enabled: bool | None = None,
        cycle: int | None = None,
        speed: int | None = None,
        density: float | None = None,
        glow: float | None = None,
        seed: int | None = None,
    ) -> None:
        if enabled is not None:
            self._matrix_enabled = enabled
        if cycle is not None:
            self._matrix_cycle = max(8, int(cycle))
        if speed is not None:
            self._matrix_speed = max(1, int(speed))
        if density is not None:
            self._matrix_density = max(0.4, float(density))
        if glow is not None:
            self._matrix_glow = max(0.4, float(glow))
        if seed is not None:
            self._matrix_seed = seed
            self._matrix_columns = self._build_matrix_columns()

    def _build_matrix_columns(self):
        columns = []
        step = max(8, int(16 / self._matrix_density))
        rng = random.Random(self._matrix_seed)
        for x in range(0, self.W, step):
            row_offsets = []
            for _ in range(rng.randint(8, 18)):
                row_offsets.append(rng.randint(0, self.H + 28))
            columns.append((x, tuple(sorted(row_offsets))))
        return columns

    def _draw_matrix_rain(self, draw: ImageDraw.ImageDraw, phase: int):
        if not self._matrix_enabled:
            return
        for x, rows in self._matrix_columns:
            for idx, base_y in enumerate(rows):
                y = (base_y + phase * self._matrix_speed + idx * 2) % (self.H + 50)
                if y < self.H:
                    glow = int((90 + (idx % 6) * 18) * self._matrix_glow)
                    color = (10, max(80, glow), 34)
                    draw.point((x, y), fill=color)
                    if idx % 2 == 0:
                        draw.point((x + 1, y), fill=(40, min(255, int(170 * self._matrix_glow)), 90))
                    if idx % 3 == 0:
                        draw.point((x, max(0, y - 1)), fill=(110, 255, 180))

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

    def _apply_bg_texture(self, draw: ImageDraw.ImageDraw):
        for x in range(0, self.W, 24):
            for y in range(0, self.H, 24):
                if (x // 24 + y // 24) % 2 == 0:
                    draw.rectangle(
                        [x, y, x + 12, y + 12],
                        fill=(18, 18, 35),
                    )
                else:
                    draw.rectangle(
                        [x + 8, y + 8, x + 20, y + 20],
                        fill=(12, 28, 52),
                    )

        for x in range(0, self.W, 70):
            draw.line([(x, 0), (x, self.H)], fill=(20, 255, 240, 30), width=1)

    def new_frame(self) -> Frame:
        img = Image.new("RGB", (self.W, self.H), self.bg_color)
        draw = ImageDraw.Draw(img)
        phase = self._matrix_step % self._matrix_cycle
        self._apply_bg_texture(draw)
        if self._matrix_enabled:
            self._draw_matrix_rain(draw, phase)
        self._draw_grid(draw)
        self._matrix_step = (self._matrix_step + 1) % self._matrix_cycle
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
                (self.W - len(sub) * 8 - 20, 14),
                sub,
                font=self.FONTS["med"],
                fill=sub_color,
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
