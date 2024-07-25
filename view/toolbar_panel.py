import customtkinter as tk
from tkinter import LEFT, RIGHT

from view import icons, TOOLBAR_ICON_COLOR, TOOLBAR_BUTTON_HEIGHT, TOOLBAR_BUTTON_WIDTH, TOOLBAR_FG_COLOR, \
    TOOLBAR_HOVER_COLOR, TOOLBAR_HEADER_COLOR


class SelectFolderButton(tk.CTkFrame):
    def __init__(self, master: tk.CTkFrame, command=None, text="Destination folder...", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.command = command

        self.select_folder_icon = tk.CTkLabel(self,
                                              image=icons.open_folder(color=TOOLBAR_ICON_COLOR),
                                              text="",
                                              compound="top",
                                              height=TOOLBAR_BUTTON_HEIGHT,
                                              width=TOOLBAR_BUTTON_WIDTH,
                                              fg_color=TOOLBAR_FG_COLOR,
                                              )
        self.select_folder_icon.pack(side=LEFT, padx=5)

        self.select_folder_label = tk.CTkLabel(self,
                                               text=text,
                                               corner_radius=5,
                                               height=TOOLBAR_BUTTON_HEIGHT - 10,
                                               width=400,
                                               anchor="w",
                                               fg_color="white",
                                               bg_color=TOOLBAR_FG_COLOR,
                                               )
        self.select_folder_label.pack(side=LEFT, padx=5, expand=True)

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
        if "command" in kwargs:
            self.command = kwargs.pop("command")
            self.unbind("<Button-1>")
            self.bind("<Button-1>", self.command)
            self.select_folder_label.unbind("<Button-1>")
            self.select_folder_label.bind("<Button-1>", self.command)
            self.select_folder_icon.unbind("<Button-1>")
            self.select_folder_icon.bind("<Button-1>", self.command)

        if "text" in kwargs:
            self.select_folder_label.configure(text=kwargs.pop("text"))

        super().configure(self, **kwargs)


class ToolbarPanel(tk.CTkFrame):
    def __init__(self, master: tk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)

        self.name_label = tk.CTkLabel(self,
                                      text="Duplicate remover",
                                      font=("San Francisco", 18),
                                      height=20,
                                      text_color=TOOLBAR_HEADER_COLOR)
        self.name_label.pack(side=LEFT, pady=2, padx=5)

        self.add_button = tk.CTkButton(self,
                                       image=icons.plus(color=TOOLBAR_ICON_COLOR),
                                       text="",
                                       compound="top",
                                       height=TOOLBAR_BUTTON_HEIGHT,
                                       width=TOOLBAR_BUTTON_WIDTH,
                                       fg_color=TOOLBAR_FG_COLOR,
                                       hover_color=TOOLBAR_HOVER_COLOR
                                       )
        self.add_button.pack(side=LEFT, padx=5, pady=5)

        self.remove_button = tk.CTkButton(self,
                                          image=icons.minus(color=TOOLBAR_ICON_COLOR),
                                          text="",
                                          compound="top",
                                          height=TOOLBAR_BUTTON_HEIGHT,
                                          width=TOOLBAR_BUTTON_WIDTH,
                                          fg_color=TOOLBAR_FG_COLOR,
                                          hover_color=TOOLBAR_HOVER_COLOR
                                          )
        self.remove_button.pack(side=LEFT, padx=5, pady=5)

        self.config_button = tk.CTkButton(self,
                                          image=icons.configs(color=TOOLBAR_ICON_COLOR),
                                          text="",
                                          compound="top",
                                          height=TOOLBAR_BUTTON_HEIGHT,
                                          width=TOOLBAR_BUTTON_WIDTH,
                                          fg_color=TOOLBAR_FG_COLOR,
                                          hover_color=TOOLBAR_HOVER_COLOR
                                          )
        self.config_button.pack(side=RIGHT, padx=5, pady=5)

        # pick folder frame
        self.select_folder_button = SelectFolderButton(self,
                                                       text="Destination folder...",
                                                       fg_color=TOOLBAR_FG_COLOR,
                                                       height=TOOLBAR_BUTTON_HEIGHT)
        self.select_folder_button.pack(side=RIGHT, padx=5, pady=5)

        self.run_button = tk.CTkButton(self,
                                       image=icons.run(color=TOOLBAR_ICON_COLOR),
                                       text="",
                                       compound="top",
                                       height=TOOLBAR_BUTTON_HEIGHT,
                                       width=TOOLBAR_BUTTON_WIDTH,
                                       fg_color=TOOLBAR_FG_COLOR,
                                       hover_color=TOOLBAR_HOVER_COLOR
                                       )
        self.run_button.pack(side=RIGHT, padx=5, pady=5)

    def set_destination_directory(self, text: str):
        self.select_folder_button.configure(text=text)
