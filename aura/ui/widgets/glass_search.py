import customtkinter as ctk

from aura.ui.widgets.glass_entry import GlassEntry

from aura.ui.widgets.glass_icon import GlassIcon


class GlassSearch(

    GlassEntry

):

    """
    ==================================================

                Glass Search

    Composition

        GlassBar
            +
        Search Icon
            +
        CTkEntry

    Used by

        Memory
        Study Hub
        Plugins
        Settings
        Calendar
        News

    ==================================================
    """

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(

        self,

        master,

        placeholder="Search...",

        size=(500,60),

        **kwargs

    ):

        super().__init__(

            master,

            placeholder=placeholder,

            bar="search_bar",

            size=size,

            **kwargs

        )

        self.build_search()

    # ==================================================
    # Build Search
    # ==================================================

    def build_search(

        self

    ):

        self.text = GlassIcon(

            self.content,

            category="system",

            name="search",

            size=(22,22)

        )

        self.text.place(

            relx=0.03,

            rely=0.5,

            anchor="w"

        )

        self.entry.pack_forget()

        self.entry.pack(

            fill="both",

            expand=True,

            padx=(52,18),

            pady=10

        )

    # ==================================================
    # Search Text
    # ==================================================

    def search(

        self

    ):

        return self.get()
    
    # ==================================================
    # Set Search
    # ==================================================

    def set_search(

        self,

        text

    ):

        self.set(

            text

        )

    # ==================================================
    # Clear Search
    # ==================================================

    def clear_search(

        self

    ):

        self.clear()

    # ==================================================
    # Bind Search
    # ==================================================

    def bind_search(

        self,

        callback

    ):

        self.bind(

            "<Return>",

            callback

        )

