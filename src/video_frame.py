import os
import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from video_import_frame import VideoImportFrame
from video_renderer_frame import VideoRendererFrame
from video_select_frame import VideoSelectFrame
from sys import platform
from time_utils import TimeUtils
from file_utils import FileUtils


# videos input
class VideoFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.components = []
        self.max_num_of_videos = 4
        self.video_list = []
        self.timeline_arr = []
        self.trimmed_video_list = []
        self.video_label_text = tk.StringVar(
            value=f"Videos {len(self.video_list)} of 4")
        self.output_directory = os.getcwd()
        self.file_utils = FileUtils()
        self.time_utils = TimeUtils()
        self.output_file_name = tk.StringVar(
            value=f"{self.time_utils.get_current_timestamp()}.mp4")
        self.output_width = 0
        self.output_height = 0
        self.is_filename_escaped = False

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

    def generate_video_with_ffmpeg(self):
        # remove output file if exists
        self.file_utils.clean_up_temp_files()

        # for win32|macOS, wrap the video path w/ quotes
        if self.is_filename_escaped == False:
            for idx, video in enumerate(self.video_list):
                self.video_list[idx] = self.file_utils.escape_file_name(video)
            self.is_filename_escaped = True

        # calculate output video resolution
        # this will scale all inputs to match the max width & max height
        self.calculate_output_resolutions()

        # logging
        start_time = datetime.now()
        print("generating video...")
        print(
            f'using audio track {self.master.audio_setting_component.audio_track_variable.get() + 1}')
        print("================timeline start================")
        print(self.master.timeline_component.get_timeline_text())
        print("================timeline end==================")

        # video processing
        try:
            # parse timeline
            self.timeline_arr = self.master.timeline_component.parse_timeline()

            # trim videos
            self.process_trimmed_videos()

            # concatenate trimmed videos
            output_file = self.concatenate_trimmed_videos()

            # get audio from selected video
            output_sound = self.process_audio()

            # combine video and audio into final file
            self.finalize_video(output_file, output_sound)
        except Exception as err:
            self.master.status_component.set_and_log_status(
                "An error occurred while generating video :(")
            print(err)

        # logging
        end_time = datetime.now()
        self.master.status_component.set_and_log_status(
            f"video is ready! Taking total of {round((end_time - start_time).total_seconds(), 2)} seconds")

    def calculate_output_resolutions(self):
        self.output_width = 0
        self.output_height = 0

        # Get information about the videos
        for video in self.video_list:
            cmd = f"ffprobe -v error -show_entries stream=width,height -of csv=p=0 {video}"
            output = subprocess.check_output(cmd, shell=True)
            width, height = output.decode().strip().split(",")
            self.output_width = max(self.output_width, int(width))
            self.output_height = max(self.output_height, int(height))

        self.master.status_component.set_and_log_status(
            f"output resolution is determined at {self.output_width} x {self.output_height}")

    def process_trimmed_videos(self):
        for idx, timeline in enumerate(self.timeline_arr):
            video, start, end = timeline.split(",")
            trimmed_output = os.path.join(
                self.output_directory, f"trimmed_{idx}.mp4")
            self.trimmed_video_list.append(trimmed_output)
            cmd = f"ffmpeg -i {self.video_list[int(video) - 1]} -ss {start} -to {end} -vf scale={self.output_width}:{self.output_height} -c:a copy {self.file_utils.escape_file_name(trimmed_output)}"
            subprocess.check_output(cmd, shell=True)
        self.master.status_component.set_and_log_status(
            "completed trimming videos")

    def concatenate_trimmed_videos(self):
        output_file = os.path.join(self.output_directory, "output.mp4")
        input_args = ""
        ffmpeg_filter = f"'[0:v][1:v]concat=n={len(self.trimmed_video_list)}:v=1:a=0'"

        for trimmed_video in self.trimmed_video_list:
            input_args += f"-i {self.file_utils.escape_file_name(trimmed_video)} "

        if platform == "win32":
            # remove the single quote ' if it's windows
            ffmpeg_filter = f"[0:v][1:v]concat=n={len(self.trimmed_video_list)}:v=1:a=0"

        cmd = f"ffmpeg {input_args} -filter_complex {ffmpeg_filter} -c:v libx264 -crf 23 -preset medium -y -vsync 2 {self.file_utils.escape_file_name(output_file)}"
        subprocess.check_output(cmd, shell=True)
        self.master.status_component.set_and_log_status(
            "completed concatenating trimmed videos")

        return output_file

    def process_audio(self):
        output_sound = os.path.join(self.output_directory, "audio.aac")
        cmd = f"ffmpeg -i {self.video_list[self.master.audio_setting_component.audio_track_variable.get()]} -vn -acodec copy {self.file_utils.escape_file_name(output_sound)}"
        subprocess.check_output(cmd, shell=True)
        self.master.status_component.set_and_log_status(
            "completed processing audio")

        return output_sound

    def finalize_video(self, output_file, output_sound):
        final_file = os.path.join(
            self.output_directory, f"{self.output_file_name.get()}.mp4")
        cmd = f"ffmpeg -i {self.file_utils.escape_file_name(output_file)} -i {self.file_utils.escape_file_name(output_sound)} -map 0:v -map 1:a -c copy -shortest -y -vsync 2 {self.file_utils.escape_file_name(final_file)}"
        subprocess.check_output(cmd, shell=True)
        self.master.status_component.set_and_log_status(
            "video is processed and ready for use")
