# Локальные заголовки stb
add_library(stb_headers INTERFACE)
target_include_directories(stb_headers INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/stb)

# Собираем все .cpp из src/
file(GLOB_RECURSE MODULE_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

# Создаем Python-модуль
pybind11_add_module(_dick_cpp ${MODULE_SOURCES})

# Привязываем stb
target_link_libraries(_dick_cpp PRIVATE stb_headers)

# Убираем префикс "lib"
set_target_properties(_dick_cpp PROPERTIES
    PREFIX ""
    OUTPUT_NAME "_dick_cpp"
)

# Установка для scikit-build-core
install(TARGETS _dick_cpp
    LIBRARY DESTINATION _dick_cpp
    RUNTIME DESTINATION _dick_cpp
)

# Для MSVC
if(MSVC)
    add_compile_options(/utf-8)  # И source, и execution charset = UTF-8
endif()

# Для GCC/Clang (обычно не нужно, но на всякий случай)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-finput-charset=UTF-8 -fexec-charset=UTF-8)
endif()