import tkinter as tk
from tkinter import ttk, filedialog as fd


# videos input
class VideoInputFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.video_list = []
        self.video_label_text = tk.StringVar(
            value=f"Videos {len(self.video_list)} of 2")

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
