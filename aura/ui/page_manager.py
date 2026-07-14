import customtkinter as ctk


class PageManager:

    def __init__(self, parent):

        self.parent = parent

        self.pages = {}

        self.current_page = None

    def register_page(self, name, page):

        self.pages[name] = page

    def show_page(self, name):

        if self.current_page:

            self.current_page.grid_remove()

        page = self.pages[name]

        page.grid(
            row=1,
            column=1,
            sticky="nsew"
        )

        self.current_page = page

    def get_current_page(self):

        return self.current_page