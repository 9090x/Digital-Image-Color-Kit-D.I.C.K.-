from customtkinter import CTkImage
from PIL.Image import Image

def extractor(PATH: str) -> tuple[tuple[str], tuple[str]]:
    """Экстрактор цветовой палитры из фото

    Args:
        PATH (str): Путь до файла

    Returns:
        tuple[tuple[str], tuple[str]]: HEX Кодиравка | RGB Кодиравка
    """
    ...

def converter(PATH: str, chr_palette: str) -> str:
    """Конвертер изображений в ASCII-арт

    Args:
        PATH (str): Путь до файла
        chr_palette (str): Палитра символов (от светлого, до тёмного)

    Returns:
        str: изображение ввиде строки
    """
    ...

def generator(first_color: tuple[int, int, int], second_color: tuple[int, int, int]) -> tuple[tuple[tuple[str], tuple[str]], CTkImage, Image]:
    """Генератор градиентов (Gradient Maker)

    Args:
        first_color (tuple[int, int, int]): Первый цвет (RGB)
        second_color (tuple[int, int, int]): Второй цвет (RGB)

    Returns:
        tuple[tuple[tuple[str], tuple[str]], CTkImage, Image]: _description_
    """
    ...