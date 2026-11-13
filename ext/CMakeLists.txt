include(FetchContent)

# Тянем pybind11 с GitHub (стабильная ветка)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.13.6
)
FetchContent_MakeAvailable(pybind11)

# Собираем модуль из всех .cpp в src/
file(GLOB_RECURSE DICK_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

pybind11_add_module(_dick_cpp ${DICK_SOURCES})

# Имя выходного файла (без lib-префикса на Linux)
set_target_properties(_dick_cpp PROPERTIES
    PREFIX ""
    OUTPUT_NAME "_dick_cpp"
)

target_link_libraries(_dick_cpp PRIVATE some_lib)

# Устанавливаем .so/.pyd прямо в пакет dick/
install(TARGETS _dick_cpp
    LIBRARY DESTINATION dick
    RUNTIME DESTINATION dick
)