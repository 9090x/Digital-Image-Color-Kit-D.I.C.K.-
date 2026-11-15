# Импортируем всё из скомпилированного C++ модуля
from ._dick_cpp import (
    extractor,
    ImageNotFoundError,
    ImageDecodeError,
)

# Явно указываем, что экспортируется при `from dick import *`
__all__ = [
    "extractor",
    "ImageNotFoundError",
    "ImageDecodeError",
]

# Опционально: версия пакета (можно брать из pyproject.toml)
__version__ = "0.1.0"