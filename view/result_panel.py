# import customtkinter as tk
# from tkinter import (
#     X,
#     W,
#     BOTH,
#     TOP,
#     END,
#     NONE,
#     ttk,
#     HORIZONTAL,
# )
#
# from model import events
# from model.pubsub import PubSubBroker
#
# ODD_TAG = "odd"
# EVEN_TAG = "even"
#
# # This is the list of all default command in the "Text" tag that modify the text
# COMMANDS_TO_REMOVE = (
#     "<Control-Key-h>",
#     "<Meta-Key-Delete>",
#     "<Meta-Key-BackSpace>",
#     "<Meta-Key-d>",
#     "<Meta-Key-b>",
#     "<<Redo>>",
#     "<<Undo>>",
#     "<Control-Key-t>",
#     "<Control-Key-o>",
#     "<Control-Key-k>",
#     "<Control-Key-d>",
#     "<Key>",
#     "<Key-Insert>",
#     "<<PasteSelection>>",
#     "<<Clear>>",
#     "<<Paste>>",
#     "<<Cut>>",
#     "<Key-BackSpace>",
#     "<Key-Delete>",
#     "<Key-Return>",
#     "<Control-Key-i>",
#     "<Key-Tab>",
#     "<Shift-Key-Tab>",
# )
#
#
# class ReadOnlyText(tk.CTkTextbox):
#     is_tag_initialized = False
#
#     def __init__(self, master, **kwargs):
#         tk.CTkTextbox.__init__(self, master, **kwargs)
#         if not ReadOnlyText.is_tag_initialized:
#             self.initialize_tag()
#
#         # Create a new binding table list, replace the default Text binding table by the ResultReadOnlyText one
#         bindTags = tuple(
#             tag if tag != "Text" else "ReadOnlyText" for tag in self._textbox.bindtags()
#         )
#         self._textbox.bindtags(bindTags)
#
#     def initialize_tag(self):
#         """
#         Just go through all binding for the Text widget.
#         If the command is allowed, recopy it in the ROText binding table.
#         """
#         for key in self._textbox.bind_class("Text"):
#             if key not in COMMANDS_TO_REMOVE:
#                 command = self._textbox.bind_class("Text", key)
#                 self._textbox.bind_class("ReadOnlyText", key, command)
#         ReadOnlyText.is_tag_initialized = True
#
#
# class ResultsPanel(tk.CTkFrame):
#     def __init__(self, master: tk.CTkFrame, pubsub: PubSubBroker, **kwargs):
#         super().__init__(master, **kwargs)
#
#         # subscribe to events
#         self.pubsub = pubsub
#         self.pubsub.subscribe(events.SCANNING, self.scanning_change)
#         self.pubsub.subscribe(events.RESULTS_ARRIVED, self.show_final_result)
#
#         self.topLabel = tk.CTkLabel(
#             self,
#             font=("San Francisco", 12),
#             text="Scan results",
#             height=14,
#             text_color="black",
#             anchor=W,
#         )
#         self.topLabel.pack(side=TOP, fill=X, expand=False, padx=10)
#
#         # separator
#         self.top_separator = ttk.Separator(self, orient=HORIZONTAL)
#         self.top_separator.pack(side=TOP, fill=X, expand=False)
#
#         self.label_text = ReadOnlyText(
#             self,
#             font=("Courier New", 14),
#             text_color="black",
#             bg_color="grey85",
#             fg_color="grey85",
#             wrap=NONE,
#         )
#         self.label_text.pack(side=TOP, fill=BOTH, expand=True)
#
#         self.label_text.tag_config(EVEN_TAG, background="#e0e0e0")
#         self.label_text.tag_lower(EVEN_TAG)
#         self.label_text.tag_config(ODD_TAG, background="#ffffff")
#         self.label_text.tag_lower(ODD_TAG)
#
#     def show_final_result(self, duplicates):
#         if len(duplicates) == 0:
#             return
#
#         tag = ODD_TAG
#         for i, entries in enumerate(duplicates):
#             text = "\n".join([f"{value}" for i, value in enumerate(entries)]) + "\n"
#             self.label_text.insert(END, text, tag)
#             tag = EVEN_TAG if tag == ODD_TAG else ODD_TAG
#
#     def scanning_change(self, is_scanning):
#         if is_scanning:
#             if self.label_text:
#                 self.label_text.delete(1.0, END)
