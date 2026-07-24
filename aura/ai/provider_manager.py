from aura.utils.debug import Debug


class ProviderManager:

    """
    ==========================================

            WEBSTER Provider Manager

    ==========================================

    Responsibilities

        • Register Providers

        • Activate Provider

        • Switch Providers

        • Automatic Failover

        • Health Monitoring

    Sprint 21.1.6
    """

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(

        self

    ):

        self.providers = {}

        self.active_provider = None

        self.active_name = None

        Debug.log(

            "ProviderManager",

            "Initialized"

        )

    # ==========================================
    # Register
    # ==========================================

    def register(

        self,

        name,

        provider

    ):

        name = name.lower()

        self.providers[name] = provider

        Debug.log(

            "ProviderManager",

            f"Registered {name}"

        )

    # ==========================================
    # Activate
    # ==========================================

    def activate(

        self,

        name

    ):

        name = name.lower()

        if name not in self.providers:

            raise ValueError(

                f"Provider '{name}' not found."

            )

        self.active_provider = self.providers[

            name

        ]

        self.active_name = name

        Debug.log(

            "ProviderManager",

            f"Activated {name}"

        )

    # ==========================================
    # Current Provider
    # ==========================================

    def current(

        self

    ):

        return self.active_provider

    # ==========================================
    # Current Name
    # ==========================================

    def current_name(

        self

    ):

        return self.active_name

    # ==========================================
    # Exists
    # ==========================================

    def exists(

        self,

        name

    ):

        return name.lower() in self.providers

    # ==========================================
    # Registered Providers
    # ==========================================

    def get_registered(

        self

    ):

        return list(

            self.providers.keys()

        )