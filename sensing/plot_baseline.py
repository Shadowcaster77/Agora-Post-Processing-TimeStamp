################################################################################
# Plot a grouped horizontal bar plot of the time breakdown (two bars per step),
# and highlight when the second bar is longer (i.e., slower).
#
# Author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
import numpy as np

# Step names
config = ["Sparse", "RFsynth Default", "Control", "Dense-Mix", "Dense-DSSS", "Wideband"]
y = np.arange(len(config))
bar_height = 0.25

# Searchlight (A) vs RISE (B) / DeepRadar (C)
speedup_A = [1.97, 1.33, 1.37, 0.96, 1.57, 0.05]
speedup_B = [38.93, 40.84, 38.80, 34.48, 26.95, 36.26]
speedup_C = [1, 1, 1, 1, 1, 1]

pd_A =  [18.18, 38.46, 2.78, 0.88, 11.11, 0.00]
pd_B =  [63.63, 84.61, 41.66, 41.22, 62.96, 76.19]
pd_C =  [18.18, 24.08, 2.78, 3.51, 0.00, 0.00]

pfa_A = [98.91, 99.62, 99.93, 99.93, 97.00, 100.00]
pfa_B = [33.33, 26.67, 50.00, 67.80, 72.58, 27.27]
pfa_C = [81.82, 76.92, 97.22, 95.74, 100.00, 100.00]

iou_A = [23.20, 31.90, 11.57, 10.68, 20.44, 13.07]
iou_B = [61.59, 70.59, 48.42, 60.00, 66.38, 66.18]
iou_C = [29.71, 28.78, 22.76, 17.70, 32.87, 5.80]

# Reverse the order for plotting
config = config[::-1]
speedup_A = speedup_A[::-1]
speedup_B = speedup_B[::-1]
speedup_C = speedup_C[::-1]
pd_A = pd_A[::-1]
pd_B = pd_B[::-1]
pd_C = pd_C[::-1]
pfa_A = pfa_A[::-1]
pfa_B = pfa_B[::-1]
pfa_C = pfa_C[::-1]
iou_A = iou_A[::-1]
iou_B = iou_B[::-1]
iou_C = iou_C[::-1]

# Plot settings
font_label = 20
font_tick = 20
fig_size = (20, 4.8)

# Metric titles and data
titles = ["Speedup to DeepRadar", r"$P_d$ (%)", r"$P_{fa}$ (%)", "IoU (%)"]
data_pairs = [
    (speedup_A, speedup_B, speedup_C, "log", [0.1, max(speedup_B)*15]),
    (pd_A, pd_B, pd_C, "linear", [0, 100]),
    (pfa_A, pfa_B, pfa_C, "linear", [0, 100]),
    (iou_A, iou_B, iou_C, "linear", [0, 100]),
]

# Create 2×2 subplots
fig, axs = plt.subplots(1, 4, figsize=fig_size, sharey=True)

for idx, (ax, (data_a, data_b, data_c, scale, xlim), title) in enumerate(zip(axs.flat, data_pairs, titles)):
    bars_A = ax.barh(y + bar_height, data_a, height=bar_height,
                     facecolor='white', edgecolor='tab:blue', hatch='///',
                     label='Searchlight', zorder=10)
    bars_C = ax.barh(y, data_c, height=bar_height,
                     facecolor='white', edgecolor='tab:green', hatch='\\\\\\',
                     label='DeepRadar', zorder=10)
    bars_B = ax.barh(y - bar_height, data_b, height=bar_height,
                     facecolor='white', edgecolor='tab:orange', hatch='xxx',
                     label='RISE', zorder=10)

    # Title and axis
    ax.set_xlabel(title, fontsize=font_label)
    ax.set_xlim(xlim)
    ax.set_xscale(scale)
    ax.grid(axis='x', linestyle='--', alpha=0.7, zorder=1)

    # Y-axis labels on left only
    if idx % 2 == 0:
        ax.set_yticks(y)
        ax.set_yticklabels(config, fontsize=font_tick)
    else:
        ax.set_yticks(y)
        ax.set_yticklabels(config, fontsize=font_tick)
    
    # ax.invert_yaxis()
    ax.tick_params(axis='x', labelsize=font_tick)

    # Annotate speedup with "×"
    if title == "Speedup to DeepRadar":
        for i in range(len(config)):
            ax.text(data_b[i] * 1.2, y[i] - bar_height,
                    f"{data_b[i]:.2f}×", va='center', fontsize=font_tick)

# Shared legend on top
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.02),
           fontsize=font_tick, ncol=3, frameon=False)

plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.savefig("figs/baseline.pdf", bbox_inches='tight')
