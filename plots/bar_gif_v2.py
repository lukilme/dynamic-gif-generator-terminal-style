import random

from PIL import Image

from .constants import Palette
from .gif_canvas import GifCanvas
from .util import save_gif


def make_bar_gif(
    labels: list[str],
    values: list[float],
    title: str = ">> BAR CHART",
    subtitle: str = "",
    footer: str = "",
    colors: list | None = None,
    out_path: str = "bar.gif",
    n_frames: int = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {},
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    colors = colors or [Palette.for_lang(l, i) for i, l in enumerate(labels)]
    max_val = max(values) if values else 1
    ox, oy = 60, 320
    chart_w, chart_h = 420, 220
    n_bars = len(values)
    gap = 18
    bar_w = (chart_w - gap * (n_bars - 1)) / n_bars if n_bars else chart_w
    frames = []
    for f in range(n_frames):
        fr = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.6))
        canvas.draw_header(fr.draw, title, subtitle)
        fr.draw.line([ox, oy, ox + chart_w, oy], fill=Palette.GRID)
        x = ox
        for i, (lbl, val) in enumerate(zip(labels, values)):
            col = colors[i % len(colors)]
            wobble = random.randint(-2, 2) if f % 6 == 0 else 0
            bar_h = (val / max_val) * chart_h * prog
            top = oy - bar_h
            fr.draw.rectangle(
                [x + wobble, top, x + bar_w + wobble, oy],
                fill=tuple(max(0, c - 60) for c in col),
                outline=col,
            )
            if prog > 0.5:
                fr.draw.text((x, top - 16), f"{val:.0f}", font=FONTS["small"], fill=col)
            fr.draw.text((x, oy + 6), lbl[:8], font=FONTS["small"], fill=Palette.WHITE)
            x += bar_w + gap
        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))
    save_gif(out_path, frames, canvas=canvas)
    return frames
