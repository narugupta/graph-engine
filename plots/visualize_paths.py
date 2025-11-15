import os
import pandas as pd
import matplotlib.pyplot as plt
import random
import networkx as nx
import osmnx as ox

# =======================================================
# 1️Heuristic Scaling Plot (Flexible CSV Parsing)
# =======================================================

csv_path = "../build/heuristic_scaling.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print(f"Loaded heuristic data: {csv_path}")
else:
    print("No heuristic_scaling.csv found — generating demo data.")
    df = pd.DataFrame({
        "alpha": [0, 0.5, 1, 2, 5],
        "cost": [30.5, 30.5, 30.5, 30.5, 30.5]
    })

# --- detect columns automatically ---
if "alpha" in df.columns and "cost" in df.columns:
    x, y, xlabel, ylabel = df["alpha"], df["cost"], "Heuristic Weight α", "Path Cost"
elif "A*_cost" in df.columns and "alpha" in df.columns:
    x, y, xlabel, ylabel = df["alpha"], df["A*_cost"], "Heuristic Weight α", "A* Path Cost"
elif len(df.columns) >= 2:
    cols = df.columns[:2]
    x, y, xlabel, ylabel = df[cols[0]], df[cols[1]], cols[0], cols[1]
else:
    raise ValueError(f"Unsupported CSV format: columns={df.columns}")

plt.figure(figsize=(7,5))
plt.plot(x, y, marker="o", label="A* Path Cost")
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title("A* Path Cost Stability vs Heuristic Strength")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("heuristic_scaling.png", dpi=300)
print("Saved heuristic_scaling.png")

# =======================================================
# 2️Optional: Real OSM Path Visualization
# =======================================================

try:
    place = "Zurich, Switzerland"
    print("Downloading sample map for path visualization...")
    G = ox.graph_from_place(place, network_type="drive")
    G = ox.project_graph(G)

    # FIXED: wrap in list() so random.sample() works
    nodes = list(G.nodes())
    start, goal = random.sample(nodes, 2)

    route = nx.shortest_path(G, start, goal, weight="length")
    fig, ax = ox.plot_graph_route(G, route, route_linewidth=3, node_size=0, bgcolor='white')
    fig.savefig("sample_route.png", dpi=300, bbox_inches="tight")
    print("Saved sample_route.png (OSM path visualization)")
except Exception as e:
    print(f"Skipped OSM path plot: {e}")
