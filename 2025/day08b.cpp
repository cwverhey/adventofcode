// g++-15 -std=c++20 -O0 day08b.cpp -o day08b && ./day08b < day08example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day08b.cpp -o day08b && time ./day08b < day08input.txt

#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>
#include <algorithm>
#include <ranges>
#include <unordered_set>
#include <functional>

using ulli = unsigned long long int;

struct Point { int x, y, z, cluster; };

std::istream& operator>>(std::istream& is, Point& p) {
    char _;
    return is >> p.x >> _ >> p.y >> _ >> p.z;
}

std::ostream& operator<<(std::ostream& os, const Point& p) {
    return os << p.x << ' ' << p.y << ' ' << p.z << " (cluster " << p.cluster << ')';
}

ulli semidistance(const Point& p, const Point& q) {
    return static_cast<ulli>(p.x-q.x)*(p.x-q.x) + static_cast<ulli>(p.y-q.y)*(p.y-q.y) + static_cast<ulli>(p.z-q.z)*(p.z-q.z);
}

struct Connection {
    int pIdx, qIdx; ulli distance;

    bool operator<(const Connection& other) const {
        return distance < other.distance;
    }
};

std::ostream& operator<<(std::ostream& is, const Connection& c) {
    return is << c.pIdx << " <-> " << c.qIdx << " = " << c.distance;
}

int main() {

    std::vector<Point> points;
    std::vector<Connection> connections;

    std::cout << "Points:\n";
    int i = 0;
    Point p;
    while (std::cin >> p) {

        // store point
        p.cluster = i;
        points.emplace_back(p);
        std::cout << i << ": " << p << '\n';

        // store length of connections to all previous points
        for (int j = 0; j < i; ++j) {
            Connection newConnection{i, j, semidistance(p, points[j])};
            connections.emplace_back(newConnection);
        }

        ++i;
    }

    std::cout << "\nSorting... ";
    std::sort(connections.begin(), connections.end());

    std::cout << "Clustering...\n\n";
    Connection& lastConnection = connections[0];
    for (Connection& c : connections) {

        // merge clusters of both points
        int pCluster = points[c.pIdx].cluster;
        int qCluster = points[c.qIdx].cluster;
        if(pCluster == qCluster)
            continue;
        for (Point& q : points)
            if (q.cluster == qCluster)
                q.cluster = pCluster;

        // check if we have only one cluster
        bool singleCluster = true;
        for (Point& p : points) {
            if (p.cluster != points[0].cluster) {
                singleCluster = false;
                break;
            }
        }
        if (singleCluster) {
            lastConnection = c;
            break;
        }
    }

    std::cout << "Last connection: ";
    std::cout << points[lastConnection.pIdx] << " to " << points[lastConnection.qIdx] << "\n\n";

    std::cout << points[lastConnection.pIdx].x << " * " << points[lastConnection.qIdx].x << " = " << points[lastConnection.pIdx].x * points[lastConnection.qIdx].x << '\n';
    return 0;
}