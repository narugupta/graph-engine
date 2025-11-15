#pragma once
#include <bits/stdc++.h>
using namespace std;

class Graph {
private:
    vector<vector<pair<int, double>>> adj;        // Adjacency list
    vector<pair<double, double>> coordinates;   
    int num_nodes = 0;
    int num_edges = 0;

public:
    Graph() = default;
    Graph(int n) : adj(n), num_nodes(n) {}

    // ==========================================================
    // Add edge
    // ==========================================================
    void addEdge(int u, int v, double w) {
        if (u >= num_nodes || v >= num_nodes) {
            cerr << "Error: Node index out of bounds (" << u << ", " << v << ")\n";
            return;
        }
        adj[u].push_back({v, w});
        num_edges++;
    }

    // ==========================================================
    // Coordinate utilities (for A*)
    // ==========================================================
    void set_coords(int node, double x, double y) {
        if ((size_t)node >= coordinates.size())
            coordinates.resize(node + 1, {0.0, 0.0});
        coordinates[node] = {x, y};
    }

    pair<double, double> coords(int node) const {
        if (node < 0 || node >= (int)coordinates.size())
            return {0.0, 0.0};
        return coordinates[node];
    }

    // ==========================================================
    // Load graph from CSV
    // Supports both real-world (non-contiguous) and synthetic graphs
    // ==========================================================
    void loadFromCSV(const string &fileName,[[maybe_unused]] bool withCoords = false) {
        ifstream file(fileName);
        if (!file.is_open())
            throw runtime_error("Could not open file: " + fileName);

        string header;
        getline(file, header); // Skip header
        string line;

        unordered_map<long long, int> idmap; // Real → internal index
        vector<tuple<int, int, double>> edges;
        long long uid, vid;
        double w;
        int nextIndex = 0;

        while (getline(file, line)) {
            if (line.empty()) continue;

            stringstream ss(line);
            string a, b, c;
            if (!getline(ss, a, ',')) continue;
            if (!getline(ss, b, ',')) continue;
            if (!getline(ss, c, ',')) continue;

            try {
                uid = stoll(a);
                vid = stoll(b);
                w = stod(c);
            } catch (...) {
                cerr << "Skipping malformed line: " << line << endl;
                continue;
            }

            if (!idmap.count(uid)) idmap[uid] = nextIndex++;
            if (!idmap.count(vid)) idmap[vid] = nextIndex++;

            int u = idmap[uid];
            int v = idmap[vid];
            edges.emplace_back(u, v, w);
        }
        file.close();

        // Allocate adjacency and coordinates
        num_nodes = nextIndex;
        adj.assign(num_nodes, {});
        coordinates.assign(num_nodes, {0.0, 0.0});

        // Assign random coordinates if none present
        mt19937 rng(42);
        uniform_real_distribution<double> coord(0.0, 1000.0);
        for (int i = 0; i < num_nodes; ++i)
            set_coords(i, coord(rng), coord(rng));

        // Build adjacency list
        for (auto [u, v, w] : edges)
            addEdge(u, v, w);

        num_edges = (int)edges.size();
        cout << "CSV loaded: " << num_nodes
             << " unique nodes, " << num_edges << " edges.\n";
    }

    // ==========================================================
    // Stats and accessors
    // ==========================================================
    void printStats() const {
        cout << "Number of nodes: " << num_nodes << endl;
        cout << "Number of edges: " << num_edges << endl;
    }

    const vector<pair<int, double>> &neighbors(int u) const {
        return adj[u];
    }

    int nodes() const {
        return num_nodes;
    }
};

// ==========================================================
// Algorithm declarations
// ==========================================================
vector<double> dijkstra(const Graph &g, int start);
vector<double> a_star(const Graph &g, int start, int goal,
                      function<double(int, int)> heuristic);
vector<double> dijkstra_parallel(const Graph &g, int start, int num_threads = 4);

