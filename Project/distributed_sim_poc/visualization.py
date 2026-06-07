import matplotlib.pyplot as plt
import numpy as np

# 1. The New Empirical Data
latencies = [0, 5, 10, 25, 50, 75, 100]

# Warehouse Robot Data
wh_optimistic = [645.30, 719.39, 740.24, 768.08, 793.30, 735.39, 771.42]
wh_conservative = [482.35, 107.78, 56.53, 28.64, 16.51, 11.63, 8.97]

# Forest Fire Data
ff_optimistic = [129.87, 132.48, 131.71, 131.90, 132.10, 127.03, 128.92]
ff_conservative = [104.79, 63.52, 47.31, 25.38, 15.18, 10.26, 7.94]

# 2. Setup the dual-plot figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)
fig.suptitle('Throughput Degradation vs. Network Latency (100x100 Grid)', fontsize=20, fontweight='bold', y=1.05)

# --- Subplot 1: Warehouse Robots ---
ax1.plot(latencies, wh_optimistic, marker='o', linewidth=3, markersize=8, label='Optimistic (Ours)', color='#2ecc71')
ax1.plot(latencies, wh_conservative, marker='s', linewidth=3, markersize=8, label='Conservative', color='#e74c3c')
ax1.set_title('Simulation A: Warehouse Robot Routing', fontsize=15, pad=15)
ax1.set_xlabel('Network Latency (ms)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Throughput (Ticks / Second)', fontsize=13, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(fontsize=12)

# --- Subplot 2: Forest Fire ---
ax2.plot(latencies, ff_optimistic, marker='o', linewidth=3, markersize=8, label='Optimistic (Ours)', color='#2ecc71')
ax2.plot(latencies, ff_conservative, marker='s', linewidth=3, markersize=8, label='Conservative', color='#e74c3c')
ax2.set_title('Simulation B: Forest Fire Cellular Automata', fontsize=15, pad=15)
ax2.set_xlabel('Network Latency (ms)', fontsize=13, fontweight='bold')
ax2.set_ylabel('Throughput (Ticks / Second)', fontsize=13, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(fontsize=12)

# 3. Final layout and save
plt.tight_layout()
plt.savefig('final_dual_benchmark_chart.png', bbox_inches='tight')
print("Chart successfully generated and saved as 'final_dual_benchmark_chart.png'")