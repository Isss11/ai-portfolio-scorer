import requests
import collections
from datetime import datetime
import base64

from .ttl_cache import TTLCache
from .routes.AIQuery import AIQuery
import math
from .config import GITHUB_TOKEN

ttl_cache = TTLCache(5 * 60)

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


def flatten(l):
    return [item for sublist in l for item in sublist]


@ttl_cache
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


# Sourced from https://github.com/anuraghazra/github-readme-stats
@ttl_cache
def get_user_top_languages(username):
    url = "https://api.github.com/graphql"
    query = """
query userInfo($login: String!) {
    user(login: $login) {
        # fetch only owner repos & not forks
        repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
            nodes {
                name
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                    edges {
                        size
                        node {
                            color
                            name
                        }
                    }
                }
            }
        }
    }
}
    """

    variables = {"login": username}

    body = {"query": query, "variables": variables}
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
    }

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    lang_sizes = collections.defaultdict(int)

    def map_repo_node(repo):
        return repo["languages"]["edges"]

    repos = data["data"]["user"]["repositories"]["nodes"]

    for lang in flatten(map(map_repo_node, repos)):
        key = (lang["node"]["name"], lang["node"]["color"])
        lang_sizes[key] += lang["size"]

    sorted_langs = sorted(lang_sizes.items(), key=lambda x: x[1], reverse=True)

    def map_lang(lang):
        return {"name": lang[0][0], "color": lang[0][1], "size": lang[1]}

    sorted_langs = list(map(map_lang, sorted_langs))

    return sorted_langs


@ttl_cache
def get_user_popularity(username, ai_prompt=True):
    url = "https://api.github.com/graphql"
    query = """
        query userInfo($login: String!) {
            user(login: $login) {
                repositories(first: 100) {
                    nodes {
                        name
                        forks {
                            totalCount
                        }
                        watchers {
                            totalCount
                        }
                        stargazers {
                            totalCount
                        }
                    }
                }
            }
        }
        """

    variables = {"login": username}

    body = {"query": query, "variables": variables}
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
    }

    response = requests.post(url, json=body, headers=headers)
    result = response.json()

    repositories = result["data"]["user"]["repositories"]["nodes"]
    total_popularity = 0

    for repo in repositories:
        total_popularity += 2 * repo["forks"]["totalCount"]
        total_popularity += repo["watchers"]["totalCount"]
        total_popularity += repo["stargazers"]["totalCount"]

    popularity_score = round(200 / (1 + math.exp(-0.02 * total_popularity)) - 100)

    feedback = []
    if ai_prompt:
        # Creating a Gemini instance to query for popularity score feedback
        gemini = AIQuery()
        feedback = gemini.generate_impact_feedback(popularity_score)

    return {"score": popularity_score, "feedback": feedback}


@ttl_cache
def get_user_exerience(username, ai_prompt=True):
    profile_data = get_user_top_languages(username)
    total_experience = 0

    for lang in profile_data:
        total_experience += lang["size"]

    experience_score = round(
        (2000000 / (1 + math.exp(-0.0000015 * total_experience)) - 1000000) / 10000
    )

    feedback = []
    if ai_prompt:
        gemini = AIQuery()
        top_three_langs = [lang["name"] for lang in profile_data[:3]]
        feedback = gemini.generate_experience_feedback(
            experience_score, top_three_langs
        )

    return {"score": experience_score, "feedback": feedback}


@ttl_cache
def get_user_quality(username):
    top_three_languages = get_user_top_languages(username)[:2]
    languages = []
    for obj in top_three_languages:
        languages.append(obj["name"])

    repos = get_repo_list(username)
    language_repo_dict = filter_repos_by_languages(username, repos, languages, limit=1)
    files = get_files_to_scrape(username, language_repo_dict)
    file_content = retrieve_files(username, files)
    scorer = AIQuery()
    stringifiedFiles = scorer.getStringifiedFiles(file_content)
    feedback = scorer.getFeedback(stringifiedFiles)

    score = min(100, max(0, round(feedback["score"])))

    # print(top_three_languages)
    return {
        "score": score,
        "feedback": feedback["feedback"],
    }


def get_all_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
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


def get_repo_list(username):
    repo_list = []

    repos = get_all_user_repos(username)
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


def filter_repos_by_languages(username, repo_list, languages, limit=None):
    repos_by_language = {}

    if type(languages) == str:
        repos_by_language[languages] = []
    else:
        for language in languages:
            repos_by_language[language] = []

    # print(f"{repo_list=}")
    for repo in repo_list:
        repo_languages = get_repo_languages(username, repo["name"])

        for language in repo_languages:
            try:
                if limit == None or len(repos_by_language[language]) < limit:
                    repos_by_language[language].append(repo["name"])
            except:
                pass

    return repos_by_language


def get_repo_languages(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/languages"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve languages: {response.status_code}")
        return None


def get_files_to_scrape(username, language_repo_dict):
    files = {}

    for language, repo_list in language_repo_dict.items():
        try:
            for repo in repo_list:
                lang_files = []
                locate_files(username, repo, language, lang_files)
                files[language] = {"repo": repo, "files": lang_files}
        except:
            pass

    return files


def locate_files(username, repo_name, language, files, path=""):
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item["type"] == "file" and item["path"].endswith(FILE_TYPES[language]):
                files.append(item["path"])
            elif item["type"] == "dir":
                locate_files(username, repo_name, language, files, item["path"])
    else:
        print(f"Failed to retrieve contents: {response.status_code}")


def retrieve_files(username, repo_files_dict):
    raw_file_content = {}
    max_file_count = 10
    file_count = 0

    for language, location in repo_files_dict.items():
        repo = location["repo"]
        raw_file_content[language] = {"repo": repo, "files": []}

        for path in location["files"]:
            raw_code = retrieve_file_from_repo(username, repo, path)
            raw_file_content[language]["files"].append(
                {"name": path, "content": raw_code}
            )
            file_count += 1

            if file_count >= max_file_count:
                return raw_file_content

    return raw_file_content


def retrieve_file_from_repo(username, repo, path):
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
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
    print(get_user_exerience("ericbuys"))
