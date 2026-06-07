import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 1. THE FIX: Use true numerical values for the X-axis to preserve mathematical scale
x_values = [100, 10000, 100000, 1000000]

rate_0 = [0.0045, 0.3896, 3.2557, 27.2158]
rate_50 = [0.0080, 0.7817, 6.0947, 55.3116]
rate_100 = [0.0082, 0.8807, 7.0939, 67.6741]

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

# Plotting with true numerical X values
ax.plot(x_values, rate_0, marker='o', linewidth=3, markersize=8, label='0% Conflict Rate', color='#3498db')
ax.plot(x_values, rate_50, marker='s', linewidth=3, markersize=8, label='50% Conflict Rate', color='#f39c12')
ax.plot(x_values, rate_100, marker='^', linewidth=3, markersize=8, label='100% Conflict Rate', color='#e74c3c')

# 2. THE FORMATTING: Make the large X-axis numbers readable (e.g., "1,000,000")
ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# Labels and Styling
ax.set_ylabel('Resolution Time (Milliseconds)', fontsize=13, fontweight='bold')
ax.set_xlabel('Boundary Size (Number of Cells)', fontsize=13, fontweight='bold')
ax.set_title('Algorithm Scalability: True Linear Time O(N)', fontsize=16, fontweight='bold', pad=20)

ax.legend(fontsize=12, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.7)

# Annotate the highest points
ax.annotate(f'{rate_100[-1]:.1f}ms', xy=(x_values[-1], rate_100[-1]), xytext=(-35, 5), 
            textcoords='offset points', ha='right', fontweight='bold', color='#e74c3c')
ax.annotate(f'{rate_0[-1]:.1f}ms', xy=(x_values[-1], rate_0[-1]), xytext=(-35, -15), 
            textcoords='offset points', ha='right', fontweight='bold', color='#3498db')

plt.tight_layout()
plt.savefig('core_scalability_true_linear.png')
print("✅ Chart saved as 'core_scalability_true_linear.png'")