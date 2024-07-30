# import customtkinter as tk
# from tkinter import BOTH
#
# from model.model import PubSubBroker
# from view.root_panel import RootPanel
#
# tk.set_appearance_mode("System")
# tk.set_default_color_theme("blue")
#
#
# # TODO Implement proper menus for this application
# # TODO Disable views during search like toolbar, folder list, etc
# class ApplicationView(tk.CTk):
#     def __init__(self, pubsub: PubSubBroker):
#         super().__init__()
#
#         self.minsize(1000, 400)
#         self.title("Duplicate remover")
#
#         # center window on screen
#         self.window_corner_radius = 10
#         w = self.winfo_screenwidth() * 0.50
#         h = self.winfo_screenheight() * 0.50
#         ws = self.winfo_screenwidth()
#         hs = self.winfo_screenheight()
#         x = (ws / 2) - (w / 2)
#         y = (hs / 2) - (h / 2)
#         self.geometry("%dx%d+%d+%d" % (w, h, x, y))
#
#         # root frame
#         self.root = RootPanel(self, pubsub)
#         self.root.pack(fill=BOTH, expand=True)
