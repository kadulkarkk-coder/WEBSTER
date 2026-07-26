"""
Spidey — Smartest Pal In Doing Everything Your-way
===================================================
The main AI companion that coordinates between user, HELVAC engine,
and all WEBSTER subsystems.
"""

import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Union

from webster.config.branding import AI_NAME, WAKE_WORD
from webster.core.logger import Logger
from webster.core.brain import HelvacEngine, Task, TaskType, TaskResult
from webster.core.memory import MemoryManager
from webster.core.errors import WebsterError


class SpideyAssistant:
    """
    Spidey — The main AI companion of WEBSTER.
    
    Responsibilities:
    - Natural conversation handling
    - Task delegation to HELVAC
    - Context management
    - User preference learning
    - Multi-modal interaction coordination
    - UI callback integration for chat
    - Voice toggle support
    """

    def __init__(self, helvac: HelvacEngine, memory: MemoryManager):
        self.logger = Logger().get_logger("SPIDEY")
        self.helvac = helvac
        self.memory = memory
        self._active = False
        self._current_conversation_id = None
        self._listening_for_wake = False
        self._ui_callback: Optional[Callable[[str], None]] = None
        self._voice_enabled = False

        self.logger.info(f"{AI_NAME} assistant initialized")

    # ── UI Integration ─────────────────────────────────

    def set_ui_callback(self, callback: Callable[[str], None]):
        """Register a UI callback to receive Spidey messages."""
        self._ui_callback = callback
        self.logger.debug("UI callback registered")

    def _send_to_ui(self, message: str):
        """Send a message to the UI if callback is registered."""
        if self._ui_callback:
            try:
                self._ui_callback(message)
            except Exception as e:
                self.logger.error(f"UI callback failed: {e}")

    # ── Voice Integration ──────────────────────────────

    def toggle_voice(self):
        """Toggle voice input on/off."""
        self._voice_enabled = not self._voice_enabled
        status = "enabled" if self._voice_enabled else "disabled"
        self.logger.info(f"Voice toggled {status}")
        return self._voice_enabled

    def is_voice_enabled(self) -> bool:
        return self._voice_enabled

    # ── Activation ─────────────────────────────────────

    def activate(self):
        """Activate Spidey assistant."""
        self._active = True
        self._current_conversation_id = str(uuid.uuid4())
        self.logger.info(f"{AI_NAME} activated (conv: {self._current_conversation_id[:8]})")

    def deactivate(self):
        """Deactivate Spidey assistant."""
        self._active = False
        self._current_conversation_id = None
        self.logger.info(f"{AI_NAME} deactivated")

    @property
    def is_active(self) -> bool:
        return self._active

    # ── Conversation ───────────────────────────────────

    def process_message(self, message: str, context: dict = None) -> str:
        """Process a user message and return a response."""
        if not self._active:
            return "Spidey is not active. Say 'Hey Spidey' to wake me up!"

        if not message or not message.strip():
            return "I didn't catch that. Could you repeat?"

        context = context or {}

        # Save to memory
        self.memory.add_user_message(message)

        # Create task for HELVAC
        task = Task(
            id=str(uuid.uuid4()),
            type=TaskType.UNKNOWN,
            input=message,
            context=context,
            timestamp=time.time()
        )

        # Submit to HELVAC
        task_id = self.helvac.submit_task(task)
        result = self.helvac.wait_for_result(task_id, timeout=30.0)

        if result and result.success:
            response = result.output
        elif result:
            response = f"I ran into an issue: {result.error}. Let me try again differently."
        else:
            response = "I'm thinking... give me a moment."

        # Save response to memory
        self.memory.add_assistant_message(response)

        # Send to UI
        self._send_to_ui(response)

        return response

    def process_and_reply(self, message: str):
        """Process a message and send the reply to the UI (for chat integration)."""
        response = self.process_message(message)
        self._send_to_ui(response)

    # ── Wake Word ──────────────────────────────────────

    def check_wake_word(self, text: str) -> bool:
        """Check if text contains the wake word."""
        return WAKE_WORD in text.lower().strip()

    def on_wake_word_detected(self):
        """Handle wake word detection."""
        self.activate()
        msg = f"Hey! {AI_NAME} here. How can I help?"
        self._send_to_ui(msg)
        return msg

    # ── Capabilities ───────────────────────────────────

    def get_capabilities(self) -> List[str]:
        return [
            "Natural conversation",
            "Voice input and output",
            "Memory and context retention",
            "Study assistance (PDFs, notes, flashcards, quizzes)",
            "Web search and browsing",
            "File management",
            "Application control",
            "Calendar and scheduling",
            "Email composition",
            "Code assistance",
            "Writing and editing",
            "Research and summarization",
            "Plugin support",
            "Task automation",
        ]

    def get_personality(self) -> str:
        return (
            f"I'm {AI_NAME}, your friendly AI companion. "
            "I'm helpful, knowledgeable, and always ready to assist. "
            "I can chat naturally, help with studies, manage files, "
            "control apps, and much more. What would you like to do?"
        )

    # ── Quick Actions ──────────────────────────────────

    def quick_help(self) -> str:
        return (
            f"🌟 {AI_NAME} Quick Help\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "💬 Just chat with me naturally\n"
            "🎤 Say 'Hey Spidey' to wake me\n"
            "📚 'Study [topic]' for learning\n"
            "📄 'Read [file]' for documents\n"
            "🌐 'Search [query]' for web\n"
            "⚙ 'Open [app]' for automation\n"
            "📝 'Take notes' for notes\n"
            "🧠 'Remember this' for memory"
        )

    # ── Status ─────────────────────────────────────────

    def status(self) -> dict:
        return {
            "active": self._active,
            "conversation_id": self._current_conversation_id,
            "wake_word": WAKE_WORD,
            "memory_enabled": self.memory is not None,
            "helvac_running": self.helvac is not None,
            "ui_callback_registered": self._ui_callback is not None,
            "voice_enabled": self._voice_enabled,
        }

    def shutdown(self):
        """Clean shutdown of Spidey."""
        self.deactivate()
        self._ui_callback = None
        self.logger.info(f"{AI_NAME} shut down")
