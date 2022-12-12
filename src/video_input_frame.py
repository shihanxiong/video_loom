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

        self.grid(row=0, sticky="N")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        video_label = ttk.Label(
            self, textvariable=self.video_label_text, padding=(10))
        video_label.grid(row=0)
        self.video_import_button = ttk.Button(
            self, text="Import a video", padding=(10), command=self.select_file)
        self.video_import_button.grid(row=1)

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
            print(self.video_list)
            if len(self.video_list) == 2:
                self.video_import_button["state"] = "disable"
            self.video_label_text.set(f"Videos {len(self.video_list)} of 2")

    def generate_video(self):
        # logging
        start_time = datetime.now()
        print("generating video...")
        print(
            f'using audio track {self.master.audio_setting_component.audio_track_variable.get() + 1}')

        # remove output file if exists
        if os.path.exists(self.output_file_name.get()):
            os.remove(self.output_file_name.get())

        # video processing
        stream = ffmpeg.input(os.path.abspath(self.video_list[0]))
        stream = ffmpeg.hflip(stream)
        stream = ffmpeg.output(stream, self.output_file_name.get())
        try:
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            print("stdout:", e.stdout.decode("utf8"))
            print("stderr:", e.stderr.decode('utf8'))
            raise e

        # logging
        end_time = datetime.now()
        print(
            f"video is ready! Taking total of {(end_time - start_time).total_seconds()} seconds")
