import random

from PIL import Image

from .constants import Palette
from .gif_canvas import GifCanvas
from .util import save_gif


def make_merged_donut_gif(
    repos: list[dict],
    title: str = ">> LANGUAGES · ALL REPOS",
    subtitle: str = "",
    footer: str = "",
    out_path: str = "all_langs_merged.gif",
    n_frames: int = 40,
    glitch_frames: list[int] | None = None,
    canvas: GifCanvas | None = None,
    FONTS: dict = {},
) -> list[Image.Image]:
    from .donut_gif import make_donut_gif

    all_langs = sorted({lang for repo in repos for lang in repo["languages_percent"]})
    values = [
        sum(float(repo["languages_percent"].get(lang, 0)) for repo in repos)
        for lang in all_langs
    ]
    return make_donut_gif(
        labels=all_langs,
        values=values,
        title=title,
        subtitle=subtitle,
        footer=footer,
        out_path=out_path,
        n_frames=n_frames,
        glitch_frames=glitch_frames,
        canvas=canvas,
        FONTS=FONTS,
    )


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
    return make_merged_donut_gif(
        repos=[{"languages_percent": dict(zip(labels, values))}],
        title=title,
        subtitle=subtitle,
        footer=footer,
        out_path=out_path,
        n_frames=n_frames,
        glitch_frames=glitch_frames,
        canvas=canvas,
        FONTS=FONTS,
    )
