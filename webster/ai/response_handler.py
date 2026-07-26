"""
WEBSTER Response Handler
=========================
Processes and formats AI responses before display.
"""

import re
from typing import Any, Dict, List, Optional


class ResponseHandler:
    """
    Post-processes AI responses:
    - Detects and formats markdown
    - Extracts code blocks
    - Identifies intents/actions
    - Sanitizes content
    """

    def __init__(self):
        self._action_patterns = {
            "open_app": re.compile(r'\[open_app:(.+?)\]', re.IGNORECASE),
            "open_url": re.compile(r'\[open_url:(.+?)\]', re.IGNORECASE),
            "search": re.compile(r'\[search:(.+?)\]', re.IGNORECASE),
            "remind": re.compile(r'\[remind:(.+?)\]', re.IGNORECASE),
            "create_note": re.compile(r'\[create_note:(.+?)\]', re.IGNORECASE),
        }

    def process(self, response: str) -> Dict[str, Any]:
        """Process a raw AI response."""
        actions = self._extract_actions(response)
        clean_response = self._remove_action_tags(response)
        code_blocks = self._extract_code_blocks(clean_response)
        has_code = len(code_blocks) > 0

        return {
            "text": clean_response.strip(),
            "actions": actions,
            "code_blocks": code_blocks,
            "has_code": has_code,
            "raw": response,
        }

    def _extract_actions(self, text: str) -> List[Dict[str, str]]:
        """Extract actionable commands from response."""
        actions = []
        for action_name, pattern in self._action_patterns.items():
            matches = pattern.findall(text)
            for match in matches:
                actions.append({"type": action_name, "value": match.strip()})
        return actions

    def _remove_action_tags(self, text: str) -> str:
        """Remove action tag markers from text."""
        for pattern in self._action_patterns.values():
            text = pattern.sub("", text)
        return text

    def _extract_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """Extract code blocks with language info."""
        blocks = []
        pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
        for match in pattern.finditer(text):
            blocks.append({
                "language": match.group(1) or "text",
                "code": match.group(2).strip(),
            })
        return blocks

    def format_for_display(self, response: str) -> str:
        """Format response for chat display."""
        processed = self.process(response)
        text = processed["text"]

        # Format code blocks for better display
        for block in processed["code_blocks"]:
            lang = block["language"]
            code = block["code"]
            formatted = f"\n[{lang.upper()}]\n{code}\n[/{lang.upper()}]\n"
            text = text.replace(f"```{lang}\n{code}```", formatted)

        return text

    def has_actions(self, response: str) -> bool:
        """Check if response contains executable actions."""
        return len(self._extract_actions(response)) > 0

    def sanitize(self, text: str) -> str:
        """Sanitize response text."""
        text = text.replace("\r\n", "\n")
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
