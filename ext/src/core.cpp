#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>
#include <stdexcept>

namespace py = pybind11;

// 1. Простая математика
int add(int a, int b) {
    return a + b;
}

// 2. Работа со строками
std::string greet(const std::string& name) {
    return "Hello, " + name + " from C++!";
}

// 3. Проверка исключений (std::invalid_argument -> ValueError в Python)
double divide(double a, double b) {
    if (b == 0.0) {
        throw std::invalid_argument("Division by zero is not allowed");
    }
    return a / b;
}

// Макрос регистрации модуля. Имя должно совпадать с тем, что в CMakeLists.txt
PYBIND11_MODULE(dick, m) {
    m.doc() = "C++ extension for dick library";
    
    // py::arg делает аргументы именованными в Python (хорошая практика)
    m.def("add", &add, "Add two integers", py::arg("a"), py::arg("b"));
    m.def("greet", &greet, "Greet someone", py::arg("name"));
    m.def("divide", &divide, "Divide two numbers", py::arg("a"), py::arg("b"));
}