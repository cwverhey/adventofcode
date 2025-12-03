// g++-15 -O0 day03b.cpp -o day03b && ./day03b < day03example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day03b.cpp -o day03b && ./day03b < day03input.txt

#include <iostream>
#include <string>
#include <algorithm>

using ulli = unsigned long long int;

const int batteriesEnabled = 12;

int main() {
    ulli joltage{0};
    while (true) {
        std::string bank;
        std::cin >> bank;
        if(bank == "") break;

        std::string enabled = bank.substr(bank.size() - batteriesEnabled); // start with last n batteries enabled
        std::string unchecked = bank.substr(0, bank.size() - batteriesEnabled); // rest of the bank
        while(!unchecked.empty()) {
            char c = unchecked.back();  // grab rightmost disabled battery
            unchecked.pop_back();
            if(c >= enabled[0]) {  // test it's at least as strong as current leftmost enabled battery
                enabled.insert(enabled.begin(), c);  // enable it
                int weakestLink = enabled.size()-1;  // need to discard one enabled battery: remove the first enabled battery that's weaker than its right neighbour, or the last one
                for(unsigned int i = 1; i < enabled.size()-1; ++i) {
                    if(enabled[i] < enabled[i+1]) {
                        weakestLink = i;
                        break;
                    }
                }
                enabled.erase(weakestLink, 1);   
            }
        }
        joltage += stoll(enabled);
    }
    std::cout << joltage << '\n';
    return 0;
}
