################################################################################
# Plot a single figure with 2 lines and bar plots for PD, PFA, and IoU over SNR
# based on the measurements from the SNR sweep.
#
# Author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
import numpy as np

# data
snr = [10, 5, 0, -5, -10, -15, -20]
pd  = [0.5151, 0.4528, 0.3309, 0.2848, 0.1476, 0.0536, 0.0000]
pfa = [0.4496, 0.4274, 0.3500, 0.0000, 0.0000, 0.1000, 0.0000]
iou = [0.4081, 0.4112, 0.2737, 0.1835, 0.1077, 0.0415, 0.0000]

snr = np.array(snr)
x = np.arange(len(snr))  # bar positions

# figure settings (font size)
font_title = 20
font_label = 20
font_tick = 20
fig_size = (6.4, 4.8) # default value
lw = 4
markersize = 12

###

fig, ax1 = plt.subplots(figsize=fig_size)

line1, = ax1.plot(x, pd, 'o-', color='tab:blue', label=r'$P_d$', linewidth=lw,
                  markersize=markersize)
line2, = ax1.plot(x, pfa, 's--', color='tab:orange', label=r'$P_{fa}$',
                  linewidth=lw, markersize=markersize)
ax1.set_xlabel('SNR (dB)', fontsize=font_label)
ax1.set_ylim(0, 0.6)
ax1.set_ylabel(r'Probability ($P_d$, $P_{fa}$)', fontsize=font_label,
               color='black')
ax1.tick_params(axis='both', labelsize=font_tick, labelcolor='black')
ax1.set_xticks(x)
ax1.set_xticklabels(snr, fontsize=font_tick)

# IoU bars on right y-axis
ax2 = ax1.twinx()
bars = ax2.bar(x, iou, width=0.4, color='tab:green', alpha=0.5)
ax2.set_ylim(0, 0.5)
ax2.set_ylabel('IoU', fontsize=font_label, color='tab:green')
ax2.tick_params(axis='y', labelsize=font_tick, labelcolor='tab:green')

# Make ax1 (lines) draw on top
ax1.set_zorder(ax2.get_zorder() + 1)     # Ensure ax1 is drawn above
ax1.patch.set_visible(False)             # Make ax1 background transparent

# Combine legends
lines = [line1, line2, bars]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper right', fontsize=font_tick)


plt.tight_layout()
plt.savefig('figs/snr_pd_pfa_iou.pdf', format='pdf', bbox_inches='tight')
