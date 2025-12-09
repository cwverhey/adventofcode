// g++-15 -std=c++20 -O0 day09a.cpp -o day09a && ./day09a < day09example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day09a.cpp -o day09a && time ./day09a < day09input.txt

#include <iostream>
#include <vector>

using ulli = unsigned long long int;
using ui = unsigned int;

struct Point { ui x, y; };

std::istream& operator>>(std::istream& is, Point& p) {
    char _;
    return is >> p.x >> _ >> p.y;
}

std::ostream& operator<<(std::ostream& os, const Point& p) {
    return os << p.x << ',' << p.y;
}

ulli ManhattanArea(const Point& p, const Point& q) {
    return (1+std::abs(long(p.x) - long(q.x))) * (1+std::abs(long(p.y) - long(q.y)));
}

int main() {

    std::vector<Point> redTiles;
    ulli largestRectangle = 0;

    Point p;
    while (std::cin >> p) {
        for (Point q : redTiles)
            largestRectangle = std::max(largestRectangle, ManhattanArea(p, q));
        redTiles.emplace_back(p);
    }

    std::cout << largestRectangle << '\n';

    return 0;
}