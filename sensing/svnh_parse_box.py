################################################################################
# Read FFT-ed I/Q samples, plot the time-frequency diagram from .bin files
# dumped by the sensing feature of Savannah, and parse the detected bounding
# boxes.
#
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv

import helper

file_folder = '../../savannah_isac/files/sensing/'
file_prefix = file_folder + 'sensed_fft_frame'
file_midfix = '_sym'
file_postfix = '_sc0_size1024.bin'
frame_schedule = "PUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"
num_u = frame_schedule.count('U')
num_p = frame_schedule.count('P')
num_g = frame_schedule.count('G')
num_frame = 20
hide_guard = True
num_symbol_per_frame = num_u + num_p if hide_guard else num_u + num_p + num_g
fig_name = 'figs/tf_2d_csv_box.png'

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

################################################################################
# Read boxes

box_path = file_folder + 'test/box_frame0-19_sym0-70_sc0-1023.csv'
boxes = []

with open(box_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    config = next(csvreader)
    items = next(csvreader)
    for row in csvreader:
        box = [int(i) for i in row]
        boxes.append(box)

################################################################################
num_symbol = num_frame * num_symbol_per_frame
time = np.linspace(0, num_symbol, num_symbol + 1)
freq = np.linspace(0, size, size+1)
data = np.array(abs_values)

# figure settings (font size)
font_title = 20
font_label = 15
font_tick = 12
fig_size = (6.4, 4.8) # default value

fig, ax = plt.subplots(figsize=fig_size)
im = ax.pcolormesh(freq, time, 10 * np.log10(data), shading='flat')

for box in boxes:
    x1, y1, x2, y2 = box
    ax.add_patch(patches.Rectangle((x1, y1), x2-x1, y2-y1, 
                                   fill=None, edgecolor='r'))
    print(f"Box: ({x1}, {y1}) to ({x2}, {y2})")
print(f"Total {len(boxes)} boxes.")

ax.set_title("Boxed Time-Freq Plot", size=font_title)
ax.set_xlabel("Subcarrier Index", size=font_label)
ax.set_ylabel("Symbol Index", size=font_label)
ax.tick_params(axis='both', which='major', labelsize=font_tick)
plt.colorbar(im, label="Power/Frequency (dB/Hz)")
plt.tight_layout()
plt.savefig(fig_name)
