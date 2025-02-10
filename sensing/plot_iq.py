################################################################################
# Read raw I/Q samples, FFT-ed I/Q samples, and CSI from .bin files dumped by
# the sensing feature of Savannah.
# Author: Chung-Hsuan Tung
################################################################################

# import struct
import matplotlib.pyplot as plt

import helper

input_path = '../../savannah_isac/files/sensing/'

file_name = input_path + 'sensed_raw_frame0_sym0_sc0_size1088.bin'
fig_name = 'raw_iq.png'

# file_name = input_path + 'sensed_fft_frame0_sym0_sc0_size1024.bin'
# fig_name = 'fft_iq.png'

# file_name = input_path + 'sensed_csi_frame0_sc0_size1024.bin'
# fig_name = 'csi.png'

###
# Read binary data
complex_values = helper.read_complex_samples(file_name)

# Separate real, imaginary, and absolute parts
real_parts = [c.real for c in complex_values]
imag_parts = [c.imag for c in complex_values]
abs_values = [abs(c) for c in complex_values]

###
# Print basic info
print(f"Data length = {len(complex_values)} complex numbers.")

###

# Create subplots
fig, axes = plt.subplots(3, 1, figsize=(8, 6), sharex=True)

# Plot real parts
axes[0].plot(real_parts, marker='.', linestyle='-', color='r', label="Real")
axes[0].set_ylabel("Real Part")
axes[0].set_title("Real, Imaginary, and Absolute Values of Complex Numbers")
axes[0].legend()
axes[0].grid(True)

# Plot imaginary parts
axes[1].plot(imag_parts, marker='.', linestyle='-', color='b', label="Imag")
axes[1].set_ylabel("Imaginary Part")
axes[1].legend()
axes[1].grid(True)

# Plot absolute values
axes[2].plot(abs_values, marker='.', linestyle='-', color='g', label="Abs Value")
axes[2].set_xlabel("Index")
axes[2].set_ylabel("Absolute Value")
axes[2].legend()
axes[2].grid(True)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig(fig_name)
