#!/bin/bash
# collect_memory.sh
# Automates Valgrind Massif profiling for multiple graph sizes

OUTPUT="mem_profile.csv"
echo "nodes,peak_memory_MB" > $OUTPUT

for n in 10000 50000 100000; do
  echo "Running for $n nodes..."
  
  # Regenerate the graph for this size
  python3 data/generate_graph.py --nodes $n
  
  # Run Valgrind (silencing stdout)
  valgrind --tool=massif --massif-out-file=massif.out.${n} ./build/graph_engine > /dev/null 2>&1
  
  # Extract the peak heap usage (mem_heap_B)
  PEAK=$(grep "mem_heap_B=" massif.out.${n} | awk -F= '{print $2}' | sort -n | tail -1)
  PEAK_MB=$(awk -v B=$PEAK 'BEGIN {print B/1024/1024}')
  
  echo "${n},${PEAK_MB}" >> $OUTPUT
  echo "${n} nodes → ${PEAK_MB} MB peak"
done

echo "Memory profiling complete. Results saved to $OUTPUT"
