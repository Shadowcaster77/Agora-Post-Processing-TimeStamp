################################################################################
# Plot two figures, one for p_d and one for p_fa. Each figure has test cases,
# and y-axis is the probability of detection or false alarm, while x-axis is 
# the IoU threshold.
#
# Author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
import numpy as np

# data
# IoU thresholds (in increasing order left to right)
thresholds = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# Pd values for each method (reversed to match threshold order)
data = {
    "Sparse":          [1.00, 1.00  , 1.00  , 1.00  , 1.00  , 0.5455, 0.4091, 0.3636, 0.3636, 0.00,   0.00],
    "RFSynth Default": [1.00, 1.00  , 1.00  , 1.00  , 0.9231, 0.9231, 0.6923, 0.6923, 0.4615, 0.00,   0.00],
    "Control":         [1.00, 0.8056, 0.6944, 0.4722, 0.4167, 0.4167, 0.4167, 0.4167, 0.3889, 0.1944, 0.00],
    "Dense-Mix":       [1.00, 1.00  , 1.00  , 0.9912, 0.9825, 0.4211, 0.4211, 0.3860, 0.3509, 0.0088, 0.00],
    "Dense-DSSS":      [1.00, 1.00  , 1.00  , 0.9259, 0.7407, 0.6296, 0.6296, 0.6296, 0.5926, 0.00,   0.00],
    "Wideband":        [1.00, 0.9048, 0.7619, 0.7619, 0.7619, 0.7619, 0.7619, 0.7619, 0.6667, 0.1429, 0.00],
}

# figure settings (font size)
font_title = 28
font_label = 24
font_tick = 24
fig_size = (6, 5) # default value
lw = 3
markersize = 10
markers = ['o', 's', '^', 'D', 'v', 'X', 'P', '*']

###
# Plot
fig, ax = plt.subplots(figsize=fig_size)
legend_handles = []

for (label, values), marker in zip(data.items(), markers):
    line, = ax.plot(thresholds, values, marker=marker, label=label,
            markersize=markersize, linewidth=lw)
    legend_handles.append(line)

# X-axis: tick labels every 0.2, grid every 0.1
xticks_major = np.arange(0.0, 1.01, 0.2)
xticks_minor = np.arange(0.0, 1.01, 0.1)
ax.set_xticks(xticks_major)
ax.set_xticklabels([f"{t:.1f}" for t in xticks_major])
ax.set_xticks(xticks_minor, minor=True)
ax.set_xlim([-0.05, 1.05])
ax.set_xlabel("IoU Threshold", fontsize=font_label)

# Y-axis: tick labels every 0.2, grid every 0.1
yticks_major = np.arange(0.0, 1.01, 0.2)
yticks_minor = np.arange(0.0, 1.01, 0.1)
ax.set_yticks(yticks_major)
ax.set_yticklabels([f"{t:.1f}" for t in yticks_major])
ax.set_yticks(yticks_minor, minor=True)
ax.set_ylim([-0.05, 1.05])
ax.set_ylabel("P$_d$", fontsize=font_label)

# Grid settings
ax.grid(which='major', linestyle='--', alpha=0.6)
ax.grid(which='minor', linestyle='--', alpha=0.6)

# Tick settings
ax.tick_params(axis='both', labelsize=font_tick)

# Title and legend
# ax.legend(title="Model", fontsize=11)
plt.tight_layout()
plt.savefig('figs/tiou_pd.pdf', format='pdf', bbox_inches='tight')

# Plot the legend in its own figure
legend_fig = plt.figure(figsize=(6, 0.5))
legend = legend_fig.legend(handles=legend_handles, loc='center', ncol=len(data),
                          fontsize=14, frameon=False)
plt.savefig('figs/tiou_pd_legend.pdf', format='pdf', bbox_inches='tight')
