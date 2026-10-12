from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / "audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_repos(user: str, page: int = 1, per_page: int = 100):
    url = f"https://api.github.com/users/{user}/repos"
    params = {"per_page": per_page, "page": page}
    logger.info(f"Requesting repositories | user={user} page={page}")

    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        logger.error(
            f"Failed to fetch repositories | status={response.status_code} user={user}"
        )
        return []

    payload = response.json()
    logger.info(f"Repositories fetched | count={len(payload)} page={page}")
    return payload


def fetch_languages(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    logger.info(f"Fetching languages | repo={repo}")

    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        logger.warning(
            f"Failed to fetch languages | repo={repo} status={response.status_code}"
        )
        return {}

    return response.json()


def calculate_percentages(lang_bytes):
    total = sum(lang_bytes.values())

    if total == 0:
        logger.info("Repository with no languages detected")
        return {}

    result = {
        lang: round((count / total) * 100, 2) for lang, count in lang_bytes.items()
    }
    logger.info(f"Percentages calculated | languages={list(result.keys())}")
    return result


def calculate_total_code(lang_bytes):
    total_code = sum(lang_bytes.values())
    logger.info(f"Total code calculated | total_bytes={total_code}")
    return total_code


def run(user: str = "lukilme", output_path: str | Path | None = None):
    output_path = Path(output_path) if output_path else DATA_DIR / "github_profile.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_repos_data = []
    total_global_bytes = 0
    logger.info(f"Starting collection | user={user}")

    page = 1
    while True:
        repos = fetch_repos(user, page=page)
        if not repos:
            logger.info("No additional pages found")
            break

        for repo in repos:
            repo_name = repo["name"]
            logger.info(f"Processing repository | repo={repo_name}")

            langs_bytes = fetch_languages(user, repo_name)
            langs_pct = calculate_percentages(langs_bytes)
            total_code_bytes = calculate_total_code(langs_bytes)
            total_global_bytes += total_code_bytes

            all_repos_data.append(
                {
                    "name": repo_name,
                    "description": repo.get("description") or "",
                    "created_at": repo.get("created_at"),
                    "total_code_bytes": total_code_bytes,
                    "languages_percent": langs_pct,
                }
            )

            time.sleep(0.5)

        page += 1

    payload = {
        "user": user,
        "total_repositories": len(all_repos_data),
        "total_code_bytes_all_repos": total_global_bytes,
        "repositories": all_repos_data,
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4)

    logger.info(
        f"File saved | file={output_path} repositories={len(all_repos_data)} total_bytes={total_global_bytes}"
    )
    print(f"File {output_path} saved successfully!")
    return payload


if __name__ == "__main__":
    run()
