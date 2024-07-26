import customtkinter as tk

from tkinter import ttk, LEFT, BOTH, RIGHT, Y, VERTICAL, X, W, TOP, NORMAL, HORIZONTAL, BOTTOM

from model.pubsub import PubSubBroker
from view.folders_panel import FoldersPanel
from view.result_panel import ResultsPanel
from view.toolbar_panel import ToolbarPanel
from view.status_panel import StatusPanel


class RootPanel(tk.CTkFrame):
    def __init__(self, master: tk.CTk, pubsub: PubSubBroker, **kwargs):
        super().__init__(master, **kwargs)

        # toolbar frame
        self.toolbar_panel = ToolbarPanel(self, pubsub)
        self.toolbar_panel.pack(side=TOP, fill=X, expand=False)

        # separator
        self.top_separator = ttk.Separator(self, orient=HORIZONTAL)
        self.top_separator.pack(side=TOP, fill=X, expand=False)

        # main area frame
        self.middle = tk.CTkFrame(self, bg_color="grey90", fg_color="grey90")
        self.middle.pack(side=TOP, fill=BOTH, expand=True)

        # left main panel
        self.folders_to_scan = FoldersPanel(self.middle, pubsub, bg_color="grey90", fg_color="grey90")
        self.folders_to_scan.pack(side=LEFT, fill=Y, expand=False)

        # separator
        self.top_separator = ttk.Separator(self.middle, orient=VERTICAL)
        self.top_separator.pack(side=LEFT, fill=BOTH, expand=False)

        # right main panel
        self.results_panel = ResultsPanel(self.middle, pubsub, bg_color="grey90", fg_color="grey90")
        self.results_panel.pack(side=LEFT, fill=BOTH, expand=True)

        # status panel frame
        self.status_panel = StatusPanel(self, pubsub, height=18)
        self.status_panel.pack(side=BOTTOM, fill=X, expand=False, ipady=2)

        self.bottom_separator = ttk.Separator(self, orient=HORIZONTAL)
        self.bottom_separator.pack(side=BOTTOM, fill=X, expand=False)
