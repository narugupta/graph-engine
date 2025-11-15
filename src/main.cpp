#include "graph.hpp"
#include <iostream>
#include <iomanip>
#include <chrono>
#include <fstream>
#include <random>
#include <functional>
using namespace std::chrono;
using namespace std;

// ==========================================================
// Benchmark function declaration (defined in benchmark.cpp)
// ==========================================================
double benchmark_run(const string& name, function<void()> func, int runs = 5);

// ==========================================================
// HEURISTIC EXAMPLES (for different graph types)
// ==========================================================

// HEURISTIC FOR GRAPHS BASED ON NODE INDEX DIFFERENCE
// auto heuristic = [](int a, int b) {
//     return abs(a - b) * 0.01; // weak estimate based on node index difference
//     // return 0.0; // equivalent to Dijkstra's algorithm
//     // return 5.0; // equivalent to Dijkstra's algorithm
// };

// HEURISTIC FOR GRAPHS WITH COORDINATES (EUCLIDEAN DISTANCE)
// auto heuristic = [&](int a, int b) {
//     auto [xa, ya] = g.coords(a);
//     auto [xb, yb] = g.coords(b);
//     return sqrt(pow(xa - xb, 2) + pow(ya - yb, 2));
// };

// ==========================================================
// MAIN FUNCTION — supports benchmarking across multiple graphs
// ==========================================================
int main(int argc, char* argv[]) {

    // ======================================================
    //  MODE SELECTION: Default (random) or Real-World graph
    // ======================================================
    bool useRealGraph = false;
    if (argc > 1 && string(argv[1]) == "real") {
        useRealGraph = true;
        cout << "Running in REAL-GRAPH mode (loading from CSV)\n";
    } else {
        cout << "Running in RANDOM-GRAPH mode (synthetic generation)\n";
    }

    // ======================================================
    //  REAL-GRAPH MODE
    // ======================================================
    if (useRealGraph) {
        Graph g;
        try {
            g.loadFromCSV("../data/real_graph.csv", true);  // <-- set to true if coords included
        } catch (const std::exception& e) {
            cerr << " Error loading real_graph.csv: " << e.what() << endl;
            return 1;
        }

        g.printStats();

        int start = 0, goal = g.nodes() - 1;

        // Euclidean heuristic using coordinates (if available)
        auto heuristic = [&](int a, int b) {
            auto [xa, ya] = g.coords(a);
            auto [xb, yb] = g.coords(b);
            return sqrt(pow(xa - xb, 2) + pow(ya - yb, 2));
        };

        cout << "\n=== Benchmarking REAL GRAPH ===\n";
        double d_time = benchmark_run("Dijkstra", [&]() { dijkstra(g, start); });
        double a_time = benchmark_run("A*", [&]() { a_star(g, start, goal, heuristic); });

        cout << fixed << setprecision(4);
        cout << "\n[REAL GRAPH] Speedup (A*/Dijkstra): " << (d_time / a_time) << "x\n";

        // ======================================================
        // Parallel Dijkstra Benchmark (Week 9+)
        // ======================================================
        cout << "\n=== Parallel Benchmark (4 threads) ===\n";
        double dp_time = benchmark_run("Dijkstra (Parallel)", [&]() { dijkstra_parallel(g, start, 4); });
        
        cout << fixed << setprecision(4);
        cout << "\nSpeedup (Parallel/Sequential): " << (d_time / dp_time) << "x\n";

        // ======================================================
        // Save performance results
        // ======================================================
        ofstream out("perf_results_real.csv");
        out << "nodes,dijkstra_ms,astar_ms,parallel_ms\n";
        out << g.nodes() << "," << d_time << "," << a_time << "," << dp_time << "\n";
        out.close();

        cout << "\n Real-graph results written to perf_results_real.csv\n";
        return 0;  // Exit after real graph test
    }

    // ==========================================================
    // RANDOM GRAPH MODE (Default)
    // ==========================================================
    vector<int> graph_sizes = {10000, 50000, 100000};

    ofstream out("perf_results.csv");
    out << "nodes,dijkstra_ms,astar_ms\n";

    // Loop through multiple graph sizes and benchmark
    for (int n : graph_sizes) {

        // ======================================================
        // Graph generation (instead of CSV loading)
        // ======================================================
        // This section generates a random directed weighted graph in-memory.
        // It replaces CSV loading to better observe scaling under Valgrind.
        cout << "Generating random graph of " << n << " nodes...\n";

        Graph g(n);

        std::mt19937 rng(42);  // Fixed seed for reproducibility
        std::uniform_real_distribution<double> w(1.0, 10.0);
        std::uniform_int_distribution<int> node(0, n - 1);

        std::uniform_real_distribution<double> coord(0.0, 1000.0);
        for (int i = 0; i < n; ++i) {
            g.set_coords(i, coord(rng), coord(rng));
        }

        // Add ~3x edges per node on average
        for (int i = 0; i < 3 * n; ++i) {
            int u = node(rng);
            int v = node(rng);
            if (u != v)
                g.addEdge(u, v, w(rng));
        }

        g.printStats();

        // ======================================================
        // HEURISTIC for A* (Euclidean Distance Based)
        // ======================================================
        // Uses the coordinate positions (if assigned) to compute
        // the straight-line distance estimate between nodes.
        // Includes safe fallbacks for incomplete data.
        auto heuristic = [&](int a, int b) -> double {
            // Guard out-of-range node indices
            if (a < 0 || b < 0 || a >= g.nodes() || b >= g.nodes()) return 0.0;

            // Try to fetch coords; if coords missing or invalid, fallback to index diff
            try {
                auto [xa, ya] = g.coords(a);
                auto [xb, yb] = g.coords(b);
                double dx = xa - xb;
                double dy = ya - yb;
                // If coordinates are identical or suspicious, fallback
                if (std::isnan(dx) || std::isnan(dy)) return std::abs(a - b) * 0.01;
                return std::sqrt(dx * dx + dy * dy);
            } catch (...) {
                // Any error -> fallback heuristic (weak but safe)
                return std::abs(a - b) * 0.01;
            }
        };

        int start = 0, goal = g.nodes() - 1;

        // ======================================================
        // Run both algorithms and benchmark execution time
        // ======================================================
        double d_time = benchmark_run("Dijkstra", [&]() { dijkstra(g, start); });
        double a_time = benchmark_run("A*", [&]() { a_star(g, start, goal, heuristic); });

        // Write performance data to CSV
        out << n << "," << d_time << "," << a_time << "\n";

        // Print real-time benchmark summary to console
        cout << fixed << setprecision(4);
        cout << "\n[" << n << " nodes] Speedup (A*/Dijkstra): " << (d_time / a_time) << "x\n";
    }

    out.close();
    cout << "\n Benchmarking complete! Results written to perf_results.csv\n";

    return 0;
}
