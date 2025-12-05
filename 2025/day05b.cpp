// g++-15 -O0 day05b.cpp -o day05b && ./day05b < day05example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day05b.cpp -o day05b && ./day05b < day05input.txt

#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm> // sort

using ulli = unsigned long long int;

void addRange(std::vector<std::pair<ulli,ulli>>& ranges, ulli& start, ulli& end) {

    ranges.push_back({start, end});

    std::sort(ranges.begin(), ranges.end(), [](const auto& a, const auto& b) {
        return a.first < b.first;
    });

    for (int i = ranges.size()-1; i > 0; --i) if (ranges[i].first <= ranges[i-1].second) {
        ranges[i-1].second = std::max(ranges[i].second, ranges[i-1].second);
        ranges.erase(ranges.begin() + i);
    }

}

void printRanges(std::vector<std::pair<ulli,ulli>>& ranges) {
    for (auto [x, y] : ranges)
        std::cout << x << '-' << y << "\n";
    std::cout << '\n';
}

int main() {
    std::vector<std::pair<ulli,ulli>> ranges;
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line == "") break;
        ulli a, b; char _; std::istringstream iss(line);
        iss >> a >> _ >> b;
        addRange(ranges, a, b);
    }
    //printRanges(ranges);
    
    ulli fresh = 0;
    for (auto [x, y] : ranges)
        fresh = fresh + y - x + 1;
    std::cout << fresh << '\n';
}