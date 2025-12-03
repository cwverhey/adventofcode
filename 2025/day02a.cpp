#include <iostream>
#include <sstream>
#include <numeric> // std::accumulate

struct Range {
    long long start;
    long long end;
    int width;
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

        long long start, end;
        for(int i = numbers[0].length(); i <= numbers[1].length(); ++i) {
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

long long rep_str(const std::string& val, const int& rep) {
    std::string result;
    for(int i = 0; i < rep; ++i)
        result += val;
    return std::stoll(result);
}

long long rep_num(const long long& val, const int& rep) {
    std::string val_str = std::to_string(val);
    return rep_str(val_str, rep);
}

void insert_repetition(const Range& range, std::vector<long long>& repetitions, long long& new_repetition) {
    if(new_repetition >= range.start && new_repetition <= range.end) { // check in range
        if (!std::binary_search(repetitions.begin(), repetitions.end(), new_repetition)) { // check unique
            auto i = std::lower_bound(repetitions.begin(), repetitions.end(), new_repetition);
            repetitions.insert(i, new_repetition); // insert in sorted position
        }
    }
}

void find_repetitions(const Range& range, const int& width, std::vector<long long>& reps) {
    int times = range.width / width;
    std::string start = std::to_string(range.start).substr(0, width);
    std::string end = std::to_string(range.end).substr(0, width);
    
    if(start == end) {
        long long rep = rep_str(start, times);
        insert_repetition(range, reps, rep);
    } else {
        long long start_num = stoll(start);
        long long end_num = stoll(end);
        for(long long i = start_num; i <= end_num; ++i) {
            long long rep = rep_num(i, times);
            insert_repetition(range, reps, rep);
        }
    }
}

int main() {
    std::string line;
    std::getline(std::cin, line);

    std::vector<Range> ranges = split_into_ranges(line);

    std::vector<long long> repetitions;
    for (const Range& range : ranges)
        if(range.width % 2 == 0)
            find_repetitions(range, range.width / 2, repetitions);

    long long sum = std::accumulate(repetitions.begin(), repetitions.end(), 0LL);
    std::cout << sum << '\n';

    return 0;
}