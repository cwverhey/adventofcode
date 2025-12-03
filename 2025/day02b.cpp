// g++-15 -O0 day02b.cpp -o day02b
// g++-15 -O3 -march=native -flto -Wall -Wextra -Wshadow day02b.cpp -o day02b
#include <vector>
#include <iostream>
#include <sstream>
#include <numeric> // std::accumulate
#include <cmath> // std::pow
#include <algorithm> // std::binary_search

using ulli = unsigned long long int;

struct Range {
    ulli start;
    ulli end;
    unsigned int width;
};

std::vector<std::string> split(std::stringstream& ss, const char& sep) {
    std::vector<std::string> result;
    std::string item;
    while(std::getline(ss, item, sep))
        result.push_back(item);
    return result;
}

std::vector<std::string> split(const std::string& s, const char& sep) {
    std::stringstream ss(s);
    return split(ss, sep);
}

// "1-10,20-110" -> { {start: 1LL, end: 9LL, length: 1}, {10,10,2}, {20,99,2}, {100,110,3} }
std::vector<Range> split_into_ranges(const std::string& s) {

    std::vector<Range> result;

    for(const auto& part : split(s, ',')) {
        std::vector<std::string> numbers = split(part, '-');

        ulli start, end;
        for(unsigned int i = numbers[0].length(); i <= numbers[1].length(); ++i) {
            if(i == numbers[0].length())
                start = std::stoll(numbers[0]);
            else
                start = std::pow(10, i-1);
            if(i == numbers[1].length())
                end = std::stoll(numbers[1]);
            else
                end = std::pow(10, i) - 1;
            result.push_back({start, end, i});
        }
    }
    return result;
}

ulli rep_str(const std::string& val, const int& rep) {
    std::string result;
    for(int i = 0; i < rep; ++i)
        result += val;
    return std::stoll(result);
}

ulli rep_num(const ulli& val, const int& rep) {
    std::string val_str = std::to_string(val);
    return rep_str(val_str, rep);
}

void insert_repetition(const Range& range, std::vector<ulli>& repetitions, ulli& new_repetition) {
    if(new_repetition >= range.start && new_repetition <= range.end) { // check in range
        if (!std::binary_search(repetitions.begin(), repetitions.end(), new_repetition)) { // check unique
            auto i = std::lower_bound(repetitions.begin(), repetitions.end(), new_repetition);
            repetitions.insert(i, new_repetition); // insert in sorted position
        }
    }
}

void find_repetitions(const Range& range, const int& width, std::vector<ulli>& reps) {
    int times = range.width / width;
    std::string start = std::to_string(range.start).substr(0, width);
    std::string end = std::to_string(range.end).substr(0, width);
    
    if(start == end) {
        ulli rep = rep_str(start, times);
        insert_repetition(range, reps, rep);
    } else {
        ulli start_num = stoll(start);
        ulli end_num = stoll(end);
        for(ulli i = start_num; i <= end_num; ++i) {
            ulli rep = rep_num(i, times);
            insert_repetition(range, reps, rep);
        }
    }
}

// 12 -> {1, 2, 6, 3, 4}
std::vector<int> divisors(const int& n, bool sorted = false) {
    std::vector<int> divisors;

    if(n == 1)
        return divisors;
    
    for (int i = 1; i <= std::sqrt(n); ++i) {
        if (n % i == 0) {
            divisors.push_back(i);
            if (i != n / i && i != 1)
                divisors.push_back(n / i);
        }
    }
    if (sorted)
        std::sort(divisors.begin(), divisors.end());
    return divisors;
}

int main() {
    std::string line;
    std::getline(std::cin, line);

    std::vector<Range> ranges = split_into_ranges(line);

    std::vector<ulli> repetitions;
    for (const Range& range : ranges) {
        for (const auto width : divisors(range.width))
            find_repetitions(range, width, repetitions);
    }

    ulli sum = std::accumulate(repetitions.begin(), repetitions.end(), 0LL);
    std::cout << sum << '\n';

    return 0;
}