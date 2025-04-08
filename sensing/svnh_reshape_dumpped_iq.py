################################################################################
# Read FFT-ed I/Q samples in frequency-division manner and generate new files
# in time-division manner.
#
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import struct

import helper

# file_prefix = '../../savannah_isac/files/sensing/test/sensed_fft_frame'
file_prefix = '../../savannah_isac/files/sensing/sensed_fft_frame'
# file_midfix = '_sym'
# file_postfix = '_sc0_size1024.bin'
# frame_schedule = "PUUUUUUUUUUUUUUUUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"
frame_schedule = "PUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU"
num_frame = 200
sensing_unit_in_frame = 40
sensing_block_size = 32
fft_size = 1024

num_u = frame_schedule.count('U')
num_p = frame_schedule.count('P')
num_g = frame_schedule.count('G')
hide_guard = True
num_symbol_per_frame = num_u + num_p if hide_guard else num_u + num_p + num_g

'''
input
filename format: sensing_fft_
                 frame<frame_start>-<frame_end>_
                 sym0-<symbol_count>_
                 sc<subcarrier_id>_
                 size<sensing_block_size>.bin
output
filename format: sensing_fft_
                 frame<frame_index>_
                 sym<symbol_id>_
                 sc<subcarrier_id>_
                 size<fft_size>.bin
'''


size = 0
abs_values = []

data = np.empty((num_frame, num_symbol_per_frame, fft_size), dtype=np.complex64)
print('data shape:', data.shape)

################################################################################
#
#  |              Frame               |              Frame               |  ...
#  |   Symbol  |  Symbol  |   Symbol  |   Symbol  |   Symbol  |  Symbol  |  ...
#  |    sc0    |
#  |    sc1    |
#  ----------------------------------------------------------- file 0
#  |    sc2    |
#  |    sc3    |
#  ----------------------------------------------------------- file 1
#  |    sc4    |
#  |    ...    |
#  ----------------------------------------------------------- file n
#
#  Each file contains a subband of IQ (a subcarrier range). The entire file
#  contains that specific subband of IQ in a frame range (ping-pong buffer size)
#  sequentially.
#
################################################################################

# read file in subcarrier dimension (frequency division)
# frame range: ping-pong buffer will lose the last unit
for frame_index in range(0, num_frame - sensing_unit_in_frame, sensing_unit_in_frame):
    for sc_id in range(0, fft_size, sensing_block_size):
        file_name = file_prefix + str(frame_index) + '-'
        file_name += str(frame_index + sensing_unit_in_frame - 1)
        file_name += '_sym0-' + str(num_symbol_per_frame)
        file_name += '_sc' + str(sc_id)
        file_name += '_size' + str(sensing_block_size) + '.bin'
        print('reading file:', file_name)

        data_raw = helper.read_complex_samples(file_name)

        # translate to intermediate data structure
        for frame_ in range(frame_index, frame_index + sensing_unit_in_frame):
            for symbol_ in range(0, num_symbol_per_frame):
                offset_frame = frame_ - frame_index
                offset_symbol = offset_frame * num_symbol_per_frame + symbol_
                offset_sc = offset_symbol * sensing_block_size
                data[frame_][symbol_][sc_id:sc_id + sensing_block_size] = \
                    data_raw[offset_sc:offset_sc + sensing_block_size]

################################################################################
#
#  |              Frame               |              Frame               |  ...
#  |   Symbol  |  Symbol  |   Symbol  |   Symbol  |   Symbol  |  Symbol  |  ...
#  |    sc0    |    sc0   |                                              |
#  |    sc1    |    sc1   |                                              |
#  |    sc2    |    sc2   |                                              |
#  |    sc3    |    sc3   |                                              |
#  |    sc4    |    sc4   |                                              |
#  |    ...    |    ...   |                                              |
#            file 0     file 1                ...                      file n
#
#  Each file contians a symbol.
#
################################################################################

# write file in frame-symbol dimension (time division)
for frame_index in range(0, num_frame - sensing_unit_in_frame):
    for symbol_index in range(0, num_symbol_per_frame):
        file_name = file_prefix + str(frame_index)
        file_name += '_sym' + str(symbol_index)
        file_name += '_sc0' + '_size' + str(fft_size) + '.bin'
        print('writing file:', file_name)
        with open(file_name, 'wb') as f:
            for i in range(fft_size):
                f.write(struct.pack('ff',
                                    data[frame_index][symbol_index][i].real,
                                    data[frame_index][symbol_index][i].imag))
