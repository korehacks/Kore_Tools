#!/usr/bin/env python3
import argparse
import re
import sys
import requests

def parse_git_input(git_input):
    """
    Parses the input to determine if it's a specific repo or just a user/org.
    Returns a dict with 'username' and optionally 'repo'.
    """
    cleaned = git_input.strip().rstrip('/')
    if cleaned.endswith('.git'):
        cleaned = cleaned[:-4]

    # Regex to extract user and optional repo from HTTPS and SSH formats
    # Handles: 'username', 'https://github.com/user', 'https://github.com/user/repo'
    patterns = [
        r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)',  # URL with repo
        r'git@github\.com:([^/]+)/([^/]+)',                      # SSH with repo
        r'(?:https?://)?(?:www\.)?github\.com/([^/]+)',          # URL user only
        r'git@github\.com:([^/]+)'                               # SSH user only
    ]

    for i, pattern in enumerate(patterns):
        match = re.search(pattern, cleaned, re.IGNORECASE)
        if match:
            if i < 2:  # Found both user and repo
                return {'username': match.group(1), 'repo': match.group(2)}
            else:      # Found user only
                return {'username': match.group(1), 'repo': None}

    # If it doesn't match any pattern, assume it's a raw username
    return {'username': cleaned, 'repo': None}

def fetch_repositories(username):
    """Fetches all public repositories for a given GitHub username/org."""
    api_url = f"https://api.github.com/users/{username}/repos"
    params = {'per_page': 100, 'type': 'owner'}
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        if response.status_code == 404:
            print(f"[-] Error: User/Org '{username}' not found.")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[-] Connection error: {e}")
        return None

def fetch_repo_files(username, repo):
    """Fetches the top-level contents (files/folders) of a specific repository."""
    api_url = f"https://api.github.com/repos/{username}/{repo}/contents"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 404:
            print(f"[-] Error: Repository '{username}/{repo}' not found.")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[-] Connection error: {e}")
        return None

def display_repos(username, repos):
    """Prints a formatted table of repositories."""
    print(f"\n[+] Found {len(repos)} public repositories for '{username}':")
    print("-" * 65)
    print(f"{'#':<4} | {'Repository Name':<30} | {'Stars':<6} | {'Language':<12}")
    print("-" * 65)
    for index, repo in enumerate(repos, 1):
        name = repo.get('name', 'N/A')
        stars = repo.get('stargazers_count', 0)
        lang = repo.get('language') or 'None'
        if len(name) > 28:
            name = name[:25] + "..."
        print(f"{index:<4} | {name:<30} | {stars:<6} | {lang:<12}")
    print("-" * 65)

def display_files(username, repo, contents):
    """Prints the contents of a repository."""
    print(f"\n[+] Top-level files/folders in '{username}/{repo}':")
    print("-" * 65)
    print(f"{'Type':<6} | {'Name':<40} | {'Size (Bytes)':<12}")
    print("-" * 65)
    for item in contents:
        item_type = item.get('type', 'unknown').upper()
        name = item.get('name', 'N/A')
        size = item.get('size', 0) if item_type == 'FILE' else '-'
        if len(name) > 38:
            name = name[:35] + "..."
        print(f"{item_type:<6} | {name:<40} | {size:<12}")
    print("-" * 65)

def main():
    parser = argparse.ArgumentParser(description="List GitHub repositories or repo contents.")
    parser.add_argument('-user', required=True, help="GitHub username, profile URL, or repository URL")
    args = parser.parse_args()

    target = parse_git_input(args.user)
    username = target['username']
    repo = target['repo']

    print(f"[ * ] Target User/Org: {username}")
    
    # Context 1: A specific repository URL was provided
    if repo:
        print(f"[ * ] Target Repo    : {repo}")
        print("[ * ] Fetching repository contents...")
        contents = fetch_repo_files(username, repo)
        if contents:
            display_files(username, repo, contents)
            
    # Context 2: Only a username or profile URL was provided
    else:
        print("[ * ] Fetching account repositories...")
        repos = fetch_repositories(username)
        if repos is not None:
            if not repos:
                print(f"[!] {username} has no public repositories.")
            else:
                display_repos(username, repos)

if __name__ == "__main__":
    main()