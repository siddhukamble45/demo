import os
import requests
from datetime import datetime

# GitHub API token and repo details
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'siddhukamble45'
REPO_NAME = 'demo'
API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}'

changelog_path = 'CHANGELOG.md'
version = '0.0.3'  # Update this dynamically if needed
date = datetime.now().strftime('%B %dth %Y')
note = "Note: A new YAML based mechanism has been added to support no-code customization and creation of recognizers. The default recognizers are now automatically loaded from file."


def get_merged_prs():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    pr_url = f'{API_URL}/pulls?state=closed'
    response = requests.get(pr_url, headers=headers)
    response.raise_for_status()
    prs = response.json()

    merged_prs = [pr for pr in prs if pr.get('merged_at') is not None]
    return merged_prs


def format_pr_entry(pr):
    title = pr.get('title')
    number = pr.get('number')
    user = pr.get('user', {}).get('login', 'unknown')
    url = pr.get('html_url')
    return f"- {title} (#{number}) (Thanks {user}) {url}"


def append_changelog_entry(prs):
    with open(changelog_path, 'a') as file:
        file.write(f'\n{version} - {date}\n')
        file.write(f'{note}\n\n')
        file.write('### Added\n')
        for pr in prs:
            file.write(format_pr_entry(pr) + '\n')


if __name__ == '__main__':
    prs = get_merged_prs()
    append_changelog_entry(prs)
