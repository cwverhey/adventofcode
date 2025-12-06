// g++-15 -O0 day05b.cpp -o day05b && ./day05b < day05example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day05b.cpp -o day05b && ./day05b < day05input.txt

#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm> // sort

using ulli = unsigned long long int;

void addRange(std::vector<std::pair<ulli,ulli>>& ranges, std::pair<ulli,ulli>& newRange) {

    // add in sorted position
    auto it = std::lower_bound(ranges.begin(), ranges.end(), newRange, [](const auto& a, const auto& b){
        return a.first < b.first;
    });
    ranges.insert(it, newRange);

    // merge overlaps
    for (int i = ranges.size()-1; i > 0; --i) {
        if (ranges[i].first <= ranges[i-1].second) {
            ranges[i-1].second = std::max(ranges[i].second, ranges[i-1].second);
            ranges.erase(ranges.begin() + i);
        }
        if (ranges[i].second < newRange.first)
            break;
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
        std::pair<ulli,ulli> newRange; char _; std::istringstream iss(line);
        iss >> newRange.first >> _ >> newRange.second;
        addRange(ranges, newRange);
    }
    //printRanges(ranges);
    
    ulli fresh = 0;
    for (auto [x, y] : ranges)
        fresh = fresh + y - x + 1;
    std::cout << fresh << '\n';
}