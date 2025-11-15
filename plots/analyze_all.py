import os
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# File paths (relative to build/)
# =============================
base_path = "../build"
perf_path = os.path.join(base_path, "perf_results.csv")
real_path = os.path.join(base_path, "perf_results_real.csv")
mem_path = os.path.join(base_path, "mem_profile.csv")
heuristic_path = os.path.join(base_path, "heuristic_scaling.csv")

# =============================
# Load CSVs safely
# =============================
def load_csv(path, name):
    if os.path.exists(path):
        print(f"Loaded {name}: {path}")
        return pd.read_csv(path)
    else:
        print(f"Missing file: {path}")
        return pd.DataFrame()

perf_df = load_csv(perf_path, "perf data")
real_df = load_csv(real_path, "real data")
mem_df = load_csv(mem_path, "memory data")
heur_df = load_csv(heuristic_path, "heuristic data")

# =============================
# Create dashboard layout
# =============================
fig, axs = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle("Graph Engine Analysis Dashboard — Dijkstra vs A*", fontsize=14, fontweight="bold")

# ------------------------------------------------------------
# (1,1) Runtime Scaling (Random Graphs)
# ------------------------------------------------------------
if not perf_df.empty:
    axs[0, 0].plot(perf_df["nodes"], perf_df["dijkstra_ms"], label="Dijkstra", marker="o")
    axs[0, 0].plot(perf_df["nodes"], perf_df["astar_ms"], label="A*", marker="s")
    axs[0, 0].set_title("Runtime Scaling (Random Graphs)")
    axs[0, 0].set_xlabel("Nodes")
    axs[0, 0].set_ylabel("Time (ms)")
    axs[0, 0].legend()
else:
    axs[0, 0].text(0.4, 0.5, "Missing perf_results.csv", color="gray")

# ------------------------------------------------------------
# (1,2) Real-Graph Benchmark
# ------------------------------------------------------------
if not real_df.empty:
    axs[0, 1].bar(["Dijkstra", "A*"], [real_df["dijkstra_ms"].iloc[0], real_df["astar_ms"].iloc[0]],
                  color=["cornflowerblue", "orange"])
    axs[0, 1].set_title("Real-Graph Benchmark (Zurich)")
    axs[0, 1].set_ylabel("Time (ms)")
else:
    axs[0, 1].text(0.3, 0.5, "Missing perf_results_real.csv", color="gray")

# ------------------------------------------------------------
# (2,1) Memory Scaling (Valgrind Massif)
# ------------------------------------------------------------
if not mem_df.empty:
    # Normalize column names to lowercase for safety
    cols = [c.lower() for c in mem_df.columns]
    mem_df.columns = cols

    # Try to detect which columns exist
    if "nodes" in cols and "peak_mb" in cols:
        x = mem_df["nodes"]
        y = mem_df["peak_mb"]
    elif "time" in cols and "mem_mb" in cols:
        x = mem_df["time"]
        y = mem_df["mem_mb"]
    elif len(mem_df.columns) >= 2:
        x = mem_df.iloc[:, 0]
        y = mem_df.iloc[:, 1]
    else:
        axs[1, 0].text(0.3, 0.5, "Invalid mem_profile.csv format", color="gray")
        x, y = [], []

    if len(x) > 0:
        axs[1, 0].plot(x, y, label="Peak Memory (MB)", marker="^")
        axs[1, 0].set_title("Memory Scaling (Valgrind Massif)")
        axs[1, 0].set_xlabel("Nodes / Time")
        axs[1, 0].set_ylabel("Memory (MB)")
        axs[1, 0].legend()
    else:
        axs[1, 0].text(0.3, 0.5, "Empty memory data", color="gray")
else:
    axs[1, 0].text(0.2, 0.5, "Missing mem_profile.csv", color="gray")


# ------------------------------------------------------------
# (2,2) Heuristic Scaling (A*)
# ------------------------------------------------------------
if not heur_df.empty:
    # Normalize column names
    cols = [c.lower().strip() for c in heur_df.columns]
    heur_df.columns = cols

    # Try to find appropriate columns
    if "alpha" in cols and "time" in cols:
        x, y = heur_df["alpha"], heur_df["time"]
    elif "α" in cols and "time" in cols:
        x, y = heur_df["α"], heur_df["time"]
    elif "a" in cols and "time" in cols:
        x, y = heur_df["a"], heur_df["time"]
    elif "time_ms" in cols:
        x = range(len(heur_df))
        y = heur_df["time_ms"]
    else:
        x, y = range(len(heur_df)), heur_df.iloc[:, -1]
        print("Heuristic columns not labeled 'alpha'/'time', using fallback indices")

    axs[1, 1].plot(x, y, marker="o", color="darkorange", label="A* Runtime (ms)")
    axs[1, 1].set_title("Heuristic Scaling (α vs Runtime)")
    axs[1, 1].set_xlabel("α (Heuristic Weight)")
    axs[1, 1].set_ylabel("Time (ms)")
    axs[1, 1].legend()

    # Find best α automatically
    min_idx = y.idxmin()
    optimal_alpha = x.iloc[min_idx] if hasattr(x, "iloc") else x[min_idx]
    min_time = y.iloc[min_idx] if hasattr(y, "iloc") else y[min_idx]
    print(f"Optimal α ≈ {optimal_alpha} (fastest runtime {min_time:.3f} ms)")
else:
    axs[1, 1].text(0.25, 0.5, "Missing heuristic_scaling.csv", color="gray")


# ------------------------------------------------------------
# Save figure
# ------------------------------------------------------------
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("analysis_dashboard.png", dpi=200)
print("Saved analysis_dashboard.png (full comparison dashboard)")
plt.show()
