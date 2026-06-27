import requests
import json
import time
import logging

logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def fetch_repos(user, page=1, per_page=100):
    url = f"https://api.github.com/users/{user}/repos"
    params = {"per_page": per_page, "page": page}
    logger.info(f"Requesting repositories | user={user} page={page}")

    response = requests.get(url, params=params)

    if response.status_code != 200:
        logger.error(
            f"Failed to fetch repositories | status={response.status_code} user={user}"
        )
        return []

    logger.info(
        f"Repositories fetched | count={len(response.json())} page={page}"
    )

    return response.json()


def fetch_languages(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"

    logger.info(f"Fetching languages | repo={repo}")

    response = requests.get(url)

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
        lang: round((count / total) * 100, 2)
        for lang, count in lang_bytes.items()
    }

    logger.info(f"Percentages calculated | languages={list(result.keys())}")

    return result


def calculate_total_code(lang_bytes):
    total_code = sum(lang_bytes.values())
    logger.info(f"Total code calculated | total_bytes={total_code}")
    return total_code


def main():
    user = "lukilme"
    all_repos_data = []
    total_global_bytes = 0

    logger.info(f"Starting collection | user={user}")

    page = 1
    while True:
        repos = fetch_repos(user, page=page)

        if not repos:
            logger.info("No additional pages found")
            break

        for r in repos:
            repo_name = r["name"]

            logger.info(f"Processing repository | repo={repo_name}")

            langs_bytes = fetch_languages(user, repo_name)
            langs_pct = calculate_percentages(langs_bytes)
            total_code_bytes = calculate_total_code(langs_bytes)

            total_global_bytes += total_code_bytes

            repo_data = {
                "name": repo_name,
                "description": r["description"] or "",
                "created_at": r["created_at"],
                "total_code_bytes": total_code_bytes,
                "languages_percent": langs_pct
            }

            all_repos_data.append(repo_data)

            time.sleep(0.3)

        page += 1

    final_output = {
        "user": user,
        "total_repositories": len(all_repos_data),
        "total_code_bytes_all_repos": total_global_bytes,
        "repositories": all_repos_data
    }

    with open("data.json", "w") as f:
        json.dump(final_output, f, indent=4)

    logger.info(
        f"File saved | file=data.json repositories={len(all_repos_data)} total_bytes={total_global_bytes}"
    )

    print("File data.json saved successfully!")


if __name__ == "__main__":
    main()