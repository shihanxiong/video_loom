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
