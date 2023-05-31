import sys
from sys import platform


class SysUtils:
    def __init__(self):
        pass

    @staticmethod
    def is_running_in_pyinstaller_bundle():
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            # running in a pyinstaller bundle
            return True
        else:
            # running in a normal python process
            return False

    @staticmethod
    def is_win32():
        return platform == "win32"

    @staticmethod
    def is_macos():
        return platform == "darwin"

    @staticmethod
    def is_other():
        return SysUtils.is_win32 == False and SysUtils.is_macos == False
