from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from plots.util import load_fonts
from plots.constants import Palette
import pandas as pd
import json
FONTS = load_fonts()

from plots.line_chart_gif import make_line_chart_gif
from plots.bar_chart_gif import make_bar_chart_gif
from plots.donut_gif import make_donut_gif
from plots.stacked_bar_gif import make_stacked_bar_gif
from plots.merged_donut_gif import make_merged_donut_gif

if __name__ == "__main__":

    with open("./data.json") as file:
        data = json.load(file)

    # DATA = {
    #     "user": "lukilme",
    #     "total_repositories": 17,
    #     "total_code_bytes_all_repos": 626857,
    #     "repositories": [
    #         {
    #             "name": "big-data-analysis-cluster",
    #             "total_code_bytes": 67878,
    #             "languages_percent": {"HiveQL":36.85,"Scala":24.78,"Shell":20.5,"XML":9.32,"Dockerfile":6.83,"Perl":1.05,"INI":0.66},
    #         },
    #         {
    #             "name": "bubble-music-mirror",
    #             "total_code_bytes": 261,
    #             "languages_percent": {"Python":100.0},
    #         },
    #         {
    #             "name": "django-classroom",
    #             "total_code_bytes": 6474,
    #             "languages_percent": {"Python":95.68,"Dockerfile":4.32},
    #         },
    #         {
    #             "name": "dynamic-gif-generator",
    #             "total_code_bytes": 1832,
    #             "languages_percent": {"Python":100.0},
    #         },
    #     ],
    # }
    DATA = data
    print(DATA['repositories'])
    repos = DATA["repositories"]

    make_bar_chart_gif(
        labels   = [r["name"] for r in repos],
        values   = [r["total_code_bytes"] for r in repos],
        title    = ">> REPO SIZE  BYTES",
        subtitle = f"@{DATA['user']}",
        footer   = f"TOTAL: {DATA['total_code_bytes_all_repos']:,} bytes  |  REPOS: {DATA['total_repositories']}",
        colors   = [Palette.CYAN, Palette.MAGENTA, Palette.GREEN, Palette.YELLOW],
        out_path = "imgs/repo_sizes.gif",
        FONTS = FONTS
    )

    bd = repos[0]
    make_donut_gif(
        labels   = list(bd["languages_percent"].keys()),
        values   = list(bd["languages_percent"].values()),
        title    = ">> LANGUAGE BREAKDOWN",
        subtitle = bd["name"][:28],
        footer   = f"7 languages  |  {bd['total_code_bytes']:,} bytes",
        out_path = "imgs/language_pie.gif",
        FONTS = FONTS
    )
    make_merged_donut_gif(
        repos    = repos,
        title    = ">> LANGUAGES · ALL REPOS",
        out_path = "imgs/all_langs_merged.gif",
        FONTS = FONTS
    )

    all_langs = sorted({l for r in repos for l in r["languages_percent"]})
    matrix    = [[r["languages_percent"].get(l, 0) for l in all_langs] for r in repos]
    make_stacked_bar_gif(
        categories = [r["name"] for r in repos],
        groups     = all_langs,
        matrix     = matrix,
        title      = ">> STACK: LANG / REPO",
        footer     = "% of total bytes per repo",
        out_path   = "imgs/stacked_langs.gif",
        FONTS = FONTS
    )

    import datetime
    dates = sorted(
        [r.get("created_at", "")[:10] for r in DATA["repositories"] if r.get("created_at")],
    )
    make_line_chart_gif(
        series    = {"bytes": [r["total_code_bytes"] for r in repos]},
        x_labels  = [r["name"][:8] for r in repos],
        title     = ">> BYTES OVER REPOS",
        subtitle  = f"@{DATA['user']}",
        footer    = "ordered by creation date",
        colors    = [Palette.CYAN],
        out_path  = "imgs/bytes_line.gif",
        FONTS = FONTS
    )