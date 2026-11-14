def HextoRgb(HEX: str) -> tuple[int, int, int] | None:
    """Переобразует HEX кадировку в RGB.

    Args:
        HEX (str): HEX строка - от 0(000000), до 16777215(FFFFFF). БЕЗ ПРИСТАВКИ `0x`!

    Returns:
        tuple[int, int, int]: Кортеж с RGB цветами
    """

    #Валидация данных
    #-----------------------------------------------------------------------------------------
    if not isinstance(HEX, str): return None
    if len(HEX) != 6 or not set(HEX).issubset(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "F")): return None

    return int(HEX[0:2:], 16), int(HEX[2:4:], 16), int(HEX[4::], 16)

