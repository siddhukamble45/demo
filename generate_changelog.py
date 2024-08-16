import os
import re
import requests

# GitHub API token and repo details
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'siddhukamble45'
REPO_NAME = 'demo'
API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}'

changelog_path = 'docs/CHANGELOG.md'


def get_current_version():
    with open('user_manager/VERSION') as file:
        for line in file:
            if line.startswith('__version__'):
                # Extract the version value from the line
                version = line.split('=')[1].strip().strip("'\"")
                return version
    raise ValueError("Version not found")




def get_latest_pr():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    pr_url = f'{API_URL}/pulls?state=closed&sort=updated&direction=desc'
    response = requests.get(pr_url, headers=headers)
    response.raise_for_status()
    prs = response.json()

    for pr in prs:
        if pr.get('merged_at') is not None:
            return pr
    return None


def categorize_pr(title):
    if title.startswith('ENH:'):
        return 'Added'
    elif title.startswith('BUG:'):
        return 'Changed'
    else:
        return 'General'


def update_changelog(pr):
    version = get_current_version()
    title = pr.get('title')
    number = pr.get('number')
    user = pr.get('user', {}).get('login', 'unknown')
    url = pr.get('html_url')
    description = f"- {title} (#{number}) (Thanks {user}) {url}"
    section = categorize_pr(title)

    with open(changelog_path, 'r') as file:
        lines = file.readlines()

    # Create the "Unreleased" section for the current version
    version_header = f'## user-manager-{version} - [Unreleased]'
    if version_header not in ''.join(lines):
        lines.insert(0, f'{version_header}\n\n### Added\n\n### Changed\n\n### General\n\n')

    # Find the correct section to append the PR details
    print("## Description::", description)
    for i, line in enumerate(lines):
        if line.strip() == f'### {section}':
            lines.insert(i + 1, f'{description}\n')
            break
    print("## Lines::", lines)
    with open(changelog_path, 'w') as file:
        file.writelines(lines)


if __name__ == '__main__':
    pr = get_latest_pr()
    if pr:
        update_changelog(pr)
