# GUI/backend/dick_backend.py
from PIL import Image
from typing import Tuple, List

class DickBackend:
    def extractor(self, image_path: str, num_colors: int = 5) -> Tuple[List[str], List[Tuple[int, int, int]]]:
        """Извлекает палитру из изображения"""
        img = Image.open(image_path).convert('RGB')
        img = img.resize((150, 150))
        img = img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
        
        palette_data = img.getpalette()[:num_colors * 3]
        hexes = []
        rgbs = []
        
        for i in range(0, len(palette_data), 3):
            r, g, b = palette_data[i], palette_data[i+1], palette_data[i+2]
            hex_val = f"#{r:02x}{g:02x}{b:02x}"
            hexes.append(hex_val)
            rgbs.append((r, g, b))
            
        return hexes, rgbs
    
    def to_ascii(self, image_path: str, palette: str = "standard", width: int = 100) -> str:
        """Конвертирует изображение в ASCII-арт"""
        palettes = {
            "standard": "@%#*+=-:. ",
            "blocks": "█▓▒░ ",
            "minimal": "#-. "
        }
        
        img = Image.open(image_path).convert('L')
        wpercent = (width / float(img.size[0]))
        height = int((float(img.size[1]) * float(wpercent)) * 0.5)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        pixels = img.getdata()
        chars = palettes.get(palette, palettes["standard"])
        new_pixels = [chars[(pixel * (len(chars) - 1)) // 255] for pixel in pixels]
        new_pixels = "".join(new_pixels)
        
        ascii_str = ""
        for i in range(0, len(new_pixels), width):
            ascii_str += new_pixels[i:i + width] + "\n"
            
        return ascii_str
    
    def make_gradient(self, color1, color2, steps: int = 10) -> Tuple[List[str], List[Tuple[int, int, int]]]:
        """Создает градиент между двумя цветами"""
        def parse_color(c):
            if isinstance(c, str):
                c = c.lstrip('#')
                return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
            return c
        
        c1 = parse_color(color1)
        c2 = parse_color(color2)
        
        hexes = []
        rgbs = []
        
        for i in range(steps):
            ratio = i / (steps - 1)
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            
            rgb_tuple = (r, g, b)
            hex_val = f"#{r:02x}{g:02x}{b:02x}"
            hexes.append(hex_val)
            rgbs.append(rgb_tuple)
            
        return hexes, rgbs