import requests
import os
import re
from datetime import datetime
import base64

from src.config import GITHUB_TOKEN

FILE_TYPES = {
    "C": (".c", ".h"),
    "C++": (".cpp", ".hpp", ".cc", ".cxx", ".h", ".hh", ".hxx"),
    "C#": (".cs"),
    "Java": (".java"),
    "Python": (".py"),
    "JavaScript": (".js"),
    "TypeScript": (".ts"),
    "Ruby": (".rb"),
    "Go": (".go"),
    "Rust": (".rs"),
    "Swift": (".swift"),
    "Kotlin": (".kt", ".kts"),
    "HTML": (".html", ".htm"),
    "CSS": (".css"),
    "PHP": (".php"),
    "ASP.NET": (".aspx", ".ascx", ".ashx", ".asmx"),
    "Bash": (".sh"),
    "Perl": (".pl", ".pm"),
    "PowerShell": (".ps1"),
    "Batch": (".bat", ".cmd"),
    "JSON": (".json"),
    "XML": (".xml"),
    "YAML": (".yaml", ".yml"),
    "CSV": (".csv"),
    "Markdown": (".md"),
    "SCSS": (".scss"),
    "Sass": (".sass"),
    "Less": (".less"),
    "SQL": (".sql"),
    "CMake": (".cmake"),
    "Haskell": (".hs"),
    "Erlang": (".erl", ".hrl"),
    "Lisp": (".lisp", ".lsp"),
    "Scheme": (".scm", ".ss"),
    "Prolog": (".pl", ".pro"),
    "R": (".R", ".r"),
    "MATLAB": (".m"),
    "Julia": (".jl"),
    "SAS": (".sas"),
    "Assembly": (".asm", ".s"),
    "Fortran": (".f", ".for", ".f90", ".f95"),
    "COBOL": (".cob", ".cbl"),
    "Ada": (".adb", ".ads"),
}


def get_user_info(username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data


def extract_github_username(url):
    pattern = r"github\.com/([A-Za-z0-9-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def get_all_user_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    repos = []

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            repos.extend(data)

            # Check if there are more pages
            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                url = None
        else:
            print(f"Failed to retrieve repositories: {response.status_code}")
            break

    return repos


def get_repo_list(username, token):
    repo_list = []

    repos = get_all_user_repos(username, token)
    for repo in repos:
        repo_info = {}
        keys = ["name", "pushed_at"]

        # Skipping forked repo's
        if repo["fork"]:
            continue

        for key in keys:
            repo_info[key] = repo[key]

        repo_info["popularity"] = calculate_repo_popularity(repo)
        repo_list.append(repo_info)

    sorted_repos = sorted(
        repo_list, key=lambda x: parse_github_time_str(x["pushed_at"]), reverse=True
    )
    return sorted_repos


def calculate_repo_popularity(repo):
    keys = ["forks_count", "stargazers_count", "watchers_count"]
    popularity = 0

    for key in keys:
        if key == "forks_count":
            multiplier = 2
        else:
            multiplier = 1

        popularity += multiplier * repo[key]

    return popularity


def parse_github_time_str(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")


def filter_repos_by_languages(username, token, repo_list, languages, limit=None):
    repos_by_language = {}

    if type(languages) == str:
        repos_by_language[languages] = []
    else:
        for language in languages:
            repos_by_language[language] = []

    print(f"{repo_list=}")
    for repo in repo_list:
        repo_languages = get_repo_languages(username, token, repo["name"])

        for language in repo_languages:
            try:
                if limit == None or len(repos_by_language[language]) < limit:
                    repos_by_language[language].append(repo["name"])
            except:
                pass

    return repos_by_language


def get_repo_languages(username, token, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/languages"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve languages: {response.status_code}")
        return None


def get_files_to_scrape(username, token, language_repo_dict):
    files = {}

    for language, repo_list in language_repo_dict.items():
        try:
            for repo in repo_list:
                lang_files = []
                locate_files(username, token, repo, language, lang_files)
                files[language] = {"repo": repo, "files": lang_files}
        except:
            pass

    return files


def locate_files(username, token, repo_name, language, files, path=""):
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item["type"] == "file" and item["path"].endswith(FILE_TYPES[language]):
                files.append(item["path"])
            elif item["type"] == "dir":
                locate_files(username, token, repo_name, language, files, item["path"])
    else:
        print(f"Failed to retrieve contents: {response.status_code}")


def retrieve_files(username, token, repo_files_dict):
    raw_file_content = {}

    for language, location in repo_files_dict.items():
        repo = location["repo"]
        raw_file_content[language] = {"repo": repo, "files": []}

        for path in location["files"]:
            raw_code = retrieve_file_from_repo(username, token, repo, path)
            raw_file_content[language]["files"].append(
                {"name": path, "content": raw_code}
            )

    return raw_file_content


def retrieve_file_from_repo(username, token, repo, path):
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json().get("content")
        decoded_content = base64.b64decode(content).decode("utf-8")
        return decoded_content
    else:
        print(f"Failed to retrieve file. Status code: {response.status_code}")
        return None


if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        print("Error: GITHUB_TOKEN environment variable not set")
        exit()

    # Get username
    github_profile_url = "https://github.com/ericbuys"
    # github_profile_url = "https://github.com/Isss11"
    # github_profile_url = "https://github.com/joelharder4?tab=repositories"
    # github_profile_url = "https://github.com/wiwichips?page=1&tab=repositories"
    username = extract_github_username(github_profile_url)
    languages = ["Python", "HTML"]

    # Get repos
    repos = get_repo_list(username, token)
    language_repo_dict = filter_repos_by_languages(
        username, token, repos, languages, limit=1
    )
    print(f"{language_repo_dict=}")

    # Get file content
    files = get_files_to_scrape(username, token, language_repo_dict)
    print(f"{files=}")
    file_content = retrieve_files(username, token, files)
    print(f"{file_content=}")
