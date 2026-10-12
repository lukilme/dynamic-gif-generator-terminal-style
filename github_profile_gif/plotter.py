from __future__ import annotations

import json
from pathlib import Path

from plots.constants import Palette
from plots.util import load_fonts

FONTS = load_fonts()

from plots.bar_chart_gif import make_bar_chart_gif
from plots.bar_gif_v2 import make_bar_gif as make_bar_gif_v2
from plots.donut_gif import make_donut_gif
from plots.gauge_gif import make_gauge_gif
from plots.line_chart_gif import make_line_chart_gif
from plots.line_gif import make_line_gif as make_line_gif_v2
from plots.merged_donut_gif import make_merged_donut_gif
from plots.radar_gif import make_radar_gif
from plots.stacked_bar_gif import make_stacked_bar_gif

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_FILE = ROOT / "data" / "github_profile.json"
DEFAULT_OUTPUT_DIR = ROOT / "assets" / "gifs"


def run(data_file: str | Path | None = None, output_dir: str | Path | None = None):
    data_file = Path(data_file) if data_file else DEFAULT_DATA_FILE
    output_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    with data_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    repos = data["repositories"]
    if not repos:
        raise ValueError(f"No repositories found in {data_file}")

    make_bar_chart_gif(
        labels=[r["name"] for r in repos],
        values=[r["total_code_bytes"] for r in repos],
        title=">> REPO SIZE  BYTES",
        subtitle=f"@{data['user']}",
        footer=f"TOTAL: {data['total_code_bytes_all_repos']:,} bytes  |  REPOS: {data['total_repositories']}",
        colors=[Palette.CYAN, Palette.MAGENTA, Palette.GREEN, Palette.YELLOW],
        out_path=str(output_dir / "repo_sizes.gif"),
        FONTS=FONTS,
    )

    repo = repos[0]
    make_donut_gif(
        labels=list(repo["languages_percent"].keys()),
        values=list(repo["languages_percent"].values()),
        title=">> LANGUAGE BREAKDOWN",
        subtitle=repo["name"][:28],
        footer=f"{len(repo['languages_percent'])} languages  |  {repo['total_code_bytes']:,} bytes",
        out_path=str(output_dir / "language_pie.gif"),
        FONTS=FONTS,
    )

    make_merged_donut_gif(
        repos=repos,
        title=">> LANGUAGES · ALL REPOS",
        out_path=str(output_dir / "all_langs_merged.gif"),
        FONTS=FONTS,
    )

    all_langs = sorted({language for repo in repos for language in repo["languages_percent"]})
    matrix = [[repo["languages_percent"].get(language, 0) for language in all_langs] for repo in repos]
    make_stacked_bar_gif(
        categories=[repo["name"] for repo in repos],
        groups=all_langs,
        matrix=matrix,
        title=">> STACK: LANG / REPO",
        footer="% of total bytes per repo",
        out_path=str(output_dir / "stacked_langs.gif"),
        FONTS=FONTS,
    )

    make_line_chart_gif(
        series={"bytes": [repo["total_code_bytes"] for repo in repos]},
        x_labels=[repo["name"][:8] for repo in repos],
        title=">> BYTES OVER REPOS",
        subtitle=f"@{data['user']}",
        footer="ordered by creation date",
        colors=[Palette.CYAN],
        out_path=str(output_dir / "bytes_line.gif"),
        FONTS=FONTS,
    )

    make_radar_gif(
        labels=all_langs,
        values=[sum(repo["languages_percent"].get(language, 0) for repo in repos) for language in all_langs],
        title=">> LANGUAGES RADAR",
        subtitle=f"@{data['user']}",
        footer="sum of percentages across all repos",
        color=Palette.MAGENTA,
        out_path=str(output_dir / "langs_radar.gif"),
        FONTS=FONTS,
    )

    make_bar_gif_v2(
        labels=[repo["name"] for repo in repos],
        values=[repo["total_code_bytes"] for repo in repos],
        title=">> REPO SIZE  BYTES",
        subtitle=f"@{data['user']}",
        footer=f"TOTAL: {data['total_code_bytes_all_repos']:,} bytes  |  REPOS: {data['total_repositories']}",
        colors=[Palette.CYAN, Palette.MAGENTA, Palette.GREEN, Palette.YELLOW],
        out_path=str(output_dir / "repo_sizes_v2.gif"),
        FONTS=FONTS,
    )

    make_line_gif_v2(
        labels=[repo["name"] for repo in repos],
        values=[repo["total_code_bytes"] for repo in repos],
        title=">> BYTES OVER REPOS",
        subtitle=f"@{data['user']}",
        footer="ordered by creation date",
        color=Palette.CYAN,
        out_path=str(output_dir / "bytes_line_v2.gif"),
        FONTS=FONTS,
    )

    make_gauge_gif(
        value=data["total_code_bytes_all_repos"],
        max_value=1000000,
        title=">> TOTAL CODE BYTES",
        subtitle=f"@{data['user']}",
        label=f"{data['total_code_bytes_all_repos']:,} bytes",
        footer=f"across {data['total_repositories']} repos",
        color=Palette.CYAN,
        out_path=str(output_dir / "total_bytes_gauge.gif"),
        FONTS=FONTS,
    )

    print(f"GIFs created in {output_dir}")
    return output_dir


if __name__ == "__main__":
    run()
