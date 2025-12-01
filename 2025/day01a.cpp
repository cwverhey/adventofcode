#include <iostream>
#include <string>

int main () {
    int dial = 50;
    int zeroes = 0;

    std::string command;
    while (std::getline(std::cin, command)) {
        int movement = std::stoi(command.substr(1));
        if (command[0] == 'L')
            dial -= movement;
        else
            dial += movement;
        if (dial % 100 == 0)
            zeroes++;
    }

    std::cout << zeroes << "\n";

    return 0;
}
