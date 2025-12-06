// g++-15 -O0 day06a.cpp -o day06a && ./day06a < day06example.txt
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day06a.cpp -o day06a && ./day06a < day06input.txt

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

    std::vector<char> operators;

    // read input
    std::vector<int> numbers_in;
    int x;
    while(std::cin >> x)
        numbers_in.emplace_back(x);
    std::cin.clear(); std::cin.unget(); // clear cin fail state, go back 1 char

    char c;
    while(std::cin >> c)
        operators.emplace_back(c);
    
    // arrange numbers
    int size = operators.size();
    std::vector<std::vector<int>> numbers(size);
    int i = 0;
    for(int n : numbers_in) {
        numbers[i].emplace_back(n);
        i++;
        if (i == size) i = 0;
    }

    // result
    ulli result = 0;
    for (int i = 0; i < operators.size(); ++i)
        if (operators[i] == '+')
            result += vectorSum(numbers[i]);
        else
            result += vectorProduct(numbers[i]);
    std::cout << result << '\n';

    return 0;
}