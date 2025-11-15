#include "graph.hpp"
#include <queue>
#include <limits>
#include <vector>
#include <functional>
#include <utility>
#include <cmath>
#include <iostream>
using namespace std;

// ======================================================
// A* Algorithm with Path Reconstruction
// Returns both distance vector and predecessor map
// ======================================================
pair<vector<double>, vector<int>> a_star_with_path(
    const Graph& g, int start, int goal,
    function<double(int,int)> heuristic)
{
    const int n = g.nodes();
    if (n == 0 || start < 0 || goal < 0 || start >= n || goal >= n) {
        cerr << "Invalid start/goal indices or empty graph.\n";
        return {{}, {}};
    }

    vector<double> gscore(n, numeric_limits<double>::infinity());
    vector<double> fscore(n, numeric_limits<double>::infinity());
    vector<int> came_from(n, -1);
    vector<bool> visited(n, false);

    gscore[start] = 0.0;
    double h0 = 0.0;
    try {
        h0 = heuristic(start, goal);
        if (!isfinite(h0)) h0 = 0.0;
    } catch (...) {
        h0 = 0.0;
    }
    fscore[start] = h0;

    using P = pair<double, int>; // (fscore, node)
    priority_queue<P, vector<P>, greater<P>> pq;
    pq.emplace(fscore[start], start);

    while (!pq.empty()) {
        auto [f, u] = pq.top();
        pq.pop();

        if (u < 0 || u >= n) continue; // Defensive check

        if (visited[u]) continue;
        visited[u] = true;

        if (u == goal)
            return {gscore, came_from};

        for (const auto& [v, weight] : g.neighbors(u)) {
            if (v < 0 || v >= n) continue; // Skip invalid neighbors

            double tentative_gscore = gscore[u] + weight;
            if (tentative_gscore < gscore[v]) {
                gscore[v] = tentative_gscore;

                double h = 0.0;
                try {
                    h = heuristic(v, goal);
                    if (!isfinite(h)) h = 0.0;
                } catch (...) {
                    h = 0.0;
                }

                fscore[v] = tentative_gscore + h;
                came_from[v] = u;
                pq.emplace(fscore[v], v);
            }
        }
    }

    cerr << "Goal not reached by A*.\n";
    return {gscore, came_from};
}

// ======================================================
// Simple A* wrapper (for benchmarking only)
// ======================================================
vector<double> a_star(const Graph& g, int start, int goal,
                      function<double(int,int)> heuristic)
{
    auto [dist, _] = a_star_with_path(g, start, goal, heuristic);
    return dist;
}
