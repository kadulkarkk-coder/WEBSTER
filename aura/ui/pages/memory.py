import customtkinter as ctk

class MemoryPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        label = ctk.CTkLabel(
            self,
            text="🧠 Memory",
            font=("Segoe UI",30,"bold")
        )

        label.pack(pady=50)