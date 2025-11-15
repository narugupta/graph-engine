#include "graph.hpp"
#include "minheap.hpp"
#include <queue>
#include <limits>
#include <vector>
#include <utility>
using namespace std;

vector<double> dijkstra(const Graph &g, int start){
    const int n=g.nodes();
    vector<double> dist(n, numeric_limits<double>::infinity());
    dist[start]=0.0;
    vector<bool> visited(n, false);

    // using P=pair<double,int>;    //distance, node
    // priority_queue<P,vector<P>,greater<P>>pq;
    MinHeap pq;
    pq.push(0.0,start);

    while(!pq.empty()){
        // auto[dis,node]=pq.top();
        // pq.pop();
        auto [dis,node] = pq.pop(); //->similar to pq.top() + pq.pop() in MeanHeap
            // Skip if we’ve already processed this node
        if (visited[node]) continue;
        visited[node] = true;

        // Skip outdated distances
        if (dis > dist[node]) continue;


        for(const auto&[neighbor,weight]:g.neighbors(node)){
            if(dis+weight<dist[neighbor]){
                dist[neighbor]=dis+weight;
                // pq.push({dist[neighbor],neighbor});
                pq.push(dist[neighbor], neighbor);  //-> similar to pq.push({dist[neighbor], neighbor}) in MeanHeap
            }
        }
    }
    return dist;
}