#include "graph.hpp"
#include "minheap.hpp"
#include <vector>
#include <limits>
#include <utility>
using namespace std;

// ======================================================
// Dijkstra with path reconstruction
// ======================================================
pair<vector<double>, vector<int>> dijkstra_with_path(const Graph &g, int start)
{
    const int n = g.nodes();
    vector<double> dist(n, numeric_limits<double>::infinity());
    vector<int> prev(n, -1);
    vector<bool> visited(n, false);

    dist[start] = 0.0;
    MinHeap pq;
    pq.push(0.0, start);   

    while (!pq.empty()) {
        auto [d, u] = pq.pop();
        if (visited[u]) continue;
        visited[u] = true;

        for (const auto &[v, w] : g.neighbors(u)) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                prev[v] = u;
                pq.push(dist[v], v);
            }
        }
    }
    return { dist, prev };
}

// ======================================================
// Reconstructs path from predecessor vector
// ======================================================
vector<int> reconstruct_path(int start, int goal, const vector<int> &prev)
{
    vector<int> path;
    for (int at = goal; at != -1; at = prev[at])
        path.push_back(at);
    reverse(path.begin(), path.end());
    if (!path.empty() && path[0] == start)
        return path;
    return {};  // Empty if no path found
}
