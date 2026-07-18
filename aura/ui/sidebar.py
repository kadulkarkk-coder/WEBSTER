import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, controller):

        super().__init__(
            master,
            width=220,
            corner_radius=0
        )

        self.controller = controller

        self.grid_propagate(False)

        self.build()

    # -------------------------------------

    def build(self):

        # Logo

        logo = ctk.CTkLabel(
            self,
            text="WEBSTER",
            font=("Segoe UI", 26, "bold")
        )

        logo.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Whatever Every Brilliant \nSystem Truly Executes... Reliably.",
            font=("Segoe UI", 12)
        )

        subtitle.pack(pady=(0, 25))

        # -----------------------
        # Navigation Buttons
        # -----------------------

        self.chat_button = self.create_button(
            "💬 Talk to Webster",
            self.controller.go_chat
        )

        self.study_button = self.create_button(
            "📚 Study-tingle",
            self.controller.go_study
        )

        self.memory_button = self.create_button(
            "🧠 Who is Peter?",
            self.controller.go_memory
        )

        self.plugin_button = self.create_button(
            "🔌 Extra Webs",
            self.controller.go_plugins
        )

        self.settings_button = self.create_button(
            "⚙ Settings",
            self.controller.go_settings
        )

        # Push footer to bottom

        spacer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        spacer.pack(expand=True, fill="both")

        footer = ctk.CTkLabel(
            self,
            text="Version 0.0.21",
            font=("Segoe UI", 11)
        )

        footer.pack(pady=20)

    # -------------------------------------

    def create_button(self, text, command):

        button = ctk.CTkButton(
            self,
            text=text,
            height=45,
            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=6
        )

        return button