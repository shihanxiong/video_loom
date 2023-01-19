import os
import tkinter as tk
from tkinter import ttk, filedialog as fd
from datetime import datetime
from video_renderer_frame import VideoRendererFrame

'''
For moviepy pyinstaller import issue, see: https://github.com/Zulko/moviepy/issues/591
'''
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.audio.io.AudioFileClip import AudioFileClip
# from moviepy.editor import concatenate_videoclips


# videos input
class VideoInputFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.video_list = []
        self.video_label_text = tk.StringVar(
            value=f"Videos {len(self.video_list)} of 2")
        self.output_file_name = tk.StringVar(
            value=f"{self.get_current_timestamp()}.mp4")

        # layout
        self.total_columns = 4
        self.grid(row=0, sticky="NEW")

        # layout - rows
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1, minsize=200)
        self.rowconfigure(3, weight=1)

        # layout - columns
        for c_idx in range(self.total_columns):
            self.columnconfigure(c_idx, weight=1)

        # video rendering
        self.video_renderer_component = VideoRendererFrame(
            self, padding=(10, 0))
        self.video_renderer_component.grid(row=2, columnspan=2, sticky="NEWS")

        # video import / clear
        video_label = ttk.Label(
            self, textvariable=self.video_label_text, padding=(10))
        video_label.grid(row=0, columnspan=4)
        self.video_import_button = ttk.Button(
            self, text="Import a video", padding=(10), command=self.select_file)
        self.video_import_button.grid(row=1, column=0, sticky="EW")
        self.clear_video_list_button = ttk.Button(
            self, text="Clear video list", padding=(10), command=self.clear_video_list)
        self.clear_video_list_button.grid(row=1, column=1, sticky="EW")
        self.play_all_videos_button = ttk.Button(self, text="Play all videos", state="disable", padding=(
            10), command=self.video_renderer_component.play_all)
        self.play_all_videos_button.grid(row=1, column=2, sticky="EW")
        self.pause_all_videos_button = ttk.Button(self, text="Pause all videos", state="disable", padding=(
            10), command=self.video_renderer_component.pause_all)
        self.pause_all_videos_button.grid(row=1, column=3, sticky="EW")

        # video selection
        self.select_video_button_1 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.timeline_component.insert_timestamp(0))
        self.select_video_button_1.grid(row=3, column=0, sticky="EW")
        self.select_video_button_2 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.timeline_component.insert_timestamp(1))
        self.select_video_button_2.grid(row=3, column=1, sticky="EW")

    def select_file(self):
        filetypes = (
            ('video files', '*.mp4'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename != "":
            self.video_list.append(filename)
            self.refresh()
            self.master.status_component.set_and_log_status(
                f"Imported {filename}")

    def refresh(self):
        self.video_label_text.set(f"Videos {len(self.video_list)} of 2")
        print(self.video_list)

        if len(self.video_list) > 0:
            self.set_buttons_status(
                [self.play_all_videos_button, self.pause_all_videos_button], "enable")
            self.video_renderer_component.load_videos()
        else:
            self.set_buttons_status(
                [self.play_all_videos_button, self.pause_all_videos_button], "disable")

        if len(self.video_list) == 2:
            self.set_buttons_status([self.video_import_button], "disable")
            self.master.toolbar_component.enable_generate_button()
        else:
            self.set_buttons_status([self.video_import_button], "enable")
            self.master.toolbar_component.disable_generate_button()

    def clear_video_list(self):
        self.video_list = []
        self.refresh()
        self.master.status_component.set_and_log_status("video list cleared")

    def get_stream_audio(self):
        audio_clip = AudioFileClip(os.path.abspath(
            self.video_list[self.master.audio_setting_component.audio_track_variable.get()]))
        return audio_clip

    def generate_video(self):
        # logging
        start_time = datetime.now()
        print("generating video...")
        print(
            f'using audio track {self.master.audio_setting_component.audio_track_variable.get() + 1}')
        print("================timeline start================")
        print(self.master.timeline_component.get_timeline_text())
        print("================timeline end==================")

        # remove output file if exists
        if os.path.exists(self.output_file_name.get()):
            os.remove(self.output_file_name.get())

        # video processing
        try:
            # audio
            audio_clip = self.get_stream_audio()

            # video
            clip_1 = VideoFileClip(os.path.abspath(
                self.video_list[0])).subclip(3, 6)
            clip_2 = VideoFileClip(os.path.abspath(
                self.video_list[1])).subclip(8, 12)
            final_clip = concatenate_videoclips(
                [clip_1, clip_2]).set_audio(audio_clip)
            final_clip.write_videofile(self.output_file_name.get(
            ), fps=48, audio_codec="aac", codec="mpeg4", threads=8)
        except:
            self.master.status_component.set_and_log_status(
                "An error occurred while generating video :(")

        # logging
        end_time = datetime.now()
        self.master.status_component.set_and_log_status(
            f"video is ready! Taking total of {round((end_time - start_time).total_seconds(), 2)} seconds")

    def get_current_timestamp(self):
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def set_buttons_status(self, buttons, status):
        for button in buttons:
            button["state"] = status
