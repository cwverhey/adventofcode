// g++-15 -O0 day04b.cpp -o day04b && ./day04b < day04example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day04b.cpp -o day04b && ./day04b < day04input.txt

#include <vector>
#include <iostream>
#include <functional>

struct PointNeighbours {
    int walls{0}, full{0}, empty{0};

    PointNeighbours operator+(const PointNeighbours& other) const {
        return {
            walls + other.walls, full + other.full, empty + other.empty
        };
    }

};

std::ostream& operator<<(std::ostream& os, const PointNeighbours& p) {
    return os << "walls: " << p.walls << ", full: " << p.full << ", empty: " << p.empty;
}

class Map {

    public:

    std::vector<std::vector<char>> map;
    int width, height;

    Map(std::istream& input) {
        std::string line;
        while (std::getline(input, line)) {
            std::vector<char> chars(line.begin(), line.end());
            map.push_back(chars);
        }
        width = map[0].size();
        height = map.size();
    }

    PointNeighbours neighbours(int x, int y) {
        PointNeighbours result = PointNeighbours();
        for (int nx = x-1; nx <= x+1; ++nx) {
            for (int ny = y-1; ny <= y+1; ++ny) {
                if (nx == x && ny == y)
                    continue;
                if (nx < 0 || nx == width || ny < 0 || ny == height)
                    result.walls++;
                else if (map[ny][nx] == '@')
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
        for (std::vector<char> row : m.map) {
            for (char c : row)
                os << c;
            os << '\n';
        }
        os << m.width << 'x' << m.height;
    return os;
}


int main() {
    Map map = Map(std::cin);
    std::cout << map << '\n';

    int qualifyingRolls = 0;
    for(int i = 0; i < 1000; ++i)
    map.forAllPoints([&map, &qualifyingRolls](int& x, int& y) {
        if (map.map[y][x] == '@' && map.neighbours(x,y).full < 4) {
            qualifyingRolls++;
            map.map[y][x] = '.';
        }
    });
    std::cout << qualifyingRolls << '\n';

    return 0;
}