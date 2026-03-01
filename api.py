import requests
import json
import time

def fetch_repos(user, page=1, per_page=100):
    url = f"https://api.github.com/users/{user}/repos"
    params = {"per_page": per_page, "page": page}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Falha ao obter repositórios: {response.status_code}")
        return []
    return response.json()

def fetch_languages(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    response = requests.get(url)
    if response.status_code != 200:
        return {}
    return response.json()

def calculate_percentages(lang_bytes):
    total = sum(lang_bytes.values())
    if total == 0:
        return {}
    return {lang: round((count / total)*100, 2) for lang, count in lang_bytes.items()}

def main():
    user = "lukilme"
    all_repos_data = []

    page = 1
    while True:
        repos = fetch_repos(user, page=page)
        if not repos:  # sem mais páginas
            break
        for r in repos:
            repo_name = r["name"]
            desc = r["description"] or ""
            stars = r["stargazers_count"]
            forks = r["forks_count"]
            created_at = r["created_at"]

            langs_bytes = fetch_languages(user, repo_name)
            langs_pct = calculate_percentages(langs_bytes)

            repo_data = {
                "name": repo_name,
                "description": desc,
                "created_at": created_at,
                "languages_percent": langs_pct
            }
            all_repos_data.append(repo_data)

            time.sleep(0.5)

        page += 1

    with open("data.json", "w") as f:
        json.dump(all_repos_data, f, indent=4)

    print("Arquivo data.json salvo com sucesso!")

if __name__ == "__main__":
    main()