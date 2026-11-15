from _dick_cpp import _dick_cpp

def HextoRgb(HEX: str) -> tuple[int, int, int] | tuple[int, int, int, float] | None:
    """Переобразует HEX кадировку в RGB.

    Args:
        HEX (str): HEX строка - от 0(000000), до 16777215(FFFFFF), `!Не считая прозрачность!`. БЕЗ ПРИСТАВКИ `0x`!

    Returns:
        tuple[int, int, int]: Кортеж с RGB цветами
    """

    #Валидация данных
    #-----------------------------------------------------------------------------------------
    if not isinstance(HEX, str): return None
    if len(HEX) not in (6, 8) or not set(HEX).issubset(("0123456789ABCDF")): return None

    #-----------------------------------------------------------------------------------------
    if len(HEX) == 6: return int(HEX[0:2:], 16), int(HEX[2:4:], 16), int(HEX[4::], 16)
    return int(HEX[0:2:], 16), int(HEX[2:4:], 16), int(HEX[4:6:], 16), int(HEX[6::], 16)/255

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
    return _dick_cpp.converter(PATH, palette, aim, width, height)