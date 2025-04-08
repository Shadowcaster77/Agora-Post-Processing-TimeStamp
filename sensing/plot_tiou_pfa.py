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
    "Sparse":          [0.0000, 0.0000, 0.0000, 0.0385, 0.0385, 0.3846, 0.6538, 0.6923, 0.6923, 1.0000, 1.0000],
    "RFSynth Default": [0.0000, 0.0667, 0.0667, 0.1333, 0.2000, 0.2000, 0.4000, 0.4000, 0.6000, 1.0000, 1.0000],
    "Control":         [0.0000, 0.0333, 0.1667, 0.4333, 0.5000, 0.5000, 0.5000, 0.5000, 0.5333, 0.7667, 1.0000],
    "Dense-Mix":       [0.0000, 0.2055, 0.2055, 0.2192, 0.2329, 0.6712, 0.6712, 0.6986, 0.7260, 0.9932, 1.0000],
    "Dense-DSSS":      [0.0000, 0.3065, 0.3871, 0.5323, 0.6613, 0.7258, 0.7258, 0.7258, 0.7419, 1.0000, 1.0000],
    "Wideband":        [0.0000, 0.0455, 0.2727, 0.2727, 0.2727, 0.2727, 0.2727, 0.2727, 0.3636, 0.8636, 0.9545]
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
ax.set_ylabel("P$_{fa}$", fontsize=font_label)

# Grid settings
ax.grid(which='major', linestyle='--', alpha=0.6)
ax.grid(which='minor', linestyle='--', alpha=0.6)

# Tick settings
ax.tick_params(axis='both', labelsize=font_tick)

# Title and legend
# ax.legend(title="Model", fontsize=11)
plt.tight_layout()
plt.savefig('figs/tiou_pfa.pdf', format='pdf', bbox_inches='tight')

# Plot the legend in its own figure
legend_fig = plt.figure(figsize=(6, 0.5))
legend = legend_fig.legend(handles=legend_handles, loc='center', ncol=len(data),
                          fontsize=14, frameon=False)
plt.savefig('figs/tiou_pfa_legend.pdf', format='pdf', bbox_inches='tight')
