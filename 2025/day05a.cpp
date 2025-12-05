// g++-15 -O0 day05a.cpp -o day05a && ./day05a < day05example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day05a.cpp -o day05a && ./day05a < day05input.txt

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

bool inRange(std::vector<std::pair<ulli,ulli>>& ranges, ulli val) {
    int left = 0, right = ranges.size()-1;
    while (left <= right) {
        int mid = left + (right-left)/2;
        auto [start, end] = ranges[mid];
        if (val < start)
            right = mid - 1;
        else if (val > end)
            left = mid + 1;
        else
            return true; //std::cout << val << " in " << start << '-' << end << '\n';
    }
    return false;
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

    int fresh = 0;
    while (std::getline(std::cin, line)) {
        ulli a; std::istringstream iss(line);
        iss >> a;
        fresh += inRange(ranges, a);
    }
    std::cout << fresh << '\n';
}