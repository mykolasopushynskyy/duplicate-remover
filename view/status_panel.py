import customtkinter as tk
from tkinter import LEFT

from model.pubsub import PubSubBroker, Topic

DEFAULT_STATUS_TEXT = "···"


class StatusPanel(tk.CTkFrame):
    def __init__(self, master: tk.CTkFrame, pubsub: PubSubBroker, **kwargs):
        super().__init__(master, **kwargs)

        # subscribe to events
        self.pubsub = pubsub
        self.pubsub.subscribe(Topic.STATUS_MESSAGE_SET, self.set_message)

        # status panel elements
        self.name_label = tk.CTkLabel(self,
                                      text=DEFAULT_STATUS_TEXT,
                                      font=("San Francisco", 18),
                                      height=18)
        self.name_label.pack(side=LEFT, padx=10)

    def set_message(self, message):
        if message is None or len(message) == 0:
            self.name_label.configure(text=DEFAULT_STATUS_TEXT)
        else:
            self.name_label.configure(text=message)

