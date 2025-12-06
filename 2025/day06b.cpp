// g++-15 -O0 day06b.cpp -o day06b && ./day06b < day06example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day06b.cpp -o day06b && ./day06b < day06input.txt

#include <iostream>
#include <sstream>
#include <vector>
#include <ranges>
#include <numeric>

using ulli = unsigned long long int;

ulli vectorSum(std::vector<int>& v) {
    return std::accumulate(v.begin(), v.end(), ulli{0}, std::plus{});
}

ulli vectorProduct(std::vector<int>& v) {
    return std::accumulate(v.begin(), v.end(), ulli{1}, std::multiplies{});
}

int main() {

    // read input into 2D char vector
    std::vector<std::vector<char>> input;
    std::string line;
    while(std::getline(std::cin, line)) {
        input.push_back(std::vector<char>(line.begin(), line.end()));
    }
    int max_col = input[0].size() - 1;
    int max_row = input.size() - 1;

    // scan right to left
    ulli result = 0;
    std::vector<int> problem_numbers;
    for(int col = max_col; col >= 0; --col) {

        // read number
        std::string number;
        for(int row = 0; row < max_row; ++row)
            number += input[row][col];
        problem_numbers.emplace_back(std::stoi(number));

        // operate
        char op = input[max_row][col];
        if (op == ' ')
            continue;
        if (op == '+')
            result += vectorSum(problem_numbers);
        if (op == '*')
            result += vectorProduct(problem_numbers);
        problem_numbers.clear();
        col--;
    }
    std::cout << result << '\n';

    return 0;
}