#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdexcept>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#include <cmath>
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
    uint8_t r{};
    uint8_t g{};
    uint8_t b{};
    uint8_t a{};


    string toBytes() const {
        string result;
        result.reserve(4);
        result.push_back(static_cast<unsigned char>(r));
        result.push_back(static_cast<unsigned char>(g));
        result.push_back(static_cast<unsigned char>(b));
        result.push_back(static_cast<unsigned char>(a));
        return result;
    }

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

//-----------------------------------------------------------------------------------------converter-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------MAIN_FUNC
string converter(const string& PATH, const string& palette, const double aim, const int width, const int height){
    //-----------------------------------------------------------------------------------------image
    int img_width, img_height, channels;
    auto img_data = std::unique_ptr<unsigned char[], void(*)(unsigned char*)>(
        stbi_load(PATH.c_str(), &img_width, &img_height, &channels, 0), 
        [](unsigned char* p) { stbi_image_free(p); }
    );

    //-----------------------------------------------------------------------------------------validation
    if (!img_data){
        throw ImageNotFoundError("Image `" + PATH + "`not exist!");
    }
    if (width < 1 || width > img_width || height < 1 ||  height > img_height) throw py::value_error("`width`{" + to_string(width) + "} and `height`{" + to_string(height) + "} must be bigger than `0` and smaller than image's size");
    if (aim < 0.0 || aim > 1.0) throw py::value_error("`aim`{" + to_string(aim) + "} must be from `0` to `1`");

    //-----------------------------------------------------------------------------------------MAIN
    const double K {(255.0 * aim)/(palette.length()-1)};
    const int chunk_width{img_width / width}, chunk_height{img_height / height}, chunk_size{chunk_width * chunk_height};
    string output {""};
    output.reserve(height * (width + 1));

    //-----------------------------------------------------------------------------------------core_itteration
    for (int global_y{0}; global_y < height; ++global_y){
        for (int global_x{0}; global_x < width; ++global_x){
            uint64_t R{0}, G{0}, B{0}, A{0};

            const int actual_y{global_y*chunk_height}, actual_x{global_x*chunk_width};

            //-----------------------------------------------------------------------------------------sub_core_itteration
            for (int sub_y{actual_y}; sub_y < actual_y+chunk_height; ++sub_y){
                for (int sub_x{actual_x}; sub_x < actual_x+chunk_width; ++sub_x){
                    const int index = (sub_y * img_width + sub_x) * channels;
                    R += img_data[index];
                    G += img_data[index+1];
                    B += img_data[index+2];
                    if (channels == 4) A += img_data[index+3];
                }
            }

            //-----------------------------------------------------------------------------------------math
            const int index_chr = static_cast<int>(
                ((0.2126*(static_cast<double>(R)/chunk_size) + 
                0.7152*(static_cast<double>(G)/chunk_size) +
                0.0722*(static_cast<double>(B)/chunk_size)) *
                ((channels != 4) ? 1.0:(static_cast<double>(A)/chunk_size/255))) /
                K
            );
            output.push_back(palette[(index_chr >= palette.length()) ? (palette.length()-1) : index_chr]);
        }
        output += "\n";
    }
    
    return output;
}

//-----------------------------------------------------------------------------------------generator-----------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------MAIN_FUNC

pair<pair<vector<string>, vector<string>>, py::bytes> generator(const tuple<uint8_t, uint8_t, uint8_t, uint8_t> FirstColor, const tuple<uint8_t, uint8_t, uint8_t, uint8_t> SecondColor, const int width, const int height){
    //-----------------------------------------------------------------------------------------validation
    if (width < 2)  throw py::value_error("`width`{" + to_string(width) + "} must be bigger than `2` or equal");
    if (height < 2)  throw py::value_error("`height`{" + to_string(height) + "} must be bigger than `1` or equal");

    //-----------------------------------------------------------------------------------------MAIN
    const double kR {static_cast<double>(static_cast<int16_t>(get<0>(SecondColor)) - static_cast<int16_t>(get<0>(FirstColor)))/static_cast<double>(width)},
                kG {static_cast<double>(static_cast<int16_t>(get<1>(SecondColor)) - static_cast<int16_t>(get<1>(FirstColor)))/static_cast<double>(width)},
                kB {static_cast<double>(static_cast<int16_t>(get<2>(SecondColor)) - static_cast<int16_t>(get<2>(FirstColor)))/static_cast<double>(width)},
                kA {static_cast<double>(static_cast<int16_t>(get<3>(SecondColor)) - static_cast<int16_t>(get<3>(FirstColor)))/static_cast<double>(width)};
    vector<Color> cache;
    string output_str {};
    output_str.reserve(width*4);
    cache.reserve(width);
    
    //-----------------------------------------------------------------------------------------fill
    for (int x{0}; x < width-1; ++x){
        cache.push_back(Color{static_cast<uint8_t>(get<0>(FirstColor)+static_cast<int>(kR*x)), static_cast<uint8_t>(get<1>(FirstColor)+static_cast<int>(kG*x)), static_cast<uint8_t>(get<2>(FirstColor)+static_cast<int>(kB*x)), static_cast<uint8_t>(get<3>(FirstColor)+static_cast<int>(kA*x))});
        output_str += cache[x].toBytes();
    }
    cache.push_back(Color{get<0>(SecondColor), get<1>(SecondColor), get<2>(SecondColor), get<3>(SecondColor)});
    output_str += cache[width-1].toBytes();
    
    
    return make_pair(VectorsColorOfString(cache), py::bytes(output_str));
}

//-----------------------------------------------------------------------------------------
// Макрос регистрации модуля.
PYBIND11_MODULE(_dick_cpp, m) {
    m.doc() = "C++ extension for dick library";
    
    //errors
    py::register_exception<ImageNotFoundError>(m, "ImageNotFoundError", PyExc_FileNotFoundError);

    //m.def("add", &add, "Add two integers", py::arg("a"), py::arg("b"));
    m.def("extractor", &extractor, "...", py::arg("PATH"));
    m.def("converter", &converter, "...", py::arg("PATH"), py::arg("palette"), py::arg("aim"), py::arg("width"), py::arg("height"));
    m.def("generator", &generator, "...", py::arg("FirstColor"), py::arg("SecondColor"), py::arg("width"), py::arg("height"));
}