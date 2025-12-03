// g++-15 -O0 day03b.cpp -o day03b && ./day03b < day03example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day03b.cpp -o day03b && ./day03b < day03input.txt

#include <iostream>

using ulli = unsigned long long int;

const int batteriesEnabled = 12;

std::pair<int, int> firstHighest(const std::string& bank, const unsigned int start, const unsigned int end) {
    int pos{0}, val{0};
    for(unsigned int i = start; i <= end; ++i) if(bank[i] > val) {
        pos = i;
        val = bank[i];
    }
    val -= '0';
    return {pos, val};
}

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
            auto nextEnabled = firstHighest(bank, left, right);
            bank_value = bank_value * 10 + nextEnabled.second;
            left = nextEnabled.first + 1;
            right++;
        }

        joltage += bank_value;
    }

    std::cout << joltage << '\n';
    return 0;
}
