from aura.ui.sidebar import Sidebar

from aura.ui.header import Header

from aura.ui.home import Home

from aura.ui.statusbar import StatusBar


class Layout:

    def __init__(self, root):

        self.root = root

    def build(self):

        self.root.grid_columnconfigure(1, weight=1)

        self.root.grid_rowconfigure(1, weight=1)

        sidebar = Sidebar(self.root)

        sidebar.grid(

            row=0,

            column=0,

            rowspan=3,

            sticky="ns"

        )

        header = Header(self.root)

        header.grid(

            row=0,

            column=1,

            sticky="ew"

        )

        home = Home(self.root)

        home.grid(

            row=1,

            column=1,

            sticky="nsew"

        )

        status = StatusBar(self.root)

        status.grid(

            row=2,

            column=1,

            sticky="ew"

        )