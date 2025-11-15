#pragma once
#include <vector>
#include <utility>
#include <limits>
#include <unordered_map>

struct MinHeap {
    std::vector<std::pair<double,int>> heap;
    std::unordered_map<int,int> pos; // node → index in heap

    bool empty() const { return heap.empty(); }

    void swap_nodes(int i, int j) {
        std::swap(heap[i], heap[j]);
        pos[heap[i].second] = i;
        pos[heap[j].second] = j;
    }

    void push(double dist, int node) {
        if (pos.count(node)) { // decrease-key
            if (dist < heap[pos[node]].first) {
                heap[pos[node]].first = dist;
                sift_up(pos[node]);
            }
            return;
        }
        heap.emplace_back(dist, node);
        pos[node] = heap.size() - 1;
        sift_up(pos[node]);
    }

    void sift_up(int i) {
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (heap[parent].first <= heap[i].first) break;
            swap_nodes(parent, i);
            i = parent;
        }
    }

    void sift_down(int i) {
        int n = heap.size();
        while (true) {
            int left = 2*i+1, right = 2*i+2, smallest = i;
            if (left < n && heap[left].first < heap[smallest].first) smallest = left;
            if (right < n && heap[right].first < heap[smallest].first) smallest = right;
            if (smallest == i) break;
            swap_nodes(i, smallest);
            i = smallest;
        }
    }

    std::pair<double,int> pop() {
        auto top = heap.front();
        swap_nodes(0, heap.size()-1);
        heap.pop_back();
        pos.erase(top.second);
        if (!heap.empty()) sift_down(0);
        return top;
    }
};
