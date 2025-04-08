################################################################################
# Plot a horizontal bar plot of the time breakdown.
#
# Author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
import numpy as np

# data
# Step names and times (in ms)
x = np.array([1024, 512, 256, 128, 64, 32])
y = np.array([1, 4, 16, 64, 256, 1024])
y1 = [244.7404, 125.3270, 67.3215, 38.0795, 22.1518, 19.0639]   # Line 1
y2 = [236.5843, 117.4783, 62.7935, 33.7642, 14.9236, 8.2666]   # Line 2

# figure settings (font size)
font_title = 20
font_label = 20
font_tick = 20
fig_size = (6.4, 4.8) # default value
lw = 4
markersize = 12

###

# Create plot
plt.figure(figsize=fig_size)
plt.plot(x, y1, 'o-', color='tab:blue', label='Maximum',
         markersize=markersize, linewidth=lw, zorder=10)
plt.plot(x, y2, '^--', color='tab:orange', label='Average',
         markersize=markersize, linewidth=lw, zorder=10)
plt.axhline(20.48, color='red', linestyle='--', linewidth=lw, zorder=5)

# X-axis: log scale, reversed
plt.xscale('log', base=2)
plt.yscale('log', base=2)
plt.gca().invert_xaxis()  # Reverse the x-axis
plt.xticks(x, [str(v) for v in x], fontsize=font_tick)
plt.yticks(y, [str(v) for v in y], fontsize=font_tick)
plt.tick_params(axis='both', labelsize=font_tick)
plt.ylim(1, 300)

# Labels, legend, and grid
plt.xlabel("Subband Size", fontsize=font_label)
plt.ylabel("Time (ms)", fontsize=font_label)
plt.grid(True, which='both', linestyle='--', zorder=1)
plt.legend(fontsize=font_tick, loc='lower left', ncol=2)

plt.tight_layout()
plt.savefig('figs/time_vs_subband.pdf', format='pdf', bbox_inches='tight')
