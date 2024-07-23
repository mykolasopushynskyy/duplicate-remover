import os
import icons
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter import filedialog
from tkinter.constants import LEFT, BOTTOM, BOTH, RIGHT, Y, VERTICAL, X, W, TOP, SW, NW

BOTTOM_PANEL_BG_COLOR = "light grey"


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.default_bg = self["background"]
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, e):
        self.default_bg = self["background"]
        self.config(background="#d9d1cf")

    def on_leave(self, e):
        self.config(background=self.default_bg)


class FileExplorer(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # icon images
        self.folder_40 = icons.folder(40)
        self.minus = icons.minus()
        self.plus = icons.plus()

        self.idx = 1
        self.root = tk.Frame(self)
        self.top = tk.Frame(self.root)
        self.separator = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        self.bottom = tk.Frame(self.root, bg=BOTTOM_PANEL_BG_COLOR)

        self.add_button = tk.Button(self.bottom, image=self.plus, text="Add", compound=LEFT,
                                    command=self.browse_directory, highlightthickness=0, borderwidth=-1)

        self.remove_button = tk.Button(self.bottom, image=self.minus, text="Remove", compound=LEFT,
                                       command=self.remove_directory, highlightthickness=0, borderwidth=-1)

        self.canvas = tk.Canvas(self.top)
        self.frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self.top, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window(0, 0, window=self.frame)
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.root.pack(fill=BOTH, expand=True)

        self.top.pack(side=TOP, fill=BOTH, expand=True)
        self.separator.pack(side=TOP, fill=X, expand=False)
        self.bottom.pack(side=BOTTOM, fill=X, expand=False)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=False)

        self.add_button.pack(side=LEFT)
        self.remove_button.pack(side=LEFT)

    def browse_directory(self):
        home = os.path.expanduser("~")
        directory = filedialog.askdirectory(initialdir=home)
        if directory:
            self.add_directory(directory)

    def remove_directory(self):
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
        background = "systemTransparent" if idx % 2 == 1 else "grey85"

        frame = tk.Frame(self.frame, bg=background)
        frame.pack(fill=X, expand=False)

        icon_label = tk.Label(frame, image=self.folder_40, bg=background)
        icon_label.pack(side=LEFT, padx=5)

        name_label = tk.Label(frame, text=path, bg=background, font=("San Francisco", 12))
        name_label.pack(anchor=W)

        size_label = tk.Label(frame, text=f"Size: {size}", font=("San Francisco", 10), fg="grey", bg=background)
        size_label.pack(anchor=W)

        path_label = tk.Label(frame, text=date, font=("San Francisco", 10), fg="dodger blue", bg=background)
        path_label.pack(anchor=W)

    def get_folder_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return self.convert_size(total_size)

    @staticmethod
    def convert_size(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

    @staticmethod
    def date_format(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    window = tk.Tk()
    window.minsize(600, 400)
    explorer = FileExplorer(window, bg="white")

    explorer.pack(expand=True, fill=BOTH)
    window.mainloop()
