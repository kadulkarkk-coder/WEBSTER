import customtkinter as ctk


class StatusBar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master, height=30)

        label = ctk.CTkLabel(

            self,

            text="Ready | AI ● | Mic ○ | Camera ○ | Internet ●"

        )

        label.pack(side="left", padx=15)