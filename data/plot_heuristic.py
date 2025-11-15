import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("heuristic_scaling.csv")

plt.figure(figsize=(7,5))
plt.plot(df["scale"], df["runtime_ms"], 'o-', label="Runtime (ms)")
plt.xlabel("Heuristic Scaling Factor (α)")
plt.ylabel("Runtime (ms)")
plt.title("Heuristic Scaling vs Runtime (A*)")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(7,5))
plt.plot(df["scale"], df["diff"], 'o-', color='red', label="Path Cost Difference")
plt.xlabel("Heuristic Scaling Factor (α)")
plt.ylabel("|A* - Dijkstra| Path Cost")
plt.title("Heuristic Scaling vs Accuracy Deviation")
plt.legend()
plt.grid()
plt.show()
