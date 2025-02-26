################################################################################
# Read FFT-ed I/Q samples from .bin files dumped by the sensing feature of
# Savannah, and find the bounding box with reduced Searchlight method.
# Author: Chung-Hsuan Tung
################################################################################

import time as t
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import product
from functools import cmp_to_key
from scipy.ndimage import convolve
from scipy.ndimage import laplace

import helper

# file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
file_prefix = '../data/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
num_frame = 20
num_symbol_per_frame = 5
fig_name = 'fft_box_2d_best_15.png'

'''
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''

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

################################################################################
# Generate the kernel sizes for the Searchlight method

num_symbol = num_frame * num_symbol_per_frame
time = np.linspace(0, num_symbol, num_symbol + 1)
freq = np.linspace(0, fft_size, fft_size+1)
data_abs = np.array(abs_values)

# Box size search in time-bandwidth product
t_size = list(range(1, num_symbol))
# f_size = list(range(1, fft_size))
# only accept power of 2 sizes
f_size = [1 << i for i in range(int(math.log2(fft_size)+1))]
# test
# t_size = list(range(1, 5))
# f_size = list(range(1, 3))

# Populate time-bandwidth products
tb_prod_list = list(product(t_size, f_size))

# Sort kernel sizes with time-bandwidth product
# ref: https://stackoverflow.com/questions/18265935/how-do-i-create-a-list-with-numbers-between-two-values
# def tb_prod(item):
#     return item[0] * item[1]
# def compare(item1, item2):
#     return tb_prod(item1) - tb_prod(item2)
# tb_prod_list.sort(key=cmp_to_key(compare))
# tb_prod_list.sort(key=cmp_to_key(lambda x, y: tb_prod(x) - tb_prod(y)))
tb_prod_list.sort(key=cmp_to_key(lambda x, y: x[0] * x[1] - y[0] * y[1]))

print('number of kernels = {}'.format(len(tb_prod_list)))

################################################################################
# Calculate 2D prefix sum (assuming uniform kernel contents)
#   creation: calculate row prefix sum then column prefix sum
#   calculation: regtangular area of (x1, y1) - (x2, y2)
#      ans = arr(x2, y2) - arr(x2, y1-1) - arr(x1-1, y2) + arr(x1-1, y1-1)
# ref: https://www.geeksforgeeks.org/prefix-sum-2d-array/

ps_abs = np.cumsum(abs_values, axis=0)
ps_abs = np.cumsum(ps_abs, axis=1)
def get_sum_in_area(psum, x1, y1, x2, y2):
    '''
    a | b
    -----
    c | d
    '''
    assert x1 <= x2 and y1 <= y2, 'coordinate must be in order: x1<=x2, y1<=y2'
    a = psum[x1-1][y1-1] if x1-1 >= 0 and y1-1 >= 0 else 0
    b = psum[x1-1][y2] if x1-1 >= 0 else 0
    c = psum[x2][y1-1] if y1-1 >= 0 else 0
    d = psum[x2][y2]
    return d - c - b + a

# ps_exp = np.array([[10, 30, 60], [5, 10, 20], [2, 4, 6]])
# ps_exp = np.array([[10, 30, 60], [15, 45, 95], [17, 51, 107]])
# print(get_ps_in_area(ps_exp, 0, 1, 2, 2))

def clean_area(mat, x1, y1, x2, y2):
    assert x1 >= 0 and y1 >= 0 and x2 < len(mat) and y2 < len(mat[0]),\
           'out of bound'

    # erase the area
    for i in range(x1, x2):
        for j in range(y1, y2):
            mat[i][j] = 0

    # re-calculate prefix sum matrix
    mat = np.cumsum(mat, axis=0)
    mat = np.cumsum(mat, axis=1)
    return mat

################################################################################
# Naive method without prefix sum

# def get_sum_in_area(mat, x1, y1, x2, y2):
#     assert x1 >= 0 and y1 >= 0 and x2 < len(mat) and y2 < len(mat[0]), 'out of bound'
#     sum = 0
#     for i in range(x1, x2):
#         for j in range(y1, y2):
#             sum = sum + mat[i][j]
#     return sum

# def clean_area(mat, x1, y1, x2, y2):
#     assert x1 >= 0 and y1 >= 0 and x2 < len(mat) and y2 < len(mat[0]), 'out of bound'
#     for i in range(x1, x2):
#         for j in range(y1, y2):
#             mat[i][j] = 0
#     return mat

################################################################################
# Find new box edge from the power change rate

# Manually tuned threshold
thres_power_rate_change_v = 0.13
thres_power_rate_change_h = 0.008
# vertical 0.13
# horizontal 0.004

print('thres_power_rate_change_v = {}'.format(thres_power_rate_change_v))
print('thres_power_rate_change_h = {}'.format(thres_power_rate_change_h))

# Smooth the spectrogram with moving average
data_abs_smooth_v = convolve(data_abs, np.ones((5, 50)) / 250, mode='constant')
data_abs_smooth_h = convolve(data_abs, np.ones((10, 100)) / 1000, mode='constant')
# data_abs_smooth_h = convolve(data_abs_smooth_h, np.ones((1, 10)) / 10, mode='constant')
# data_abs_smooth_h = convolve(data_abs_smooth_h, np.ones((1, 50)) / 50, mode='constant')
# data_abs_smooth = convolve(data_abs_smooth, np.ones((1, 50)) / 50, mode='constant')
# data_abs_smooth = laplace(data_abs_smooth, mode='constant')
assert data_abs_smooth_v.shape == data_abs.shape, 'v shape mismatch'
assert data_abs_smooth_h.shape == data_abs.shape, 'h shape mismatch'

# Use dB so that negative edges are more obvious
data_abs_smooth_v = 10 * np.log10(data_abs_smooth_v)
data_abs_smooth_h = 10 * np.log10(data_abs_smooth_h)
power_rate_change_v = np.diff(data_abs_smooth_v, axis=0) / data_abs_smooth_v[:-1]
power_rate_change_h = np.diff(data_abs_smooth_h, axis=1) / data_abs_smooth_h[:, :-1]
# power_rate_change_v = np.diff(data_abs_smooth, axis=0)
# power_rate_change_h = np.diff(data_abs_smooth, axis=1)

# Use absolute value so that threshold can be applied straightforwardly
prc_v_abs = np.abs(power_rate_change_v)
prc_h_abs = np.abs(power_rate_change_h)
# prc_v_abs = power_rate_change_v
# prc_h_abs = power_rate_change_h
prc_v = power_rate_change_v
prc_h = power_rate_change_h

def find_edge(prc_v, prc_h, thres_v, thres_h, x, y):
    edge = {'up': x, 'down': x, 'left': y, 'right': y}
    # vertical edges
    for i in range(x, len(prc_v)):
        if prc_v[i][y] > thres_v:
            edge['up'] = i
            break
    for i in range(x, -1, -1):
        if prc_v[i][y] < -thres_v:
            edge['down'] = i
            break
    # horizontal edges
    for j in range(y, len(prc_h[0])):
        if prc_h[x][j] > thres_h:
            edge['right'] = j
            break
    for j in range(y, -1, -1):
        if prc_h[x][j] < -thres_h:
            edge['left'] = j
            break
    return edge

################################################################################
# Find the bounding boxes by iterating the kernels and performing convolution

# # Noise floor estimator: MAD
# thres_energy = np.median(np.abs(data_abs - np.median(data_abs)))
# # Noise floor estimator: Searchlight
# _k = int(0.2 * len(data_abs.flatten())) # select minimum k samples
# _m = int(0.1 * len(data_abs.flatten())) # discard m samples
# _c = 41212 # empirical correction
# thres_energy = (np.sort(data_abs.flatten())[_m:_k]).mean() * _c

thres_energy = 0.05 # magic number tested on the dataset

print('thres_energy = {}'.format(thres_energy))

# # Plot the flattened power spectrum for thresholding
# plt.figure(figsize=(4, 3))
# plt.plot(data_abs.flatten())
# plt.axhline(y=thres_energy, color='r', linestyle='--')
# plt.title('Flattened Power Spectrum')
# plt.xlabel('Index')
# plt.ylabel('Power')
# plt.tight_layout()
# plt.savefig('flattened_ps.png')
# plt.clf()
# exit(0)

boxes = []
box_centers = []

# Iterate through kernels
for (x, y) in tb_prod_list:
    area = x * y
    for i in range(0, num_symbol):
        for j in range(0, fft_size):
            if i+x < num_symbol and j+y < fft_size:
                # Calculate the energy box
                energy_sum = get_sum_in_area(ps_abs, i, j, i+x, j+y)
                energy_avg = energy_sum / area
                if energy_avg > thres_energy:
                    print('energy_sum = {}'.format(energy_sum))
                    # print('energy_avg = {}'.format(energy_avg))
                    print('kernel size = ({}, {})'.format(x, y))
                    # boxes.append([i, j, i+x, j+y])
                    box_centers.append([i+x//2, j+y//2])
                    # Identify the box edge via power change rate
                    edges = find_edge(prc_v, prc_h,
                                      thres_power_rate_change_v,
                                      thres_power_rate_change_h,
                                      i+x//2, j+y//2)
                    boxes.append([edges['down'], edges['left'], edges['up'],
                                  edges['right']])
                    # Remove found energy box
                    ps_abs = clean_area(abs_values, edges['down'],
                                        edges['left'], edges['up'],
                                        edges['right'])
                    print('box = {}'.format(boxes[-1]))
                # print('running with energy sum = {}'.format(energy_sum))
    # print('kernel size = ({}, {})'.format(x, y))

print('number of boxes = {}'.format(len(boxes)))
# print(boxes)

stored_boxes = np.array(boxes)
stored_centers = np.array(box_centers)
np.save('stored_centers.npy', stored_centers)
np.save('stored_boxes.npy', stored_boxes)

# read_boxes = np.load('stored_boxes.npy')
# read_centers = np.load('stored_centers.npy')
# box_centers = read_centers.tolist()
# boxes = read_boxes.tolist()

# print('number of boxes = {}'.format(len(boxes)))

# for center in box_centers:
#     x, y = center
#     edges = find_edge(prc_v_abs, prc_h_abs,
#                       thres_power_rate_change_v, thres_power_rate_change_h,
#                       x, y)
#     boxes.append([edges['down'], edges['left'], edges['up'], edges['right']])

################################################################################

# Plot in a spectrogram
fig, ax = plt.subplots(figsize=(8, 6))
plt.rc('legend', fontsize=20)    # fontsize of the legend
im = ax.pcolormesh(freq, time, 10 * np.log10(data_abs), shading='flat')
# im = ax.pcolormesh(freq, time, data_abs, shading='flat')
# im = ax.pcolormesh(freq, time, data_abs_smooth_v, shading='flat')
# im = ax.pcolormesh(freq, time[:-1], power_rate_change_v, shading='flat')
# im = ax.pcolormesh(freq[:-1], time, power_rate_change_h, shading='flat')
# im = ax.pcolormesh(freq, time[:-1], prc_v_abs > thres_power_rate_change_v, shading='flat')
# im = ax.pcolormesh(freq, time[:-1], prc_v_abs, shading='flat')
# im = ax.pcolormesh(freq[:-1], time, prc_h > thres_power_rate_change_h, shading='flat')
# im = ax.pcolormesh(freq[:-1], time, prc_h_abs, shading='flat')
ax.set_title("Spectrogram", size=28)
ax.set_xlabel("Subcarrier Index", size=24)
ax.set_ylabel("Symbol Index", size=24)
ax.tick_params(axis='both', labelsize=20)

for box in boxes:
    y1, x1, y2, x2 = box
    ax.add_patch(patches.Rectangle((x1, y1), x2-x1, y2-y1, 
                                   fill=None, edgecolor='r', lw=1))

for center in box_centers:
    y, x = center
    ax.plot(x, y, 'wD', markersize=6)

# plt.colorbar(im, label="Power/Frequency (1/Hz)")
plt.colorbar(im, label="Power/Frequency (dB/Hz)")
# plt.colorbar(im, label="Power change rate > threhold (T/F)")
plt.tight_layout()
plt.savefig(fig_name)

################################################################################

time_end = t.perf_counter()
print('execution time = {}'.format(time_end - time_start))
