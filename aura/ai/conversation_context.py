from aura.utils.debug import Debug


class ConversationContext:
    """
    ==================================================

            AURA Conversation Context Builder

    ==================================================

    Responsible for:

    • Assistant Identity
    • User Profile
    • Conversation History
    • Prompt Assembly

    This class NEVER talks to Gemini directly.
    It only builds the prompt that is sent to
    the provider.
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        max_messages=10

    ):

        self.max_messages = max_messages

        self.assistant_name = "AURA"

        self.assistant_role = (

            "A helpful desktop AI assistant."

        )

        Debug.log(

            "Context",

            "ConversationContext Initialized"

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

            f"History limit -> {self.max_messages}"

        )

    # --------------------------------------------------

    def get_limit(

        self

    ):

        return self.max_messages

    # ==================================================
    # Identity
    # ==================================================

    def build_identity(

        self

    ):

        lines = [

            "==============================",

            "SYSTEM",

            "==============================",

            "",

            f"You are {self.assistant_name}.",

            self.assistant_role,

            "",

            "Always be helpful.",

            "Always answer naturally.",

            "If you don't know something,"

            " admit it honestly.",

            ""

        ]

        return "\n".join(

            lines

        )

        # ==================================================
    # Profile
    # ==================================================

    def build_profile(

        self,

        memory

    ):

        Debug.log(

            "Context",

            "Building profile context"

        )

        profile = memory.get_profile()

        if not profile:

            return ""

        lines = [

            "==============================",

            "USER PROFILE",

            "==============================",

            ""

        ]

        for key, value in profile.items():

            if value in (

                None,

                "",

                [],

                {}

            ):

                continue

            title = (

                key

                .replace("_", " ")

                .title()

            )

            if isinstance(

                value,

                list

            ):

                if not value:

                    continue

                lines.append(

                    f"{title}:"

                )

                for item in value:

                    lines.append(

                        f"- {item}"

                    )

                lines.append(

                    ""

                )

            elif isinstance(

                value,

                dict

            ):

                if not value:

                    continue

                lines.append(

                    f"{title}:"

                )

                for k, v in value.items():

                    lines.append(

                        f"- {k}: {v}"

                    )

                lines.append(

                    ""

                )

            else:

                lines.append(

                    f"{title}: {value}"

                )

                lines.append(

                    ""

                )

        return "\n".join(

            lines

        )

        # ==================================================
    # History
    # ==================================================

    def build_history(

        self,

        memory

    ):

        Debug.log(

            "Context",

            "Building conversation history"

        )

        messages = memory.get_messages()

        if not messages:

            return ""

        recent = messages[

            -self.max_messages:

        ]

        lines = [

            "==============================",

            "RECENT CONVERSATION",

            "==============================",

            ""

        ]

        role_names = {

            "user": "User",

            "assistant": self.assistant_name,

            "system": "System"

        }

        for message in recent:

            role = message.get(

                "role",

                "unknown"

            )

            content = message.get(

                "content",

                ""

            )

            if not content:

                continue

            speaker = role_names.get(

                role,

                role.title()

            )

            lines.append(

                f"{speaker}:"

            )

            lines.append(

                content

            )

            lines.append(

                ""

            )

        return "\n".join(

            lines

        )

        # ==================================================
    # Prompt Builder
    # ==================================================

    def build(

        self,

        memory,

        prompt

    ):

        Debug.log(

            "Context",

            "Building complete prompt"

        )

        sections = []

        # ----------------------------------------------
        # Identity
        # ----------------------------------------------

        identity = self.build_identity()

        if identity:

            sections.append(

                identity

            )

        # ----------------------------------------------
        # Profile
        # ----------------------------------------------

        profile = self.build_profile(

            memory

        )

        if profile:

            sections.append(

                profile

            )

        # ----------------------------------------------
        # Conversation History
        # ----------------------------------------------

        history = self.build_history(

            memory

        )

        if history:

            sections.append(

                history

            )

        # ----------------------------------------------
        # Current Prompt
        # ----------------------------------------------

        sections.append(

            "\n".join(

                [

                    "==============================",

                    "CURRENT USER REQUEST",

                    "==============================",

                    "",

                    prompt

                ]

            )

        )

        final_prompt = "\n\n".join(

            sections

        )

        Debug.log(

            "Context",

            "Prompt successfully built"

        )

        return final_prompt

       # ==================================================
    # Preview
    # ==================================================

    def preview(

        self,

        memory,

        prompt

    ):

        return self.build(

            memory,

            prompt

        )

    # ==================================================
    # Assistant
    # ==================================================

    def set_assistant_name(

        self,

        name

    ):

        self.assistant_name = str(

            name

        )

    # --------------------------------------------------

    def get_assistant_name(

        self

    ):

        return self.assistant_name

    # --------------------------------------------------

    def set_assistant_role(

        self,

        role

    ):

        self.assistant_role = str(

            role

        )

    # --------------------------------------------------

    def get_assistant_role(

        self

    ):

        return self.assistant_role

    # ==================================================
    # Utilities
    # ==================================================

    def clear(

        self

    ):

        Debug.log(

            "Context",

            "Conversation Context Cleared"

        )

    # --------------------------------------------------

    def health(

        self

    ):

        return {

            "assistant": self.assistant_name,

            "history_limit": self.max_messages,

            "status": "Online"

        }

    # --------------------------------------------------

    def statistics(

        self

    ):

        return {

            "assistant": self.assistant_name,

            "role": self.assistant_role,

            "history_limit": self.max_messages

        }

    # --------------------------------------------------

    def __str__(

        self

    ):

        return (

            f"ConversationContext("

            f"assistant={self.assistant_name}, "

            f"limit={self.max_messages})"

        )