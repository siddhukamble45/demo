
changelog_path = 'docs/CHANGELOG.md'


def get_current_version():
    with open('user_manager/VERSION') as file:
        for line in file:
            if line.startswith('__version__'):
                # Extract the version value from the line
                version = line.split('=')[1].strip().strip("'\"")
                return version
    raise ValueError("Version not found")


def update_changelog():
    version = get_current_version()

    unreleased_header = f'## user-manager-{version} - [Unreleased]'
    released_header = f'## user-manager-{version} - [Released]'

    with open(changelog_path, 'r') as file:
        changelog_content = file.read()

    # Replace the Unreleased header with the Released header
    changelog_content = changelog_content.replace(unreleased_header, released_header)

    with open(changelog_path, 'w') as file:
        file.write(changelog_content)


if __name__ == '__main__':
    update_changelog()
