import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

BUILD_DIR = "../build"

# Helper function
def load_csv(filename):
    path = os.path.join(BUILD_DIR, filename)
    if os.path.exists(path):
        print(f"✅ Loaded {filename}")
        return pd.read_csv(path)
    else:
        print(f"⚠️ Missing {filename}")
        return pd.DataFrame()

# Load all data
perf_df = load_csv("perf_results.csv")
real_df = load_csv("perf_results_real.csv")
mem_df = load_csv("mem_profile.csv")
heur_df = load_csv("heuristic_scaling.csv")

# Create output folder
os.makedirs("../reports", exist_ok=True)

# 1️ Runtime Scaling Plot
if not perf_df.empty:
    plt.figure(figsize=(6,4))
    plt.plot(perf_df["nodes"], perf_df["dijkstra_ms"], marker="o", label="Dijkstra")
    plt.plot(perf_df["nodes"], perf_df["astar_ms"], marker="s", label="A*")
    plt.xlabel("Nodes")
    plt.ylabel("Runtime (ms)")
    plt.title("Runtime Scaling — Dijkstra vs A*")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("../reports/runtime_scaling.png", dpi=200)
    plt.close()

# 2️ Real Graph Plot
if not real_df.empty:
    plt.figure(figsize=(5,4))
    # plt.bar(["Dijkstra", "A*"], real_df.iloc[0,1:])
    # 2️ Real Graph Plot
if not real_df.empty:
    # Normalize headers
    real_df.columns = [c.lower().strip() for c in real_df.columns]
    # Find timing columns (ignore 'nodes' or similar)
    cols = [c for c in real_df.columns if "ms" in c or "time" in c or "dijkstra" in c or "astar" in c]
    
    # Extract first row values
    values = real_df[cols].iloc[0].values
    plt.figure(figsize=(6,4))
    plt.bar(cols, values, color=["#4472C4", "#ED7D31", "#70AD47"][:len(cols)])
    plt.title("Real Graph Benchmark (ms)")
    plt.ylabel("Time (ms)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("../reports/real_graph.png", dpi=200)
    plt.close()

    plt.title("Real Graph Benchmark")
    plt.ylabel("Time (ms)")
    plt.tight_layout()
    plt.savefig("../reports/real_graph.png", dpi=200)
    plt.close()

# 3️ Memory Profile
if not mem_df.empty:
    mem_df.columns = [c.lower() for c in mem_df.columns]
    x = mem_df[mem_df.columns[0]]
    y = mem_df[mem_df.columns[1]]
    plt.figure(figsize=(6,4))
    plt.plot(x, y, label="Peak Memory (MB)", color="darkgreen")
    plt.xlabel("Nodes / Time")
    plt.ylabel("Memory (MB)")
    plt.title("Memory Scaling (Valgrind Massif)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("../reports/memory_profile.png", dpi=200)
    plt.close()

# 4️ Heuristic Scaling
if not heur_df.empty:
    heur_df.columns = [c.lower().strip() for c in heur_df.columns]
    xcol = next((c for c in heur_df.columns if c in ["alpha", "α", "a"]), heur_df.columns[0])
    ycol = next((c for c in heur_df.columns if "time" in c), heur_df.columns[-1])

    plt.figure(figsize=(6,4))
    plt.plot(heur_df[xcol], heur_df[ycol], marker="o", color="orange")
    plt.title("A* Heuristic Scaling (α vs Runtime)")
    plt.xlabel("α (Heuristic Weight)")
    plt.ylabel("Runtime (ms)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("../reports/heuristic_scaling.png", dpi=200)
    plt.close()

#  PDF REPORT GENERATION
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Graph Engine - Performance Analysis Report", ln=True, align="C")

pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, "This report summarizes benchmarking and profiling results for Dijkstra and A* algorithms on both random and real-world graphs. Generated automatically by analyze_all_auto.py.\n")

def add_plot(title, image_path):
    if os.path.exists(image_path):
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, title, ln=True)
        pdf.image(image_path, w=170)
    else:
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, f"[Missing plot: {image_path}]", ln=True)

add_plot("Runtime Scaling", "../reports/runtime_scaling.png")
add_plot("Real Graph Benchmark", "../reports/real_graph.png")
add_plot("Memory Profile", "../reports/memory_profile.png")
add_plot("Heuristic Scaling", "../reports/heuristic_scaling.png")

pdf.output("../reports/GraphEngine_Report.pdf")
print("PDF Report generated at: ../reports/GraphEngine_Report.pdf")
