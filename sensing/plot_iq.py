################################################################################
# Read raw I/Q samples, FFT-ed I/Q samples, and CSI from .bin files dumped by
# the sensing feature of Savannah.
# Author: Chung-Hsuan Tung
################################################################################

import struct
import matplotlib.pyplot as plt

# file_name = '../../savannah_isac/files/sensing/sensed_raw_frame0_sym0_sc0_size1024.bin'
# fig_name = 'raw_iq-1.png'

# file_name = '../../savannah_isac/files/sensing/sensed_fft_frame0_sym0_sc0_size1024.bin'
# fig_name = 'fft_iq-1.png'

file_name = '../../savannah_isac/files/sensing/sensed_csi_frame0_sc0_size1024.bin'
fig_name = 'csi_iq-1.png'

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
real_parts = [c.real for c in complex_values]
imag_parts = [c.imag for c in complex_values]
abs_values = [abs(c) for c in complex_values]

###
# Print basic info
print(f"Data length = {len(complex_values)} complex numbers.")

###

# Create subplots
fig, axes = plt.subplots(3, 1, figsize=(40, 12), sharex=True)

# Plot real parts
axes[0].plot(real_parts, marker='o', linestyle='-', color='r', label="Real Part")
axes[0].set_ylabel("Real Part")
axes[0].set_title("Real, Imaginary, and Absolute Values of Complex Numbers")
axes[0].legend()
axes[0].grid(True)

# Plot imaginary parts
axes[1].plot(imag_parts, marker='o', linestyle='-', color='b', label="Imaginary Part")
axes[1].set_ylabel("Imaginary Part")
axes[1].legend()
axes[1].grid(True)

# Plot absolute values
axes[2].plot(abs_values, marker='o', linestyle='-', color='g', label="Absolute Value")
axes[2].set_xlabel("Index")
axes[2].set_ylabel("Absolute Value")
axes[2].legend()
axes[2].grid(True)

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig(fig_name)
