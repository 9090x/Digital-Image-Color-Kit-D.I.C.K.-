import customtkinter as ctk


class BasePage(ctk.CTkFrame):
    title = ""

    def __init__(self, master, backend=None, **kwargs):
        super().__init__(master, **kwargs)
        self.backend = backend
        self.build_ui()

    def build_ui(self):
        raise NotImplementedError