################################################################################
# Read the time profile result from the csv file and plot the CCDF for each
# subband size.
#
# Author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
import numpy as np


# Read the time profile result from the csv file
def read_csv_file(filename):
    data = np.genfromtxt(filename, delimiter=',')
    return data

# figure settings (font size)
font_title = 20
font_label = 20
font_tick = 20
fig_size = (6.4, 4.8) # default value
lw = 2
markersize = 9

###
# Plot

# Sort data
data_1c = read_csv_file('time_new_1c.csv')
sorted_data_1c = np.sort(data_1c)
data_2c = read_csv_file('time_new_2c.csv')
sorted_data_2c = np.sort(data_2c)
data_4c = read_csv_file('time_new_4c.csv')
sorted_data_4c = np.sort(data_4c)
data_8c = read_csv_file('time_new_8c.csv')
sorted_data_8c = np.sort(data_8c)
data_16c = read_csv_file('time_new_16c.csv')
sorted_data_16c = np.sort(data_16c)
data_32c = read_csv_file('time_new_32c.csv')
sorted_data_32c = np.sort(data_32c)

# print('99% percentile time for 16 core:', sorted_data_16c[int(0.99*len(sorted_data_16c))])
# exit(0)

# Compute CCDF: P(X > x)
ccdf_1c = 1.0 - np.arange(1, len(sorted_data_1c)+1) / len(sorted_data_1c)
ccdf_2c = 1.0 - np.arange(1, len(sorted_data_2c)+1) / len(sorted_data_2c)
ccdf_4c = 1.0 - np.arange(1, len(sorted_data_4c)+1) / len(sorted_data_4c)
ccdf_8c = 1.0 - np.arange(1, len(sorted_data_8c)+1) / len(sorted_data_8c)
ccdf_16c = 1.0 - np.arange(1, len(sorted_data_16c)+1) / len(sorted_data_16c)
ccdf_32c = 1.0 - np.arange(1, len(sorted_data_32c)+1) / len(sorted_data_32c)

# Plot
plt.figure(figsize=fig_size)
plt.plot(sorted_data_1c, ccdf_1c, marker='o', linewidth=lw,
         mfc='none', mec='tab:blue', mew=2, markersize=markersize,
         color='tab:blue', label='1 core')
plt.plot(sorted_data_2c, ccdf_2c, marker='^', linewidth=lw,
         mfc='none', mec='tab:orange', mew=2, markersize=markersize,
         color='tab:orange', label='2 core')
plt.plot(sorted_data_4c, ccdf_4c, marker='s', linewidth=lw,
         mfc='none', mec='tab:green', mew=2, markersize=markersize,
         color='tab:green', label='4 core')
plt.plot(sorted_data_8c, ccdf_8c, marker='D', linewidth=lw,
         mfc='none', mec='tab:red', mew=2, markersize=markersize,
         color='tab:red', label='8 core')
plt.plot(sorted_data_16c, ccdf_16c, marker='P', linewidth=lw,
         mfc='none', mec='tab:brown', mew=2, markersize=markersize,
         color='tab:brown', label='16 core')
plt.plot(sorted_data_32c, ccdf_32c, marker='X', linewidth=lw,
         mfc='none', mec='tab:purple', mew=2, markersize=markersize,
         color='tab:purple', label='32 core')
plt.axhline(0.01, color='black', linestyle='--', linewidth=lw, zorder=5)
plt.axvline(20.48, color='red', linestyle='--', linewidth=lw, zorder=5)
plt.figtext(0.3, 0.22, f'20.48 ms', fontsize=font_tick, ha='center', color='red')
plt.figtext(0.75, 0.60, f'99th Percentile', fontsize=font_tick, ha='center')
plt.xlabel('Time (ms)', fontsize=font_label)
# plt.ylim(10e-4, 1)
plt.ylabel('Complementary CDF', fontsize=font_label)
plt.xticks(fontsize=font_tick)
plt.yticks(fontsize=font_tick)
plt.xscale('log', base=2)
plt.xticks([8, 16, 32, 64, 128, 256, 512],
           [str(8), str(16), str(32), str(64), str(128), str(256), str(512)],
           fontsize=font_tick)
plt.grid(True)
plt.yscale('log')  # Optional: log-scale for heavy tails
plt.legend(fontsize=font_tick, loc='upper left', ncol=2)
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend().remove()
plt.tight_layout()
plt.savefig('figs/ccdf_time_vs_subband.pdf', format='pdf', bbox_inches='tight')

# Plot the legend in its own figure
legend_fig = plt.figure(figsize=(6, 0.5))
legend = legend_fig.legend(handles=handles, loc='center', ncol=6,
                          fontsize=14, frameon=False)
plt.savefig('figs/ccdf_legend.pdf', format='pdf', bbox_inches='tight')
