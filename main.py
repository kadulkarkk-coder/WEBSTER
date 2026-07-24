from aura.app.application import Application
from aura.core.ai_worker import AIWorker
from aura.voice.voice_controller import VoiceController
from aura.ai.conversation_context import ConversationContext
from aura.ui.status.status_manager import StatusManager
import traceback
from aura.ui.splash import SplashScreen
import customtkinter as ctk

status = StatusManager()


''' root = ctk.CTk()

        root.withdraw()

        splash = SplashScreen(

            root

        )

        root.wait_window(

            splash

        )

        root.destroy()'''


def main():
    try:
        app = Application()

        app.run()
    
    except Exception:

        print("\nWEBSTER FAILED TO START\n")

        traceback.print_exc()



if __name__ == "__main__":

    main()