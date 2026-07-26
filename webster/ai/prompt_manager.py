"""
WEBSTER Prompt Manager
======================
Manages Spidey's personality prompts and system instructions.
"""

from typing import Dict, List, Optional, Any


class PromptManager:
    """
    Builds prompts for Spidey with context, personality, and instructions.
    """

    SYSTEM_PROMPT = """You are Spidey, the AI companion of WEBSTER (Workspace for Enhanced Business, Study, Technology, Engineering & Research).

Personality:
- Friendly, helpful, and enthusiastic
- Uses a conversational tone
- Calls the user by name when known
- Adapts to the user's communication style
- Proactive in offering assistance

Capabilities:
- Natural conversation and Q&A
- Study assistance (notes, flashcards, quizzes)
- PDF reading and analysis
- Web search and browsing
- File management
- System automation
- Task scheduling and reminders
- Calendar management
- Code assistance
- Writing and editing

Guidelines:
- Keep responses concise and clear
- Use markdown for formatting when helpful
- Ask clarifying questions when needed
- Be honest about limitations
- Prioritize user privacy and security
- Never share personal information"""

    def __init__(self):
        self.system_prompt = self.SYSTEM_PROMPT
        self._custom_instructions: List[str] = []

    def add_instruction(self, instruction: str):
        """Add a custom instruction."""
        self._custom_instructions.append(instruction)

    def set_custom_prompt(self, prompt: str):
        """Override the system prompt."""
        self.system_prompt = prompt

    def build(self, user_input: str, context: Optional[Dict[str, Any]] = None,
              memory_summary: Optional[str] = None) -> str:
        """Build a complete prompt with context."""
        parts = [self.system_prompt]

        if self._custom_instructions:
            parts.append("\nCustom Instructions:\n" + "\n".join(f"- {i}" for i in self._custom_instructions))

        if memory_summary:
            parts.append(f"\nMemory Context:\n{memory_summary}")

        if context:
            ctx_parts = []
            if context.get("user_name"):
                ctx_parts.append(f"User: {context['user_name']}")
            if context.get("current_page"):
                ctx_parts.append(f"Current page: {context['current_page']}")
            if context.get("topic"):
                ctx_parts.append(f"Topic: {context['topic']}")
            if ctx_parts:
                parts.append("\nCurrent Context:\n" + "\n".join(ctx_parts))

        parts.append(f"\nUser: {user_input}")
        parts.append("\nSpidey:")
        return "\n".join(parts)

    def build_chat(self, messages: List[Dict[str, str]],
                   context: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """Build a chat message list with system prompt."""
        result = [{"role": "system", "content": self.system_prompt}]

        if self._custom_instructions:
            result.append({
                "role": "system",
                "content": "Custom instructions:\n" + "\n".join(f"- {i}" for i in self._custom_instructions)
            })

        for msg in messages[-20:]:  # Limit history
            result.append(msg)

        return result

    def get_system_prompt(self) -> str:
        return self.system_prompt

    def reset(self):
        """Reset to default prompt."""
        self.system_prompt = self.SYSTEM_PROMPT
        self._custom_instructions.clear()
