class AURAController:

    def __init__(self, page_manager):

        self.page_manager = page_manager

    # -------------------------
    # Navigation
    # -------------------------

    def go_home(self):
        self.page_manager.show_page("home")

    def open_study_hub(self):
        self.page_manager.show_page("study")

    def open_plugins(self):
        self.page_manager.show_page("plugins")

    def open_memory(self):
        self.page_manager.show_page("memory")

    def open_settings(self):
        self.page_manager.show_page("settings")
        