import customtkinter as ctk
from PIL import Image


class SplashScreen(ctk.CTkToplevel):

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master

    ):

        super().__init__(

            master

        )

        self.geometry(

            "300x600"

        )

        self.overrideredirect(

            True

        )

        self.configure(

            fg_color="#651e1e"

        )

        self.steps = [

            "Initializing Memory",

            "Initializing AI",

            "Loading Plugins",

            "Loading UI",

            "Preparing Spidey",

        ]

        self.current_step = 0

        self.current = 0

        self.dot_index = 0

        self._build()

        self.after(

            180,

            self.animate_dots

        )

    # ==================================================
    # UI
    # ==================================================

    def _build(

        self

    ):

        self.grid_rowconfigure(

            0,

            weight=1

        )

        self.grid_columnconfigure(

            0,

            weight=1

        )

        frame = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        frame.pack(

            fill=None

        )

        image = ctk.CTkImage(

            light_image=Image.open(

                "aura/assets/splash/splash.png"

            ),

            dark_image=Image.open(

                "aura/assets/splash/splash.png"

            ),

            size=(255,340)

        )

        logo = ctk.CTkLabel(

            frame,

            image=image,

            text=""

        )

        logo.image = image

        logo.pack(

            pady=(20,20)

        )

        self.loading_label = ctk.CTkLabel(

            frame,

            text="Loading...",

            font=(

                "Segoe UI",

                18,

                "bold"

            )

        )

        self.loading_label.pack()

        self.dots = ctk.CTkLabel(

            frame,

            text="● ○ ○ ○ ○",

            text_color="#7B0303",

            font=(

                "Segoe UI",

                22

            )

        )

        self.dots.pack(

            pady=15

        )

        version = ctk.CTkLabel(

            frame,

            text="Version 0.0.21",

            text_color="gray"

        )

        version.pack()

    # ==================================================
    # Update Loading Step
    # ==================================================

    def next_step(

        self

    ):

        if self.current_step >= len(

            self.steps

        ):

            return

        self.loading_label.configure(

            text=self.steps[

                self.current_step

            ]

        )

        self.current_step += 1

    # ==================================================
    # Loading Dots
    # ==================================================

    def animate_dots(

        self

    ):

        dots = [

            "○",

            "○",

            "○",

            "○",

            "○"

        ]

        index = self.dot_index % 5

        dots[index] = "●"

        self.dots.configure(

            text=" ".join(

                dots

            )

        )

        self.dot_index += 1

        self.after(

            180,

            self.animate_dots

        )

    # ==================================================
    # Finish
    # ==================================================

    def finish(

        self

    ):

        self.destroy()