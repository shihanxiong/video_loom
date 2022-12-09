from sys import platform
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from windows import set_dpi_awareness


# methods
def select_file():
    filetypes = (
        ('video files', '*.mp4'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename != "":
        video_list.append(filename)
        showinfo(
            title='Selected File',
            message=filename
        )
        print(video_list)
        video_label.config(text=f"Videos {len(video_list)} of 2")


# app config
root = tk.Tk()
root.title("Video Loom")
root.geometry("800x1000")

if platform == "win32":
    set_dpi_awareness()  # set high resolution in windows 10
    root.resizable(False, False)  # this does not work on MacOS
if platform == "darwin":
    pass
else:
    pass


# app layout
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=20)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)


# variables
video_list = []
audio_track_variable = tk.IntVar()


# videos input
video_component = ttk.Frame(root, padding=(10, 0))
video_component.grid(row=0, sticky="N")
video_component.rowconfigure(0, weight=0)
video_component.rowconfigure(1, weight=1)

video_label = ttk.Label(
    video_component, text=f"Videos {len(video_list)} of 2")
video_label.grid(row=0)

video_import_button = ttk.Button(video_component, text="Import a video",
                                 padding=(10), command=select_file)
video_import_button.grid(row=1)


# audio setting
audio_setting_component = ttk.Frame(root, padding=(20, 0))
audio_setting_component.grid(row=1, sticky="NEW")
audio_setting_component.rowconfigure(0, weight=0)
audio_setting_component.rowconfigure(1, weight=1)
audio_setting_component.columnconfigure(0, weight=1)
audio_setting_component.columnconfigure(1, weight=1)

audio_setting_label = ttk.Label(
    audio_setting_component, text="Audio Settings")
audio_setting_label.grid(row=0, columnspan=3)

audio_track_option_1 = ttk.Radiobutton(
    audio_setting_component, text="Audio track 1", variable=audio_track_variable, value=0)
audio_track_option_2 = ttk.Radiobutton(
    audio_setting_component, text="Audio track 2", variable=audio_track_variable, value=1)
audio_track_option_1.grid(row=1, column=0, sticky="N")
audio_track_option_2.grid(row=1, column=1, sticky="N")


# timeline
timeline_component = ttk.Frame(root, padding=(10, 10))
timeline_component.grid(row=2, sticky="SEW")
timeline_component.rowconfigure(0, weight=0)
timeline_component.rowconfigure(1, weight=1)
timeline_component.columnconfigure(0, weight=1)
timeline_component.columnconfigure(1, weight=0)

timeline_label = ttk.Label(timeline_component, text="Timeline")
timeline_label.grid(row=0)

timeline_text = tk.Text(timeline_component, height=16)
timeline_text.grid(row=1, column=0, sticky="EW")

text_scroll = ttk.Scrollbar(
    timeline_component, orient="vertical", command=timeline_text.yview)
text_scroll.grid(row=1, column=1, sticky="NS")
timeline_text["yscrollcommand"] = text_scroll.set


# toolbar
toolbar_component = ttk.Frame(root, padding=(10, 0))
toolbar_component.grid(row=3, sticky="NEW")

toolbar_component.columnconfigure(0, weight=1)
toolbar_component.columnconfigure(1, weight=1)

generate_button = ttk.Button(
    toolbar_component, text="Generate Video", padding=(10))
generate_button.grid(row=0, column=0, sticky="EW")

quit_button = ttk.Button(toolbar_component, text="Quit",
                         padding=(10), command=root.destroy)
quit_button.grid(row=0, column=1, sticky="EW")


# app execution
root.mainloop()
