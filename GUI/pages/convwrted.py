from ._base_page import BasePage
import customtkinter as ctk
from .. import theme
from tkinterdnd2 import DND_FILES
from PIL import Image
from tkinter import filedialog

class AsciiPage(BasePage):
    title = "Конвертер изображений в ASCII-арт"

    def on_drop(self, event):
        path =self.tk.splitlist(event.data)[0]
        self.load(path)

    def load(self, path):
        self.show_image(path)
        self.ascii_art= self.backend.to_ascii(path)

        self.save_btn.configure(state="normal")

        self.save_hint.configure(text="Ваш ASCII-арт готов!\nНажмите кнопку, чтобы сохранить его в файл.")
        self.save_hint.configure(text_color=theme.TEXT)

    def show_image(self, path):
        img= Image.open(path)
        img.thumbnail((380, 400))
        self._image= ctk.CTkImage(light_image=img, size=img.size)
        self.hint.configure(image=self._image, text="")
    
    def build_ui(self):
        self.title =ctk.CTkLabel(
            self, text="ASCII Art",
            font=theme.FONT_TITLE, 
            text_color=theme.HONEY
        )
        self.title.pack(side="top", anchor="w", padx=40, pady=(30, 0))

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=(20, 40))

        self.zone=ctk.CTkFrame(
            self.main_frame, 
            width=480,     
            height=520,    
            corner_radius=20, 
            border_width=2, 
            border_color=theme.BORDER,
            fg_color=theme.SURFACE_2
        )
        self.zone.pack(side="left", fill="y", padx=(0, 20))
        self.zone.pack_propagate(False)

        self.hint=ctk.CTkLabel(
            self.zone, 
            text="Перетащите изображение сюда\nили нажмите кнопку ниже",
            font=theme.FONT_BODY, 
            text_color=theme.TEXT_MUTED,
        )
        self.hint.pack(expand=True)

        self.zone.drop_target_register(DND_FILES)
        self.zone.dnd_bind("<<Drop>>", self.on_drop)

        self.button = ctk.CTkButton(
            self.zone, 
            width=200, 
            height=48, 
            text="Выбрать файл",
            font=theme.FONT_BUTTON, 
            text_color=theme.TEXT_ON_HONEY, 
            fg_color=theme.HONEY, 
            hover_color=theme.HONEY_HOVER,
            command=self.on_choose
        )
        self.button.pack(side="bottom", pady=(0, 30))

        self.output_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.output_container.pack(side="left", fill="both", expand=True)

        self.save_group = ctk.CTkFrame(self.output_container, fg_color="transparent")
        self.save_group.pack(expand=True)

        self.save_hint = ctk.CTkLabel(
            self.save_group,
            text="Здесь появится\nкнопка сохранения",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_MUTED,
            justify="center"
        )
        self.save_hint.pack(pady=(0, 20))

        self.save_btn = ctk.CTkButton(
            self.save_group,
            text="Скачать TXT",
            width=200,  
            height=48,
            corner_radius=12,
            font=theme.FONT_BUTTON,
            text_color=theme.TEXT_ON_HONEY, 
            fg_color=theme.HONEY,           
            hover_color=theme.HONEY_HOVER,
            command=self.on_save,
            state="disabled"
        )
        self.save_btn.pack()

    def on_choose(self):
        path=filedialog.askopenfilename(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if path:
            self.load(path)

    def on_save(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Сохранить ASCII-арт как"
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.ascii_art)