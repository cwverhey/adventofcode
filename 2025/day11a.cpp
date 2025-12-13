// g++-15 -std=c++20 -O0 day11a.cpp -o day11a && ./day11a < day11example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day11a.cpp -o day11a && time ./day11a < day11input.txt

#include <iostream>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm> // std::find

int getNameId(const std::string& name, std::vector<std::string>& deviceNames) {

    auto it = std::find(deviceNames.begin(), deviceNames.end(), name);
    if (it != deviceNames.end())
        return std::distance(deviceNames.begin(), it);
    
    deviceNames.emplace_back(name);
    return deviceNames.size()-1;

}

int path_count(std::vector<std::vector<int>>& devices, int startID, int endID) {
    int result = 0;
    for (int i: devices[startID]) {
        if (i == endID)
            ++result;
        else
            result += path_count(devices, i, endID);
    }
    return result;
}

int main() {

    std::vector<std::vector<int>> devices;
    std::vector<std::string> deviceNames;
    int startID;
    int endID;

    std::string line;
    std::string name;
    while (std::getline(std::cin, line)) {

        int source = getNameId(line.substr(0,3), deviceNames);

        std::vector<int> targets;
        for (int i = 0; i*4+5 < line.size(); ++i)
            targets.emplace_back(getNameId(line.substr(i*4+5, 3), deviceNames));

        if (devices.size() < source + 1)
            devices.resize(source+1);

        devices[source] = targets;

    }

    for (int i = 0; i < devices.size(); ++i) {
        std::cout << "device " << i << ": " << deviceNames[i] << '\n';
        for (int j = 0; j < devices[i].size(); ++j) {
            std::cout << "    " << devices[i][j] << ": " << deviceNames[ devices[i][j] ] << '\n';
        }
        if (deviceNames[i] == "you")
            startID = i;
        if (deviceNames[i] == "out")
            endID = i;
    }

    std::cout << startID << " -> " << endID << "\n\n";

    std::cout << "Answer: " << path_count(devices, startID, endID) << '\n';

    return 0;
}