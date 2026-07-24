import customtkinter as ctk


class NewsPage(ctk.CTkFrame):

    def __init__(

        self,

        master

    ):

        super().__init__(

            master

        )

        label = ctk.CTkLabel(

            self,

            text="📰 Daily Brief\n\nComing Soon",

            font=(

                "Segoe UI",

                24,

                "bold"

            )

        )

        label.pack(

            expand=True

        )