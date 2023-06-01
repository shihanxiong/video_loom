from abc import ABC, abstractmethod
from tkinter import filedialog as fd


class ComponentInterface(ABC):
    _FILE_TYPES = (("video files", "*.mp4"), ("All files", "*.*"))

    @abstractmethod
    def refresh(self):
        pass

    def disable_button(self, button):
        button["state"] = "disable"

    def enable_button(self, button):
        button["state"] = "enable"

    def set_button_text(self, button, text):
        button.config(text=text)

    def select_file(self):
        filename = fd.askopenfilename(
            title="Open a file", initialdir="/", filetypes=self._FILE_TYPES
        )

        if filename == "":
            return None

        return filename

    def select_files(self):
        filenames = fd.askopenfilenames(
            title="Open a file", initialdir="/", filetypes=self._FILE_TYPES
        )

        return filenames
