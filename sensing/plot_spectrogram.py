################################################################################
# Read FFT-ed I/Q samples, and plot the spectrogram from .bin files dumped by
# the sensing feature of Savannah.
# Author: Chung-Hsuan Tung
################################################################################


import struct
import numpy as np
import matplotlib.pyplot as plt

file_prefix = '../../savannah_isac/files/sensing/sensing_fft_'
file_postfix = '_sc0-1024.bin'
frame_range = range(0, 200)
fig_name = 'fft_tf.png'

real_parts = []
imag_parts = []
comp_values = []
abs_values = []

for frame_index in frame_range:
    file_name = file_prefix + str(frame_index) + file_postfix

    # Read binary data
    complex_values = []
    try:
        with open(file_name, "rb") as file:
            while True:
                # Read two 32-bit floats (real and imaginary parts)
                data = file.read(8)  # 4 bytes for real, 4 bytes for imaginary
                if not data:
                    break
                # Unpack the binary data
                real, imag = struct.unpack('ff', data)  # 'ff' means two floats
                complex_values.append(complex(real, imag))
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        exit(1)

    # Separate real, imaginary, and absolute parts
    real_parts.append([c.real for c in complex_values])
    imag_parts.append([c.imag for c in complex_values])
    abs_values.append([abs(c) for c in complex_values])
    comp_values.append(complex_values)

###
# Print basic info
print(f"{len(real_parts)} frames, ")
print(f"each with {len(comp_values[0])} complex numbers.")

###

time = np.linspace(0, 200, 201)
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
plt.ylabel("Frame Index", size=24)
plt.tight_layout()
plt.savefig(fig_name)
