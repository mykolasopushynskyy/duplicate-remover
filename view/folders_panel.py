import customtkinter as tk
from tkinter import LEFT, X, W, BOTH, RIGHT

from model import TOOLBAR_WINDOW_BUTTON_SIZE, TOOLBAR_WINDOW_BUTTON_RADIUS, TOOLBAR_WINDOW_BUTTON_CLOSE_COLOR
from model.pubsub import Topic, PubSubBroker
from view import icons, ARROW, TOOLBAR_HOVER_COLOR, TOOLBAR_FG_COLOR


class FolderEntry(tk.CTkFrame):
    def __init__(self, master, path, size, date, image, remove_item_callback: callable, bg_color=None, **kwargs):
        super().__init__(master, **kwargs)

        self.path = path

        self.icon_label = tk.CTkLabel(self, text="", image=image)
        self.icon_label.pack(side=LEFT, padx=5)

        self.path_label = tk.CTkLabel(self, text=path, font=("San Francisco", 12), height=16, bg_color=bg_color)
        self.path_label.pack(anchor=W, pady=2)

        self.size_label = tk.CTkLabel(self, text=f"Size: {size}", font=("San Francisco", 10), height=14,
                                      text_color="grey",
                                      bg_color=bg_color)
        self.size_label.pack(anchor=W, pady=2)

        self.date_label = tk.CTkLabel(self, text=f"Date: {date}", font=("San Francisco", 10), height=14,
                                      text_color="dodger blue", bg_color=bg_color)
        self.date_label.pack(anchor=W, pady=2)

        self.remove_button = tk.CTkButton(self,
                                          text="",
                                          compound="top",
                                          height=TOOLBAR_WINDOW_BUTTON_SIZE,
                                          width=TOOLBAR_WINDOW_BUTTON_SIZE,
                                          fg_color=TOOLBAR_HOVER_COLOR,
                                          bg_color=TOOLBAR_FG_COLOR,
                                          hover_color=TOOLBAR_WINDOW_BUTTON_CLOSE_COLOR,
                                          cursor=ARROW,
                                          corner_radius=TOOLBAR_WINDOW_BUTTON_RADIUS,
                                          command=lambda: remove_item_callback(self.path)
                                          )
        self.remove_button.place(x=-4, relx=1.0, y=4, anchor="ne")

        self.bind_common(self, self.icon_label, self.path_label, self.size_label, self.date_label)

    def bind_common(self, *args):
        for e in args:
            e.bind("<Enter>", self.on_enter)
            e.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.remove_button.configure(fg_color=TOOLBAR_WINDOW_BUTTON_CLOSE_COLOR)

    def on_leave(self, enter):
        self.remove_button.configure(fg_color=TOOLBAR_HOVER_COLOR)

    def set_value(self, path, size, date, image, bg_color):
        self.path = path

        self.configure(fg_color=bg_color, bg_color=bg_color)
        self.icon_label.configure(image=image)
        self.path_label.configure(text=self.path, bg_color=bg_color)
        self.size_label.configure(text=f"Size: {size}", bg_color=bg_color)
        self.date_label.configure(text=f"Date: {date}", bg_color=bg_color)


class FoldersPanel(tk.CTkScrollableFrame):
    def __init__(self, master: tk.CTkFrame, pubsub: PubSubBroker, **kwargs):
        super().__init__(master, **kwargs)

        # subscribe to events
        self.pubsub = pubsub
        self.pubsub.subscribe(Topic.FOLDERS_TO_SCAN_CHANGED, self.update_folders)

        # elements
        self.elements = []

        # icon images
        self.folder_22 = icons.folder(40)

    def update_folders(self, folders: dict):

        folders = list(folders.values())
        for idx, folder in enumerate(folders):
            path = folder.get("path")
            size = folder.get("size")
            date = folder.get("date")
            color = "grey90" if idx % 2 == 0 else "grey85"

            if idx < len(self.elements):
                self.elements[idx].set_value(path, size, date, self.folder_22, color)
            else:
                self.add_folder_entry(path, size, date)

        if len(self.elements) > len(folders):
            elements_to_remove = self.elements[len(folders):len(self.elements)]

            for element in elements_to_remove:
                element.destroy()

            self.elements = [e for e in self.elements if e not in elements_to_remove]

    def add_folder_entry(self, path, size, date):
        idx = len(self.elements)
        color = "grey90" if idx % 2 == 0 else "grey85"

        def remove_folder_entry(abs_path): self.pubsub.publish(Topic.REMOVE_FOLDER_PRESSED, abs_path)
        entry = FolderEntry(self, path, size, date, self.folder_22, remove_folder_entry, fg_color=color, bg_color=color)
        entry.pack(fill=X, expand=False)

        self.elements.append(entry)

