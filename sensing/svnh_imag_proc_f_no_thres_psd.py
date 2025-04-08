################################################################################
# Read FFT-ed I/Q samples from .bin files dumped by the sensing feature of
# Savannah, and find the bounding box with classic image processing method.
#
#   1. Adaptive thresholding using Otsu
#   2. Morphological operations to eliminate noise
#   3. Connected component labeling to find the bounding boxes
#
# In this file, data_strip for adaptive threshold is dividing FREQUENCY bands.
#
# Author: Chung-Hsuan Tung
################################################################################

import sys
import time as t
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
from scipy.ndimage import binary_dilation
from scipy.ndimage import binary_erosion
from scipy.ndimage import gaussian_filter1d
from collections import deque

import helper

file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
# file_prefix = '../data/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
num_frame = 40
num_symbol_per_frame = 50
RFSYNTH_DATA_ID = input("Enter the rfsynth id (e.g., test): ") or 'test'

'''
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''

# figure settings (font size)
font_title = 20
font_label = 20
font_tick = 20
fig_size = (6.4, 4.8) # default value

time_start = t.perf_counter()

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
# avoid log(0) = -inf
data_abs[data_abs == 0] = min(data_abs[data_abs > 0])
data_abs = 10 * np.log10(data_abs)

print('max of data_abs: ', np.max(data_abs))
print('min of data_abs: ', np.min(data_abs))
print('mean of data_abs: ', np.mean(data_abs))

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_abs, shading='flat', linewidth=0)
cbar = plt.colorbar()
cbar.ax.tick_params(labelsize=font_tick)
cbar.ax.set_ylabel("Power (dB)", size=font_label)
# plt.title("Input Time-Freq Plot", size=font_title)
plt.xlabel("Frequency Index", size=font_label)
plt.ylabel("Time Index", size=font_label)
plt.xticks(np.arange(0, fft_size+1, 256))
plt.yticks(np.arange(0, num_symbol+1, 500))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf.png')
plt.close()

################################################################################
# Summation over time axis -> project the sum to frequency axis

proj_freq = np.sum(data_abs, axis=0)

plt.figure(figsize=fig_size)
plt.plot(freq[:-1], proj_freq)
plt.title('Projection to Freq Axis', size=font_title)
plt.xlabel('Frequency Index', size=font_label)
plt.ylabel('Power Sum', size=font_label)
plt.xticks(np.arange(0, fft_size+1, 256))
# plt.yticks(np.arange(0, 13, 2))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_proj_freq.png')
plt.close()

################################################################################
# Set up a threshold to filter out the noise -> only work on the high power part

# thres_time_sum = 1.5e-3 * num_symbol
thres_time_sum = 8.5e-4 * num_symbol * fft_size / 1024
# thres_time_sum = 15e-4 * num_symbol * fft_size / 1024
# thres_time_sum = 30e-4 * num_symbol * fft_size / 1024
# from the figure we pick thres = 1.7/20 for a 20-frame, each with 70 symbols
# fft_size / 1024 to normalize the threshold for different FFT sizes
# thres_time_sum = 0.8 # used when the spectrogram has 200 frames (1000 symbols)
# thres_time_sum = 0 # bypassing the thresholding

print('thres_time_sum:', thres_time_sum)

plt.figure(figsize=fig_size)
plt.plot(freq[:-1], proj_freq)
plt.axhline(y=thres_time_sum, color='r',
            linestyle='--', label='Threshold = {}'.format(thres_time_sum))
# plt.title('Projection to Freq Axis + Threshold', size=font_title)
plt.xlabel('Frequency Index', size=font_label)
plt.ylabel('PSD Sum', size=font_label)
plt.xticks(np.arange(0, fft_size+1, 256))
# plt.yticks(np.arange(0, 13, 2))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.legend(prop={'size': 20})
plt.tight_layout()
plt.savefig('figs/imag_proc_proj_freq_thres.pdf', format='pdf')
plt.close()

################################################################################
# Plot the spectrogram with the filtered time axis

proj_freq_bin = proj_freq > thres_time_sum

# thres = thres_time_sum / num_symbol
# data_strip = data_abs > thres * 3

data_strip = data_abs * proj_freq_bin[np.newaxis, :]
data_strip = data_abs # no thresholding

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_strip, shading='flat', linewidth=0)
cbar = plt.colorbar()
cbar.ax.tick_params(labelsize=font_tick)
cbar.ax.set_ylabel("Power (dB)", size=font_label)
plt.xlabel("Frequency Index", size=font_label)
plt.ylabel("Time Index", size=font_label)
plt.xticks(np.arange(0, fft_size+1, 256))
plt.yticks(np.arange(0, num_symbol+1, 500))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_high_energy.png')
plt.close()

################################################################################
# Find the threshold for each of the symbol (dynamic thresholding using Otsu)

print('sum of cx : ', np.sum(data_strip))
print('max of cx : ', np.max(data_strip))
print('min of cx : ', np.min(data_strip))

print('max of data_strip: ', np.max(data_strip))
print('min of data_strip: ', np.min(data_strip))
print('mean of data_strip: ', np.mean(data_strip))

# Rescale image to 0-255
data_strip = (data_strip - np.min(data_strip)) / (np.max(data_strip) - np.min(data_strip)) * 255
data_strip = data_strip.astype(np.uint8)

print('max of gray scale imag: ', np.max(data_strip))
print('min of gray scale imag: ', np.min(data_strip))
print('mean of gray scale imag: ', np.mean(data_strip))

his, bins = np.histogram(data_strip, np.arange(0, 257))
plt.figure(figsize=fig_size)
plt.plot(bins[:-1], his)
plt.title('Histogram of Gray Scale Image', size=font_title)
plt.xlabel('Pixel Value', size=font_label)
plt.ylabel('Number of Pixels', size=font_label)
plt.xticks(np.arange(0, 257, 32))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_hist.png')
plt.close()

def otsu(gray):
    pixel_number = len(gray)
    # pixel_number = len(gray) * len(gray[0])
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
        value = Wb * Wf * (mub - muf) ** 2

        if value > final_value:
            final_thresh = t
            final_value = value
    # print('final_value = ', final_value)
    # print('threshold = ', final_thresh)
    final_img = gray.copy()
    final_img[gray >= final_thresh] = 1
    final_img[gray < final_thresh] = 0
    return final_img, final_thresh

def gaussian_thres(arr, window_size=11, c=3):
    pad_size = window_size // 2
    arr_pad = np.pad(arr, pad_size, mode='edge')
    arr_thres = np.zeros_like(arr)

    local_mean = gaussian_filter1d(arr_pad, sigma=window_size/6)[pad_size:-pad_size]

    arr_thres[arr > local_mean - c] = 1
    return arr_thres

otsu_list = []

for i in range(len(data_strip[0])):

    data_strip[:, i], thres_temp = otsu(data_strip[:, i])
    otsu_list.append(thres_temp)
    # if proj_freq_bin[i]:
    #     # print("subcarrier index:", i)
    #     # print("max = ", np.max(data_strip[:, i]))
    #     # print("min = ", np.min(data_strip[:, i]))
    #     # print("sum:", np.sum(data_strip[:, i]))
    #     data_strip[:, i], thres_temp = otsu(data_strip[:, i])
    #     otsu_list.append(thres_temp)
    #     # print("num after otsu:", np.sum(data_strip[:, i]))
    #     # data_strip[:, i] = gaussian_thres(data_strip[:, i])
    # else:
    #     otsu_list.append(0)
# data_strip = otsu(data_strip)

print("num of ones:", np.sum(data_strip))
# print("num of zeros:", np.sum(data_strip == 0))

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_strip, cmap=ListedColormap(['white', 'black']),
               shading='flat', linewidth=0)
# plt.colorbar(label="Power/Frequency (dB/Hz)")
# plt.title("Binarized Time-Freq Plot", size=font_title)
plt.xlabel("Frequency Index", size=font_label)
plt.ylabel("Time Index", size=font_label)
plt.xticks(np.arange(0, fft_size+1, 256))
plt.yticks(np.arange(0, num_symbol+1, 500))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_otsu.png')
plt.close()

# plot otsu threshold
plt.figure(figsize=fig_size)
plt.plot(freq[:-1], otsu_list)
plt.title('Otsu Threshold', size=font_title)
plt.xlabel('Frequency Index', size=font_label)
plt.ylabel('Otsu Threshold', size=font_label)
plt.xticks(np.arange(0, fft_size+1, 256))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_otsu.png')
plt.close()

################################################################################
# Dilate the binary image to form continuous energy regions

##
se_3 = np.array([1, 1, 1])
kernel_3 = np.ones((3, 3), np.uint8)
kernel_5 = np.ones((5, 5), np.uint8)
kernel_7 = np.ones((11, 11), np.uint8)

# Vertical dilation/erosion
for i in range(len(data_strip[0])):
    data_strip[:, i] = binary_erosion(data_strip[:, i], structure=se_3)
    data_strip[:, i] = binary_dilation(data_strip[:, i], structure=se_3)

data_strip = binary_erosion(data_strip, structure=kernel_3, border_value=0)
data_strip = binary_dilation(data_strip, structure=kernel_3)

# Fill the holes in the energy blocks
data_strip = binary_dilation(data_strip, structure=kernel_5)
data_strip = binary_erosion(data_strip, structure=kernel_5, border_value=0)

data_strip = binary_erosion(data_strip, structure=kernel_7, border_value=0)
data_strip = binary_dilation(data_strip, structure=kernel_7)

##

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_strip, cmap=ListedColormap(['white', 'black']),
               shading='flat', linewidth=0)
# plt.colorbar(label="Power/Frequency (dB/Hz)")
# plt.title("TF Plot after Morphological Operation", size=font_title)
plt.xlabel("Frequency Index", size=font_label)
plt.ylabel("Time Index", size=font_label)
plt.xticks(np.arange(0, fft_size+1, 256))
plt.yticks(np.arange(0, num_symbol+1, 500))
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_dilated.png')
plt.close()

# exit(0)

################################################################################
# Find and label the connected components
#
# Agorithm:
#   1. Iterate through the matrix
#   2. If any energy detected, propagate to find the connected components and
#      identify the edges by finding left-most, right-most, top-most, and bottom
#      -most pixels.
#   3. During propagation, mark the pixels as detected (erase).

UNDETECTED_ENERGY = 1
NO_ENERGY = 0
boxes = []

# non-recursive version, similar processing time but less memory (no stack)
def propagate(mat, x, y) -> list:
    x_lim, y_lim = len(mat), len(mat[0])
    queue = deque([(x, y)])
    mat[x, y] = NO_ENERGY
    
    l = r = x
    t = b = y
    
    while queue:
        cx, cy = queue.popleft()
        
        l = min(l, cx)
        r = max(r, cx)
        t = min(t, cy)
        b = max(b, cy)
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < x_lim and 0 <= ny < y_lim:
                if mat[nx, ny] == UNDETECTED_ENERGY:
                    mat[nx, ny] = NO_ENERGY # Mark as visited
                    queue.append((nx, ny))
    
    return [l, r, t, b]

for i in range(len(data_strip)):
    for j in range(len(data_strip[0])):
        if data_strip[i, j] == UNDETECTED_ENERGY:
            edges = propagate(data_strip, i, j)
            boxes.append(edges)

print('Number of boxes:', len(boxes))

fig, ax = plt.subplots(figsize=fig_size)
im = ax.pcolormesh(freq, time, data_abs, shading='flat', linewidth=0)

for box in boxes:
    y1, y2, x1, x2 = box
    ax.add_patch(patches.Rectangle((x1, y1), x2-x1, y2-y1, 
                                   fill=None, edgecolor='r'))
    print(f"Box: ({x1}, {y1}) to ({x2}, {y2})")

# ax.set_title("Boxed Time-Freq Plot", size=font_title)
ax.set_xlabel("Frequency Index", size=font_label)
ax.set_ylabel("Time Index", size=font_label)
ax.tick_params(axis='both', which='major', labelsize=font_tick)
plt.xticks(np.arange(0, fft_size+1, 256))
plt.yticks(np.arange(0, num_symbol+1, 500))
cbar = plt.colorbar(im, label="Power (dB)")
cbar.ax.tick_params(labelsize=font_tick)
cbar.ax.set_ylabel("Power (dB)", size=font_label)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_box.png')
plt.close()

boxes.sort(key=lambda box: box[3])
boxes.sort(key=lambda box: box[2])
boxes.sort(key=lambda box: box[1])
boxes.sort(key=lambda box: box[0])

print('Bounding boxes:')
for box in boxes:
    print(box)

################################################################################

time_end = t.perf_counter()
print(f"Execution time: {time_end - time_start:.2f} seconds")

################################################################################
# Save the bounding boxes to a file

boxes_np = np.array(boxes)
np.save('boxes_' + RFSYNTH_DATA_ID + '.npy', boxes_np)
print('Bounding boxes ({}) are saved to boxes_{}.npy'.format(
    len(boxes_np), RFSYNTH_DATA_ID))
