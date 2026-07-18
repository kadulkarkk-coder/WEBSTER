"""
response_pipeline.py

Central response pipeline for A.U.R.A.
"""

from aura.core.ai_worker import AIWorker


class ResponsePipeline:

    def __init__(
        self,
        ai_worker,
        status_manager,
        context_manager,
        voice_controller
    ):

        self.ai = ai_worker
        self.status = status_manager
        self.context = context_manager
        self.voice = voice_controller

    # -------------------------

    def process(self, user_text):

        # Save user message
        self.context.add_user_message(user_text)

        # AI is thinking
        self.status.set_status("Thinking")

        # Generate reply
        reply = self.ai.generate(user_text)

        # Save AI reply
        self.context.add_ai_message(reply)

        # Ready
        self.status.set_status("Ready")

        # Speak if enabled
        self.voice.speak(reply)

        return reply