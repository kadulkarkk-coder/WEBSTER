from aura.config.settings import Settings
from aura.utils.logger import Logger
from aura.core.launcher import Launcher

from aura.services.service_manager import ServiceManager

from aura.plugins.plugin_manager import PluginManager
from aura.plugins.hello_plugin.plugin import HelloPlugin

from aura.ui.main_window import MainWindow

from aura.services.ai_service import AIService
from aura.services.memory_service import MemoryService
from aura.services.study_service import StudyService
from aura.services.voice_service import VoiceService
from aura.services.vision_service import VisionService
from aura.ai.chat_manager import ChatManager


class Application:

    def __init__(self):

        # -------------------------
        # Core Managers
        # -------------------------

        self.services = ServiceManager()

        self.settings = Settings()
        self.logger = Logger()

        self.launcher = Launcher(
            settings=self.settings,
            logger=self.logger
        )

        self.plugin_manager = PluginManager()
        memory = MemoryService()

        # -------------------------
        # Register Core Services
        # -------------------------

        self.services.register("settings", self.settings)
        self.services.register("logger", self.logger)
        self.services.register("launcher", self.launcher)
        self.services.register("plugin_manager", self.plugin_manager)
        self.services.register("memory", memory)

        # -------------------------
        # Register Plugins
        # -------------------------

        hello = HelloPlugin()

        self.plugin_manager.register(hello)

        # -------------------------
        # Create AURA Services
        # -------------------------

        self.ai = AIService()
        self.study = StudyService()
        self.voice = VoiceService()
        self.vision = VisionService()

        # -------------------------
        # Register AURA Services
        # -------------------------

        self.services.register("ai", self.ai)
        self.services.register("study", self.study)
        self.services.register("voice", self.voice)
        self.services.register("vision", self.vision)
        self.chat = ChatManager()

        self.services.register(
            "chat",
            self.chat
        )

    def initialize_services(self):

        self.logger.info("Initializing Services...")

        for name in [
            "ai",
            "memory",
            "study",
            "voice",
            "vision"
        ]:

            service = self.services.get(name)

            service.initialize()

        self.logger.info("All Services Initialized")

    def print_summary(self):

        print("\n========== AURA SUMMARY ==========\n")

        print("Registered Services:")

        for service in self.services.list_services():
            print(f"  • {service}")

        print("\nLoaded Plugins:")

        for plugin in self.plugin_manager.list_plugins():
            print(f"  • {plugin.name} ({plugin.version})")

        print("\n==================================\n")

    def run(self):

        self.logger.info("Application Starting")

        self.launcher.start()

        self.initialize_services()

        self.print_summary()

        window = MainWindow(self.services)

        window.mainloop()

        self.logger.info("Application Closed")
