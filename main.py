from aura.app.application import Application
from aura.core.ai_worker import AIWorker
from aura.voice.voice_controller import VoiceController
from aura.ai.conversation_context import ConversationContext
from aura.ui.status.status_manager import StatusManager
import traceback

status = StatusManager()


def main():
    
    try:

        app = Application()

        app.run()

    except Exception:

        print("\nAURA FAILED TO START\n")

        traceback.print_exc()



if __name__ == "__main__":

    main()