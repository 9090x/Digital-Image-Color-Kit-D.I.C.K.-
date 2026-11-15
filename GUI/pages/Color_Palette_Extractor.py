from ._base_page import BasePage
import customtkinter as ctk
from .. import theme
from tkinter import filedialog
from tkinterdnd2 import DND_FILES
from PIL import Image


def clean_hex(h):
    """'#828282FF' или '828282' -> '#828282'"""
    return "#" + str(h).strip().lstrip("#")[:6].upper()

class PalettePage(BasePage):
    title = "Палитра"

    def build_ui(self):
        ctk.CTkLabel(
            self, 
            text="Палитра из фото",
            font=theme.FONT_TITLE, 
            text_color=theme.HONEY
        ).pack(side="top", anchor="w", padx=40, pady=(30, 0))

        self.zone = ctk.CTkFrame(
            self, width=340, 
            height=420, 
            corner_radius=20,
            border_width=2, 
            border_color=theme.BORDER,
            fg_color=theme.SURFACE_2
        )
        self.zone.pack(side="left", padx=(40, 0), pady=(20, 40))
        self.zone.pack_propagate(False)

        self.hint = ctk.CTkLabel(
            self.zone,
            text="Перетащите изображение сюда\nили нажмите кнопку ниже",
            font=theme.FONT_BODY, 
            text_color=theme.TEXT_MUTED
        )
        self.hint.pack(expand=True)

        self.zone.drop_target_register(DND_FILES)
        self.zone.dnd_bind("<<Drop>>", self.on_drop)

        self.choose_btn = ctk.CTkButton(
            self.zone, text="Выбрать файл", height=44,
            corner_radius=12, 
            font=theme.FONT_BUTTON,
            text_color=theme.TEXT_ON_HONEY,
            fg_color=theme.HONEY, 
            hover_color=theme.HONEY_HOVER,
            command=self.on_choose
        )
        self.choose_btn.pack(side="bottom", pady=(0, 30))

        self.clear_btn = ctk.CTkButton(
            self.zone, text="Отменить выбор", height=44,
            corner_radius=12,
            font=theme.FONT_BUTTON,
            text_color=theme.TEXT,
            fg_color=theme.SURFACE_2,
            hover_color=theme.BORDER,
            border_width=2,
            border_color=theme.BORDER,
            command=self.reset
        )
        self.clear_btn.pack(side="bottom", pady=(0, 10))

        self.color_list = ctk.CTkScrollableFrame(
            self, corner_radius=20,
            fg_color=theme.SURFACE_2,
            border_width=2, 
            border_color=theme.BORDER,
        )
        self.color_list.pack(side="left", fill="both",expand=True,padx=40, pady=(20, 40),)
        self.empty_label = ctk.CTkLabel(
            self.color_list, 
            text="Здесь появятся цвета",
            font=theme.FONT_BODY, 
            text_color=theme.TEXT_MUTED,
        )
        self.empty_label.pack(pady=20)

    def on_drop(self, event):
        path = self.tk.splitlist(event.data)[0]
        self.load(path)

    def on_choose(self):
        path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if path:
            self.load(path)

    def load(self, path):
        self.show_image(path)
        hexes, rgbs = self.backend.extractor(path)
        self.show_colors(hexes, rgbs)


    def show_image(self, path):
        img = Image.open(path)
        img.thumbnail((300, 280))
        self._image = ctk.CTkImage(light_image=img, size=img.size)
        self.hint.configure(image=self._image, text="")


    def clear_color(self):
        for w in self.color_list.winfo_children():
            w.destroy()

    def show_colors(self, hexes, rgbs):
        self.clear_color()
        s = set()
        for h, rgb in zip(hexes, rgbs):
            h = clean_hex(h)
            if h in s:
                continue
            s.add(h)

            row = ctk.CTkFrame(self.color_list, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=4)

            ctk.CTkFrame(
                row, width=70, height=44, corner_radius=10,
                fg_color=h, border_width=2, border_color=theme.BORDER,
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=h, width=90, anchor="w",
                font=theme.FONT_MONO_BODY, text_color=theme.TEXT,
            ).pack(side="left", padx=(14, 0))

            ctk.CTkLabel(
                row, text=str(tuple(rgb)), anchor="w")
    def reset(self):
        self._image = None
        self.hint.configure(image="", text="Перетащите изображение сюда\nили нажмите кнопку ниже")

        self.clear_color()
        self.empty_label = ctk.CTkLabel(
            self.color_list,
            text="Здесь появятся цвета",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_MUTED,
        )
        self.empty_label.pack(pady=20)