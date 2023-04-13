import os
import glob


class FileUtils():
    def __init__(self):
        pass

    def clean_up_temp_files(self):
        try:
            for f in glob.glob("*.mp4"):
                os.remove(f)
            for f in glob.glob("*.aac"):
                os.remove(f)
        except OSError:
            pass

    def escape_file_name(self, filename):
        return f"\"{filename}\""

    def get_latest_version_from_changelog(self):
        changelog_path = os.path.join(os.getcwd(), 'changelog.md')

        with open(changelog_path, 'r') as f:
            text = f.read()
            lines = text.split('\n')
            for line in lines:
                if line.startswith('###'):
                    return line.split(' ')[1]

        return 'Unknown'
