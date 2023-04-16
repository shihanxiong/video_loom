import os
import pygame
from tkinter import ttk
from tkVideoPlayer import TkinterVideo
from pdb import set_trace


# video renderer
class VideoRendererFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # pygame
        pygame.init()
        self.mixer = pygame.mixer

    def refresh(self):
        # dynamically create video player instances
        self.videoplayers = []
        for i in range(len(self.master.video_list)):
            videoplayer = TkinterVideo(self, scaled=True, keep_aspect=True)
            videoplayer.load(os.path.abspath(self.master.video_list[i]))
            videoplayer.grid(row=0, column=i, sticky="NEWS",
                             padx=(10), pady=(20))
            self.videoplayers.append(videoplayer)

    def load_audio_preview(self):
        if self.master.master.settings_component.audio_setting_component.has_audio_preview():
            self.mixer.music.load(
                self.master.master.settings_component.audio_setting_component.get_audio_preview())

    def play_all(self):
        self.master.master.status_component.set_and_log_status(
            "playing all videos")
        for videoplayer in self.videoplayers:
            videoplayer.play()

        # audio
        if self.mixer.music.get_pos() == -1:
            self.load_audio_preview()
            self.mixer.music.play()
        else:
            self.mixer.music.unpause()

    def pause_all(self):
        self.master.master.status_component.set_and_log_status(
            "pausing all videos")
        for videoplayer in self.videoplayers:
            videoplayer.pause()

        # audio
        self.mixer.music.pause()

    def seek(self, value):
        self.mixer.music.set_pos(value)
