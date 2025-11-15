// src/accuracy_test.cpp
// Accuracy validation between Dijkstra and A*

#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
#include <functional>
#include <chrono>
#include "graph.hpp"
#include "path_reconstruct.hpp"  // declarations only

using namespace std;
using namespace chrono;

int main() {
    const int N = 2000;
    Graph g(N);
    std::mt19937 rng(123);
    uniform_real_distribution<double> w(1.0, 10.0);
    uniform_int_distribution<int> node(0, N - 1);
    uniform_real_distribution<double> coord(0.0, 1000.0);

    // Assign random coordinates for Euclidean heuristic
    for (int i = 0; i < N; ++i)
        g.set_coords(i, coord(rng), coord(rng));

    // Add ~3× edges per node
    for (int i = 0; i < 3 * N; ++i) {
        int u = node(rng), v = node(rng);
        if (u != v)
            g.addEdge(u, v, w(rng));
    }

    int start = 0, goal = N - 1;

    // === BASELINE COMPARISON ===
    cout << "Running accuracy test on " << N << " nodes...\n";

    auto [dist_d, prev_d] = dijkstra_with_path(g, start);
    auto [dist_a, prev_a] = a_star_with_path(g, start, goal, [&](int a, int b) {
        auto [xa, ya] = g.coords(a);
        auto [xb, yb] = g.coords(b);
        return sqrt(pow(xa - xb, 2) + pow(ya - yb, 2));
    });

    double cost_d = dist_d[goal];
    double cost_a = dist_a[goal];

    if (isinf(cost_d) && isinf(cost_a)) {
        cout << "Both algorithms report: no path.\n";
        return 0;
    }

    cout << "Dijkstra cost: " << cost_d << "\n";
    cout << "A* cost: " << cost_a << "\n";

    double error = fabs(cost_d - cost_a);
    if (error < 1e-6)
        cout << "Path cost match confirmed!\n";
    else
        cout << "Path cost mismatch: Δ=" << error << "\n";

    auto path_d = reconstruct_path(start, goal, prev_d);
    auto path_a = reconstruct_path(start, goal, prev_a);
    cout << "Dijkstra path length: " << path_d.size()
         << " | A* path length: " << path_a.size() << "\n\n";

    // === HEURISTIC SCALING EXPERIMENT ===
    cout << "Running heuristic scaling experiment...\n";

    vector<double> scales = {0.0, 0.5, 1.0, 2.0, 5.0};
    ofstream out("heuristic_scaling.csv");
    out << "scale,astar_cost,error_ms,runtime_ms\n";

    for (double alpha : scales) {
        auto heuristic_scaled = [&](int a, int b) {
            auto [xa, ya] = g.coords(a);
            auto [xb, yb] = g.coords(b);
            double h = sqrt(pow(xa - xb, 2) + pow(ya - yb, 2));
            return alpha * h;
        };

        auto t1 = high_resolution_clock::now();
        auto [dist_as, prev_as] = a_star_with_path(g, start, goal, heuristic_scaled);
        auto t2 = high_resolution_clock::now();

        double cost_as = dist_as[goal];
        double diff = fabs(cost_d - cost_as);
        double runtime = duration_cast<microseconds>(t2 - t1).count() / 1000.0;

        cout << "alpha=" << alpha
             << " → A* cost=" << cost_as
             << ", dell=" << diff
             << ", time=" << runtime << " ms\n";

        out << alpha << "," << cost_as << "," << diff << "," << runtime << "\n";
    }

    out.close();
    cout << "\n Results saved to heuristic_scaling.csv\n";

    return 0;
}
