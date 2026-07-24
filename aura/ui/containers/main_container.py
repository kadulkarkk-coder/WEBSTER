import customtkinter as ctk


class MainContainer(

    ctk.CTkFrame

):

    def __init__(

        self,

        master

    ):

        super().__init__(

            master,

            fg_color="transparent"

        )

        self.grid_rowconfigure(

            1,

            weight=1

        )

        self.grid_columnconfigure(

            0,

            weight=1

        )