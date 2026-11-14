#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdexcept>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <iostream>
#include <vector>
#include <string>
#include <tuple>


using namespace std;
namespace py = pybind11;

//-----------------------------------------------------------------------------------------
pair<int, int> extractor(string PATH){
    int width, height, channels;
    unsigned char* img_data = stbi_load(PATH.c_str(), &width, &height, &channels, 0);
    stbi_image_free(img_data);
    return make_pair(width, height);
}


//-----------------------------------------------------------------------------------------
// Макрос регистрации модуля. Имя должно совпадать с тем, что в CMakeLists.txt
PYBIND11_MODULE(_dick_cpp, m) {
    m.doc() = "C++ extension for dick library";
    
    // py::arg делает аргументы именованными в Python (хорошая практика)
    //m.def("add", &add, "Add two integers", py::arg("a"), py::arg("b"));
    m.def("extractor", &extractor, "TEST", py::arg("PATH"));
}