import customtkinter as ctk

class PluginsPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        label = ctk.CTkLabel(
            self,
            text="🔌 Plugins",
            font=("Segoe UI",30,"bold")
        )

        label.pack(pady=50)