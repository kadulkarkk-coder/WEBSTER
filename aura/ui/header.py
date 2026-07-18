import customtkinter as ctk


class Header(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master, height=70)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(

            self,

            text="WEBSTER",

            font=("Segoe UI", 28, "bold")

        )

        title.grid(row=0, column=0, padx=20, pady=(12, 0))

        subtitle = ctk.CTkLabel(

            self,

            text="🕷️\nWhatever Every System Executes Reliably",

            font=("Segoe UI", 12)

        )

        subtitle.grid(row=1, column=0, padx=20, pady=(0, 10))