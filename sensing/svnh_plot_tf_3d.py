################################################################################
# Read FFT-ed I/Q samples, and plot the 3D time-frequency diagram from .bin
# files dumped by the sensing feature of Savannah.
#
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import helper


# file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
file_prefix = '../data/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
num_frame = 20
num_symbol_per_frame = 5
fig_name = 'figs/tf_3d.png'

'''
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''

################################################################################
# Read the IQ samples for Savannah's DumpToFile() in DoSensingFreq

comp_values = []
abs_values = []

for frame_index in range(0, num_frame):
    for symbol_index in range(0, num_symbol_per_frame):
        file_name = file_prefix + str(frame_index) +\
                    file_midfix + str(symbol_index) + file_postfix

        # Read binary data
        complex_values = helper.read_complex_samples(file_name)

        # Separate real, imaginary, and absolute parts
        abs_values.append([abs(c) for c in complex_values])
        comp_values.append(complex_values)

###
# Print basic info
fft_size = len(abs_values[0])
print(f"{len(abs_values)} symbols ", end='')
print(f"({num_frame} frames x each {num_symbol_per_frame} symbols), ")
print(f"each with {fft_size} complex numbers.")

num_symbol = num_frame * num_symbol_per_frame
time = np.linspace(0, num_symbol, num_symbol + 1)
freq = np.linspace(0, fft_size, fft_size+1)
data_abs = np.array(abs_values)

F, T = np.meshgrid(freq[:-1], time[:-1])


fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={"projection": "3d"})
# fig = plt.figure(figsize=(8, 6))
# ax = fig.add_subplot(111, projection='3d')
plt.rc('legend', fontsize=20)    # fontsize of the legend
# im = ax.pcolormesh(freq, time, 10 * np.log10(data_abs), shading='flat')
im = ax.plot_surface(F, T, 10 * np.log10(data_abs), cmap=cm.viridis)
ax.set_title("Time-Freq Plot", size=28)
ax.set_xlabel("Subcarrier Index", size=20)
ax.set_ylabel("Symbol Index", size=20)
ax.tick_params(axis='both', labelsize=16)
plt.colorbar(im, label="Power/Frequency (dB/Hz)")
plt.tight_layout()
plt.savefig(fig_name)
