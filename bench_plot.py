import pandas as pd
import matplotlib.pyplot as plt
import os

# Load CSV (adjust if it's in build/)
df = pd.read_csv("build/perf_results.csv")

# Create the plot
plt.figure(figsize=(8,5))
plt.plot(df["nodes"], df["dijkstra_ms"], marker='o', label="Dijkstra")
plt.plot(df["nodes"], df["astar_ms"], marker='o', label="A*")

plt.xlabel("Number of Nodes")
plt.ylabel("Average Runtime (ms)")
plt.title("Performance Scaling: Dijkstra vs A*")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save instead of showing
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/perf_scaling.png")

print("Plot saved as plots/perf_scaling.png")
