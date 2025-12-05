// g++-15 -O0 day04a.cpp -o day04a && ./day04a < day04example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day04a.cpp -o day04a && ./day04a < day04input.txt

#include <vector>
#include <iostream>
#include <functional>

struct PointNeighbours {
    int walls{0}, full{0}, empty{0};
};

std::ostream& operator<<(std::ostream& os, const PointNeighbours& p) {
    return os << "walls: " << p.walls << ", full: " << p.full << ", empty: " << p.empty;
}

class Map {

    public:

        std::vector<std::vector<bool>> map;
        int width, height;

        Map(std::istream& input) {
            std::string line;
            while (std::getline(input, line)) {
                std::vector<bool> line_bool;
                for (char c : line)
                    line_bool.emplace_back(c == '@');
                map.emplace_back(line_bool);
            }
            width = map[0].size();
            height = map.size();
        }

        PointNeighbours neighbours(int x, int y) {
            PointNeighbours result;
            for (int nx = x-1; nx <= x+1; ++nx) {
                for (int ny = y-1; ny <= y+1; ++ny) {
                    if (nx == x && ny == y)
                        continue;
                    if (nx < 0 || nx == width || ny < 0 || ny == height)
                        result.walls++;
                    else if (map[ny][nx])
                        result.full++;
                    else
                        result.empty++;
                }
            }
            return result;
        };

        void forAllPoints(std::function<void(int&, int&)> yield) {
            for(int x = 0; x < width; ++x)
                for(int y = 0; y < height; ++y)
                    yield(x, y);
        }

};

std::ostream& operator<<(std::ostream& os, const Map& m) {
        for (auto& row : m.map) {
            for (bool b : row)
                os << (b ? "🟩" : "⬜");
            os << '\n';
        }
        os << m.width << 'x' << m.height;
    return os;
}

int main() {
    Map map = Map(std::cin);
    std::cout << map << '\n';

    int qualifyingRolls = 0;
    map.forAllPoints([&map, &qualifyingRolls](int& x, int& y) {
        if (map.map[y][x] && map.neighbours(x,y).full < 4)
            qualifyingRolls++;
    });
    std::cout << qualifyingRolls << '\n';

    return 0;
}