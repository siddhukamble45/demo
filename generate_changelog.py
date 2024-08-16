import os
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


def get_title_without_prefix(title):
    if title[3] == ':':
        return title[4:]
    if title[4] == ':':
        return title[5:]
    return title


def update_changelog(pr):
    version = get_current_version()
    title = pr.get('title')
    number = pr.get('number')
    user = pr.get('user', {}).get('login', 'unknown')
    url = pr.get('html_url')
    section = categorize_pr(title)
    title = get_title_without_prefix(title)
    description = f"- {title} (#{number}) (Thanks {user}) {url}"

    # Read the changelog and join lines into a single string
    with open(changelog_path, 'r') as file:
        changelog_content = file.read()
    with open(changelog_path, 'r') as file:
        changelog_lines = file.readlines()

    version_header = f'## user-manager-{version} - [Unreleased]'
    released_header = f'## user-manager-{version} - [Released]'
    if version_header not in changelog_content:
        version_header_line = (f'{version_header}\n\n'
                               f'### Added\n\n'
                               f'### Changed\n\n'
                               f'### General\n\n')
        version_header_lines = version_header_line.split('\n')
        start_line = 4
        for header_line in version_header_lines:
            changelog_lines.insert(start_line, f'{header_line}\n')
            start_line += 1

    if released_header not in changelog_content:
        if description not in changelog_content:
            for i, line in enumerate(changelog_lines):
                if line.strip() == f'### {section}':
                    changelog_lines.insert(i + 1, f'{description}\n')
                    break
            with open(changelog_path, 'w') as file:
                file.writelines(changelog_lines)


if __name__ == '__main__':
    pr = get_latest_pr()
    if pr:
        update_changelog(pr)
