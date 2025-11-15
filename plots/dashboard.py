import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================
# Paths
# ============================
base_path = "../build"
perf_path = os.path.join(base_path, "perf_results.csv")
real_path = os.path.join(base_path, "perf_results_real.csv")
mem_path = os.path.join(base_path, "mem_profile.csv")
heur_path = os.path.join(base_path, "heuristic_scaling.csv")

# ============================
# Load CSVs safely
# ============================
@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()

perf_df = load_csv(perf_path)
real_df = load_csv(real_path)
mem_df = load_csv(mem_path)
heur_df = load_csv(heur_path)

# ============================
# Streamlit App Layout
# ============================
st.set_page_config(page_title="Graph Engine Dashboard", layout="wide")
st.title("Graph Engine — A* vs Dijkstra Benchmark Dashboard")

st.markdown("""
This interactive dashboard visualizes performance, accuracy, and memory benchmarks from your Graph Engine project.
Use the tabs below to explore each aspect.
""")

# ============================
# Tabs
# ============================
tab1, tab2, tab3, tab4 = st.tabs([
    "Runtime Scaling",
    "Real Graph Benchmark",
    "Memory Profile",
    "Heuristic Scaling"
])

# ======================================================
# Runtime Scaling
# ======================================================
with tab1:
    st.header("Runtime Scaling on Random Graphs")
    if not perf_df.empty:
        fig = px.line(perf_df, x="nodes", y=["dijkstra_ms", "astar_ms"],
                      markers=True,
                      labels={"value": "Time (ms)", "nodes": "Number of Nodes"},
                      title="Runtime Comparison (Random Graphs)")
        st.plotly_chart(fig, use_container_width=True)

        # Compute average speedup
        perf_df["speedup"] = perf_df["dijkstra_ms"] / perf_df["astar_ms"]
        avg_speedup = perf_df["speedup"].mean()
        st.metric("Average Speedup (A*/Dijkstra)", f"{avg_speedup:.2f}x")
    else:
        st.warning("Missing perf_results.csv — run ./bin/graph_engine first.")

# ======================================================
# Real Graph Benchmark
# ======================================================
with tab2:
    st.header("Real-Graph Benchmark (Zurich or other city)")
    if not real_df.empty:
        fig = px.bar(real_df.melt(var_name="Algorithm", value_name="Time (ms)"),
                     x="Algorithm", y="Time (ms)",
                     color="Algorithm", title="Real-Graph Performance")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing perf_results_real.csv — run ./bin/graph_engine real first.")

# ======================================================
# Memory Profile
# ======================================================
with tab3:
    st.header("Memory Usage (Valgrind Massif Profile)")
    if not mem_df.empty:
        mem_df.columns = [c.lower() for c in mem_df.columns]
        if "nodes" in mem_df.columns and "peak_mb" in mem_df.columns:
            x, y = mem_df["nodes"], mem_df["peak_mb"]
        elif "time" in mem_df.columns and "mem_mb" in mem_df.columns:
            x, y = mem_df["time"], mem_df["mem_mb"]
        else:
            x, y = mem_df.iloc[:, 0], mem_df.iloc[:, 1]

        fig = px.line(x=x, y=y, markers=True,
                      labels={"x": "Nodes / Time", "y": "Peak Memory (MB)"},
                      title="Memory Scaling (Valgrind Massif)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Missing mem_profile.csv — generate via valgrind + ms_print.")

# ======================================================
# Heuristic Scaling
# ======================================================
with tab4:
    st.header("A* Heuristic Scaling (α vs Runtime)")
    if not heur_df.empty:
        heur_df.columns = [c.lower().strip() for c in heur_df.columns]
        xcol = next((c for c in heur_df.columns if c in ["alpha", "α", "a"]), heur_df.columns[0])
        ycol = next((c for c in heur_df.columns if "time" in c), heur_df.columns[-1])

        fig = px.line(heur_df, x=xcol, y=ycol, markers=True,
                      labels={xcol: "α (Heuristic Weight)", ycol: "Runtime (ms)"},
                      title="Heuristic Influence on A* Runtime")
        st.plotly_chart(fig, use_container_width=True)

        min_idx = heur_df[ycol].idxmin()
        st.metric("Optimal α", heur_df[xcol].iloc[min_idx])
    else:
        st.warning("Missing heuristic_scaling.csv — run ./bin/graph_accuracy first.")

st.markdown("---")
st.caption("CERN Graph Engine Project — Week 10 Visualization Dashboard © 2025")
