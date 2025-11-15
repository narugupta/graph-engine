#include "graph.hpp"
#include <chrono>
#include <iostream>
#include <vector>
#include <functional>
#include <cmath>
#include <nlohmann/json.hpp>
using json = nlohmann::json;
using namespace std;
using namespace std::chrono;

double benchmark_run(const string& name, function<void()> func, int runs=5){
    vector<double> times;
    times.reserve(runs);
    
    for(int i=0;i<runs;i++){
        auto t1=high_resolution_clock::now();
        func();
        auto t2=high_resolution_clock::now();
        double duration=duration_cast<milliseconds>(t2-t1).count()/1000.0; //microseconds
        times.push_back(duration);
    }

        double avg=0.0;
        for(const auto & t: times) avg+=t;
        avg/=runs;

        double var=0.0;
        for(const auto & t: times) var+=(t-avg)*(t-avg);
        var/=runs;
        double stddev=sqrt(var);

        cout<<name<<" Avg: "<<avg<<" ms ±  "<<stddev<<" ms\n";
        return avg;
}

void export_json(const std::string &filename, const std::vector<std::tuple<int,double,double>> &data) {
    json j;
    for (auto &[nodes, d_time, a_time] : data) {
        j["results"].push_back({
            {"nodes", nodes},
            {"dijkstra_ms", d_time},
            {"astar_ms", a_time},
            {"speedup", d_time / a_time}
        });
    }
    std::ofstream out(filename);
    out << j.dump(4);
    out.close();
    std::cout << "JSON saved to " << filename << std::endl;
}