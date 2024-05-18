import requests
import os
import re
from datetime import datetime

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
        "Accept": "application/vnd.github.v3+json"
    }
    repos = []

    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            repos.extend(data)
            
            # Check if there are more pages
            if 'next' in response.links:
                url = response.links['next']['url']
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
        keys = ['name', 'pushed_at']
        
        # Skipping forked repo's
        if repo['fork']:
            continue
        
        for key in keys:
            repo_info[key] = repo[key]

        repo_info['popularity'] = calculate_repo_popularity(repo)
        repo_list.append(repo_info)
    
    sorted_repos = sorted(repo_list, key=lambda x: parse_github_time_str(x['pushed_at']), reverse=True)
    return sorted_repos

def calculate_repo_popularity(repo):
    keys = ['forks_count', 'stargazers_count', 'watchers_count']
    popularity = 0

    for key in keys:
        if key == 'forks_count':
            multiplier = 2
        else:
            multiplier = 1

        popularity += multiplier * repo[key]
    
    return popularity

def parse_github_time_str(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

def filter_repos_by_languages(username, token, repo_list, languages):
    repos_by_language = {}

    if type(languages) == str:
        repos_by_language[languages] = []

    print(f"{repo_list=}")
    for repo in repo_list:
        repo_languages = get_repo_languages(username, token, repo['name'])
        print(repo['name'], repo_languages)

def get_repo_languages(username, token, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/languages"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve languages: {response.status_code}")
        return None

def list_files(repo_owner, repo_name, token, path=""):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file':
                print(item['path'])
            elif item['type'] == 'dir':
                list_files(repo_owner, repo_name, token, item['path'])
    else:
        print(f"Failed to retrieve contents: {response.status_code}")

if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        print("Error: GITHUB_TOKEN environment variable not set")
        exit

    # Get username
    github_profile_url = "https://github.com/Isss11"
    # github_profile_url = "https://github.com/joelharder4?tab=repositories"
    # github_profile_url = "https://github.com/wiwichips?page=1&tab=repositories"
    username = extract_github_username(github_profile_url)
    languages = ["Java", "Python"]


    repos = get_repo_list(username, token)
    repos = filter_repos_by_languages(username, token, repos, languages)
    print(len(repos), repos)
    #     # 
    #     print(get_repo_languages(username, repo_name, token))
    
    # list_files(username, repo_name, token)

    # if token is None:
    #     print("Error: GITHUB_TOKEN environment variable not set")
    # else:
    #     # list_repos(username, token)
    #     print(get_repo_languages(username, repo_name, token))