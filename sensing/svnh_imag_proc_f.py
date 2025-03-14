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
from scipy.ndimage import binary_dilation
from scipy.ndimage import binary_erosion
from scipy.ndimage import gaussian_filter1d
from collections import deque

import helper

# file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
file_prefix = '../data/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
num_frame = 32
num_symbol_per_frame = 70

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

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, 10 * np.log10(data_abs), shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Input Time-Freq Plot", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf.png')
plt.close()

################################################################################
# Summation over frequency axis -> project the sum to time axis

proj_freq = np.sum(data_abs, axis=0)

plt.figure(figsize=fig_size)
plt.plot(freq[:-1], proj_freq)
plt.title('Projection to Freq Axis', size=font_title)
plt.xlabel('FFT Index', size=font_label)
plt.ylabel('Power Sum', size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_proj_freq.png')
plt.close()

################################################################################
# Set up a threshold to filter out the noise -> only work on the high power part

thres_time_sum = 8.5e-4 * num_symbol
# from the figure we pick thres = 1.7/20 for a 20-frame, each with 70 symbols
# thres_time_sum = 0.8 # used when the spectrogram has 200 frames (1000 symbols)
# thres_time_sum = 0 # bypassing the thresholding

print('thres_time_sum:', thres_time_sum)

plt.figure(figsize=fig_size)
plt.plot(freq[:-1], proj_freq)
plt.axhline(y=thres_time_sum, color='r',
            linestyle='--', label='Threshold = {}'.format(thres_time_sum))
plt.title('Projection to Freq Axis + Threshold', size=font_title)
plt.xlabel('Symbol Index', size=font_label)
plt.ylabel('Power Sum', size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.legend()
plt.tight_layout()
plt.savefig('figs/imag_proc_proj_freq_thres.png')
plt.close()

################################################################################
# Plot the spectrogram with the filtered time axis

proj_freq_bin = proj_freq > thres_time_sum

data_strip = data_abs * proj_freq_bin[np.newaxis, :]

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, 10 * np.log10(data_strip), shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Stripped Time-Freq Plot", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_high_energy.png')
plt.close()

################################################################################
# Find the threshold for each of the symbol (dynamic thresholding using Otsu)

# Rescale image to 0-255
data_strip = (data_strip - np.min(data_strip)) / (np.max(data_strip) - np.min(data_strip)) * 255
data_strip = data_strip.astype(np.uint8)

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
    final_img = gray.copy()
    final_img[gray >= final_thresh] = 1
    final_img[gray < final_thresh] = 0
    return final_img

def gaussian_thres(arr, window_size=11, c=3):
    pad_size = window_size // 2
    arr_pad = np.pad(arr, pad_size, mode='edge')
    arr_thres = np.zeros_like(arr)

    local_mean = gaussian_filter1d(arr_pad, sigma=window_size/6)[pad_size:-pad_size]

    arr_thres[arr > local_mean - c] = 1
    return arr_thres

for i in range(len(data_strip[0])):
    if proj_freq_bin[i]:
        data_strip[:, i] = otsu(data_strip[:, i])
        # data_strip[:, i] = gaussian_thres(data_strip[:, i])
# data_strip = otsu(data_strip)

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_strip, shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("Binarized Time-Freq Plot", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_otsu.png')
plt.close()

################################################################################
# Dilate the binary image to form continuous energy regions

struct_element = np.array([1, 1, 1])
kernel = np.ones((3, 3), np.uint8)

# Fill the holes in the energy blocks
data_strip = binary_dilation(data_strip, structure=kernel)
data_strip = binary_dilation(data_strip, structure=kernel)
data_strip = binary_erosion(data_strip, structure=kernel, border_value=1)
data_strip = binary_erosion(data_strip, structure=kernel, border_value=1)

# Eliminate the vertical lines that is our of blocks
data_strip = binary_erosion(data_strip, structure=kernel, border_value=1)
data_strip = binary_erosion(data_strip, structure=kernel, border_value=1)
data_strip = binary_dilation(data_strip, structure=kernel)
data_strip = binary_dilation(data_strip, structure=kernel)

# Horizontal dilation/erosion
for i in range(len(data_strip)):
    data_strip[i] = binary_erosion(data_strip[i], structure=struct_element)
    data_strip[i] = binary_erosion(data_strip[i], structure=struct_element)
    data_strip[i] = binary_erosion(data_strip[i], structure=struct_element)
    data_strip[i] = binary_dilation(data_strip[i], structure=struct_element)
    data_strip[i] = binary_dilation(data_strip[i], structure=struct_element)
    data_strip[i] = binary_dilation(data_strip[i], structure=struct_element)

plt.figure(figsize=fig_size)
plt.pcolormesh(freq, time, data_strip, shading='flat')
plt.colorbar(label="Power/Frequency (dB/Hz)")
plt.title("TF Plot after Morphological Operation", size=font_title)
plt.xlabel("Subcarrier Index", size=font_label)
plt.ylabel("Symbol Index", size=font_label)
plt.tick_params(axis='both', which='major', labelsize=font_tick)
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_dilated.png')
plt.close()

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

# sys.setrecursionlimit(10000)
# # abbreviation: l (left), r (right), t (top), b (bottom)
# def propagate(mat, x, y) -> list:
#     ll = lr = lt = lb = x
#     rl = rr = rt = rb = x
#     tl = tr = tt = tb = y
#     bl = br = bt = bb = y
#     mat[x, y] = NO_ENERGY
#     x_lim, y_lim = len(mat), len(mat[0])
#     if x-1 >= 0 and mat[x-1, y] == UNDETECTED_ENERGY:
#         [ll, rl, tl, bl] = propagate(mat, x-1, y)
#     if x+1 < x_lim and mat[x+1, y] == UNDETECTED_ENERGY:
#         [lr, rr, tr, br] = propagate(mat, x+1, y)
#     if y-1 >= 0 and mat[x, y-1] == UNDETECTED_ENERGY:
#         [lt, rt, tt, bt] = propagate(mat, x, y-1)
#     if y+1 < y_lim and mat[x, y+1] == UNDETECTED_ENERGY:
#         [lb, rb, tb, bb] = propagate(mat, x, y+1)
#     l = min(x, ll, lr, lt, lb)
#     r = max(x, rl, rr, rt, rb)
#     t = min(y, tl, tr, tt, tb)
#     b = max(y, bl, br, bt, bb)

#     return [l, r, t, b]

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
im = ax.pcolormesh(freq, time, 10 * np.log10(data_abs), shading='flat')

for box in boxes:
    y1, y2, x1, x2 = box
    ax.add_patch(patches.Rectangle((x1, y1), x2-x1, y2-y1, 
                                   fill=None, edgecolor='r'))
    print(f"Box: ({x1}, {y1}) to ({x2}, {y2})")

ax.set_title("Boxed Time-Freq Plot", size=font_title)
ax.set_xlabel("Subcarrier Index", size=font_label)
ax.set_ylabel("Symbol Index", size=font_label)
ax.tick_params(axis='both', which='major', labelsize=font_tick)
plt.colorbar(im, label="Power/Frequency (dB/Hz)")
plt.tight_layout()
plt.savefig('figs/imag_proc_tf_box.png')
plt.close()

################################################################################

time_end = t.perf_counter()
print(f"Execution time: {time_end - time_start:.2f} seconds")


################################################################################
# Save the bounding boxes to a file

boxes_np = np.array(boxes)
np.save('boxes.npy', boxes_np)
print('Bounding boxes ({}) are saved to boxes.npy'.format(len(boxes_np)))
