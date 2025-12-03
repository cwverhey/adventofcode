// g++-15 -O0 day03a.cpp -o day03a
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day03a.cpp -o day03a

#include <iostream>

int main() {
    int joltage{0};
    while (true) {
        std::string bank;
        std::cin >> bank;
        if(bank == "") break;

        int aVal{0}, bVal{0};
        for(int i = 0; i < bank.length()-1; ++i) {
            int charVal = bank[i];
            if(charVal > aVal) {
                aVal = charVal;
                bVal = 0;
            } else {
                bVal = std::max(bVal, charVal);
            }
        }
        bVal = std::max(bVal, static_cast<int>(bank.back()));
        joltage += (aVal-'0')*10 +(bVal-'0');
    }
    std::cout << joltage << '\n';
    return 0;
}
