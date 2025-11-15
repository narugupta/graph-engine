cmake_minimum_required(VERSION 3.16)
project(GraphEngine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ==========================================================
# Include headers
# ==========================================================
include_directories(include)

# ==========================================================
# Main Executable — graph_engine (Benchmark + Perf)
# ==========================================================
add_executable(graph_engine
    src/main.cpp
    src/dijkstra.cpp
    src/astar.cpp
    src/benchmark.cpp
    src/dijkstra_parallel.cpp
    include/graph.hpp
)


# Optional optimization flags (helps with perf testing)
target_compile_options(graph_engine PRIVATE -O2 -Wall -Wextra)

# ==========================================================
# Accuracy Validation Executable — graph_accuracy
# ==========================================================
# This program will compare A* and Dijkstra results
# ==========================================================
add_executable(graph_accuracy
    src/accuracy_test.cpp   
    src/path_reconstruct.cpp 
    src/dijkstra.cpp
    src/astar.cpp
    include/graph.hpp
    include/minheap.hpp
)

target_compile_options(graph_accuracy PRIVATE -O2 -Wall -Wextra)

find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    target_link_libraries(graph_engine PUBLIC OpenMP::OpenMP_CXX)
    target_link_libraries(graph_accuracy PUBLIC OpenMP::OpenMP_CXX)
endif()


# ==========================================================
# Output Directory (for clean organization)
# ==========================================================
set_target_properties(graph_engine PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set_target_properties(graph_accuracy PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
