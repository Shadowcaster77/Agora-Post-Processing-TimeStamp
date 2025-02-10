################################################################################
# Read FFT-ed I/Q samples, and plot the spectrogram from .bin files dumped by
# the sensing feature of Savannah.
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt

import helper

file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
frame_range = range(0, 200)
sybmol_range = range(0, 5)
idx = 4
fig_name = 'fft_sym{}_box.png'.format(idx)

'''
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''

real_parts = []
imag_parts = []
comp_values = []
abs_values = []

for frame_index in frame_range:
    for symbol_index in sybmol_range:
        file_name = file_prefix + str(frame_index) + file_midfix + str(symbol_index) + file_postfix

        # Read binary data
        complex_values = helper.read_complex_samples(file_name)

        # Separate real, imaginary, and absolute parts
        real_parts.append([c.real for c in complex_values])
        imag_parts.append([c.imag for c in complex_values])
        abs_values.append([abs(c) for c in complex_values])
        comp_values.append(complex_values)

###
# Print basic info
print(f"{len(real_parts)} symbols, ")
print(f"each with {len(comp_values[0])} complex numbers.")

###

box_size_range = range(1, 1024)
prefix_sum_abs_values = np.cumsum(abs_values[idx], axis=0)
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

print(f"Max start = {max_start}")
print(f"Max end = {max_end}")

# Find new box edge from the power change rate
power_change_rate = np.diff(abs_values[idx])/abs_values[idx][:-1]
max_start = np.argmax(power_change_rate[:max_start]) # search from center to left
max_end = np.argmin(power_change_rate[max_end:]) + max_end # search from center to right

print(f"Max average power = {max_avg_power}")
print(f"Max start = {max_start}")
print(f"Max end = {max_end}")

# Plot in a waveform
plt.figure(figsize=(20, 6))
plt.rc('axes', labelsize=28)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=20)    # fontsize of the legend
plt.axvline(x=max_start, color='r', linestyle='--')
plt.axvline(x=max_end, color='r', linestyle='--')
plt.plot(abs_values[idx], marker='o', linestyle='-', color='g', label="Absolute Value")
# plt.plot(power_change_rate, marker='o', linestyle='-', color='g', label="Power Change Rate")
plt.xlabel("Subcarrier Index")
plt.ylabel("Absolute Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(fig_name)
