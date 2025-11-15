# import pandas as pd
# import random

# def generate_graph(n, m):
#     edges = []
#     for _ in range(m):
#         u, v = random.randint(0, n-1), random.randint(0, n-1)
#         if u != v:
#             w = round(random.random() * 10, 2)
#             edges.append((u, v, w))
#     return pd.DataFrame(edges, columns=["u", "v", "w"])

# for n in [10000, 50000, 100000]:
#     m = 3 * n
#     df = generate_graph(n, m)
#     df.to_csv(f"graph_{n}.csv", index=False, header=False)
#     print(f" graph_{n}.csv created.")

# Generating graphs with coordinates for A* algorithm
import pandas as pd
import numpy as np
import os

def generate_graph(n_nodes=10000, avg_degree=3):
    coords = np.random.rand(n_nodes, 2) * 100
    edges = []

    for u in range(n_nodes):
        for _ in range(avg_degree):
            v = np.random.randint(0, n_nodes)
            if v != u:
                w = np.linalg.norm(coords[u] - coords[v])  # Euclidean distance
                edges.append((u, v, round(w, 2), coords[u][0], coords[u][1]))

    df = pd.DataFrame(edges, columns=["u", "v", "w", "x", "y"])
    df.to_csv(f"graph_{n_nodes}.csv", index=False)
    print(f" graph_{n_nodes}.csv created with coordinates")

for n in [10000, 50000, 100000]:
    generate_graph(n)
