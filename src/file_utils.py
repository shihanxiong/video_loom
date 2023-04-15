import os
import sys
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

    def get_bundled_file_path(self, filename):
        # get the path to the temporary directory containing the bundled files
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))

        # construct the path to the file
        file_path = os.path.join(base_path, filename)

        return file_path

    def get_latest_version_from_changelog(self):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # running in a pyinstaller bundle
            changelog_path = self.get_bundled_file_path('changelog.md')
        else:
            # running in a normal python process
            changelog_path = os.path.join(os.getcwd(), 'changelog.md')

        with open(changelog_path, 'r') as f:
            text = f.read()
            lines = text.split('\n')
            for line in lines:
                if line.startswith('###'):
                    return line.split(' ')[1]

        return 'Unknown'
