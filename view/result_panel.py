import customtkinter as tk
from tkinter import LEFT, X, W, BOTH, RIGHT, TOP, END, Y, DISABLED, NORMAL, NONE

from model.pubsub import PubSubBroker, Topic


class ResultsPanel(tk.CTkFrame):
    def __init__(self, master: tk.CTkFrame, pubsub: PubSubBroker, **kwargs):
        super().__init__(master, **kwargs)

        # subscribe to events
        self.pubsub = pubsub
        self.pubsub.subscribe(Topic.SCANNING, self.scanning_change)
        self.pubsub.subscribe(Topic.RESULTS_ARRIVED, self.show_final_result)

        # self.configure(fg_color="red")
        self.label_text = tk.CTkTextbox(self,
                                        font=("Courier New", 14),
                                        text_color="black",
                                        bg_color="grey85",
                                        fg_color="grey85",
                                        state=NORMAL,
                                        wrap=NONE
                                        )
        self.label_text.pack(side=TOP, fill=BOTH, expand=True)

    def show_final_result(self, duplicates):
        if len(duplicates) == 0:
            return

        text = "┌───┬──────────────────────────────────────────────────────────────\n"
        for i, entries in enumerate(duplicates):
            text += "\n".join([f"│{i + 1:<3}│ {value}" for i, value in enumerate(entries)])
            if i < len(duplicates) - 1:
                text += "\n├───┼──────────────────────────────────────────────────────────────\n"
        text += "\n└───┴──────────────────────────────────────────────────────────────"

        self.label_text.insert(1.0, text)

    def scanning_change(self, is_scanning):
        if is_scanning:
            if self.label_text:
                self.label_text.delete(1.0, END)
