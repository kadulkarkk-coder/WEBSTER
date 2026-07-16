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
            text="🤖 A.U.R.A.",
            font=("Segoe UI", 26, "bold")
        )

        logo.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Artificial Utilitarian\nResearch Agent",
            font=("Segoe UI", 12)
        )

        subtitle.pack(pady=(0, 25))

        # -----------------------
        # Navigation Buttons
        # -----------------------

        self.chat_button = self.create_button(
            "💬 Chat",
            self.controller.go_chat
        )

        self.study_button = self.create_button(
            "📚 Study Hub",
            self.controller.go_study
        )

        self.memory_button = self.create_button(
            "🧠 Memory",
            self.controller.go_memory
        )

        self.plugin_button = self.create_button(
            "🔌 Plugins",
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
            text="Version 0.0.17\nSprint 17.5",
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