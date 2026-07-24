import customtkinter as ctk


class SpideyCore(ctk.CTkFrame):

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(

        self,

        master,

        size=120

    ):

        super().__init__(

            master,

            fg_color="transparent"

        )

        self.size = size

        self.state = "idle"

        self.animation_job = None

        self.pulse_up = True

        self.current_size = size

        self.colors = {

            "idle": "#7B0303",

            "thinking": "#7B0303",

            "listening": "#1976D2",

            "speaking": "#8E44AD",

            "offline": "#777777",

            "sleeping": "#555555",

            "error": "#FF6B35"

        }

        self.build()

        self.start_animation()

    # ==========================================
    # UI
    # ==========================================

    def build(

        self

    ):

        self.glow = ctk.CTkFrame(

            self,

            width=self.size + 34,

            height=self.size + 34,

            corner_radius=(self.size + 34) // 2,

            fg_color="#250000"

        )

        self.glow.pack(

            padx=15,

            pady=15

        )

        self.ring = ctk.CTkFrame(

            self.glow,

            width=self.size + 16,

            height=self.size + 16,

            corner_radius=(self.size + 16) // 2,

            fg_color="#4A0000"

        )

        self.ring.place(

            relx=0.5,

            rely=0.5,

            anchor="center"

        )

        self.orb = ctk.CTkFrame(

           self.ring,

           width=self.size,

           height=self.size,

           corner_radius=self.size // 2,

           fg_color=self.colors["idle"]

        )

        self.orb.place(

            relx=0.5,

            rely=0.5,

            anchor="center"

        )

    # ==========================================
    # State
    # ==========================================

    def set_state(

        self,

        state

    ):

        self.state = state

        color = self.colors.get(

            state,

            self.colors["idle"]

        )

        self.orb.configure(

            fg_color=color

        )

        if state == "thinking":

            self.glow.configure(

                fg_color="#2B0000"

            )

            self.ring.configure(

               fg_color="#550000"

           )

        elif state == "listening":

            self.glow.configure(

                fg_color="#001B38"

            )

            self.ring.configure(

                fg_color="#0D47A1"

           )

        elif state == "speaking":

            self.glow.configure(

                fg_color="#2A0038"

            )

            self.ring.configure(

                fg_color="#7B1FA2"

            )

        elif state == "offline":

            self.glow.configure(

               fg_color="#222222"
 
            )

            self.ring.configure(

                fg_color="#555555"

            )

        elif state == "error":

            self.glow.configure(

                fg_color="#552200"

            )

            self.ring.configure(

                fg_color="#FF6B35"

            )

        else:

            self.glow.configure(

                fg_color="#250000"

            )

            self.ring.configure(

                fg_color="#4A0000"

            )

    # ==========================================
    # Animation
    # ==========================================

    def start_animation(self):

        if self.animation_job:

            self.after_cancel(

                self.animation_job

            )

        self.animate()

    # ------------------------------------------

    def animate(self):

        if self.state == "offline":

            return

        if self.pulse_up:

            self.current_size += 1

            if self.current_size >= self.size + 6:

                self.pulse_up = False

        else:

            self.current_size -= 1

            if self.current_size <= self.size:

                self.pulse_up = True

        self.orb.configure(

            width=self.current_size,

            height=self.current_size,

            corner_radius=self.current_size // 2

        )

        self.ring.configure(

            width=self.current_size + 16,

            height=self.current_size + 16,

            corner_radius=(self.current_size + 16) // 2

        )

        self.glow.configure(

            width=self.current_size + 34,

            height=self.current_size + 34,

            corner_radius=(self.current_size + 34) // 2

        )

        self.animation_job = self.after(

            35,

            self.animate

        )

    # ==========================================
    # Controls
    # ==========================================

    def stop_animation(self):

        if self.animation_job:

            self.after_cancel(

                self.animation_job

            )

            self.animation_job = None

    # ==========================================
    # Status
    # ==========================================

    def get_state(self):

        return self.state