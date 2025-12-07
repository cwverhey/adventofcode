// g++-15 -O0 day07b2.cpp -o day07b2 && ./day07b2 < day07example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day07b2.cpp -o day07b2 && time ./day07b2 < day07input.txt

// assumptions:
// * there's only one S, and it's on the first line
// * every 2nd line is empty space
// * the manifold is wide enough for all beams (ie no splitters on the left- and rightmost columns of the input .txt)

#include <iostream>
#include <vector>
#include <numeric>

using ulli = unsigned long long int;

template <typename T>
T sum(std::vector<T>& v) {
    return std::accumulate(v.begin(), v.end(), T{0});
}

int main() {

    int manifoldWidth;
    std::vector<ulli> beamCount; // per position
    std::string line;

    // first line: get width, find start point
    std::getline(std::cin, line);
    manifoldWidth = line.size();
    beamCount.assign(manifoldWidth, 0);
    beamCount[line.find('S')] = 1;
    std::getline(std::cin, line); // skip empty space

    // other lines: find splitters
    ulli carryForward = 0, newCarryForward = 0;
    while (std::getline(std::cin, line)) {
        for (int i = 0; i < manifoldWidth; ++i) {
            if (line[i] == '^') {
                beamCount[i-1] += beamCount[i];
                newCarryForward = beamCount[i];
                beamCount[i] = 0;
            } else {
                newCarryForward = 0;
            }
            beamCount[i] += carryForward;
            carryForward = newCarryForward;
        }
        std::getline(std::cin, line); // skip empty space
    }

    std::cout << sum(beamCount) << '\n';

    return 0;
}