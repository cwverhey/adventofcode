// g++-15 -std=c++20 -O0 day11b.cpp -o day11b && ./day11b < day11example2.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day11b.cpp -o day11b && time ./day11b < day11input.txt

#include <iostream>
#include <vector>
#include <algorithm> // std::find
#include <unordered_map>

using ulli = unsigned long long int;

std::vector<std::vector<int>> devices;
std::vector<std::string> deviceNames;
int endID;
int dacID;
int fftID;

int getNameId(const std::string& name) {

    auto it = std::find(deviceNames.begin(), deviceNames.end(), name);
    if (it != deviceNames.end())
        return std::distance(deviceNames.begin(), it);
    
    deviceNames.emplace_back(name);
    return deviceNames.size()-1;

}

struct CacheKey {
    int deviceID; bool dacSeen, fftSeen;
    bool operator==(const CacheKey& other) const {
        return deviceID == other.deviceID && dacSeen == other.dacSeen && fftSeen == other.fftSeen;
    }
};

struct CacheKeyHash {
    std::size_t operator()(const CacheKey& k) const {
        return std::hash<int>{}(k.deviceID) ^ (k.dacSeen << 1) ^ (k.fftSeen << 2);
    }
};

ulli path_count(int startID, bool dacSeen, bool fftSeen) {

    static std::unordered_map<CacheKey, ulli, CacheKeyHash> cache;
    CacheKey key{startID, dacSeen, fftSeen};

    auto it = cache.find(key);
    if (it != cache.end())
        return it->second;

    ulli result = 0;

    if (startID == dacID)
        dacSeen = true;
    if (startID == fftID)
        fftSeen = true;

    for (int i: devices[startID]) {
        if (i == endID) {
            if (dacSeen && fftSeen)
                ++result;
        } else {
            result += path_count(i, dacSeen, fftSeen);
        }
    }

    return cache[key] = result;
}

int main() {

    int startID;

    std::string line;
    std::string name;
    while (std::getline(std::cin, line)) {

        int source = getNameId(line.substr(0,3));

        std::vector<int> targets;
        for (int i = 0; i*4+5 < line.size(); ++i)
            targets.emplace_back(getNameId(line.substr(i*4+5, 3)));

        if (devices.size() < source + 1)
            devices.resize(source+1);

        devices[source] = targets;

    }

    for (int i = 0; i < devices.size(); ++i) {
        std::cout << "device " << i << ": " << deviceNames[i] << "\n";
        for (int j = 0; j < devices[i].size(); ++j) {
            std::cout << "    " << devices[i][j] << ": " << deviceNames[ devices[i][j] ] << "\n";
        }
    }

    for (int i = 0; i < deviceNames.size(); ++i) {
        if (deviceNames[i] == "svr")
            startID = i;
        if (deviceNames[i] == "out")
            endID = i;
        if (deviceNames[i] == "dac")
            dacID = i;
        if (deviceNames[i] == "fft")
            fftID = i;
    }

    std::cout << startID << " -> " << endID << " via DAC: " << dacID << " and FFT: " << fftID << '\n';

    std::cout << "Answer: " << path_count(startID, false, false) << '\n';

    return 0;
}