from sys import platform
import tkinter as tk
from tkinter import ttk, END, filedialog as fd
from tkinter.messagebox import showinfo
from windows import set_dpi_awareness
from video import generate_video
from video_input_frame import VideoInputFrame
from audio_setting_frame import AudioSettingFrame


class VideoLoom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_configure()
        self.title("Video Loom - v1.0-beta")
        self.geometry("800x1000")

        # app layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # components
        self.video_component = VideoInputFrame(self, padding=(10, 0))
        self.audio_setting_component = AudioSettingFrame(self, padding=(20, 0))

    def app_configure(self):
        if platform == "win32":
            set_dpi_awareness()  # set high resolution in windows 10
            self.resizable(False, False)  # this does not work on MacOS
        elif platform == "darwin":
            pass
        else:
            pass


# methods
def insert_timestamp(e):
    timeline_text.insert(END, e.char + "\n")


# app config
root = VideoLoom()
default_font = ("Courier", 14)
s = ttk.Style()
s.configure('.', font=default_font)


# timeline
timeline_component = ttk.Frame(root, padding=(10, 10))
timeline_component.grid(row=2, sticky="SEW")
timeline_component.rowconfigure(0, weight=0)
timeline_component.rowconfigure(1, weight=1)
timeline_component.columnconfigure(0, weight=1)
timeline_component.columnconfigure(1, weight=0)

timeline_label = ttk.Label(timeline_component, text="Timeline", padding=(10))
timeline_label.grid(row=0)

timeline_text = tk.Text(timeline_component, height=16, font=default_font)
timeline_text.grid(row=1, column=0, sticky="EW")

text_scroll = ttk.Scrollbar(
    timeline_component, orient="vertical", command=timeline_text.yview)
text_scroll.grid(row=1, column=1, sticky="NS")
timeline_text["yscrollcommand"] = text_scroll.set

for i in range(1, 3):
    root.bind(str(i), insert_timestamp)


# toolbar
toolbar_component = ttk.Frame(root, padding=(10, 0))
toolbar_component.grid(row=3, sticky="NEW")

toolbar_component.columnconfigure(0, weight=1)
toolbar_component.columnconfigure(1, weight=1)

generate_button = ttk.Button(
    toolbar_component, text="Generate Video", padding=(10), command=generate_video)
generate_button.grid(row=0, column=0, sticky="EW")

quit_button = ttk.Button(toolbar_component, text="Quit",
                         padding=(10), command=root.destroy)
quit_button.grid(row=0, column=1, sticky="EW")


# app execution
root.mainloop()
