################################################################################
# Read FFT-ed I/Q samples from .bin files dumped by the sensing feature of
# Savannah, and find the bounding box with reduced Searchlight method in 1D.
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt

import helper

file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size2048.bin'
num_frame = 200
num_symbol_per_frame = 5
idx = 3
fig_name = 'fft_sym{}_box.png'.format(idx)

'''
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''

frame_index = idx // num_symbol_per_frame
symbol_index = idx % num_symbol_per_frame

file_name = file_prefix + str(frame_index) + file_midfix + str(symbol_index) + file_postfix
complex_values = helper.read_complex_samples(file_name)
abs_values = [abs(c) for c in complex_values]

###

box_size_range = range(1, 1024)
prefix_sum_abs_values = np.cumsum(abs_values, axis=0)
max_avg_power = 0 # find the maximum average power in a bounding box
max_start = 0
max_end = 0

for box_size in box_size_range:
    for start in range(0, 1024 - box_size):
        end = start + box_size
        avg_power = (prefix_sum_abs_values[end] - prefix_sum_abs_values[start]) / box_size
        if avg_power > max_avg_power:
            max_avg_power = avg_power
            max_start = start
            max_end = end

##
# Print the convolution results
print(f"Max start = {max_start}")
print(f"Max end = {max_end}")

# Find new box edge from the power change rate
power_change_rate = np.diff(abs_values)/abs_values[:-1]
max_start = np.argmax(power_change_rate[:max_start]) # search from center to left
max_end = np.argmin(power_change_rate[max_end:]) + max_end # search from center to right

##
# Print the final results
print(f"Max average power = {max_avg_power}")
print(f"Max start = {max_start}")
print(f"Max end = {max_end}")

##
# Plot in a waveform

# Create a figure with two subplots
fig, axes = plt.subplots(2, 1, figsize=(20, 12))  # 1 row, 2 columns

# Set global font sizes
plt.rc('legend', fontsize=20)    # fontsize of the legend

# First subplot: Absolute Value
axes[0].axvline(x=max_start, color='r', linestyle='--')
axes[0].axvline(x=max_end, color='r', linestyle='--')
axes[0].plot(abs_values, marker='o', linestyle='-', color='tab:blue', label="Absolute Value")
# axes[0].set_xlabel("Subcarrier Index", fontsize=28)
axes[0].set_ylabel("Absolute Value", fontsize=28)
axes[0].tick_params(axis='both', labelsize=20)
axes[0].legend()
axes[0].grid(True)

# Second subplot: Power Change Rate
axes[1].axvline(x=max_start, color='r', linestyle='--')
axes[1].axvline(x=max_end, color='r', linestyle='--')
axes[1].plot(power_change_rate, marker='o', linestyle='-', color='tab:orange', label="Power Change Rate")
axes[1].set_xlabel("Subcarrier Index", fontsize=28)
axes[1].set_ylabel("Power Change Rate", fontsize=28)
axes[1].tick_params(axis='both', labelsize=20)
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig(fig_name)
