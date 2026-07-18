from aura.utils.debug import Debug


class ConversationContext:
    """
    ==================================================

            AURA Context Engine

    ==================================================

    Responsible for building the complete prompt
    that is sent to the AI.

    Structure

    ----------------------------
    System
    Profile
    Recent Conversation
    Current Prompt
    ----------------------------

    Sprint 21.2

    • System Prompt
    • Profile Injection
    • Recent Conversation
    • Prompt Builder

    Sprint 22

    • Semantic Memory

    Sprint 23

    • Token Budget
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self, max_messages=20):

        self.max_messages = max_messages

    # ==================================================
    # Build Context
    # ==================================================

    def build(

        self,

        memory,

        prompt

    ):

        Debug.log(

            "Context",

            "Building Context"

        )

        sections = []

        sections.append(

            self.build_system()

        )

        sections.append(

            self.build_profile(

                memory

            )

        )

        sections.append(

            self.build_recent(

                memory

            )

        )

        sections.append(

            self.build_prompt(

                prompt

            )

        )

        return "\n\n".join(

            section

            for section in sections

            if section

        )

    # ==================================================
    # System
    # ==================================================

    def build_system(self):

        return (
            "SYSTEM\n"
            "------\n"
            "You are AURA.\n"
            "You are a helpful AI assistant.\n"
            "Use previous conversations when useful.\n"
            "Answer clearly and accurately.\n"
            "Do not invent information."
        )

    # ==================================================
    # Profile
    # ==================================================

    def build_profile(

        self,

        memory

    ):

        profile = memory.get_profile()

        if not profile:

            return ""

        lines = [

            "PROFILE",

            "-------"

        ]

        fields = [

            "name",

            "nickname",

            "age",

            "grade",

            "school",

            "location",

            "occupation",

            "bio"

        ]

        for field in fields:

            value = profile.get(

                field

            )

            if value:

                lines.append(

                    f"{field}: {value}"

                )

        for key in [

            "interests",

            "skills",

            "goals",

            "likes",

            "dislikes"

        ]:

            value = profile.get(

                key

            )

            if value:

                lines.append(

                    f"{key}: {', '.join(value)}"

                )

        return "\n".join(

            lines

        )

    # ==================================================
    # Recent Conversation
    # ==================================================

    def build_recent(

        self,

        memory

    ):

        messages = memory.get_messages()

        recent = messages[-self.max_messages:]

        if not recent:

            return ""

        lines = [

            "RECENT CONVERSATION",

            "-------------------"

        ]

        for message in recent:

            role = message.get(

                "role",

                "user"

            )

            content = message.get(

                "content",

                ""

            )

            lines.append(

                f"{role}: {content}"

            )

        return "\n".join(

            lines

        )

    # ==================================================
    # Current Prompt
    # ==================================================

    def build_prompt(

        self,

        prompt

    ):

        return (

            "CURRENT USER MESSAGE\n"

            "--------------------\n"

            f"user: {prompt}"

        )

    # ==================================================
    # Configuration
    # ==================================================

    def set_limit(

        self,

        limit

    ):

        self.max_messages = max(

            1,

            int(limit)

        )

        Debug.log(

            "Context",

            f"Limit -> {self.max_messages}"

        )

    # --------------------------------------------------

    def get_limit(self):

        return self.max_messages

    # ==================================================
    # Statistics
    # ==================================================

    def context_length(

        self,

        memory

    ):

        return len(

            memory.get_messages()

        )

    # --------------------------------------------------

    def estimated_tokens(

        self,

        text

    ):

        return len(

            text.split()

        ) * 1.3

    # ==================================================
    # Utilities
    # ==================================================

    def clear(self):

        Debug.log(

            "Context",

            "Context cleared"

        )