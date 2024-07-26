import customtkinter as tk
from tkinter import LEFT, RIGHT

from model import events
from model.pubsub import PubSubBroker
from view import (
    TOOLBAR_ICON_COLOR,
    TOOLBAR_BUTTON_HEIGHT,
    TOOLBAR_BUTTON_WIDTH,
    TOOLBAR_FG_COLOR,
    TOOLBAR_HOVER_COLOR,
    TOOLBAR_HEADER_COLOR,
    ARROW,
)
from util import icons


class SelectFolderButton(tk.CTkFrame):
    def __init__(
        self,
        master: tk.CTkFrame,
        command=None,
        text="Destination folder...",
        *args,
        **kwargs
    ):
        super().__init__(master, *args, **kwargs)

        self.command = command

        self.select_folder_icon = tk.CTkLabel(
            self,
            image=icons.open_folder(color=TOOLBAR_ICON_COLOR),
            text="",
            compound="top",
            height=TOOLBAR_BUTTON_HEIGHT,
            width=TOOLBAR_BUTTON_WIDTH,
            fg_color=TOOLBAR_FG_COLOR,
        )
        self.select_folder_icon.pack(side=LEFT, padx=(5, 0))

        self.select_folder_label = tk.CTkLabel(
            self,
            text=text,
            corner_radius=5,
            height=TOOLBAR_BUTTON_HEIGHT - 10,
            width=400,
            anchor="w",
            fg_color="white",
            bg_color=TOOLBAR_FG_COLOR,
        )
        self.select_folder_label.pack(side=LEFT, padx=(0, 5), expand=True)

        self.bind("<Button-1>", self.command)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.select_folder_label.bind("<Button-1>", self.command)
        self.select_folder_label.bind("<Enter>", self.on_enter)
        self.select_folder_label.bind("<Leave>", self.on_leave)

        self.select_folder_icon.bind("<Button-1>", self.command)
        self.select_folder_icon.bind("<Enter>", self.on_enter)
        self.select_folder_icon.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(fg_color=TOOLBAR_HOVER_COLOR)

    def on_leave(self, enter):
        self.configure(fg_color=TOOLBAR_FG_COLOR)

    def configure(self, **kwargs):
        if "text" in kwargs:
            self.select_folder_label.configure(text=kwargs.pop("text"))

        super().configure(**kwargs)


class ToolbarPanel(tk.CTkFrame):
    def __init__(self, master: tk.CTkFrame, pubsub: PubSubBroker, **kwargs):
        super().__init__(master, **kwargs)

        # subscribe to events
        self.pubsub = pubsub
        self.pubsub.subscribe(
            events.MERGE_FOLDER_CHANGED, self.set_destination_directory
        )

        self.name_label = tk.CTkLabel(
            self,
            text="Duplicate remover",
            font=("San Francisco", 18),
            height=20,
            text_color=TOOLBAR_HEADER_COLOR,
        )
        self.name_label.pack(side=LEFT, pady=2, padx=(10, 5))

        self.add_button = tk.CTkButton(
            self,
            image=icons.plus(color=TOOLBAR_ICON_COLOR),
            text="",
            compound="top",
            height=TOOLBAR_BUTTON_HEIGHT,
            width=TOOLBAR_BUTTON_WIDTH,
            fg_color=TOOLBAR_FG_COLOR,
            hover_color=TOOLBAR_HOVER_COLOR,
            command=self.add_new_folder,
            cursor=ARROW,
        )
        self.add_button.pack(side=LEFT, padx=(0, 5), pady=5)

        self.config_button = tk.CTkButton(
            self,
            image=icons.configs(color=TOOLBAR_ICON_COLOR),
            text="",
            compound="top",
            height=TOOLBAR_BUTTON_HEIGHT,
            width=TOOLBAR_BUTTON_WIDTH,
            fg_color=TOOLBAR_FG_COLOR,
            hover_color=TOOLBAR_HOVER_COLOR,
            cursor=ARROW,
        )
        self.config_button.pack(side=RIGHT, padx=(0, 5), pady=5)

        # pick folder frame
        self.select_folder_button = SelectFolderButton(
            self,
            command=self.select_folder,
            text="Destination folder...",
            fg_color=TOOLBAR_FG_COLOR,
            height=TOOLBAR_BUTTON_HEIGHT,
        )
        self.select_folder_button.pack(side=RIGHT, padx=(0, 5), pady=5)

        self.scan_button = tk.CTkButton(
            self,
            image=icons.run(color=TOOLBAR_ICON_COLOR),
            text="",
            compound="top",
            height=TOOLBAR_BUTTON_HEIGHT,
            width=TOOLBAR_BUTTON_WIDTH,
            fg_color=TOOLBAR_FG_COLOR,
            hover_color=TOOLBAR_HOVER_COLOR,
            command=self.scan,
            cursor=ARROW,
        )
        self.scan_button.pack(side=RIGHT, padx=(0, 5), pady=5)

    def set_destination_directory(self, text: str):
        self.select_folder_button.configure(text=text)

    def add_new_folder(self):
        self.pubsub.publish(events.ADD_FOLDER_PRESSED, None)

    def select_folder(self, *args):
        self.pubsub.publish(events.SELECT_FOLDER_PRESSED, None)

    def scan(self, *args):
        self.pubsub.publish(events.SCAN_DUPLICATES_PRESSED, None)
