// g++-15 -std=c++20 -O0 day12a.cpp -o day12a && ./day12a < day12example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day12a.cpp -o day12a && time ./day12a < day12input.txt

#include <iostream>
#include <vector>

struct Shape {std::vector<bool> px; int size;};

int shapeSum(std::vector<bool>& shape) {
    int result = 0;
    for (bool b : shape)
        if (b)
            ++result;
    return result;
}

int main() {

    std::vector<Shape> shapes;
    int fitting = 0;

    std::string line;
    Shape shape;
    while (std::getline(std::cin, line)) {

        int s = line.size();
        if (s == 0) {
            shape.size = shapeSum(shape.px);
            shapes.emplace_back(shape);
        } else if (s == 2) {
            shape.px.clear();
        } else if (s == 3) {
            for (char& c : line)
                shape.px.emplace_back(c == '#');
        } else {
            int w = stoi(line.substr(0, 2));
            int h = stoi(line.substr(3, 2));

            int a = stoi(line.substr(7, 2));
            int b = stoi(line.substr(10, 2));
            int c = stoi(line.substr(13, 2));
            int d = stoi(line.substr(16, 2));
            int e = stoi(line.substr(19, 2));
            int f = stoi(line.substr(22, 2));

            int areaAvailable = w*h;
            int minNeeded = a*shapes[0].size + b*shapes[1].size + c*shapes[2].size + d*shapes[3].size + e*shapes[4].size + f*shapes[5].size;
            int maxNeeded = (a+b+c+d+e+f)*9;

            std::cout << w << 'x' << h << ':' << a << ' ' << b << ' ' << c << ' ' << d << ' ' << e << ' ' << f << '|' << areaAvailable << ' ' << minNeeded << ' ' << maxNeeded << ' ';

            if (areaAvailable < minNeeded)
                std::cout << "no fit";
            else if (areaAvailable >= maxNeeded) {
                fitting++;
                std::cout << "fit";
            } else
                std::cout << "???";

            std::cout << '\n';

        }
    }

    for (Shape s : shapes) {
        for (bool b : s.px)
            std::cout << b;
        std::cout << " = " << s.size << '\n';
    }

    std::cout << fitting << '\n';

}