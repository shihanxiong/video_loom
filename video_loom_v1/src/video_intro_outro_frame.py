import tkinter as tk
from tkinter import ttk
from component_interface import ComponentInterface
from tktooltip import ToolTip


class VideoIntroOutroFrame(ttk.Frame, ComponentInterface):
    _BUTTON_TEXT_IMPORT_INTRO = "Add intro"
    _BUTTON_TEXT_IMPORT_OUTRO = "Add outro"

    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # props
        self.import_intro_button = ttk.Button(
            self, text=self._BUTTON_TEXT_IMPORT_INTRO, command=self.import_intro
        )
        ToolTip(
            self.import_intro_button,
            msg="Import a video as intro for the final generated video, it will be using its own audio track",
            delay=0,
        )
        self.import_outro_button = ttk.Button(
            self, text=self._BUTTON_TEXT_IMPORT_OUTRO, command=self.import_outro
        )
        ToolTip(
            self.import_outro_button,
            msg="Import a video as outro for the final generated video, it will be using its own audio track",
            delay=0,
        )

        self.import_intro_button.grid(row=0, column=0, sticky="EW")
        self.import_outro_button.grid(row=0, column=1, sticky="EW")

    def refresh(self):
        if self.master.intro == None:
            self.enable_button(self.import_intro_button)
        else:
            self.disable_button(self.import_intro_button)

        if self.master.outro == None:
            self.enable_button(self.import_outro_button)
        else:
            self.disable_button(self.import_outro_button)

    def import_intro(self):
        filename = self.select_file()

        if filename != None:
            self.master.intro = filename
            self.refresh()

    def import_outro(self):
        filename = self.select_file()

        if filename != None:
            self.master.outro = filename
            self.refresh()
