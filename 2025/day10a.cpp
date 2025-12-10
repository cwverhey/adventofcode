// g++-15 -std=c++20 -O0 day10a.cpp -o day10a && ./day10a < day10example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day10a.cpp -o day10a && time ./day10a < day10input.txt

#include <iostream>
#include <vector>
#include <sstream>
#include <regex>
#include <algorithm>
#include <cstdint>

using state = uint16_t;

void printState(const state& s) {
    for (int i = 16; i >= 0; --i)
        std::cout << ((s >> i) & 1 ? "🟡" : "🟠");
}

void printModifier(const state& s) {
    for (int i = 16; i >= 0; --i)
        std::cout << ((s >> i) & 1 ? "🔀" : "⬛");
}

struct Machine { state goal{0}; std::vector<state> buttons; std::vector<int> joltages; };

std::ostream& operator<<(std::ostream& os, const Machine& m) {

    printState(m.goal);
    os << '\n';

    for (state b : m.buttons) {
        printModifier(b);
        os << '\n';
    }

    os << "joltages: ";
    for (int j : m.joltages)
        os << j << ' ';

    return os;
}

void combinations(const std::vector<state>& arr, int n, int start, std::vector<int>& current, std::vector<std::vector<int>>& result) {
    if (current.size() == n) {
        result.push_back(current);
        return;
    }
    for (int i = start; i < arr.size(); ++i) {
        current.push_back(arr[i]);
        combinations(arr, n, i + 1, current, result);
        current.pop_back();
    }
}

int main() {

    int requiredPresses = 0;

    std::regex re_square(R"(\[([^\]]+)\])");
    std::regex re_parentheses(R"(\((.*?)\))");
    std::regex re_numbers(R"((\d+))");
    std::regex re_curly(R"(\{([^}]+)\})");
    std::smatch matches;
    std::string line;
    while (getline(std::cin, line)) {

        Machine machine;
        std::cout << "new machine:\n";
        
        // parse goal
        std::regex_search(line, matches, re_square);
        std::string goal = matches[1];
        std::reverse(goal.begin(), goal.end());
        for (char c : goal) {
            machine.goal <<= 1;
            machine.goal |= c == '#';
        }

        // parse buttons
        for (std::sregex_iterator it(line.begin(), line.end(), re_parentheses), end; it != end; ++it) {
            std::string subline = (*it)[1].str();
            state s = 0;
            for (std::sregex_iterator it2(subline.begin(), subline.end(), re_numbers), end; it2 != end; ++it2)
                s |= (1 << stoi((*it2)[1].str()));
            machine.buttons.emplace_back(s);
        }

        // parse joltages
        std::regex_search(line, matches, re_curly);
        std::string substr = matches[1];
        for (std::sregex_iterator it(substr.begin(), substr.end(), re_numbers), end; it != end; ++it)
            machine.joltages.emplace_back(stoi((*it)[1].str()));

        std::cout << machine << "\n\n";

        // try n combinations of buttons
        int success = false;
        int n = 0;
        while (!success) {
            ++n;
            std::cout << "try " << n << " button(s)\n";

            std::vector<int> current;
            std::vector<std::vector<int>> result;
            combinations(machine.buttons, n, 0, current, result);
            for (auto& comb : result) {

                state s = 0;
                for (state x : comb) {
                    s ^= x;
                    //printModifier(x);
                    //std::cout << '\n';
                }
                printState(s);
                std::cout << "\n";

                if(s == machine.goal) {
                    success = true;
                    break;
                }
            }
        }

        std::cout << "done in " << n << " presses\n\n";
        requiredPresses += n;
    }

    std::cout << requiredPresses << '\n';

    return 0;
}