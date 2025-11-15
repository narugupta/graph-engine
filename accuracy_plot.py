import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("perf_results.csv")

plt.figure(figsize=(8,5))
plt.plot(df["nodes"], df["dijkstra_ms"], label="Dijkstra Runtime", marker='o')
plt.plot(df["nodes"], df["astar_ms"], label="A* Runtime", marker='o')
plt.title("Runtime Comparison: Dijkstra vs A*")
plt.xlabel("Nodes")
plt.ylabel("Time (ms)")
plt.legend()
plt.grid(True)
plt.savefig("accuracy_runtime.png")
plt.show()
