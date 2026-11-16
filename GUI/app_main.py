import customtkinter as ctk
from PIL import Image
from . import theme
from .pages._base_page import BasePage
from .pages.Color_Palette_Extractor import PalettePage
from .pages.convwrted import AsciiPage
from .pages.gradient_page import GradientPage
from tkinterdnd2 import TkinterDnD
from _dick_cpp import dick_wrapper as _dick


class DnDWindow(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class App:
    def __init__(self):
        self.root = DnDWindow(fg_color=theme.BG)
        self.root.geometry("1200x650")
        self.root.title("Digital Image Color Kit")
        self.root.minsize(900, 600)
        self.root.maxsize(1200, 650)

        ctk.set_appearance_mode("Dark")

        self.sidebar = ctk.CTkFrame(
            self.root, 
            width=120, 
            corner_radius=0, 
            fg_color=theme.SURFACE
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.container = ctk.CTkFrame(
            self.root, 
            width=120,
            corner_radius=0, 
            fg_color=theme.SURFACE)
        self.container.pack_propagate(False)
        self.container.pack(
            side="right", 
            fill="both", 
            expand=True, 
            padx=20, 
            pady=20)

        self.menu_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_box.place(relx=0.5, rely=0.5, anchor="center")

        self.button_gradient = ctk.CTkButton(
            self.menu_box, width=96, height=56, corner_radius=12,
            text="Градиент", font=theme.FONT_BUTTON,
            text_color=theme.HONEY,
            fg_color=theme.SURFACE, hover_color=theme.BG
        )
        self.button_gradient.pack(pady=8)

        self.button_color_pallete=ctk.CTkButton(
            self.menu_box, 
            width=96, 
            height=56, 
            corner_radius=12,
            text="Палитра", 
            font=theme.FONT_BUTTON,
            text_color=theme.HONEY,
            fg_color=theme.SURFACE, 
            hover_color=theme.BG
        )
        self.button_color_pallete.pack(pady=8)

        self.button_conwerted =ctk.CTkButton(
            self.menu_box, 
            width=96, 
            height=56, 
            corner_radius=12,
            text="ASCII", font=theme.FONT_BUTTON,
            text_color=theme.HONEY,
            fg_color=theme.SURFACE, 
            hover_color=theme.BG
        )
        self.button_conwerted.pack(pady=8)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {
            "gradient":GradientPage(master=self.container, backend=_dick), # Заполнить
            "palette":PalettePage(master=self.container, backend=_dick),# Заполнить
            "ascii":AsciiPage(master=self.container, backend=_dick)# Заполнить
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")
            
        self.button_gradient.configure(command=lambda: self.show_page("gradient"))
        self.button_color_pallete.configure(command=lambda: self.show_page("palette"))
        self.button_conwerted.configure(command=lambda: self.show_page("ascii"))
        
        self.show_page("gradient")

    def run(self):
        self.root.mainloop()

    def show_page(self, key):
        self.pages[key].tkraise()
        

if __name__ == "__main__":
    App().run()
