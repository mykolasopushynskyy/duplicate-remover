import customtkinter as tk
from tkinter import LEFT, X, W, BOTH, RIGHT, TOP


class MultiEntry(tk.CTkFrame):
    def __init__(self, master, entries: list, bg_color, **kwargs):
        super().__init__(master, **kwargs)

        self.entries = entries

        for i, value in enumerate(self.entries):
            label = tk.CTkLabel(self, text=f"{i + 1}: {value}", font=("San Francisco", 10), height=14,
                                fg_color=bg_color, bg_color=bg_color)
            label.pack(anchor=W, pady=3, padx=5)


class ResultsPanel(tk.CTkScrollableFrame):
    def __init__(self, master: tk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        self.items = None
        self.root = tk.CTkFrame(self, bg_color="grey90", fg_color="grey90")
        self.root.pack(side=TOP, fill=BOTH, expand=True)

    def show_final_result(self, duplicates):
        self.items = [i for i in duplicates if len(i) > 1]
        self.items.sort(key=len, reverse=True)

        for i, entries in enumerate(self.items):
            bg_color = "grey90" if i % 2 == 1 else "grey85"
            multi_entry = MultiEntry(self.root, entries, bg_color=bg_color, fg_color=bg_color)
            multi_entry.pack(fill=X, expand=False, pady=(0, 5))

    def clear(self):
        self.root.destroy()
        self.root = tk.CTkFrame(self, bg_color="grey90", fg_color="grey90")
        self.root.pack(side=TOP, fill=BOTH, expand=True)
