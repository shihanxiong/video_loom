import os
import tkinter as tk
from tkinter import ttk, filedialog as fd
from datetime import datetime
import ffmpeg


# videos input
class VideoInputFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.video_list = []
        self.video_label_text = tk.StringVar(
            value=f"Videos {len(self.video_list)} of 2")
        self.output_file_name = tk.StringVar(value="output.mp4")

        self.total_rows = 3
        self.total_columns = 2
        self.grid(row=0, sticky="N")
        for r_idx in range(self.total_rows):
            self.rowconfigure(r_idx, weight=1)
        for c_idx in range(self.total_columns):
            self.columnconfigure(c_idx, weight=1)

        # video import / clear
        video_label = ttk.Label(
            self, textvariable=self.video_label_text, padding=(10))
        video_label.grid(row=0, columnspan=2)
        self.video_import_button = ttk.Button(
            self, text="Import a video", padding=(10), command=self.select_file)
        self.video_import_button.grid(row=1, column=0, sticky="W")
        self.clear_video_list_button = ttk.Button(
            self, text="Clear video list", padding=(10), command=self.clear_video_list)
        self.clear_video_list_button.grid(row=1, column=1, sticky="E")

        # video rendering

        # video selection
        self.select_video_button_1 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.timeline_component.insert_timestamp(0))
        self.select_video_button_1.grid(row=3, column=0, sticky="S")
        self.select_video_button_2 = ttk.Button(self, text="Select", padding=(
            10), command=lambda: self.master.timeline_component.insert_timestamp(1))
        self.select_video_button_2.grid(row=3, column=1, sticky="S")

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
        if len(self.video_list) == 2:
            self.video_import_button["state"] = "disable"
            self.master.toolbar_component.generate_button["state"] = "enable"
        else:
            self.video_import_button["state"] = "enable"
            self.master.toolbar_component.generate_button["state"] = "disable"

    def clear_video_list(self):
        self.video_list = []
        self.refresh()
        self.master.status_component.set_and_log_status("video list cleared")

    def get_stream_audio(self):
        pts = "PTS-STARTPTS"
        stream = ffmpeg.input(os.path.abspath(
            self.video_list[self.master.audio_setting_component.audio_track_variable.get()]))
        audio = stream.filter_("asetpts", pts)
        return audio

    def generate_video(self):
        # logging
        start_time = datetime.now()
        print("generating video...")
        print(
            f'using audio track {self.master.audio_setting_component.audio_track_variable.get() + 1}')

        # remove output file if exists
        if os.path.exists(self.output_file_name.get()):
            os.remove(self.output_file_name.get())

        # get selected audio
        audio = self.get_stream_audio()

        # video processing
        try:
            stream = ffmpeg.input(os.path.abspath(self.video_list[0]))
            video = ffmpeg.hflip(stream)
            video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
            output = ffmpeg.output(
                video_and_audio, self.output_file_name.get(), format="mp4")
            ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            print("stdout:", e.stdout.decode("utf8"))
            print("stderr:", e.stderr.decode('utf8'))
            raise e

        # logging
        end_time = datetime.now()
        self.master.status_component.set_and_log_status(
            f"video is ready! Taking total of {round((end_time - start_time).total_seconds(), 2)} seconds")
