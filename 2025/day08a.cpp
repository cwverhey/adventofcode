// g++-15 -std=c++20 -O0 day08a.cpp -o day08a && ./day08a < day08example.txt
// g++-15 -std=c++20 -O3 -march=native -flto -Wall -Wextra -Wshadow day08a.cpp -o day08a && time ./day08a < day08input.txt

#include <iostream>
#include <vector>
#include <cmath>  // sqrt
#include <algorithm>  // sort
#include <unordered_set>

using ulli = unsigned long long int;

const int CONNECTIONS = 1000;

struct Point { int x, y, z; };

std::istream& operator>>(std::istream& is, Point& p) {
    char _;
    return is >> p.x >> _ >> p.y >> _ >> p.z;
}

std::ostream& operator<<(std::ostream& os, const Point& p) {
    return os << p.x << ' ' << p.y << ' ' << p.z;
}

float distance(const Point& p, const Point& q) {
    return std::sqrt( (p.x-q.x)*(p.x-q.x) + (p.y-q.y)*(p.y-q.y) + (p.z-q.z)*(p.z-q.z) );
}

ulli semidistance(const Point& p, const Point& q) {
    return static_cast<ulli>(p.x-q.x)*(p.x-q.x) + static_cast<ulli>(p.y-q.y)*(p.y-q.y) + static_cast<ulli>(p.z-q.z)*(p.z-q.z);
}

struct Connection { int pIdx, qIdx; ulli distance; };

std::ostream& operator<<(std::ostream& is, const Connection& c) {
    return is << c.pIdx << " <-> " << c.qIdx << " = " << c.distance;
}

int findInsertionPoint(const std::vector<Connection>& connections, const Connection& newConnection) {
    auto it = std::lower_bound(connections.begin(), connections.end(), newConnection,
    [](const Connection& a, const Connection& b) {
        return a.distance < b.distance;
    });
    return std::distance(connections.begin(), it);
}

bool hasOverlap(const std::vector<int>& a, const std::vector<int>& b) {
    std::unordered_set<int> s(a.begin(), a.end());
    return std::ranges::any_of(b, [&](int x){ return s.contains(x); });
}

int main() {

    std::vector<Point> points;
    std::vector<Connection> connections;

    std::cout << "Points:\n";
    int i = 0;
    Point p;
    while (std::cin >> p) {

        // store point
        points.emplace_back(p);
        std::cout << i << ": " << p << '\n';

        // check length to all previous points, keep shortest ones
        for (int j = 0; j < i; ++j) {
            Connection newConnection{i, j, semidistance(p, points[j])};
            int newIndex = findInsertionPoint(connections, newConnection);
            if (newIndex < CONNECTIONS) {
                connections.insert(connections.begin() + newIndex, newConnection);
                if (connections.size() > CONNECTIONS)
                    connections.pop_back();
            }
        }
        ++i;
    }

    std::cout << "\nShortest connections:\n";
    for(Connection c : connections)
        std::cout << c << '\n';

    std::cout << "\nClusters:\n";
    std::vector<std::vector<int>> clusters;
    for (int pi = 0; pi < points.size(); ++pi) {

        // find all neighbouring IDs
        std::vector<int> neighbourIds;
        for (int ci = 0; ci < connections.size(); ++ci) {
            if (pi == connections[ci].pIdx)
                neighbourIds.emplace_back(connections[ci].qIdx);
            else if (pi == connections[ci].qIdx)
                neighbourIds.emplace_back(connections[ci].pIdx);
        }

        // find clusters that they're in
        std::vector<int> neighbourClusters;
        for (int ci = 0; ci < clusters.size(); ++ci)
            if (hasOverlap(clusters[ci], neighbourIds))
                neighbourClusters.emplace_back(ci);

        // join cluster(s)
        if(neighbourClusters.size() == 0) {
            clusters.push_back({pi});
        } else {
            clusters[ neighbourClusters[0] ].emplace_back(pi);
            for (int nci = neighbourClusters.size()-1; nci > 0; --nci) {
                clusters[ neighbourClusters[0] ].insert(clusters[ neighbourClusters[0] ].end(), clusters[ neighbourClusters[nci] ].begin(), clusters[ neighbourClusters[nci] ].end());
                clusters.erase(clusters.begin() + neighbourClusters[nci]);
            }
        }
    }

    for (std::vector<int> cluster : clusters) {
        for (int i : cluster)
            std::cout << i << ' ';
        std::cout << '\n';
    }

    // Cluster sizes
    std::vector<int> clusterSizes;
    for (std::vector<int> cluster : clusters)
        clusterSizes.push_back(cluster.size());
    std::sort(clusterSizes.begin(), clusterSizes.end(), std::greater<int>());

    std::cout << "\nAnswer:\n";
    std::cout << clusterSizes[0]*clusterSizes[1]*clusterSizes[2] << '\n';

    return 0;
}