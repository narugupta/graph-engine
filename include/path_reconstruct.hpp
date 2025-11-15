#pragma once
#include "graph.hpp"
#include <vector>
#include <functional>
#include <utility>

std::pair<std::vector<double>, std::vector<int>> dijkstra_with_path(const Graph& g, int start);
std::pair<std::vector<double>, std::vector<int>> a_star_with_path(const Graph& g, int start, int goal, std::function<double(int,int)> heuristic);
std::vector<int> reconstruct_path(int start, int goal, const std::vector<int>& prev);
