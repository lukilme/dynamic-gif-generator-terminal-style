import random

from PIL import Image

from .constants import Palette
from .gif_canvas import GifCanvas
from .util import save_gif


def make_gauge_gif(
    value: float,
    max_value: float = 100,
    title: str = ">> TOTAL CODE BYTES",
    subtitle: str = "",
    label: str = "",
    footer: str = "",
    color: tuple | None = None,
    out_path: str = "gauge.gif",
    n_frames: int = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {},
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    color = color or Palette.CYAN
    value = max(0.0, min(float(value), float(max_value)))
    frames = []
    cx, cy = 220, 190
    radius = 130
    start_angle = 210
    end_angle = 330

    for f in range(n_frames):
        fr = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.8))
        visible_ratio = (value / max_value) * prog if max_value else 0.0
        sweep = 300 * visible_ratio

        canvas.draw_header(fr.draw, title, subtitle)
        fr.draw.arc(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            start=start_angle,
            end=start_angle + sweep,
            fill=color,
            width=20,
        )
        fr.draw.ellipse(
            [cx - 52, cy - 52, cx + 52, cy + 52],
            fill=canvas.bg_color,
            outline=Palette.GRID,
        )
        fr.draw.text(
            (cx - 45, cy - 10),
            label or f"{int(value * prog):,}",
            font=FONTS.get("med", FONTS.get("small")),
            fill=color,
        )
        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))

    save_gif(out_path, frames, canvas=canvas)
    return frames


def make_donut_gif(
    labels: list[str],
    values: list[float],
    title: str = ">> DONUT CHART",
    subtitle: str = "",
    footer: str = "",
    colors: list | None = None,
    out_path: str = "donut.gif",
    n_frames: int = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {},
) -> list[Image.Image]:
    return make_gauge_gif(
        value=sum(values),
        max_value=max(sum(values), 1),
        title=title,
        subtitle=subtitle,
        label=f"{sum(values):,.0f}",
        footer=footer,
        color=colors[0] if colors else Palette.CYAN,
        out_path=out_path,
        n_frames=n_frames,
        glitch_frames=glitch_frames,
        canvas=canvas,
        FONTS=FONTS,
    )
