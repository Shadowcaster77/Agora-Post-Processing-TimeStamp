################################################################################
# Plot a grouped horizontal bar plot of the time breakdown (two bars per step),
# and highlight when the second bar is longer (i.e., slower).
#
# Author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
import numpy as np

# Step names
steps = ["Sparse", "RFsynth Default", "Control", "Dense-Mix", "Dense-DSSS", "Wideband"]

# Example data: Method A and Method B times
times_A = [1, 1, 1, 1, 1, 1]   # Baseline
times_B = [19.79, 30.71, 28.29, 35.74, 17.13, 791.49]  # To compare

# Settings
font_title = 20
font_label = 20
font_tick = 20
fig_size = (6.4, 4.8)
bar_height = 0.35
lw = 4
markersize = 12

# Create horizontal grouped bar chart
y = np.arange(len(steps))
fig, ax = plt.subplots(figsize=fig_size)
# Bars with patterns and black edge
bars_A = ax.barh(y - bar_height/2, times_A, height=bar_height,
                 facecolor='white', edgecolor='tab:blue', hatch='///',
                 label='Searchlight', zorder=10)

bars_B = ax.barh(y + bar_height/2, times_B, height=bar_height,
                 facecolor='white', edgecolor='tab:orange', hatch='xxx',
                 label='RISE', zorder=10)
# Axes and labels
ax.set_xlabel("Speedup", fontsize=font_label)
ax.set_yticks(y)
ax.set_yticklabels(steps, fontsize=font_tick)
ax.tick_params(axis='x', labelsize=font_tick)
ax.set_xlim(0.1, max(max(times_A), max(times_B)) * 100)
ax.set_xscale('log')
ax.invert_yaxis()
ax.grid(axis='x', linestyle='--', alpha=1, zorder=1)
# ax.legend(fontsize=font_tick)
ax.legend(
    loc='lower center',          # Anchor point inside the legend box
    bbox_to_anchor=(0.5, 1.02),  # X=0.5 (center), Y=just above the top
    fontsize=font_tick,
    ncol=2,                      # Optional: arrange legend entries in multiple columns
    frameon=False                # Optional: remove legend box border
)

# Annotate each bar
for i in range(len(steps)):
    # ax.text(times_A[i] + 2, y[i] - bar_height/2, f"{times_A[i]:.2f}", va='center', fontsize=font_tick)
    ax.text(times_B[i] + 2, y[i] + bar_height/2, f"{times_B[i]:.2f}x", va='center', fontsize=font_tick)

plt.tight_layout()
plt.savefig('figs/speedup.pdf', format='pdf', bbox_inches='tight')
