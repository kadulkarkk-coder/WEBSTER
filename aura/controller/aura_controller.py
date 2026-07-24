from aura.utils.debug import Debug
from aura.ui.components.spidey_core import SpideyCore

class AURAController:

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        page_manager,

        services

    ):

        self.page_manager = page_manager

        self.services = services

        self.memory = self.services.get(

            "memory"

        )

        self.ai = self.services.get(

            "ai"

        )

        self.spidey_core = None

        Debug.log(

            "Controller",

            "Initialized"

        )

    # ==================================================
    # Service Access
    # ==================================================

    def get_service(
        self,
        name
    ):

        return self.services.get(
            name
        )
 

    # ==================================================
    # Status
    # ==================================================

    def get_status(self):

        status = self.get_service(
            "status_manager"
        )

        if status is None:

            return "Ready"

        return status.get_text()

    # ==================================================
    # Navigation
    # ==================================================

    def show_page(
        self,
        page
    ):

        self.page_manager.show_page(
            page
        )

    def go_chat(self):

        self.show_page(
            "chat"
        )

    def go_study(self):

        self.show_page(
            "study"
        )

    def go_plugins(self):

        self.show_page(
            "plugins"
        )

    def go_memory(self):

        self.show_page(
            "memory"
        )

    def go_settings(self):

        self.show_page(
            "settings"
        )

    def go_calendar(self):

        self.page_manager.show_page(
            "calendar"
        )


    def go_fomo(self):

            self.page_manager.show_page(
            "fomo"
        )


    def go_news(self):

        self.page_manager.show_page(
            "news"
            )
        
    def go_calendar(

        self

    ):

        self.page_manager.show_page(

            "calendar"

        )


    def go_fomo(

        self

    ):

        self.page_manager.show_page(

            "fomo"

        )


    def go_news(

        self

    ):

        self.page_manager.show_page(

            "news"

        )

    # ==================================================
    # Spidey Core
    # ==================================================

    
    # --------------------------------------------------

    # ==================================================
    # Streaming Chat
    # ==================================================

    def stream_message(
        self,
        prompt
    ):

        """
        Generator used by AIWorker.
        """

        prompt = prompt.strip()

        if not prompt:

            return

        memory = self.get_service(
            "memory"
        )

        ai = self.get_service(
            "ai"
        )

        status = self.get_service(
            "status_manager"
        )

        if status:

            status.thinking()

            
        
        # ==================================================
        # Save User Message
        # ==================================================

        memory.add_user(
            prompt
        )

        Debug.log(

            "AI",

            "Streaming response..."

        )

        # ==================================================
        # Stream Response
        # ==================================================

        response = ""

        started = False

        for chunk in ai.stream(

            memory,

            prompt

        ):

            if not started:

                if status:

                    status.speaking()

                started = True

            response += chunk

            yield chunk

        # ==================================================
        # Save Assistant Response
        # ==================================================

        memory.add_assistant(
            response
        )

        if status:

            status.idle()

        Debug.log(

               "Controller",

        "Streaming complete"

        )
    # ==================================================
    # Memory
    # ==================================================

    def clear_memory(self):

        memory = self.get_service(
            "memory"
        )

        if memory is None:

            return

        memory.clear_chat()

        Debug.log(
            "Controller",
            "Memory cleared"
        )

    # --------------------------------------------------

    def export_chat(self):

        memory = self.get_service(
            "memory"
        )

        if memory is None:

            return ""

        return memory.export_chat()

    # ==================================================
    # Settings
    # ==================================================

    def get_setting(
        self,
        key,
        default=None
    ):

        memory = self.get_service(
            "memory"
        )

        if memory is None:

            return default

        return memory.get_setting(
            key,
            default
        )

    # --------------------------------------------------

    def set_setting(
        self,
        key,
        value
    ):

        memory = self.get_service(
            "memory"
        )

        if memory is None:

            return

        memory.set_setting(
            key,
            value
        )

    # ==================================================
    # Shutdown
    # ==================================================

    def shutdown(self):

        Debug.log(
            "Controller",
            "Saving memory..."
        )

        memory = self.get_service(
            "memory"
        )

        if memory:

            memory.save()

        Debug.log(
            "Controller",
            "Shutdown complete"
        )