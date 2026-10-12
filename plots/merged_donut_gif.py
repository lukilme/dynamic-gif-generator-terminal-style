import random

from PIL import Image

from .constants import Palette
from .gif_canvas import GifCanvas
from .util import save_gif


def make_line_gif(
    labels: list[str],
    values: list[float],
    title: str = ">> LINE CHART",
    subtitle: str = "",
    footer: str = "",
    color: tuple | None = None,
    out_path: str = "line.gif",
    n_frames: int = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {},
) -> list[Image.Image]:
    canvas = canvas or GifCanvas(fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]
    color = color or Palette.for_lang(labels[0] if labels else "line", 0)
    max_val = max(values) if values else 1
    min_val = min(values) if values else 0
    span = max(max_val - min_val, 1e-6)
    ox, oy = 60, 320
    chart_w, chart_h = 420, 220
    n_pts = len(values)
    step = chart_w / max(n_pts - 1, 1)
    frames = []
    pts_all = [
        (ox + i * step, oy - ((v - min_val) / span) * chart_h)
        for i, v in enumerate(values)
    ]
    for f in range(n_frames):
        fr = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.7))
        canvas.draw_header(fr.draw, title, subtitle)
        fr.draw.line([ox, oy, ox + chart_w, oy], fill=Palette.GRID)
        fr.draw.line([ox, oy - chart_h, ox, oy], fill=Palette.GRID)
        n_visible = max(2, int(n_pts * prog))
        visible = pts_all[:n_visible]
        wobble = random.randint(-2, 2) if f % 6 == 0 else 0
        vis_wobbled = [(x + wobble, y) for x, y in visible]
        if len(vis_wobbled) > 1:
            fr.draw.line(vis_wobbled, fill=color, width=3, joint="curve")
        for i, (x, y) in enumerate(vis_wobbled):
            fr.draw.ellipse(
                [x - 4, y - 4, x + 4, y + 4], fill=color, outline=Palette.WHITE
            )
        if prog > 0.6:
            for i, lbl in enumerate(labels):
                if i < len(pts_all):
                    lx = pts_all[i][0]
                    fr.draw.text(
                        (lx - 10, oy + 6),
                        lbl[:6],
                        font=FONTS["small"],
                        fill=Palette.WHITE,
                    )
        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))
    save_gif(out_path, frames, canvas=canvas)
    return frames
