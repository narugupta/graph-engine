import pandas as pd
import matplotlib.pyplot as plt
import re
import glob
import os

# --------------------------------------------
# Parse massif output files and extract peaks
# --------------------------------------------
def parse_massif_output(filename):
    peak_mem = None
    with open(filename, "r") as f:
        for line in f:
            if "mem_heap_B=" in line:
                m = re.search(r"mem_heap_B=(\d+)", line)
                if m:
                    val = int(m.group(1))
                    peak_mem = max(val, peak_mem or 0)
    return peak_mem / (1024 * 1024) if peak_mem else None


# --------------------------------------------
# Collect all massif.out.* files
# --------------------------------------------
files = sorted(glob.glob("../build/massif.out.*"))
results = []
for f in files:
    peak = parse_massif_output(f)
    algo = "A*" if "astar" in f else "Dijkstra"
    nodes = re.search(r"(\d+)", f).group(1)
    results.append({"Algorithm": algo, "Nodes": int(nodes), "PeakMB": peak})

df = pd.DataFrame(results)
df.to_csv("mem_profile.csv", index=False)
print("Memory data saved to mem_profile.csv")

# --------------------------------------------
# Plot peak memory usage
# --------------------------------------------
plt.figure(figsize=(8,5))
for algo, d in df.groupby("Algorithm"):
    plt.plot(d["Nodes"], d["PeakMB"], marker="o", label=algo)
plt.xlabel("Nodes")
plt.ylabel("Peak Memory (MB)")
plt.title("Memory Usage Scaling (Valgrind Massif)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("memory_usage.png", dpi=300)
print("Saved: memory_usage.png")
