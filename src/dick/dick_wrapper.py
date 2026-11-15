from _dick_cpp import _dick_cpp
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image

def extractor(PATH: str) -> tuple[list[str], list[str]]:
    """Извлекает цветовую палитру из изображения по заданному пути.
    Функция загружает изображение, извлекает все уникальные цвета, сортирует их 
    и формирует палитру из 16 цветов, равномерно распределенных по отсортированному набору. 
    Возвращает два списка со строковыми представлениями этих цветов в форматах HEX и RGB.

    Args:
        PATH (str): Строка, содержащая путь к файлу изображения.

    Returns:
        tuple[list[str], list[str]]: Пара списков строк, где первый список содержит 
                                        HEX-коды цветов, а второй — их RGB-коды.
    """
    return _dick_cpp.extractor(PATH)

def converter(PATH: str, palette: str, width: int, height: int, aim=0.9) -> str:
    """Преобразует изображение в символьное (ASCII-арт) представление.
    Функция разбивает изображение на пропорциональные блоки, вычисляет среднюю 
    яркость (с учетом альфа-канала, если он есть) для каждого блока по формуле 
    люминанса и сопоставляет полученное значение с символами из заданной палитры.

    Args:
        PATH (str): Путь к файлу исходного изображения.
        palette (str): Строка символов для отрисовки, упорядоченная от самого 
                       "темного" к самому "светлому" (минимум 2 символа).
        width (int): Целевая ширина выходного текстового изображения в символах.
        height (int): Целевая высота выходного текстового изображения в строках.
        aim (float, optional): Коэффициент масштабирования яркости для маппинга 
                               на палитру (диапазон: >0.0 до 1.0). Регулирует 
                               общую яркость и контрастность результата. Defaults to 0.9.

    Returns:
        str: Многострочная строка, представляющая собой символьную копию 
             исходного изображения.
    """
    return _dick_cpp.converter(PATH, palette, aim, width, height)

def generator(first_color: tuple[int, int, int] | tuple[int, int, int, int|float], second_color: tuple[int, int, int] | tuple[int, int, int, int|float], width: int, height: int) -> tuple[tuple[tuple[str], tuple[str]], CTkImage, Image.Image]:
    """Генерирует плавный градиент между двумя заданными цветами.
    Основная математика интерполяции выполняется на стороне C++ для максимальной 
    скорости, после чего результат упаковывается в удобные для Python объекты.

    Args:
        first_color (tuple[int, int, int] | tuple[int, int, int, int]): Начальный цвет градиента в формате RGB или RGBA.
        second_color (tuple[int, int, int] | tuple[int, int, int, int]): Конечный цвет градиента в формате RGB или RGBA.
        width (int): Ширина генерируемого изображения в пикселях.
        height (int): Высота генерируемого изображения в пикселях.

    Returns:
        tuple[tuple[tuple[str], tuple[str]], CTkImage, Image.Image]: Кортеж из трех элементов:
            1. Пара кортежей со строковыми представлениями цветов (первый кортеж содержит HEX-коды, второй — строки формата RGB/RGBA).
            2. Объект `CTkImage`, полностью готовый для вставки в интерфейс CustomTkinter.
            3. Объект `Image.Image` (PIL/Pillow), представляющий собой исходное сгенерированное растровое изображение.
    """
    if not (len(first_color) in (3, 4) or len(first_color) in (3, 4)): raise ValueError("`first_color` and `second_color` must be RGB or RGBA")
    if len(first_color) == 3: first_color = (*first_color, 255)
    if len(second_color) == 3: second_color = (*second_color, 255)
    if isinstance(first_color[3], float): first_color = (*first_color[:-1:], int(255*first_color[3]))
    if isinstance(second_color[3], float): second_color = (*second_color[:-1:], int(255*second_color[3]))

    colors, byte_str = _dick_cpp.generator(first_color, second_color, width, height)
    image = Image.frombytes("RGBA", (width, height), byte_str*height)
    return colors, CTkImage(image, size=(width, height)), image