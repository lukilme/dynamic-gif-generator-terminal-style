import random

from PIL import Image

from .constants import Palette
from .gif_canvas import GifCanvas
from .util import save_gif


def make_progress_race_gif(
    labels: list[str],
    values: list[float],
    title: str = ">> PROGRESS RACE",
    subtitle: str = "",
    footer: str = "",
    colors: list | None = None,
    out_path: str = "progress.gif",
    n_frames: int = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {},
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    colors = colors or [Palette.for_lang(l, i) for i, l in enumerate(labels)]
    max_val = max(values) if values else 1
    ox, oy = 60, 90
    bar_w = 340
    bar_h = 24
    gap = 44
    frames = []
    for f in range(n_frames):
        fr = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.7))
        canvas.draw_header(fr.draw, title, subtitle)
        y = oy
        for i, (lbl, val) in enumerate(zip(labels, values)):
            col = colors[i % len(colors)]
            wobble = random.randint(-1, 1) if f % 6 == 0 else 0
            fill_w = max(0.0, (val / max_val) * bar_w * prog)
            fill_end = max(ox, ox + fill_w + wobble)
            fr.draw.rectangle([ox, y, ox + bar_w, y + bar_h], outline=Palette.GRID)
            fr.draw.rectangle(
                [ox, y, fill_end, y + bar_h],
                fill=tuple(max(0, c - 60) for c in col),
            )
            fr.draw.text(
                (ox, y - 16), lbl[:16], font=FONTS["small"], fill=Palette.WHITE
            )
            if prog > 0.5:
                fr.draw.text(
                    (ox + bar_w + 10, y + 3),
                    f"{val:.0f}",
                    font=FONTS["small"],
                    fill=col,
                )
            y += gap
        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))
    save_gif(out_path, frames, canvas=canvas)
    return frames
