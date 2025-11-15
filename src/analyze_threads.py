import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("perf_results_parallel.csv")
plt.plot(df["threads"], df["speedup"], marker='o')
plt.xlabel("Threads")
plt.ylabel("Speedup")
plt.title("Parallel Dijkstra Scalability")
plt.grid(True)
plt.show()
