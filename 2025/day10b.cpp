// g++-15 -std=c++20 -O0 day10b.cpp -o day10b && ./day10b < day10example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day10b.cpp -o day10b && time ./day10b < day10input.txt

#include <iostream>
#include <iomanip>
#include <vector>
#include <sstream>
#include <regex>
#include <algorithm>
#include <limits>
// last call
struct Machine { std::vector<int> goal; std::vector<std::vector<int>> buttons; std::vector<bool> buttonIsLastSamurai; int width; int bestScore; };

int maxPresses(const std::vector<int>& button, const std::vector<int>& goal) {
    int result = std::numeric_limits<int>::max();
    for(int i : button)
        result = std::min(result, goal[i]);
    return result;
}

std::ostream& operator<<(std::ostream& os, const Machine& m) {

    os << "\033[1;32m";
    for (int j : m.goal)
        os << std::setw(4) << j << " | ";
    os << "goal\033[0m\n";

    for (int bi = 0; bi < m.buttons.size(); ++bi ) {
        std::vector<int> b = m.buttons[bi];
        for (int i = 0; i < m.width; ++i)
            if (std::find(b.begin(), b.end(), i) != b.end())
                os << "   1 | ";
            else
                os << "     | ";
        os << "max presses: " << maxPresses(b, m.goal);
        if (m.buttonIsLastSamurai[bi])
            os << " 🥷";
        os << '\n';
    }

    return os;
}

bool isZero(std::vector<int>& vec) {
    for (int i : vec)
        if (i)
            return false;
    return true;
}

void iterateButton(Machine& m, int& buttonId, int& totalPressed); // forward declaration

void pressButton(Machine& m, int& buttonId, int& totalPressed, const int presses, const bool isMax) {

    if(m.bestScore <= totalPressed + presses)
        return;
    
    // press
    totalPressed += presses;
    for (int i : m.buttons[buttonId])
        m.goal[i] -= presses;

    if (isMax && isZero(m.goal)) {
        std::cout << "solution in " << totalPressed << " presses\n\n";
        m.bestScore = totalPressed;
    } else if(buttonId + 1 < m.buttons.size()) {
        ++buttonId;
        iterateButton(m, buttonId, totalPressed);
        --buttonId;
    }

    // unpress
    totalPressed -= presses;
    for (int i : m.buttons[buttonId])
        m.goal[i] += presses;

}

void iterateButton(Machine& m, int& buttonId, int& totalPressed) {

    int max = maxPresses(m.buttons[buttonId], m.goal);

    pressButton(m, buttonId, totalPressed, max, true);

    if(m.buttons[buttonId].size() > 1 && !m.buttonIsLastSamurai[buttonId])
        for (int presses = max - 1; presses >= 0; --presses)
            pressButton(m, buttonId, totalPressed, presses, false);

}

void startIteration(Machine& m) {
    int buttonId = 0;
    int totalPressed = 0;
    iterateButton(m, buttonId, totalPressed);
}

int main() {

    int totalBestScore = 0;

    std::regex re_square(R"(\[([^\]]+)\])");
    std::regex re_parentheses(R"(\((.*?)\))");
    std::regex re_numbers(R"((\d+))");
    std::regex re_curly(R"(\{([^}]+)\})");
    std::smatch matches;
    std::string line;
    while (getline(std::cin, line)) {

        Machine machine;
        std::cout << "New machine:\n";

        // parse buttons
        for (std::sregex_iterator it(line.begin(), line.end(), re_parentheses), end; it != end; ++it) {
            std::string subline = (*it)[1].str();
            std::vector<int> button;
            for (std::sregex_iterator it2(subline.begin(), subline.end(), re_numbers), end; it2 != end; ++it2)
                button.emplace_back(stoi((*it2)[1].str()));
            machine.buttons.emplace_back(button);
        }

        // sort buttons by descending length
        std::sort(machine.buttons.begin(), machine.buttons.end(),
          [](const std::vector<int>& a, const std::vector<int>& b) {
              return a.size() > b.size();
          });

        // parse joltages
        std::regex_search(line, matches, re_curly);
        std::string substr = matches[1];
        for (std::sregex_iterator it(substr.begin(), substr.end(), re_numbers), end; it != end; ++it)
            machine.goal.emplace_back(stoi((*it)[1].str()));

        // set width
        machine.width = machine.goal.size();

        // lastSamurai = the last button to add to (at least) one of the joltages
        machine.buttonIsLastSamurai.resize(machine.buttons.size(), false);

        for (int gi = 0; gi < machine.width; ++gi)
            for (int bi = machine.buttons.size() - 1; bi >= 0; --bi)
                if (std::find(machine.buttons[bi].begin(), machine.buttons[bi].end(), gi) != machine.buttons[bi].end()) {
                    machine.buttonIsLastSamurai[bi] = true;
                    break;
                }

        // initialize best score
        machine.bestScore = std::numeric_limits<int>::max();

        // print
        std::cout << machine << "\n";
        std::cout << "solving...\n";
        
        // iterate
        startIteration(machine);

        // print
        //std::cout << machine << "\n";
        
        // save
        totalBestScore += machine.bestScore;
    }

    std::cout << "Answer: " << totalBestScore << '\n';

    return 0;
}