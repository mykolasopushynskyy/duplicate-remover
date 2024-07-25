import customtkinter as tk
from tkinter import LEFT

DEFAULT_STATUS_TEXT = "···"


class StatusPanel(tk.CTkFrame):
    def __init__(self, master: tk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        # status panel elements
        self.name_label = tk.CTkLabel(self,
                                      text=DEFAULT_STATUS_TEXT,
                                      font=("San Francisco", 18),
                                      height=18)
        self.name_label.pack(side=LEFT, padx=10)

    def set_message(self, data):
        if data.text is None or len(data.text) == 0:
            self.name_label.configure(text=DEFAULT_STATUS_TEXT, text_color=data.text_color)
        else:
            self.name_label.configure(text=data.text, text_color=data.text_color)

