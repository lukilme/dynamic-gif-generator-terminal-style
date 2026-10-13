import random

from PIL import Image, ImageDraw

from .constants import Palette
from .gif_canvas import GifCanvas
from .util import save_gif


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
    canvas = canvas or GifCanvas(width=1000, height=520, fonts=FONTS)
    glitch_frames = glitch_frames or [8, 16, 24, 32]

    if not labels or not values:
        return []

    total = sum(values)
    pcts = [v / total * 100 for v in values] if total else [0.0 for _ in labels]
    colors = colors or [Palette.for_lang(l, i) for i, l in enumerate(labels)]

    split_at = max(1, len(labels) // 2)
    left_labels = labels[:split_at]
    right_labels = labels[split_at:]
    left_values = pcts[:split_at]
    right_values = pcts[split_at:]

    cx, cy = canvas.W // 2, canvas.H // 2 + 8
    R, r = 188, 82
    frames = []

    for f in range(n_frames):
        fr = canvas.new_frame()
        prog = min(1.0, f / (n_frames * 0.6))

        canvas.draw_header(fr.draw, title, subtitle)

        angle = -90.0
        for i, pct in enumerate(pcts):
            sweep = 360 * (pct / 100) * prog
            col = colors[i % len(colors)]
            wobble = random.randint(-2, 2) if f % 6 == 0 else 0
            fr.draw.pieslice(
                [cx - R + wobble, cy - R, cx + R + wobble, cy + R],
                start=angle,
                end=angle + sweep,
                fill=tuple(max(0, c - 55) for c in col),
                outline=col,
                width=2,
            )
            angle += sweep

        inner_glow = Image.new("RGBA", (canvas.W, canvas.H), (0, 0, 0, 0))
        idraw = ImageDraw.Draw(inner_glow)
        idraw.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], fill=(20, 35, 52, 140))
        fr.img = Image.alpha_composite(fr.img.convert("RGBA"), inner_glow).convert("RGB")
        fr.draw = ImageDraw.Draw(fr.img)

        fr.draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(10, 16, 26),
            outline=(20, 255, 240),
            width=2,
        )
        if prog > 0.8:
            fr.draw.text(
                (cx - 40, cy - 12),
                f"{total:.0f}",
                font=FONTS["med"],
                fill=Palette.WHITE,
            )

        def draw_legend(x_start: int, dataset: list[tuple[str, float]]):
            y_start = 72
            for i, (lbl, pct) in enumerate(dataset):
                col = colors[labels.index(lbl) % len(colors)]
                iy = y_start + i * 30
                if iy > canvas.H - 80:
                    break

                panel = [x_start - 10, iy - 4, x_start + 240, iy + 22]
                fr.draw.rounded_rectangle(
                    panel,
                    radius=8,
                    fill=(28, 30, 36),
                    outline=tuple(max(0, c - 20) for c in col),
                    width=1,
                )
                fr.draw.rectangle([x_start, iy, x_start + 16, iy + 16], fill=col)
                fr.draw.text(
                    (x_start + 26, iy + 3),
                    lbl[:16],
                    font=FONTS["med"],
                    fill=Palette.WHITE,
                    stroke_width=1,
                    stroke_fill=tuple(max(0, c - 40) for c in col),
                )
                if prog > 0.45:
                    fr.draw.text(
                        (x_start + 170, iy + 3),
                        f"{pct:.1f}%",
                        font=FONTS["med"],
                        fill=col,
                        stroke_width=1,
                        stroke_fill=(15, 15, 15),
                    )

        draw_legend(54, list(zip(left_labels, left_values)))
        draw_legend(canvas.W - 290, list(zip(right_labels, right_values)))

        canvas.draw_footer(fr.draw, footer)
        frames.append(canvas.finish_frame(fr, glitch=(f in glitch_frames)))

    save_gif(out_path, frames, canvas=canvas)
    return frames
