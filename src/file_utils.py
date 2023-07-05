import os
import sys
import glob
import logging
from sys_utils import SysUtils


class FileUtils:
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
        except Exception as err:
            logging.error(f"{FileUtils.__name__}: {str(err)}")

    @staticmethod
    def escape_file_name(filename):
        if filename == None:
            return None

        return f'"{filename}"'

    @staticmethod
    def get_bundled_file_path(filename):
        try:
            # get the path to the temporary directory containing the bundled files
            base_path = getattr(
                sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))
            )

            # construct the path to the file
            file_path = os.path.join(base_path, filename)

            return file_path
        except Exception as err:
            logging.error(f"{FileUtils.__name__}: {str(err)}")

    @staticmethod
    def get_file_path(filename):
        try:
            return os.path.join(os.getcwd(), filename)
        except Exception as err:
            logging.error(f"{FileUtils.__name__}: {str(err)}")

    @staticmethod
    def get_latest_version_from_changelog():
        try:
            filename = "changelog.md"
            if SysUtils.is_running_in_pyinstaller_bundle():
                changelog_path = FileUtils.get_bundled_file_path(filename)
            else:
                changelog_path = FileUtils.get_file_path(filename)

            with open(changelog_path, "r") as f:
                text = f.read()
                lines = text.split("\n")
                for line in lines:
                    if line.startswith("###"):
                        return line.split(" ")[1]

            return "Unknown"
        except Exception as err:
            logging.error(f"{FileUtils.__name__}: {str(err)}")
