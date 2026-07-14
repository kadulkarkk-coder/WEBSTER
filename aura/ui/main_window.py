import customtkinter as ctk

from aura.ui.theme import setup_theme

from aura.ui.layout import Layout


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        setup_theme()

        self.title("A.U.R.A.")

        self.geometry("1300x800")

        self.minsize(1100, 700)

        Layout(self).build()