import tkinter as tk
from tkinter import ttk


# application status
class StatusFrame(ttk.Frame):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # variables
        self.status_variable = tk.StringVar(value="ready")

        # layouts
        self.rowconfigure(0, weight=1)

        status_label = ttk.Label(self, text="Process status:", padding=(10))
        status_label.grid(row=0, columnspan=1)

        status_text = ttk.Label(self, textvariable=self.status_variable, padding=(
            10), wraplength=(self.master.window_width - 250))
        status_text.grid(row=0, column=1, sticky="EW")

    def refresh(self):
        pass

    def set_and_log_status(self, status):
        self.status_variable.set(status)
        print(status)
