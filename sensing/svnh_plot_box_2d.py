################################################################################
# Read bounding box and time-frequency diagram, and plot into multiple figures.
#
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import helper


# file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
file_prefix = '../data/sensing/sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
num_frame = 20
num_symbol_per_frame = 5
fig_name = 'figs/boxed_tf_2d'

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

################################################################################
# Read the bounding boxes and centers

read_boxes = np.load('stored_boxes.npy')
read_centers = np.load('stored_centers.npy')
box_centers = read_centers.tolist()
boxes = read_boxes.tolist()

for i in range(len(boxes)):
    y1, x1, y2, x2 = boxes[i]
    y, x = box_centers[i]
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.rc('legend', fontsize=20)    # fontsize of the legend
    im = ax.pcolormesh(freq, time, 10 * np.log10(data_abs), shading='flat')
    ax.set_title("Time-Freq Plot", size=28)
    ax.set_xlabel("Subcarrier Index", size=24)
    ax.set_ylabel("Symbol Index", size=24)
    ax.tick_params(axis='both', labelsize=20)
    ax.add_patch(patches.Rectangle((x1, y1), x2-x1, y2-y1, 
                                   fill=None, edgecolor='r', lw=1))
    ax.plot(x, y, 'wD', markersize=6)
    plt.colorbar(im, label="Power/Frequency (dB/Hz)")
    plt.tight_layout()
    plt.savefig(fig_name+'_'+str(i)+'.png')
    plt.close()
    print(f"Saved {fig_name}_{i}.png")
