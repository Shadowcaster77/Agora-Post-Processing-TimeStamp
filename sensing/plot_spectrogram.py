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
num_frame = 200
num_symbol_per_frame = 5
fig_name = 'tf_sym.png'

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

for frame_index in range(0, num_frame):
    for symbol_index in range(0, num_symbol_per_frame):
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
print(f"{num_frame} frames, {num_symbol_per_frame} symbols per frame, ")
print(f"{len(real_parts)} symbols, ")
print(f"each with {len(comp_values[0])} complex numbers.")

###

num_symbol = num_frame * num_symbol_per_frame
time = np.linspace(0, num_symbol, num_symbol + 1)
freq = np.linspace(0, len(comp_values[0]), len(comp_values[0])+1)
data = np.array(abs_values)

plt.figure(figsize=(8, 6))
plt.rc('axes', labelsize=28)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.pcolormesh(freq, time, 10 * np.log10(data), shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Spectrogram", size=28)
plt.xlabel("Subcarrier Index", size=24)
plt.ylabel("Symbol Index", size=24)
plt.tight_layout()
plt.savefig(fig_name)
