from aura.config.settings import Settings
from aura.utils.logger import Logger

from aura.core.launcher import Launcher
from aura.core.ai_worker import AIWorker
from aura.config.branding import (
    APP_NAME,
    VERSION
)
from aura.services.service_manager import ServiceManager

from aura.services.ai_service import AIService
from aura.services.memory_service import MemoryService
from aura.services.study_service import StudyService
from aura.services.voice_service import VoiceService
from aura.services.vision_service import VisionService

from aura.voice.voice_controller import VoiceController

from aura.ai.conversation_context import ConversationContext
from aura.ai.chat_manager import ChatManager

from aura.ui.status.status_manager import StatusManager

from aura.plugins.plugin_manager import PluginManager
from aura.plugins.hello_plugin.plugin import HelloPlugin

from aura.ui.main_window import MainWindow


class Application:

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        self.services = ServiceManager()

        self._create_core()

        self._create_services()

        self._register_services()

        self._register_plugins()

    # ==================================================
    # Core
    # ==================================================

    def _create_core(self):

        self.settings = Settings()

        self.logger = Logger()

        self.launcher = Launcher(

            settings=self.settings,

            logger=self.logger

        )

        self.plugin_manager = PluginManager()

    # ==================================================
    # Services
    # ==================================================

    def _create_services(self):

        self.memory = MemoryService()

        self.status = StatusManager()

        self.context = ConversationContext()

        self.ai = AIService()

        self.study = StudyService()

        self.voice = VoiceService()

        self.vision = VisionService()

        self.ai_worker = AIWorker()

        self.voice_controller = VoiceController()

        self.chat = ChatManager()

    # ==================================================
    # Register Services
    # ==================================================

    def _register_services(self):

        register = self.services.register

        # -------------------------
        # Core
        # -------------------------

        register("settings", self.settings)

        register("logger", self.logger)

        register("launcher", self.launcher)

        register("plugin_manager", self.plugin_manager)

        # -------------------------
        # Memory
        # -------------------------

        register("memory", self.memory)

        register("status_manager", self.status)

        register(
            "conversation_context",
            self.context
        )

        # -------------------------
        # AI
        # -------------------------

        register("ai", self.ai)

        register("study", self.study)

        register("voice", self.voice)

        register("vision", self.vision)

        # -------------------------
        # Workers
        # -------------------------

        register(
            "ai_worker",
            self.ai_worker
        )

        register(
            "voice_controller",
            self.voice_controller
        )

        register(
            "chat",
            self.chat
        )

    # ==================================================
    # Plugins
    # ==================================================

    def _register_plugins(self):

        hello = HelloPlugin()

        self.plugin_manager.register(
            hello
        )

    # ==================================================
    # Initialize
    # ==================================================

    def initialize_services(

        self,

        splash=None

    ):

        self.logger.info(
            "Initializing Services..."
        )

        for service_name in (

            "memory",

            "ai",

            "study",

            "voice",

            "vision",

        ):

            service = self.services.get(
                service_name
            )

            if service is None:

                continue

            initialize = getattr(
                service,
                "initialize",
                None
            )

            if callable(initialize):

                initialize()

                self.logger.info(

                    f"{service_name} initialized."

                )

                if splash:

                    splash.next_step()

        self.logger.info(
            "All Services Initialized."
        )

    # ==================================================
    # Create Main Window
    # ==================================================

    def create_window(

        self

    ):

        return MainWindow(

            self.services

        )
    
    # ==================================================
    # Summary
    # ==================================================

    def print_summary(self):

        print()

        print("=" * 60)

        print("AURA SUMMARY")

        print("=" * 60)

        print()

        print("Registered Services:")

        for service in self.services.list_services():

            print(f" • {service}")

        print()

        print("Loaded Plugins:")

        for plugin in self.plugin_manager.list_plugins():

            print(

                f" • {plugin.name} "

                f"({plugin.version})"

            )

        print()

        print("=" * 60)

    # ==================================================
    # Run
    # ==================================================

    def run(self):

        self.logger.info(
            "Application Starting"
        )

        self.launcher.start()

        self.initialize_services()

        self.print_summary()

        window = self.create_window()

        window.mainloop()

        self.shutdown()

    # ==================================================
    # Shutdown
    # ==================================================

    def shutdown(self):

        self.logger.info(

            "Closing WEBSTER..."

        )

        memory = self.services.get(

            "memory"

        )

        if memory:

            memory.save()

        controller = self.services.get(

            "voice_controller"

        )

        if controller:

            controller.reset()

        self.logger.info(

            "Application Closed"

        )