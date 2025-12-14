// g++-15 -std=c++20 -O0 day09b.cpp -o day09b && ./day09b < day09example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day09b.cpp -o day09b && time ./day09b < day09input.txt

#include <iostream>
#include <vector>
#include <algorithm> // sort
#include <unordered_map>

using ulli = unsigned long long int;
using ui = unsigned int;

struct Point { int x, y, xRank{0}, yRank{0}; };

std::istream& operator>>(std::istream& is, Point& p) {
    char _;
    return is >> p.x >> _ >> p.y;
}

std::ostream& operator<<(std::ostream& os, const Point& p) {
    return os << p.x << ',' << p.y << " (" << p.xRank << ',' << p.yRank << ')';
}

void drawLine(std::vector<std::vector<int>>& map, const Point& p, const Point& q) {
    for (int x = std::min(p.xRank, q.xRank); x <= std::max(p.xRank, q.xRank); ++x)
        for (int y = std::min(p.yRank, q.yRank); y <= std::max(p.yRank, q.yRank); ++y)
            map[y][x] = 1;
}

void drawMap(std::vector<std::vector<int>>& map) {
    for (std::vector<int> row : map) {
        for (int b : row) {
            if (b == 0)
                std::cout << "⬜";
            else if (b == 1)
                std::cout << "⬛";
            else
                std::cout << "🟫"; 
        }
        std::cout << '\n';
    }
    std::cout << '\n';
}

void floodFill(std::vector<std::vector<int>>& map, int x, int y) {
    if (x < 0 || x >= map[0].size() || y < 0 || y >= map.size() || map[y][x] != 2)
        return;
    map[y][x] = 0;
    floodFill(map, x-1, y);
    floodFill(map, x+1, y);
    floodFill(map, x, y-1);
    floodFill(map, x, y+1);
}

ulli ManhattanArea(const Point& p, const Point& q) {
    return (1+std::abs(long(p.x) - long(q.x))) * (1+std::abs(long(p.y) - long(q.y)));
}

bool isInside(const Point& p, const Point& corner1, const Point& corner2) {
    return p.x > std::min(corner1.x, corner2.x) && p.x < std::max(corner1.x, corner2.x) && p.y > std::min(corner1.y, corner2.y) && p.y < std::max(corner1.y, corner2.y);
}

int main() {

    std::vector<Point> redTiles;
    std::vector<std::vector<int>> tileMap;
    ulli largestRectangle = 0;

    Point largestP;
    Point largestQ;

    std::vector<int> xValues;
    std::vector<int> yValues;
    
    {
        Point p;
        while (std::cin >> p) {
            redTiles.emplace_back(p);
            xValues.emplace_back(p.x);
            yValues.emplace_back(p.y);
        }
    }

    // rank X values
    std::sort(xValues.begin(), xValues.end());
    xValues.erase(std::unique(xValues.begin(), xValues.end()), xValues.end());
    std::unordered_map<int, int> xLookup;
    for (int i = 0; i < xValues.size(); ++i)
        xLookup[xValues[i]] = i;
    for (Point& p : redTiles)
        p.xRank = xLookup[p.x];
    int xRankSize = xLookup.size();

    // rank Y values
    std::sort(yValues.begin(), yValues.end());
    yValues.erase(std::unique(yValues.begin(), yValues.end()), yValues.end());
    std::unordered_map<int, int> yLookup;
    for (int i = 0; i < yValues.size(); ++i)
        yLookup[yValues[i]] = i;
    for (Point& p : redTiles)
        p.yRank = yLookup[p.y];
    int yRankSize = yLookup.size();
    
    std::cout << "x,y (xRank, yRank)\n";
    for (Point& p : redTiles)
        std::cout << p << '\n';
    
    std::cout << "xRankSize: " << xRankSize << ", yRankSize: " << yRankSize << '\n';

    // initialize map
    tileMap = std::vector<std::vector<int>>(yRankSize, std::vector<int>(xRankSize, 2));

    // draw red tiles and lines in between them
    for (int i = 0; i < redTiles.size()-1; ++i)
        drawLine(tileMap, redTiles[i], redTiles[i+1]);
    drawLine(tileMap, redTiles[redTiles.size()-1], redTiles[0]);

    // flood fill from around the edge
    for (int x = 0; x < xRankSize; ++x) {
        floodFill(tileMap, x, 0);
        floodFill(tileMap, x, yRankSize-1);
    }
    for (int y = 0; y < yRankSize; ++y) {
        floodFill(tileMap, 0, y);
        floodFill(tileMap, xRankSize-1, y);
    }

    // iterate over all possible rectangles
    for (int ip = 0; ip < redTiles.size(); ++ip) {
        Point& p = redTiles[ip];

        for (int iq = 0; iq < ip; ++iq) {
            Point& q = redTiles[iq];

            ulli area = ManhattanArea(p, q);
            if (area <= largestRectangle)
                continue;

            bool isValid = true;
            for (int ix = std::min(p.xRank, q.xRank); ix <= std::max(p.xRank, q.xRank); ++ix) {
                for (int iy = std::min(p.yRank, q.yRank); iy <= std::max(p.yRank, q.yRank); ++iy) {
                    if (tileMap[iy][ix] == 0) {
                        isValid = false;
                        break;
                    }
                }
                if (!isValid)
                    break;
            }

            if (isValid) {
                largestRectangle = area;
                largestP = p;
                largestQ = q;
            }
        }
    }

    drawLine(tileMap, largestP, largestQ);
    drawMap(tileMap);

    //std::cout << "<svg xmlns=\"http://www.w3.org/2000/svg\" stroke-width=\"0\" viewBox=\"" << xValues[0] << ' ' << yValues[0] << ' ' << xValues[xValues.size()-1] << ' ' << yValues[yValues.size()-1] << "\">\n";
    //std::cout << "<polyline fill=\"darkgreen\" points=\"";
    //for (Point& p : redTiles)
    //    std::cout << p.x << ',' << p.y << '\n';
    //std::cout << redTiles[0].x << ',' << redTiles[0].y;
    //std::cout << "\"></polyline>\n";
    //std::cout << "<rect x=\""<< std::min(largestP.x, largestQ.x) << "\" y=\"" << std::min(largestP.y, largestQ.y) << "\" width=\"" << std::abs(largestP.x - largestQ.x) << "\" height=\"" << std::abs(largestP.y - largestQ.y) << "\" fill=\"steelblue\" />\n";
    //std::cout << "</svg>";
    
    std::cout << largestRectangle << '\n';

    return 0;
}