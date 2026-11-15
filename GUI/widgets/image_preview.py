import customtkinter as ctk
from PIL import Image
from .. import theme


class ImagePreview(ctk.CTkFrame):
    def __init__(self, master, size=(480, 360), **kwargs):
        super().__init__(
            master,
            width=size[0], height=size[1],
            corner_radius=15,
            fg_color=theme.SURFACE_2,
            border_width=2, border_color=theme.BORDER,
            **kwargs,
        )
        self.size = size
        self.image_path = None
        self._ctk_image = None

        self.pack_propagate(False)

        self.label = ctk.CTkLabel(
            self, text="Здесь будет фото",
            font=theme.FONT_BODY, text_color=theme.TEXT_MUTED,
        )
        self.label.pack(expand=True)

    def set_image(self, path):
        img = Image.open(path)
        img.thumbnail((self.size[0] - 20, self.size[1] - 20))
        self._ctk_image = ctk.CTkImage(light_image=img, size=img.size)
        self.label.configure(image=self._ctk_image, text="")
        self.image_path = path