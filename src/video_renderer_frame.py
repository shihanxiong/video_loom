import os
import pygame
import logging
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

        # status
        self.is_playing = False

        # pygame
        pygame.init()
        self.mixer = pygame.mixer

    def refresh(self):
        # dynamically create video player instances
        self.videoplayers = []
        for i in range(len(self.master.video_list)):
            videoplayer = TkinterVideo(self, scaled=True, keep_aspect=True)
            videoplayer.load(os.path.abspath(self.master.video_list[i]))
            videoplayer.grid(row=0, column=i, sticky="NEWS", padx=(10), pady=(20))
            self.videoplayers.append(videoplayer)

    def load_audio_preview(self):
        try:
            if (
                self.master.master.settings_component.audio_setting_component.has_audio_preview()
            ):
                self.mixer.music.load(
                    self.master.master.settings_component.audio_setting_component.get_audio_preview()
                )
                if self.is_playing:
                    self.mixer.music.play(
                        start=self.master.video_control_component.progress_value.get()
                    )
                else:
                    self.mixer.music.set_pos(
                        self.master.video_control_component.progress_value.get()
                    )
            else:
                self.mixer.music.stop()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def unload_audio_preview(self):
        try:
            self.mixer.music.unload()
        except Exception as err:
            logging.error(f"{self.__class__.__name__}: {str(err)}")

    def play_all(self):
        self.is_playing = True
        self.master.master.status_component.set_and_log_status("playing all videos")
        for videoplayer in self.videoplayers:
            videoplayer.play()

        # audio
        if (
            self.master.master.settings_component.audio_setting_component.has_audio_preview()
        ):
            self.load_audio_preview()
            if self.mixer.music.get_pos() == -1:
                self.mixer.music.play(
                    start=self.master.video_control_component.progress_value.get()
                )
            else:
                self.mixer.music.set_pos(
                    self.master.video_control_component.progress_value.get()
                )
                self.mixer.music.unpause()

    def pause_all(self):
        self.is_playing = False
        self.master.master.status_component.set_and_log_status("pausing all videos")
        for videoplayer in self.videoplayers:
            videoplayer.pause()

        # audio
        if (
            self.master.master.settings_component.audio_setting_component.has_audio_preview()
        ):
            self.mixer.music.pause()

    def seek(self, value):
        # audio
        if (
            self.master.master.settings_component.audio_setting_component.has_audio_preview()
        ):
            self.mixer.music.set_pos(value)
