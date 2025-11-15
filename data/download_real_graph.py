import osmnx as ox
import pandas as pd

place = "Zurich, Switzerland"
G = ox.graph_from_place(place, network_type='drive')

edges = []
for u, v, data in G.edges(data=True):
    w = data.get("length", 1.0)
    edges.append((u, v, w))

df = pd.DataFrame(edges, columns=["u", "v", "weight"])

#Fix: remap IDs to contiguous range [0..N-1]
unique_nodes = pd.Index(sorted(set(df["u"]) | set(df["v"])))
mapping = {node: i for i, node in enumerate(unique_nodes)}

df["u"] = df["u"].map(mapping)
df["v"] = df["v"].map(mapping)

print(f"Original node count: {len(unique_nodes)}")
df.to_csv("real_graph.csv", index=False)
print(f"Saved {len(df)} edges to real_graph.csv")
