import customtkinter as tk
from tkinter import LEFT, X, W

from view import icons


class FoldersPanel(tk.CTkScrollableFrame):
    def __init__(self, master: tk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        # icon images
        self.folder_22 = icons.folder(40)
        self.size = 0

    def update_folders(self, folders: dict):
        for element in self.winfo_children():
            element.destroy()

        for folder in list(folders.values()):
            self.create_folder_entry(folder.get("path"), folder.get("size"), folder.get("date"))

        self.size = 0

    def create_folder_entry(self, path, size, date):
        background = "grey90" if self.size % 2 == 0 else "grey85"

        frame = tk.CTkFrame(self, fg_color=background)
        frame.pack(fill=X, expand=False)

        icon_label = tk.CTkLabel(frame, text="", image=self.folder_22)
        icon_label.pack(side=LEFT, padx=5)

        name_label = tk.CTkLabel(frame, text=path, font=("San Francisco", 12), height=16, bg_color=background)
        name_label.pack(anchor=W, pady=2)

        size_label = tk.CTkLabel(frame, text=f"Size: {size}", font=("San Francisco", 10), height=14, text_color="grey",
                                 bg_color=background)
        size_label.pack(anchor=W, pady=2)

        path_label = tk.CTkLabel(frame, text=f"Date: {date}", font=("San Francisco", 10), height=14,
                                 text_color="dodger blue", bg_color=background)
        path_label.pack(anchor=W, pady=2)

        self.size = self.size + 1
