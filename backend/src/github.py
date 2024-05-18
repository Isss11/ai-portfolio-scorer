import requests

from src.config import GITHUB_TOKEN

def get_user_info(username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data

def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {GITHUB_TOKEN}"
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
