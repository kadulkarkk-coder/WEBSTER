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

        self.providers = []

        self.current_index = 0

        self.active_provider = None

        self.active_name = None

        self.provider_order = []

        Debug.log(

            "ProviderManager",

            "Initialized"

        )

        # ==================================================
    # Switch To Next Provider
    # ==================================================

    def switch_to_next(

        self

    ):

        if not self.provider_order:

            return None

        self.current_index += 1

        if self.current_index >= len(self.provider_order):

            self.current_index = 0

        name = self.provider_order[

        self.current_index

        ]

        return self.providers[

            name

        ]
    
    # ==========================================
    # Next Provider
    # ==========================================

    def get_next_provider(

        self

    ):

        if self.active_name is None:

            return None

        try:

            index = self.provider_order.index(

                self.active_name

            )

        except ValueError:

            return None

        if index + 1 >= len(

            self.provider_order

        ):

            return None

        return self.provider_order[

            index + 1

        ]

    # ==================================================
    # Add Provider
    # ==================================================

    def add_provider(

        self,

        provider

    ):

        self.providers.append(

            provider

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

        self.providers = {}
        
        self.providers["gemini"] = provider

        provider = self.switch_to_next()

        try:

           provider.initialize()

        except Exception:

            return False

        self.provider = self.switch_to_next()

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



    # ==========================================
    # Failover
    # ==========================================

    def failover(

        self

    ):

        next_provider = self.get_next_provider()

        if next_provider is None:

            Debug.log(

                "ProviderManager",

                "No fallback provider."

            )

            return False

        if next_provider not in self.providers:

            Debug.log(

                "ProviderManager",

                f"{next_provider} not registered."

            )

            return False

        self.activate(

            next_provider

        )

        Debug.log(

            "ProviderManager",

            f"Failover -> {next_provider}"

        )

        return True

    # ==========================================
    # Reset
    # ==========================================

    def reset(

        self

    ):

        if not self.provider_order:

            return

        first = self.provider_order[0]

        if first in self.providers:

            self.activate(

                first

            )

    def health(

        self

    ):

        return {

            "active": self.active_name,

            "registered": list(

                self.providers.keys()

            ),

            "count": len(

                self.providers

            )

        }

    # ==========================================
    # Has Provider
    # ==========================================

    def has_provider(

        self,

        name

    ):

        return name.lower() in self.providers
    
    # ==========================================
    # Priority
    # ==========================================

    def set_priority(

        self,

        providers

    ):

        self.provider_order = [

            provider.lower()

            for provider in providers

        ]

        Debug.log(

            "ProviderManager",

            f"Priority : {self.provider_order}"

        )

    # ==========================================
    # Add Priority
    # ==========================================

    def add_priority(

        self,

        provider

    ):

        provider = provider.lower()

        if provider not in self.provider_order:

            self.provider_order.append(

                provider

            )

    # ==========================================
    # Remove Priority
    # ==========================================

    def remove_priority(

        self,

        provider

    ):

        provider = provider.lower()

        if provider in self.provider_order:

            self.provider_order.remove(

                provider

            )

    # ==========================================
    # Current Priority
    # ==========================================

    def get_priority(

        self

    ):

        return list(

            self.provider_order

        )