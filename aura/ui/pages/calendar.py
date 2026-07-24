import customtkinter as ctk


class CalendarPage(ctk.CTkFrame):

    def __init__(

        self,

        master

    ):

        super().__init__(

            master

        )

        label = ctk.CTkLabel(

            self,

            text="📅 Calendar\n\nComing Soon",

            font=(

                "Segoe UI",

                24,

                "bold"

            )

        )

        label.pack(

            expand=True

        )