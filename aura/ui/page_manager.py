import customtkinter as ctk


class PageManager:

    def __init__(self, root):

        self.root = root

        self.pages = {}

        self.current_page = None

    # ------------------------------------------

    def register_page(self, name, page):

        self.pages[name] = page

        page.grid(

            row=1,

            column=1,

            sticky="nsew",

            padx=(0, 15),

            pady=(0, 15)

        )

        page.grid_remove()

    # ------------------------------------------

    def show_page(self, name):

        if name not in self.pages:

            print(f"Page '{name}' not found.")

            return

        if self.current_page is not None:

            self.current_page.grid_remove()

        self.current_page = self.pages[name]

        self.current_page.grid()

    # ------------------------------------------

    def get_page(self, name):

        return self.pages.get(name)

    # ------------------------------------------

    def remove_page(self, name):

        if name in self.pages:

            page = self.pages.pop(name)

            page.destroy()

    # ------------------------------------------

    def page_exists(self, name):

        return name in self.pages

    # ------------------------------------------

    def list_pages(self):

        return list(self.pages.keys())