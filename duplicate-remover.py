import os
import tkinter

import icons
import customtkinter as tk
from datetime import datetime
from customtkinter import filedialog
from tkinter import ttk, LEFT, BOTTOM, BOTH, RIGHT, Y, VERTICAL, X, W, TOP, SW, NW, DISABLED, NORMAL, HORIZONTAL

TOOLBAR_FG_COLOR = "transparent"
TOOLBAR_HOVER_COLOR = "gray75"
TOOLBAR_ICON_COLOR = (104, 104, 104)
TOOLBAR_HEADER_COLOR = "#343434"
TOOLBAR_BUTTON_HEIGHT = 30
TOOLBAR_BUTTON_WIDTH = 40

tk.set_appearance_mode("System")  # Modes: system (default), light, dark
tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(tk.CTk):
    def __init__(self):
        super().__init__()

        self.minsize(1000, 400)
        self.title("Duplicate remover")

        # center window on screen
        w = self.winfo_screenwidth() * 0.75
        h = self.winfo_screenheight() * 0.75
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # icon images
        self.folder_22 = icons.folder(26)

        self.idx = 1

        # root frame
        self.root = tk.CTkFrame(self)
        self.root.pack(fill=BOTH, expand=True)

        # toolbar frame
        self.toolbar_panel = tk.CTkFrame(self.root)
        self.toolbar_panel.pack(side=TOP, fill=X, expand=False)

        self.top_separator = ttk.Separator(self.root, orient=HORIZONTAL)
        self.top_separator.pack(side=TOP, fill=X, expand=False, pady=0)

        # main area frame
        self.middle = tk.CTkFrame(self.root, bg_color="grey90", fg_color="grey90")
        self.middle.pack(side=TOP, fill=BOTH, expand=True)

        self.left_panel = tk.CTkScrollableFrame(self.middle, bg_color="grey90", fg_color="grey90")
        self.left_panel.pack(side=LEFT, fill=BOTH, expand=True)

        self.top_separator = ttk.Separator(self.middle, orient=VERTICAL)
        self.top_separator.pack(side=LEFT, fill=Y, expand=False, pady=0)

        self.right_panel = tk.CTkScrollableFrame(self.middle, bg_color="grey90", fg_color="grey90")
        self.right_panel.pack(side=LEFT, fill=BOTH, expand=True)

        self.bottom_separator = ttk.Separator(self.root, orient=HORIZONTAL)
        self.bottom_separator.pack(side=TOP, fill=X, expand=False, pady=0)

        # status panel frame
        self.status_panel = tk.CTkFrame(self.root)
        self.status_panel.pack(side=TOP, fill=BOTH, expand=False)

        # toolbar elements
        self.add_button = tk.CTkButton(self.toolbar_panel,
                                       image=icons.plus(color=TOOLBAR_ICON_COLOR),
                                       text="",
                                       compound="top",
                                       command=self.browse_directory_to_compare,
                                       height=TOOLBAR_BUTTON_HEIGHT,
                                       width=TOOLBAR_BUTTON_WIDTH,
                                       fg_color=TOOLBAR_FG_COLOR,
                                       hover_color=TOOLBAR_HOVER_COLOR
                                       )
        self.add_button.pack(side=LEFT, padx=5, pady=5)

        self.remove_button = tk.CTkButton(self.toolbar_panel,
                                          image=icons.minus(color=TOOLBAR_ICON_COLOR),
                                          text="",
                                          compound="top",
                                          command=self.remove_directory,
                                          height=TOOLBAR_BUTTON_HEIGHT,
                                          width=TOOLBAR_BUTTON_WIDTH,
                                          fg_color=TOOLBAR_FG_COLOR,
                                          hover_color=TOOLBAR_HOVER_COLOR
                                          )
        self.remove_button.pack(side=LEFT, padx=5, pady=5)

        self.name_label = tk.CTkLabel(self.toolbar_panel,
                                      text="Duplicate remover",
                                      font=("San Francisco", 18),
                                      height=20,
                                      text_color=TOOLBAR_HEADER_COLOR)
        self.name_label.pack(side=LEFT, pady=2, padx=5)

        self.config_button = tk.CTkButton(self.toolbar_panel,
                                          image=icons.configs(color=TOOLBAR_ICON_COLOR),
                                          text="",
                                          command=self.remove_directory,
                                          height=TOOLBAR_BUTTON_HEIGHT,
                                          width=TOOLBAR_BUTTON_WIDTH,
                                          fg_color=TOOLBAR_FG_COLOR,
                                          hover_color=TOOLBAR_HOVER_COLOR
                                          )
        self.config_button.pack(side=RIGHT, padx=5, pady=5)

        self.destination_folder = tkinter.Variable(self.root, "")
        self.merge_folder_entry = tk.CTkEntry(self.toolbar_panel,
                                              height=TOOLBAR_BUTTON_HEIGHT,
                                              state=NORMAL,
                                              width=400,
                                              placeholder_text="Destination folder...",
                                              textvariable=self.destination_folder)
        self.merge_folder_entry.pack(side=RIGHT, pady=5)

        self.select_folder_button = tk.CTkButton(self.toolbar_panel,
                                                 image=icons.open_folder(color=TOOLBAR_ICON_COLOR),
                                                 text="",
                                                 command=self.browse_destination_directory,
                                                 height=TOOLBAR_BUTTON_HEIGHT,
                                                 width=TOOLBAR_BUTTON_WIDTH,
                                                 fg_color=TOOLBAR_FG_COLOR,
                                                 hover_color=TOOLBAR_HOVER_COLOR
                                                 )
        self.select_folder_button.pack(side=RIGHT, pady=5)

        self.run_button = tk.CTkButton(self.toolbar_panel,
                                       image=icons.run(color=TOOLBAR_ICON_COLOR),
                                       text="",
                                       compound="top",
                                       command=self.remove_directory,
                                       height=TOOLBAR_BUTTON_HEIGHT,
                                       width=TOOLBAR_BUTTON_WIDTH,
                                       fg_color=TOOLBAR_FG_COLOR,
                                       hover_color=TOOLBAR_HOVER_COLOR
                                       )
        self.run_button.pack(side=RIGHT, padx=5, pady=5)

        # status panel elements
        self.name_label = tk.CTkLabel(self.status_panel,
                                      text="···",
                                      font=("San Francisco", 18),
                                      height=18)
        self.name_label.pack(side=LEFT, padx=10)

    def browse_directory_to_compare(self, *args):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home)
        if directory is not None:
            self.add_directory(directory)

    def browse_destination_directory(self, *args):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home)
        if directory is not None and os.path.isdir(directory):
            self.destination_folder.set(directory)

    def remove_directory(self, *args):
        pass

    def add_directory(self, directory):
        # for widget in self.frame.winfo_children():
        #     widget.destroy()

        if os.path.isdir(directory):
            size = self.get_folder_size(directory)
            date = self.date_format(os.stat(directory).st_ctime)
            self.create_folder_entry(directory, size, date, self.idx)

            self.idx = self.idx + 1

    def create_folder_entry(self, path, size, date, idx):
        background = "grey90" if idx % 2 == 1 else "grey85"

        frame = tk.CTkFrame(self.left_panel, fg_color=background)
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

    def get_folder_size(self, path):
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return self.convert_size(total_size)
        except FileNotFoundError as e:
            return "unknown"

    @staticmethod
    def convert_size(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

    @staticmethod
    def date_format(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S")


if __name__ == "__main__":
    app = App()
    app.mainloop()
