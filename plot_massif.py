import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------------------------------
# Function: Run Massif for given algorithm and graph size
# --------------------------------------------------
def run_massif(algo, size):
    print(f"\n🚀 Running Valgrind Massif for {algo.upper()} on {size} nodes...")
    out_file = f"build/massif_{algo}_{size}.out"

    # Run graph_engine with algorithm argument (must be handled in C++ main)
    cmd = [
        "valgrind",
        "--tool=massif",
        f"--massif-out-file={out_file}",
        "./build/graph_engine",
        algo
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f" Completed: {out_file}")
    return out_file


# --------------------------------------------------
#  Function: Parse massif.out file for peak heap memory
# --------------------------------------------------
def parse_peak(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
        matches = re.findall(r"mem_heap_B=(\d+)", content)
        if not matches:
            print(f" No memory data found in {filename}")
            return 0.0
        peak = max(map(int, matches))
        return peak / (1024 * 1024)  # Convert bytes → MB
    except Exception as e:
        print(f" Error reading {filename}: {e}")
        return 0.0


# --------------------------------------------------
#  Main profiling loop
# --------------------------------------------------
algorithms = ["dijkstra", "astar"]
graph_sizes = [10000, 50000, 100000]
results = []

for algo in algorithms:
    for size in graph_sizes:
        massif_file = run_massif(algo, size)
        peak_mb = parse_peak(massif_file)
        results.append({"algo": algo, "nodes": size, "peak_MB": peak_mb})
        print(f" {algo.upper()}({size}) → Peak Memory: {peak_mb:.3f} MB")

# Save results
df = pd.DataFrame(results)
df.to_csv("mem_profile.csv", index=False)
print("\n Results saved to mem_profile.csv")

# --------------------------------------------------
#  Plot 1: Peak Memory Scaling for each algorithm
# --------------------------------------------------
plt.figure(figsize=(7,5))
for algo, group in df.groupby("algo"):
    plt.plot(group["nodes"], group["peak_MB"], marker="o", linewidth=2, label=algo.upper())

plt.title("Peak Memory Scaling (Dijkstra vs A*)")
plt.xlabel("Number of Nodes")
plt.ylabel("Peak Heap Memory (MB)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("memory_compare.png", dpi=300)
plt.show()
print(" Saved: memory_compare.png")

# --------------------------------------------------
# 🔹 Plot 2: Detailed memory timeline for the largest A* run
# --------------------------------------------------
sample_file = f"build/massif_astar_{graph_sizes[-1]}.out"
if os.path.exists(sample_file):
    times, heap = [], []
    with open(sample_file, "r") as f:
        time, mem = None, None
        for line in f:
            if "time=" in line:
                time = float(line.split("=")[-1].strip())
            elif "mem_heap_B=" in line:
                mem = float(line.split("=")[-1].strip()) / (1024 * 1024)
                if time is not None:
                    times.append(time)
                    heap.append(mem)
                    time = None

    if times:
        plt.figure(figsize=(7,5))
        plt.plot(times, heap, marker="o", color="orange", label=f"A* ({graph_sizes[-1]} nodes)")
        plt.title(f"Heap Memory Usage Over Time (A* - {graph_sizes[-1]} nodes)")
        plt.xlabel("Execution Time (arbitrary units)")
        plt.ylabel("Heap Memory (MB)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("massif_detail.png", dpi=300)
        plt.show()
        print(" Saved: massif_detail.png")
    else:
        print(f" No time/memory data parsed from {sample_file}")
else:
    print(f" Sample file not found: {sample_file}")
