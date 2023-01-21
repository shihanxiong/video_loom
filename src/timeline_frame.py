import tkinter as tk
from tkinter import ttk, END


# timeline
class TimelineFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # frame config
        self.default_font = ("Courier", 14)

        timeline_label = ttk.Label(self, text="Timeline", padding=(10))
        timeline_label.grid(row=0)

        self.timeline_text = tk.Text(self, height=22, font=self.default_font)
        self.timeline_text.grid(row=1, column=0, sticky="EW")

        text_scroll = ttk.Scrollbar(
            self, orient="vertical", command=self.timeline_text.yview)
        text_scroll.grid(row=1, column=1, sticky="NS")
        self.timeline_text["yscrollcommand"] = text_scroll.set

    def refresh(self):
        pass

    def insert_timestamp(self, v_idx):
        self.timeline_text.insert(END, str(v_idx + 1) + "\n")

    def get_timeline_text(self):
        return self.timeline_text.get("1.0", END)
