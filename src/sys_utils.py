import sys


class SysUtils():
    def __init__(self):
        pass

    @staticmethod
    def is_running_in_pyinstaller_bundle():
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # running in a pyinstaller bundle
            return True
        else:
            # running in a normal python process
            return False
