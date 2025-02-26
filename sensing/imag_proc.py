################################################################################
# Read FFT-ed I/Q samples from .bin files dumped by the sensing feature of
# Savannah, and find the bounding box with classic image processing method.
# Author: Chung-Hsuan Tung
################################################################################


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import binary_dilation
from scipy.ndimage import binary_erosion

import helper

# file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
file_prefix = '../data/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
num_frame = 20
num_symbol_per_frame = 5
fig_name = 'imag_proc_2d.png'

'''
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''

# figure settings (font size)
font_title = 20
font_label = 15
font_tick = 12
fig_size = (6.4, 4.8) # default value

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
freq = np.linspace(0, fft_size, fft_size + 1)
data_abs = np.array(abs_values)

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, 10 * np.log10(data_abs), shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Input Spectrogram", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('imag_proc_spectrogram.png')
plt.close()

################################################################################
# Summation over frequency axis -> project the sum to time axis

proj_time = np.sum(data_abs, axis=1)

plt.figure(figsize=fig_size)
plt.plot(time[:-1], proj_time)
plt.title('Projection to Time Axis', size=font_title)
plt.xlabel('Symbol Index', size=font_label)
plt.ylabel('Power Sum', size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('imag_proc_proj_time.png')
plt.close()

################################################################################
# Set up a threshold to filter out the noise -> only work on the high power part

thres_freq_sum = 1024 / fft_size # from the figure we pick thres = 1

print('thres_freq_sum:', thres_freq_sum)

plt.figure(figsize=fig_size)
plt.plot(time[:-1], proj_time)
plt.axhline(y=thres_freq_sum, color='r',
            linestyle='--', label='Threshold = {}'.format(thres_freq_sum))
plt.title('Projection to Time Axis + Threshold', size=font_title)
plt.xlabel('Symbol Index', size=font_label)
plt.ylabel('Power Sum', size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.legend()
plt.tight_layout()
plt.savefig('imag_proc_proj_time_thres.png')
plt.close()

################################################################################
# Plot the spectrogram with the filtered time axis

proj_time_bin = proj_time > thres_freq_sum

data_strip = data_abs * proj_time_bin[:, np.newaxis]

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, 10 * np.log10(data_strip), shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Stripped Spectrogram", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('imag_proc_spectrogram_high_energy.png')
plt.close()

################################################################################
# Find the threshold for each of the symbol (dynamic thresholding using Otsu)

# Rescale image to 0-255
data_strip = (data_strip - np.min(data_strip)) / (np.max(data_strip) - np.min(data_strip)) * 255
data_strip = data_strip.astype(np.uint8)

def otsu(gray):
    pixel_number = len(gray)
    mean_weight = 1.0/pixel_number
    his, bins = np.histogram(gray, np.arange(0, 257))
    final_thresh = -1
    final_value = -1
    intensity_arr = np.arange(256)
    for t in bins[1:-1]: # This goes from 1 to 254 uint8 range (Pretty sure wont be those values)
        pcb = np.sum(his[:t])
        pcf = np.sum(his[t:])
        Wb = pcb * mean_weight
        Wf = pcf * mean_weight

        mub = np.sum(intensity_arr[:t]*his[:t]) / float(pcb)
        muf = np.sum(intensity_arr[t:]*his[t:]) / float(pcf)
        #print mub, muf
        value = Wb * Wf * (mub - muf) ** 2

        if value > final_value:
            final_thresh = t
            final_value = value
    final_img = gray.copy()
    # print(final_thresh)
    final_img[gray >= final_thresh] = 1
    final_img[gray < final_thresh] = 0
    return final_img

for i in range(len(data_strip)):
    if proj_time_bin[i]:
        data_strip[i] = otsu(data_strip[i])

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_strip, shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Binarized Spectrogram", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('imag_proc_spectrogram_otsu.png')
plt.close()

################################################################################
# Dilate the binary image to form continuous energy regions

struct_element = np.array([1, 1, 1])
kernel = np.ones((3, 3), np.uint8)

# # Horizontal dilation/erosion
# for i in range(len(data_strip)):
#     if proj_time_bin[i]:
#         data_strip[i] = binary_dilation(data_strip[i], structure=struct_element)
#         data_strip[i] = binary_dilation(data_strip[i], structure=struct_element)
#         data_strip[i] = binary_dilation(data_strip[i], structure=struct_element)
#         data_strip[i] = binary_erosion(data_strip[i], structure=struct_element)
#         data_strip[i] = binary_erosion(data_strip[i], structure=struct_element)
#         data_strip[i] = binary_erosion(data_strip[i], structure=struct_element)

# # Vertical dilation/erosion
# for i in range(len(data_strip[0])):
#     data_strip[:, i] = binary_dilation(data_strip[:, i], structure=struct_element)
#     data_strip[:, i] = binary_dilation(data_strip[:, i], structure=struct_element)
#     data_strip[:, i] = binary_dilation(data_strip[:, i], structure=struct_element)
#     data_strip[:, i] = binary_erosion(data_strip[:, i], structure=struct_element, border_value=1)
#     data_strip[:, i] = binary_erosion(data_strip[:, i], structure=struct_element, border_value=1)
#     data_strip[:, i] = binary_erosion(data_strip[:, i], structure=struct_element, border_value=1)

data_strip = binary_dilation(data_strip, structure=kernel)
data_strip = binary_dilation(data_strip, structure=kernel)
data_strip = binary_dilation(data_strip, structure=kernel)
data_strip = binary_erosion(data_strip, structure=kernel, border_value=1)
data_strip = binary_erosion(data_strip, structure=kernel, border_value=1)
data_strip = binary_erosion(data_strip, structure=kernel, border_value=1)

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_strip, shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Spectrogram after Morphological Operation", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('imag_proc_spectrogram_dilated.png')
plt.close()
