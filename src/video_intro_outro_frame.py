import tkinter as tk
from tkinter import ttk
from component_interface import ComponentInterface


class VideoIntroOutroFrame(ttk.Frame, ComponentInterface):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # props
        self.import_intro_button = ttk.Button(self, text="Add intro")
        self.import_outro_button = ttk.Button(self, text="Add outro")

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
