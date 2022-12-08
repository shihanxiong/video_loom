import tkinter as tk
from tkinter import ttk
from windows import set_dpi_awareness

# set high resolution in windows 10
set_dpi_awareness()

# app config
root = tk.Tk()
root.title("Video Loom")
root.geometry("800x1000")

# app layout
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=20)
root.rowconfigure(1, weight=6)
root.rowconfigure(2, weight=1)


# videos input
video_component = ttk.Frame(root, padding=(10, 0))
video_component.grid(row=0, sticky="EW")

video_label = ttk.Label(video_component, text="Videos").pack()


# timeline
timeline_component = ttk.Frame(root, padding=(10, 0))
timeline_component.grid(row=1, sticky="EW")

timeline_label = ttk.Label(timeline_component, text="Timeline").pack()

timeline_text = tk.Text(timeline_component, height=20).pack()


# toolbar
toolbar_component = ttk.Frame(root, padding=(10, 0))
toolbar_component.grid(row=2, sticky="EW")

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
