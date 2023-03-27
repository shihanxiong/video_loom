import os
import glob
import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from video_import_frame import VideoImportFrame
from video_renderer_frame import VideoRendererFrame
from video_select_frame import VideoSelectFrame
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips


# videos input
class VideoFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.components = []
        self.max_num_of_videos = 4
        self.video_list = []
        self.video_label_text = tk.StringVar(
            value=f"Videos {len(self.video_list)} of 4")
        self.output_file_name = tk.StringVar(
            value=f"{self.get_current_timestamp()}.mp4")

        # layout - rows
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1, minsize=220)
        self.rowconfigure(3, weight=1)

        # layout - columns
        self.total_columns = 4
        for c_idx in range(self.total_columns):
            self.columnconfigure(c_idx, weight=1)

        # video label
        video_label = ttk.Label(
            self, textvariable=self.video_label_text, padding=(10))
        video_label.grid(row=0, columnspan=4)

        # video rendering
        self.video_renderer_component = VideoRendererFrame(
            self, padding=(10, 0))
        self.video_renderer_component.grid(row=2, columnspan=4, sticky="NEWS")

        # video import / clear
        self.video_import_component = VideoImportFrame(self, padding=(10, 0))
        self.video_import_component.grid(row=1, columnspan=4, sticky="NEW")

        # video selection
        self.video_select_component = VideoSelectFrame(self, padding=(10, 0))
        self.video_select_component.grid(row=3, columnspan=4, sticky="NEW")

        # register all components
        self.components.append(self.video_import_component)
        self.components.append(self.video_renderer_component)
        self.components.append(self.video_select_component)

    def refresh(self):
        self.video_label_text.set(
            f"Videos {len(self.video_list)} of {self.max_num_of_videos}")
        print(self.video_list)

        for component in self.components:
            component.refresh()

    def get_stream_audio(self):
        audio_clip = AudioFileClip(os.path.abspath(
            self.video_list[self.master.audio_setting_component.audio_track_variable.get()]))
        return audio_clip

    def generate_video_with_ffmpeg(self):
        # remove output file if exists
        self.clean_up_temp_files()

        # calculate output video resolution
        # this will scale all inputs to match the max width & max height
        output_width, output_height = self.calculate_output_resolutions()
        pass

    # TODO: this method is deprecated, switch to using generate_video_with_ffmpeg()
    def generate_video_with_moviepy(self):
        # logging
        start_time = datetime.now()
        print("generating video...")
        print(
            f'using audio track {self.master.audio_setting_component.audio_track_variable.get() + 1}')
        print("================timeline start================")
        print(self.master.timeline_component.get_timeline_text())
        print("================timeline end==================")

        # remove output file if exists
        self.clean_up_temp_files()

        # video processing
        try:
            # parse timeline
            timeline_arr = self.master.timeline_component.parse_timeline()

            # audio
            audio_clip = self.get_stream_audio()

            # video
            video_clips = []
            for timeline in timeline_arr:
                video, start, end = map(int, timeline.split(","))
                clip = VideoFileClip(os.path.abspath(
                    self.video_list[video - 1])).subclip(start, end)
                video_clips.append(clip)

            final_clip = concatenate_videoclips(
                video_clips).set_audio(audio_clip)
            final_clip.write_videofile(self.output_file_name.get(
            ), fps=48, audio_codec="aac", codec="mpeg4", threads=8)
        except Exception as err:
            self.master.status_component.set_and_log_status(
                "An error occurred while generating video :(")
            print(err)

        # logging
        end_time = datetime.now()
        self.master.status_component.set_and_log_status(
            f"video is ready! Taking total of {round((end_time - start_time).total_seconds(), 2)} seconds")

    def get_current_timestamp(self):
        return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def clean_up_temp_files(self):
        try:
            for f in glob.glob("*.mp4"):
                os.remove(f)
            for f in glob.glob("*.aac"):
                os.remove(f)
        except OSError:
            pass

    def calculate_output_resolutions(self):
        output_width = 0
        output_height = 0

        # Get information about the videos
        for video in self.video_list:
            cmd = f"ffprobe -v error -show_entries stream=width,height -of csv=p=0 {video}"
            output = subprocess.check_output(cmd, shell=True)
            width, height = output.decode().strip().split(",")
            output_width = max(output_width, int(width))
            output_height = max(output_height, int(height))

        self.master.status_component.set_and_log_status(
            f"output resolution is determined at {output_width} x {output_height}")

        return output_width, output_height
