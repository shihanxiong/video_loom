import os
import markdown

changelog_path = os.path.join(os.getcwd(), 'changelog.md')
print(changelog_path)


with open(changelog_path, 'r') as f:
    text = f.read()
    lines = text.split('\n')
