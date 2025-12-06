// g++-15 -O0 day06b2.cpp -o day06b2 && ./day06b2 < day06example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day06b2.cpp -o day06b2 && ./day06b2 < day06input.txt

#include <iostream>
#include <sstream>
#include <vector>
#include <ranges>
#include <numeric>
#include <string>

using ulli = unsigned long long int;

int main() {

    // read input into string vector
    std::vector<std::string> input;
    std::string line;
    while(std::getline(std::cin, line))
        input.push_back(line);
    int max_row = input.size() - 1;
    int max_col = input[0].size() - 1;

    // scan left to right
    ulli result = 0;
    ulli problem_subtotal = 0;
    char op = ' ';
    for(int col = 0; col <= max_col; ++col) {

        // init new problem, read operator
        if (input[max_row][col] != ' ') {
            result += problem_subtotal;
            op = input[max_row][col];
            problem_subtotal = op == '+' ? 0 : 1;
        }

        // read number
        int number = 0;
        bool empty = true;
        for (int row = 0; row < max_row; ++row) {
            if (input[row][col] != ' ') {
                number = number * 10 + input[row][col] - '0';
                empty = false;
            }
        }
        if (empty)
            continue;

        // calculate
        if (op == '+')
            problem_subtotal += number;
        else
            problem_subtotal *= number;
    }
    result += problem_subtotal;

    std::cout << result << '\n';

    return 0;
}