#!/usr/bin/env python3
import sys
import re
import requests

def extract_username(git_url):
    """
    Extracts the username or organization name from various Git URL formats.
    """
    # Clean up whitespace and trailing slashes/git extensions
    url = git_url.strip().rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]
        
    # Regex to handle SSH formats (git@github.com:user/repo) and HTTPS formats
    patterns = [
        r'(?:https?://)?(?:www\.)?github\.com/([^/]+)',
        r'git@github\.com:([^/]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
            
    return None

def fetch_repositories(username):
    """
    Fetches all public repositories for a given GitHub username/org.
    """
    api_url = f"https://api.github.com/users/{username}/repos"
    # Per_page max is 100. For accounts with >100 repos, pagination would be needed.
    params = {'per_page': 100, 'type': 'owner'}
    headers = {'Accept': 'application/vnd.github.v3+json'}
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        
        if response.status_code == 404:
            print(f"\n[-] Error: The user/organization '{username}' was not found on GitHub.")
            return None
        elif response.status_code != 200:
            print(f"\n[-] Error: GitHub API returned status code {response.status_code}")
            return None
            
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Connection error: {e}")
        return None

def main():
    print("=" * 50)
    print("               KoreGitList Tool               ")
    print("=" * 50)
    
    git_link = input("[+] Enter GitHub Profile or Repo URL: ").strip()
    
    if not git_link:
        print("[-] Error: URL cannot be empty.")
        sys.exit(1)
        
    username = extract_username(git_link)
    
    if not username:
        print("[-] Error: Could not parse a valid GitHub username from the provided link.")
        sys.exit(1)
        
    print(f"[ * ] Target Identified: {username}")
    print(f"[ * ] Fetching repositories from GitHub API...")
    
    repos = fetch_repositories(username)
    
    if repos is not None:
        if not repos:
            print(f"\n[!] {username} has no public repositories.")
        else:
            print(f"\n[+] Found {len(repos)} public repositories for '{username}':")
            print("-" * 60)
            # Formatting the output nicely
            print(f"{'#':<4} | {'Repository Name':<30} | {'Stars':<6} | {'Language':<12}")
            print("-" * 60)
            
            for index, repo in enumerate(repos, 1):
                name = repo.get('name', 'N/A')
                stars = repo.get('stargazers_count', 0)
                lang = repo.get('language') or 'None'
                
                # Truncate long names to keep the table clean
                if len(name) > 28:
                    name = name[:25] + "..."
                    
                print(f"{index:<4} | {name:<30} | {stars:<6} | {lang:<12}")
            print("-" * 60)

if __name__ == "__main__":
    main()