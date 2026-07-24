import customtkinter as ctk


class FOMOPage(ctk.CTkFrame):

    def __init__(

        self,

        master

    ):

        super().__init__(

            master

        )

        label = ctk.CTkLabel(

            self,

            text="🔥 FOMO\n\nComing Soon",

            font=(

                "Segoe UI",

                24,

                "bold"

            )

        )

        label.pack(

            expand=True

        )