import customtkinter as tk
from tkinter import LEFT, X, W, BOTH, RIGHT, TOP

from model.pubsub import PubSubBroker, Topic


class ResultsPanel(tk.CTkScrollableFrame):
    def __init__(self, master: tk.CTkFrame, pubsub:PubSubBroker, **kwargs):
        super().__init__(master, **kwargs)

        # subscribe to events
        self.pubsub = pubsub
        self.pubsub.subscribe(Topic.SCANNING, self.scanning_change)
        self.pubsub.subscribe(Topic.RESULTS_ARRIVED, self.show_final_result)

        self.root = tk.CTkFrame(self, bg_color="grey90", fg_color="grey90")
        self.root.pack(side=TOP, fill=BOTH, expand=True)

        self.label_text = None

    def show_final_result(self, duplicates):

        bg_color = "grey85"
        text = "┌───┬──────────────────────────────────────────────────────────────\n"
        for i, entries in enumerate(duplicates):
            text += "\n".join([f"│{i + 1:<3}│ {value}" for i, value in enumerate(entries)])
            if i < len(duplicates) - 1:
                text += "\n├───┼──────────────────────────────────────────────────────────────\n"
        text += "\n└───┴──────────────────────────────────────────────────────────────"

        self.label_text = tk.CTkLabel(self.root,
                                      text=text,
                                      font=("Courier New", 14),
                                      text_color="black",
                                      height=14,
                                      justify=LEFT,
                                      bg_color=bg_color,
                                      fg_color=bg_color,
                                      anchor=W
                                      )
        self.label_text.pack(fill=X, expand=False, anchor=W, pady=5, padx=5, ipadx=5)

    def scanning_change(self, is_scanning):
        if is_scanning:
            if self.label_text:
                self.label_text.destroy()
