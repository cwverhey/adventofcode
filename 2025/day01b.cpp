#include <iostream>
#include <string>

int main () {
    int dial = 50;
    int zeroes = 0;

    std::string command;
    while (std::getline(std::cin, command)) {

        int movement = std::stoi(command.substr(1));
        if (command[0] == 'R') {

            dial += movement;
            zeroes += dial / 100;
            dial %= 100;

        } else {

            if(dial == 0)
                zeroes--;

            dial -= movement;
            zeroes += -dial / 100;
            dial %= 100;

            if(dial <= 0)
                zeroes++;

            if (dial < 0)
                dial += 100;

        }
    }

    std::cout << zeroes << "\n";
    
    return 0;
}
