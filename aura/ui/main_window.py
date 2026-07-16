import customtkinter as ctk

from aura.ui.theme import setup_theme
from aura.ui.layout import Layout


class MainWindow(ctk.CTk):

    def __init__(self, services):

        super().__init__()

        # -----------------------------
        # Store Services
        # -----------------------------

        self.services = services

        # -----------------------------
        # Theme
        # -----------------------------

        setup_theme()

        # -----------------------------
        # Window Configuration
        # -----------------------------

        self.title("A.U.R.A.")

        self.geometry("1400x900")

        self.minsize(1200, 750)

        # -----------------------------
        # Build UI
        # -----------------------------

        self.layout = Layout(
            root=self,
            services=self.services
        )

        self.layout.build()

        # -----------------------------
        # Window Close
        # -----------------------------

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    # ---------------------------------

    def on_close(self):

        print("Closing AURA...")

        self.destroy()