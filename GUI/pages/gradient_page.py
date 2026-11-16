from ._base_page import BasePage
import customtkinter as ctk
from tkinter import colorchooser
from .. import theme


class GradientPage(BasePage):
    title = "Gradient Maker"

    def build_ui(self):
        self.colors={"first": "#F2A93B", "last": "#0F0D0A"}
        self.swatches={}
        self.hex_labels={}
        self.last_result = None

        self.grid_columnconfigure(0,weight=0)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)

        ctk.CTkLabel(
            self, text="Gradient Maker",
            font=theme.FONT_TITLE, 
            text_color=theme.HONEY
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=40, pady=(30, 10))

        self.left=ctk.CTkFrame(self, fg_color="transparent")
        self.left.grid(row=1, column=0, sticky="n", padx=(40, 20), pady=(0, 30))

        self._build_color_block(self.left, "first", "Первый цвет")
        self._build_color_block(self.left, "last", "Последний цвет")

        self.make_btn =ctk.CTkButton(
            self.left, text="Создать градиент", 
            height=44, width=200,
            corner_radius=12, 
            font=theme.FONT_BUTTON,
            text_color=theme.TEXT_ON_HONEY,
            fg_color=theme.HONEY, hover_color=theme.HONEY_HOVER,
            command=self.on_make,
        )
        self.make_btn.pack(pady=(10, 0))

        self.result = ctk.CTkFrame(
            self, corner_radius=20, fg_color=theme.SURFACE_2,
            border_width=2, border_color=theme.BORDER,
        )
        self.result.grid(row=1, column=1, sticky="nsew", padx=(20, 40), pady=(0, 30))
        self.result.pack_propagate(False)

        ctk.CTkLabel(
            self.result, text= "Здесь появится градиент",
            font=theme.FONT_BODY, text_color=theme.TEXT_MUTED,
        ).pack(expand=True)

    def _build_color_block(self, parent, key, label):
        block = ctk.CTkFrame(parent, fg_color="transparent")
        block.pack(pady=10)

        ctk.CTkLabel(
            block, text=label,
            font=theme.FONT_SUBTITLE, 
            text_color=theme.TEXT
        ).pack(pady=(0, 8))

        swatch = ctk.CTkFrame(block, width=200, height=90, corner_radius=15,fg_color=self.colors[key],border_width=2, border_color=theme.BORDER,)
        swatch.pack()
        swatch.pack_propagate(False)

        hex_label = ctk.CTkLabel(
            block, text=self.colors[key],
            font=theme.FONT_MONO_BODY, 
            text_color=theme.TEXT_MUTED,
        )
        hex_label.pack(pady=6)

        ctk.CTkButton(
            block, text="Выбрать цвет", 
            width=140, height=36,
            corner_radius=10, 
            font=theme.FONT_BODY,
            text_color=theme.HONEY, 
            fg_color=theme.SURFACE_2,
            hover_color=theme.BG,
            command=lambda: self.ask_color(key),
        ).pack()

        self.swatches[key]=swatch # квадрат блока
        self.hex_labels[key] =hex_label # подпись блока

    def ask_color(self, key):
        rgb, hex_color = colorchooser.askcolor(color=self.colors[key], parent=self)
        if hex_color is None:
            return
        self.colors[key]=hex_color.upper()
        self.swatches[key].configure(fg_color=self.colors[key]) # перекрас 
        self.hex_labels[key].configure(text=self.colors[key]) #надпись нового кода цвета

    def on_make(self):
        def HexToRgb(HEX: str) -> tuple[int, int, int]:
            HEX = HEX.replace("#", "")
            return int(HEX[:2:], 16), int(HEX[2:4:], 16), int(HEX[4:6:], 16)

        first = HexToRgb(self.colors["first"])
        last = HexToRgb(self.colors["last"])

        image = self.backend.make_gradient(first, last, self.result.winfo_width(), self.result.winfo_height())[1]

        ctk_image = ctk.CTkImage(image, image, (self.result.winfo_width(), self.result.winfo_height()))

        for widget in self.result.winfo_children():
            widget.destroy()
        label = ctk.CTkLabel(self.result, image=ctk_image, text="")
        label.pack(expand=True, fill="both")
        self.__output_ctk_image = ctk_image
