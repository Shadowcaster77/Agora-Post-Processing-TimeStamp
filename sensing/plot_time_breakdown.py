################################################################################
# Plot a horizontal bar plot of the time breakdown.
#
# Author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
import numpy as np

# data
# Step names and times (in ms)
steps = ["Read Buffer", "PSD", "Otsu", "MO-2D", "MO-1D", "CCL", "Dump Box"]
times = [8.41, 12.39, 53.98, 229.60, 27.27, 9.70, 0.08]

# figure settings (font size)
font_title = 20
font_label = 20
font_tick = 20
fig_size = (6.4, 4.8) # default value
lw = 4
markersize = 12

###

# Create horizontal bar chart
fig, ax = plt.subplots(figsize=fig_size)
bars = ax.barh(steps, times, color='tab:blue', facecolor='white',
               edgecolor='tab:blue', hatch='///', zorder=10)

# Axis labels and title
ax.set_xlabel("Time (ms)", fontsize=font_label)
ax.tick_params(axis='both', labelsize=font_tick)
ax.set_xlim(0, max(times) + 100)  # Extend x-axis for better readability

# Put largest bar on top
ax.invert_yaxis()

# Grid lines for readability
ax.grid(axis='x', linestyle='--', alpha=1, zorder=1)

# Annotate each bar with its value
for bar in bars:
    width = bar.get_width()
    ax.text(width + 5, bar.get_y() + bar.get_height() / 2,
            f"{width:.2f}", va='center', fontsize=font_tick)

plt.tight_layout()
plt.savefig('figs/time_breakdown.pdf', format='pdf', bbox_inches='tight')
