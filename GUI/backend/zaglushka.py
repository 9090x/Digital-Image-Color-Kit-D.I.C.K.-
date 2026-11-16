# GUI/backend/dick_backend.py
from PIL import Image
from typing import Tuple, List
from _dick_cpp import dick_wrapper as dw

def extractor(image_path: str) -> Tuple[List[str], List[Tuple[int, int, int]]]:
    """Извлекает палитру из изображения"""
    return dw.extractor(image_path)

def to_ascii(image_path: str) -> str:
    return dw.converter(image_path, 
                        ".'^,:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$`",
                        400,
                        200)
    

def make_gradient(color1, color2, steps: int = 10) -> Tuple[List[str], List[Tuple[int, int, int]]]:
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