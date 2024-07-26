import tkinter

import customtkinter as tk
from tkinter import LEFT, X, W, BOTH, RIGHT, TOP, END, Y, DISABLED, NORMAL, NONE, ttk, HORIZONTAL

from model.pubsub import PubSubBroker, Topic

# This is the list of all default command in the "Text" tag that modify the text
commandsToRemove = (
    "<Control-Key-h>",
    "<Meta-Key-Delete>",
    "<Meta-Key-BackSpace>",
    "<Meta-Key-d>",
    "<Meta-Key-b>",
    "<<Redo>>",
    "<<Undo>>",
    "<Control-Key-t>",
    "<Control-Key-o>",
    "<Control-Key-k>",
    "<Control-Key-d>",
    "<Key>",
    "<Key-Insert>",
    "<<PasteSelection>>",
    "<<Clear>>",
    "<<Paste>>",
    "<<Cut>>",
    "<Key-BackSpace>",
    "<Key-Delete>",
    "<Key-Return>",
    "<Control-Key-i>",
    "<Key-Tab>",
    "<Shift-Key-Tab>"
)


class ReadOnlyText(tkinter.Text):
    tagInit = False

    def __init__(self, master, **kwargs):
        tkinter.Text.__init__(self, master, **kwargs)
        if not ReadOnlyText.tagInit:
            self.init_tag()

        # Create a new binding table list, replace the default Text binding table by the ResultReadOnlyText one
        bindTags = tuple(tag if tag != "Text" else "ReadOnlyText" for tag in self.bindtags())
        self.bindtags(bindTags)

    def init_tag(self):
        """
        Just go through all binding for the Text widget.
        If the command is allowed, recopy it in the ROText binding table.
        """
        for key in self.bind_class("Text"):
            if key not in commandsToRemove:
                command = self.bind_class("Text", key)
                self.bind_class("ReadOnlyText", key, command)
        ReadOnlyText.tagInit = True


class ResultsPanel(tk.CTkFrame):
    def __init__(self, master: tk.CTkFrame, pubsub: PubSubBroker, **kwargs):
        super().__init__(master, **kwargs)

        # subscribe to events
        self.pubsub = pubsub
        self.pubsub.subscribe(Topic.SCANNING, self.scanning_change)
        self.pubsub.subscribe(Topic.RESULTS_ARRIVED, self.show_final_result)

        self.topLabel = tk.CTkLabel(self,
                                    font=("San Francisco", 10),
                                    text="Scan results",
                                    height=14,
                                    text_color="grey",
                                    anchor=W)
        self.topLabel.pack(side=TOP, fill=X, expand=False, padx=10)

        # separator
        self.top_separator = ttk.Separator(self, orient=HORIZONTAL)
        self.top_separator.pack(side=TOP, fill=X, expand=False)

        self.label_text = ReadOnlyText(self,
                                       font=("Courier New", 14),
                                       # text_color="black",
                                       # bg_color="grey85",
                                       # fg_color="grey85",
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
        text += "\n└───┴──────────────────────────────────────────────────────────────\n"

        self.label_text.insert(1.0, text)

    def scanning_change(self, is_scanning):
        if is_scanning:
            if self.label_text:
                self.label_text.delete(1.0, END)
