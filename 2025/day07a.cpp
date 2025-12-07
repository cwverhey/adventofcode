// g++-15 -O0 day07a.cpp -o day07a && ./day07a < day07example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day07a.cpp -o day07a && ./day07a < day07input.txt

// assumption: there's only one S, and it's on the first line

#include <iostream>
#include <vector>

int main() {

    int beamSplitCount = 0;
    std::vector<int> beams;
    std::string line;

    std::getline(std::cin, line);
    beams.emplace_back(line.find('S'));
    for (int b : beams)
        std::cout << b << ' ';
    std::cout << '\n';

    while (std::getline(std::cin, line)) {
        std::vector<int> newbeams;
        for (int b : beams) {
            if (line[b] == ' ')
                continue;
            if (line[b] == '.')
                newbeams.emplace_back(b);
            else if (line[b] == '^') {
                beamSplitCount++;
                newbeams.emplace_back(b-1);
                newbeams.emplace_back(b+1);
            }
            line[b] = ' ';
        }
        beams = newbeams;

        std::cout << line << '\n';

    }

    for(int x : beams)
        std::cout << x << ' ';
    std::cout << '\n';

    std::cout << beamSplitCount << '\n';

    return 0;
}