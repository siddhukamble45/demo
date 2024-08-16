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


def update_changelog(pr):
    version = get_current_version()
    title = pr.get('title')
    number = pr.get('number')
    user = pr.get('user', {}).get('login', 'unknown')
    url = pr.get('html_url')
    description = f"- {title} (#{number}) (Thanks {user}) {url}"
    section = categorize_pr(title)

    # Read the changelog and join lines into a single string
    with open(changelog_path, 'r') as file:
        changelog_content = file.read()

    # Define the version header and the initial sections if they don't exist
    version_header = f'## user-manager-{version} - [Unreleased]'
    if version_header not in changelog_content:

        changelog_content = (
            f'{version_header}\n\n'
            f'### Added\n\n'
            f'### Changed\n\n'
            f'### General\n\n{changelog_content}'
        )

    # Find the position of the correct section to insert the PR details
    section_header = f'### {section}'
    insert_position = (changelog_content.find(section_header) +
                       len(section_header))

    if insert_position != -1:
        # Insert the description in the correct section
        if description not in changelog_content:
            changelog_content = (
                    changelog_content[:insert_position] +
                    f'\n{description}\n' +
                    changelog_content[insert_position:]
            )

    # Write the updated content back to the changelog file
    with open(changelog_path, 'w') as file:
        file.write(changelog_content)


if __name__ == '__main__':
    pr = get_latest_pr()
    if pr:
        update_changelog(pr)
