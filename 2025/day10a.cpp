// g++-15 -std=c++20 -O0 day10a.cpp -o day10a && ./day10a < day10example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day10a.cpp -o day10a && time ./day10a < day10input.txt

#include <iostream>
#include <vector>
#include <sstream>
#include <regex>
#include <algorithm>
#include <cstdint>

std::string readUntil(std::istream& in, char endChar) {
    std::string result;
    char c;
    while (in.get(c)) {
        if ( c == endChar)
            break;
        result.push_back(c);
    }
    return result;
}

std::string readUntil(std::string& in, char endChar) {
    std::istringstream iss(in);
    return readUntil(iss, endChar);
}

struct State {
    std::vector<int> state;
    
    bool operator==(const State& other) const {
        return state == other.state;
    }
};

std::ostream& operator<<(std::ostream& os, const State& s) {
    for (bool b : s.state)
        os << (b ? "🟡" : "🟠");
    return os;
}

struct Machine { State goal; std::vector<std::vector<int>> buttons; std::vector<int> joltages; };

std::ostream& operator<<(std::ostream& os, const Machine& m) {

    os << m.goal;

    for (std::vector<int> lamps : m.buttons) {
        os << " ( ";
        for (int l : lamps)
            os << l << ' ';
        os << ')';
    }
    os << ' ';

    for (int j : m.joltages)
        os << j << ' ';

    return os;
}

std::vector<State> nextStates(const Machine& machine, const State& state) {
    std::vector<State> result;

    for (std::vector<int> button : machine.buttons) {
        State newState = state;
        for (int pos : button)
            newState.state[pos] = !newState.state[pos];
        result.emplace_back(newState);
    }
    return result;
}



int main() {

    int requiredPresses = 0;

    // parse input
    {
        std::regex re_square(R"(\[([^\]]+)\])");
        std::regex re_parentheses(R"(\((.*?)\))");
        std::regex re_numbers(R"((\d+))");
        std::regex re_curly(R"(\{([^}]+)\})");
        std::smatch matches;
        std::string line;
        while (getline(std::cin, line)) {

            Machine machine;
            
            std::regex_search(line, matches, re_square);
            for (char c : static_cast<std::string>(matches[1]))
                machine.goal.state.push_back(c == '#');

            for (std::sregex_iterator it(line.begin(), line.end(), re_parentheses), end; it != end; ++it) {
                std::string subline = (*it)[1].str();
                std::vector<int> b;
                for (std::sregex_iterator it2(subline.begin(), subline.end(), re_numbers), end; it2 != end; ++it2)
                    b.push_back(stoi((*it2)[1].str()));
                machine.buttons.emplace_back(b);
            }

            std::regex_search(line, matches, re_curly);
            std::string substr = matches[1];
            for (std::sregex_iterator it(substr.begin(), substr.end(), re_numbers), end; it != end; ++it)
                machine.joltages.emplace_back(stoi((*it)[1].str()));

            std::cout << machine << '\n';

            // remember seen states
            std::vector<State> seenStates;

            // initialize first state
            State initialState;
            initialState.state.resize(machine.goal.state.size());
            std::vector<State> states = {initialState};

            // iterate until match
            int i = 0;
            bool success = false;
            while (!success) {
                ++i;
                std::cout << "press " << i << '\n';
                std::vector<State> newStates;
                for (State s : states) {
                    std::vector<State> n = nextStates(machine, s);
                    for (State s : n) {
                        //std::cout << s << '\n';
                        if (s == machine.goal) {
                            success = true;
                            break;
                        }
                        if (std::find(seenStates.begin(), seenStates.end(), s) == seenStates.end())
                            seenStates.emplace_back(s);
                    }
                    newStates.insert(newStates.end(), n.begin(), n.end());
                }
                if (success)
                    break;
                states = newStates;
            }
            requiredPresses += i;
        }
    }

    std::cout << requiredPresses << '\n';

    return 0;
}