#include "graph.hpp"
#include <vector>
#include <queue>
#include <limits>
#include <omp.h>
using namespace std;

// ======================================================
// Parallel Dijkstra using OpenMP
// ======================================================
vector<double> dijkstra_parallel(const Graph &g, int start, int num_threads) {
    const int n = g.nodes();
    vector<double> dist(n, numeric_limits<double>::infinity());
    vector<bool> visited(n, false);
    dist[start] = 0.0;

    omp_set_num_threads(num_threads);

    for (int iter = 0; iter < n; ++iter) {
        double minDist = numeric_limits<double>::infinity();
        int u = -1;

        // Find unvisited node with smallest distance (parallel reduction)
        #pragma omp parallel for reduction(min:minDist)
        for (int i = 0; i < n; ++i) {
            if (!visited[i] && dist[i] < minDist) {
                minDist = dist[i];
                u = i;
            }
        }

        if (u == -1) break; // No reachable nodes
        visited[u] = true;

        // Relax edges in parallel
        #pragma omp parallel for schedule(dynamic)
        for (size_t j = 0; j < g.neighbors(u).size(); ++j) {
            auto [v, weight] = g.neighbors(u)[j];
            if (dist[u] + weight < dist[v]) {
                #pragma omp critical
                {
                    if (dist[u] + weight < dist[v])
                        dist[v] = dist[u] + weight;
                }
            }
        }
    }
    return dist;
}
