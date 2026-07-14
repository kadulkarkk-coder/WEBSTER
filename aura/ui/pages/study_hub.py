import customtkinter as ctk

class StudyHub(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        label = ctk.CTkLabel(
            self,
            text="📚 Study Hub",
            font=("Segoe UI",30,"bold")
        )

        label.pack(pady=50)