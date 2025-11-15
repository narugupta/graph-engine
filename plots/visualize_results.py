import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Check that perf_results.csv exists ---
# csv_path = "../build/perf_results.csv"
csv_path = "../build/perf_results_real.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"{csv_path} not found. Run ./bin/graph_engine first.")

# === Runtime Scaling (perf_results.csv) ===
df = pd.read_csv(csv_path)

plt.figure(figsize=(7,5))
plt.plot(df["nodes"], df["dijkstra_ms"], marker="o", label="Dijkstra")
plt.plot(df["nodes"], df["astar_ms"], marker="s", label="A*")
plt.xlabel("Number of Nodes")
plt.ylabel("Average Time (ms)")
plt.title("Runtime Comparison (Synthetic Graphs)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("runtime_comparison.png", dpi=300)
print("Saved runtime_comparison.png")

# === Speedup Trend ===
df["speedup"] = df["dijkstra_ms"] / df["astar_ms"]
plt.figure(figsize=(7,5))
plt.plot(df["nodes"], df["speedup"], marker="^", color="orange")
plt.xlabel("Number of Nodes")
plt.ylabel("Speedup (A*/Dijkstra)")
plt.title("A* Speedup Scaling")
plt.grid(True)
plt.tight_layout()
plt.savefig("speedup_trend.png", dpi=300)
print("Saved speedup_trend.png")

# === Optional: show quick text summary ===
print("\nSummary:")
print(df)
print("\nAverage speedup:", round(df['speedup'].mean(), 2), "x")
