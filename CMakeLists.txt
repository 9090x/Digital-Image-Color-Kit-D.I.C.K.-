cmake_minimum_required(VERSION 3.15...3.30)
project(dick VERSION 0.1.0 LANGUAGES CXX)

# Стандарт C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# scikit-build-core автоматически настраивает пути к Python 3.13
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Собираем все .cpp из папки ext/src/
file(GLOB_RECURSE DICK_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/ext/src/*.cpp")

# Создаём Python-модуль
pybind11_add_module(_dick_cpp ${DICK_SOURCES})

# Указываем scikit-build-core установить .so/.pyd прямо в папку dick/
install(TARGETS _dick_cpp DESTINATION dick)