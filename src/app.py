import tkinter as tk
from tkinter import ttk
from windows import set_dpi_awareness

# set high resolution in windows 10
set_dpi_awareness()

# app config
root = tk.Tk()
root.title("Video Loom")
root.geometry("800x1000")
root.resizable(False, False)


# app layout
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=20)
root.rowconfigure(1, weight=3)
root.rowconfigure(2, weight=6)
root.rowconfigure(3, weight=1)


# videos input
video_component = ttk.Frame(root, padding=(10, 0))
video_component.grid(row=0, sticky="N")
video_component.rowconfigure(0, weight=0)
video_component.rowconfigure(1, weight=1)

video_label = ttk.Label(video_component, text="Videos")
video_label.grid(row=0)


# audio setting
audio_setting_component = ttk.Frame(root, padding=(10, 0))
audio_setting_component.grid(row=1, sticky="N")
audio_setting_component.rowconfigure(0, weight=0)
audio_setting_component.rowconfigure(1, weight=1)

audio_setting_label = ttk.Label(
    audio_setting_component, text="Audio Settings")
audio_setting_label.grid(row=0)


# timeline
timeline_component = ttk.Frame(root, padding=(10, 10))
timeline_component.grid(row=2, sticky="SEW")
timeline_component.rowconfigure(0, weight=0)
timeline_component.rowconfigure(1, weight=1)
timeline_component.columnconfigure(0, weight=1)
timeline_component.columnconfigure(1, weight=0)

timeline_label = ttk.Label(timeline_component, text="Timeline")
timeline_label.grid(row=0)

timeline_text = tk.Text(timeline_component, height=25)
timeline_text.grid(row=1, column=0)

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
