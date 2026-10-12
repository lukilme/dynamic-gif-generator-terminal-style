import json
import logging
import time

import requests

# configuração do logging
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def fetch_repos(user, page=1, per_page=100):
    url = f"https://api.github.com/users/{user}/repos"
    params = {"per_page": per_page, "page": page}

    logger.info(f"Requisitando repositorios | user={user} page={page}")

    response = requests.get(url, params=params)

    if response.status_code != 200:
        logger.error(
            f"Falha ao obter repositorios | status={response.status_code} user={user}"
        )
        return []

    logger.info(f"Repositorios obtidos | quantidade={len(response.json())} page={page}")

    return response.json()


def fetch_languages(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"

    logger.info(f"Buscando linguagens | repo={repo}")

    response = requests.get(url)

    if response.status_code != 200:
        logger.warning(
            f"Falha ao obter linguagens | repo={repo} status={response.status_code}"
        )
        return {}

    return response.json()


def calculate_percentages(lang_bytes):
    total = sum(lang_bytes.values())

    if total == 0:
        logger.info("Repositorio sem linguagens detectadas")
        return {}

    result = {
        lang: round((count / total) * 100, 2) for lang, count in lang_bytes.items()
    }

    logger.info(f"Percentuais calculados | linguagens={list(result.keys())}")

    return result


def main():
    user = "lukilme"
    all_repos_data = []

    logger.info(f"Iniciando coleta | user={user}")

    page = 1
    while True:
        repos = fetch_repos(user, page=page)

        if not repos:
            logger.info("Nenhuma página adicional encontrada")
            break

        for r in repos:
            repo_name = r["name"]

            logger.info(f"Processando repositorio | repo={repo_name}")

            langs_bytes = fetch_languages(user, repo_name)
            langs_pct = calculate_percentages(langs_bytes)

            repo_data = {
                "name": repo_name,
                "description": r["description"] or "",
                "created_at": r["created_at"],
                "languages_percent": langs_pct,
            }

            all_repos_data.append(repo_data)

            time.sleep(0.5)

        page += 1

    with open("data.json", "w") as f:
        json.dump(all_repos_data, f, indent=4)

    logger.info(f"Arquivo salvo | arquivo=data.json repositorios={len(all_repos_data)}")

    print("Arquivo data.json salvo com sucesso!")


if __name__ == "__main__":
    main()
