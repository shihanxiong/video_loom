import os
import sys
import glob
from sys_utils import SysUtils


class FileUtils():
    def __init__(self):
        pass

    @staticmethod
    def clean_up_temp_files():
        try:
            for f in glob.glob("*.mp4"):
                os.remove(f)
            for f in glob.glob("*.mp3"):
                os.remove(f)
            for f in glob.glob("*.aac"):
                os.remove(f)
        except OSError:
            pass

    @staticmethod
    def escape_file_name(filename):
        return f"\"{filename}\""

    @staticmethod
    def get_bundled_file_path(filename):
        # get the path to the temporary directory containing the bundled files
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))

        # construct the path to the file
        file_path = os.path.join(base_path, filename)

        return file_path

    @staticmethod
    def get_file_path(filename):
        return os.path.join(os.getcwd(), filename)

    def get_latest_version_from_changelog(self):
        filename = 'changelog.md'
        if SysUtils.is_running_in_pyinstaller_bundle():
            changelog_path = self.get_bundled_file_path(filename)
        else:
            changelog_path = self.get_file_path(filename)

        with open(changelog_path, 'r') as f:
            text = f.read()
            lines = text.split('\n')
            for line in lines:
                if line.startswith('###'):
                    return line.split(' ')[1]

        return 'Unknown'
