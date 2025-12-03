// g++-15 -O0 day03b2.cpp -o day03b2 && ./day03b2 < day03example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day03b2.cpp -o day03b2 && ./day03b2 < day03input.txt

#include <iostream>

using ulli = unsigned long long int;

const int batteriesEnabled = 12;

int main() {

    ulli joltage{0};

    while (true) {
        std::string bank;
        std::cin >> bank;
        if(bank == "") break;
        
        ulli bank_value = 0;
        unsigned int left = 0;
        unsigned int right = bank.size()-batteriesEnabled;
        while(right < bank.size()) {
            int pos{0}, val{0};
            for(unsigned int i = left; i <= right; ++i) if(bank[i] > val) {
                pos = i;
                val = bank[i];
            }
            bank_value = bank_value * 10 + (val-'0');
            left = pos + 1;
            right++;
        }

        joltage += bank_value;
    }

    std::cout << joltage << '\n';
    return 0;
}
