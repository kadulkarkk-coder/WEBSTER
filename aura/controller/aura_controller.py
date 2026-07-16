class AURAController:

    def __init__(self, page_manager, services):

        self.page_manager = page_manager
        self.services = services

        print("=" * 50)
        print("AURA Controller Initialized")
        print("Registered Services:")

        for service in self.services.list_services():
            print(f" • {service}")

        print("=" * 50)

    # ==================================================
    # Service Access
    # ==================================================

    def get_service(self, name):

        return self.services.get(name)

    # ==================================================
    # Navigation
    # ==================================================

    def go_chat(self):

        self.page_manager.show_page("chat")

    # --------------------------------------------------

    def go_study(self):

        self.page_manager.show_page("study")

    # --------------------------------------------------

    def go_plugins(self):

        self.page_manager.show_page("plugins")

    # --------------------------------------------------

    def go_memory(self):

        self.page_manager.show_page("memory")

    # --------------------------------------------------

    def go_settings(self):

        self.page_manager.show_page("settings")

    # ==================================================
    # Chat
    # ==================================================

    def send_message(self, prompt):

        prompt = prompt.strip()

        if not prompt:
            return ""

        ai = self.get_service("ai")
        memory = self.get_service("memory")

        if ai is None:
            return "[ERROR] AI Service not found."

        if memory is None:
            return "[ERROR] Memory Service not found."

        # ----------------------------------------------
        # Store User Message
        # ----------------------------------------------

        memory.add_user(prompt)

        # ----------------------------------------------
        # Generate AI Response
        # ----------------------------------------------

        try:

            response = ai.ask(prompt)

        except Exception as e:

            response = f"[AI ERROR] {e}"

        # ----------------------------------------------
        # Store Assistant Response
        # ----------------------------------------------

        memory.add_assistant(response)

        return response

    # ==================================================
    # Memory
    # ==================================================

    def clear_chat(self):

        memory = self.get_service("memory")

        if memory:

            memory.clear_chat()

    # --------------------------------------------------

    def export_chat(self):

        memory = self.get_service("memory")

        if memory:

            return memory.export_chat()

        return ""

    # ==================================================
    # Profile
    # ==================================================

    def get_setting(self, key, default=None):

        memory = self.get_service("memory")

        if memory:

            return memory.get_setting(
                key,
                default
            )

        return default

    # --------------------------------------------------

    def set_setting(self, key, value):

        memory = self.get_service("memory")

        if memory:

            memory.set_setting(
                key,
                value
            )

    # ==================================================
    # AI
    # ==================================================

    def ask_ai(self, prompt):

        ai = self.get_service("ai")

        if ai:

            return ai.ask(prompt)

        return "[ERROR] AI Service unavailable."

    # ==================================================
    # Shutdown
    # ==================================================

    def shutdown(self):

        memory = self.get_service("memory")

        if memory:

            memory.save()

        print("AURA Controller Shutdown Complete")