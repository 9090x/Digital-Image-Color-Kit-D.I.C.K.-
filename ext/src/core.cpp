#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdexcept>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <iostream>
#include <algorithm>
#include <unordered_set>
#include <string>
#include <unordered_map>
#include <vector>
#include <tuple>

//----------------------------------------------------------------------------------------- ERRORS
using namespace std;
namespace py = pybind11;

class ImageNotFoundError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

//-----------------------------------------------------------------------------------------STRUCTS
struct Color{
    uint8_t r;
    uint8_t g;
    uint8_t b;
    uint8_t a;

    Color() = default;

    string HexCode() const {
        const char hex[] = "0123456789ABCDEF";
        char buf[10];
        buf[0] = '#';
        buf[1] = hex[r >> 4];   //r//16
        buf[2] = hex[r & 0x0F]; //r%15
        buf[3] = hex[g >> 4];
        buf[4] = hex[g & 0x0F];
        buf[5] = hex[b >> 4];
        buf[6] = hex[b & 0x0F];
        buf[7] = hex[a >> 4];
        buf[8] = hex[a & 0x0F];
        buf[9] = '\0';
        return string(buf);
    }

    string RgbCode() const{
        return "rgb(" + to_string(r) + ", " + to_string(g) + ", " + to_string(b) + ", " + to_string((static_cast<double>(a) / 255.0)) + ')';
    }


    bool operator<(const Color& other) const {
        if (r != other.r) return r < other.r;
        if (g != other.g) return g < other.g;
        if (b != other.b) return b < other.b;
        return a < other.a;
    }

    bool operator==(const Color& other) const {
        return r == other.r && g == other.g && b == other.b && a == other.a;
    }

};

//-----------------------------------------------------------------------------------------Extractor-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------SUB_FUNC
pair<vector<string>, vector<string>> VectorsColorOfString(const vector<Color>& pixels){
    vector<string> hex, rgb;
    for (const Color& pixel:pixels){
        hex.push_back(pixel.HexCode());
        rgb.push_back(pixel.RgbCode());
    }

    return make_pair(hex, rgb);
}

vector<Color> generatePalette16(const vector<Color>& pixels) {
    vector<Color> palette;
    
    if (pixels.empty()) {
        return palette;
    }
    
    const size_t targetSize = 16;
    
    if (pixels.size() <= targetSize) {
        return pixels;
    }
    
    palette.reserve(targetSize);
    

    double step = static_cast<double>(pixels.size() - 1) / (targetSize - 1);
    
    for (size_t i = 0; i < targetSize; ++i) {
        size_t index = static_cast<size_t>(std::round(i * step));
        
        if (index >= pixels.size()) {
            index = pixels.size() - 1;
        }
        
        palette.push_back(pixels[index]);
    }
    
    return palette;
}

//-----------------------------------------------------------------------------------------MAIN_FUNC
pair<vector<string>, vector<string>> extractor(const string& PATH){
    //image
    int width, height, channels;
    auto img_data = std::unique_ptr<unsigned char[], void(*)(unsigned char*)>(
        stbi_load(PATH.c_str(), &width, &height, &channels, 0), 
        [](unsigned char* p) { stbi_image_free(p); }
    );

    if (!img_data){
        throw ImageNotFoundError("Image `" + PATH + "`not exist!");
    }

    //pixels parcing
    vector<Color> pixels;

    for (int y{0}; y < height; ++y){
        for (int x{0}; x < width; ++x){
            int index = (y * width + x) * channels;

            pixels.push_back({static_cast<uint8_t>(img_data[index]), static_cast<uint8_t>(img_data[index+1]), static_cast<uint8_t>(img_data[index+2]), (channels == 4)? static_cast<uint8_t>(img_data[index+3]) : uint8_t(255)});
        }
    }

    //return
    sort(pixels.begin(), pixels.end());
    pixels.erase(unique(pixels.begin(), pixels.end()), pixels.end());


    return VectorsColorOfString(generatePalette16(pixels));
}


//-----------------------------------------------------------------------------------------
// Макрос регистрации модуля. Имя должно совпадать с тем, что в CMakeLists.txt
PYBIND11_MODULE(_dick_cpp, m) {
    m.doc() = "C++ extension for dick library";
    
    //errors
    py::register_exception<ImageNotFoundError>(m, "ImageNotFoundError", PyExc_FileNotFoundError);

    // py::arg делает аргументы именованными в Python (хорошая практика)
    //m.def("add", &add, "Add two integers", py::arg("a"), py::arg("b"));
    m.def("extractor", &extractor, "TEST", py::arg("PATH"));
}