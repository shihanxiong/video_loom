import tkinter as tk
from tkinter import ttk
from audio_setting_frame import AudioSettingFrame
from video_setting_frame import VideoSettingFrame
from component_interface import ComponentInterface


# settings
class SettingsFrame(ttk.Frame, ComponentInterface):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # components
        self.audio_setting_component = AudioSettingFrame(self)
        self.audio_setting_component.grid(row=0, column=0, sticky="NEW")
        self.video_setting_component = VideoSettingFrame(self)
        self.video_setting_component.grid(row=0, column=1, sticky="NEW")

        # register all components
        self.components = [
            self.audio_setting_component,
            self.video_setting_component,
        ]

    def refresh(self):
        for component in self.components:
            component.refresh()
