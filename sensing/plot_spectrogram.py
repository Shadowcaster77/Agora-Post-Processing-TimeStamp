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
file_postfix = '_sc0_size2048.bin'
frame_schedule = "PUUUUUUUUUUUUUUUUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
num_u = frame_schedule.count('U')
num_p = frame_schedule.count('P')
num_g = frame_schedule.count('G')
num_frame = 20
hide_guard = True
num_symbol_per_frame = num_u + num_p if hide_guard else num_u + num_p + num_g
fig_name = 'tf_sym_rfsynth_g.png'

'''
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''

size = 0
abs_values = []

for frame_index in range(0, num_frame):
    for symbol_index in range(0, num_symbol_per_frame):
        file_name = file_prefix + str(frame_index) + file_midfix + str(symbol_index) + file_postfix

        # Read binary data
        complex_values = helper.read_complex_samples(file_name)

        # Separate real, imaginary, and absolute parts
        abs_values.append([abs(c) for c in complex_values])
        size = len(complex_values)

        # only P and U are received symbols
        if not hide_guard and symbol_index >= num_u + num_p:
            assert size > 0, 'size should be intialized via sensed data'
            abs_values.append([np.nan] * size)
            

###
# Print basic info
print(f"Frame schedule: ({num_p}P {num_u}U {num_g}G) {frame_schedule}")
print(f"{num_frame} frames, {num_symbol_per_frame} symbols per frame, ")
print(f"total {len(abs_values)} symbols, ")
print(f"each with {size} complex numbers.")

###

num_symbol = num_frame * num_symbol_per_frame
time = np.linspace(0, num_symbol, num_symbol + 1)
freq = np.linspace(0, size, size+1)
data = np.array(abs_values)

plt.figure(figsize=(8, 6))
plt.rc('axes', labelsize=28)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.pcolormesh(freq, time, 10 * np.log10(data), shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title(f"Spectrogram ({num_p}P {num_u}U {num_g}G)", size=28)
plt.xlabel("Subcarrier Index", size=24)
plt.ylabel("Symbol Index", size=24)
plt.tight_layout()
plt.savefig(fig_name)
