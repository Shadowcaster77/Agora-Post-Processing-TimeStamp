"""
This script plot the cpu time for each pipeline stages.

Author: cstandy
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append('..')
from python import read_cpu_time

################################################################################
# Font settings: tick size, linewidth, marker size
################################################################################

# Enable comic style
# plt.xkcd()

# Font sizes

titlesize = 28
# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=28)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=24)    # fontsize of the tick labels
plt.rc('ytick', labelsize=24)    # fontsize of the tick labels
# plt.rc('legend', fontsize=16)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# plt.rcParams.update({'font.size': 16})

FIG_SIZE_W = 6
FIG_SIZE_H = 6

################################################################################
# Param settings
################################################################################

mu = [0, 1, 2, 3]
code_rate = '0p925'
modulation = '64QAM'
num_uplink = 4
num_workers = 1

################################################################################
# I/O format
################################################################################

o_filename = '../fig/cpu_time_bar_u{}_cr{}_{}_w{}.png'.format(num_uplink, code_rate, modulation, num_workers)

################################################################################
# Read data
################################################################################

frame_time = []
fft_time = []
csi_time = []
bw_time = []
demul_time = []
decode_time = []

for i in mu:
    filename = '../log/four-config_mu_worker/u{}_cr{}_{}_mu{}_w{}.log'.format(num_uplink, code_rate, modulation, i, num_workers)
    frame, fft, csi, bw, demul, decode = read_cpu_time.avg_proc_time(filename=filename)
    frame_time.append(frame)
    fft_time.append(fft)
    csi_time.append(csi)
    bw_time.append(bw)
    demul_time.append(demul)
    decode_time.append(decode)

################################################################################
# Plot
################################################################################

bar_width = 0.5
edgecolor = "black"
linewidth = 1

plt.bar(mu, fft_time, label='FFT', width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
bottom = fft_time
plt.bar(mu, csi_time, bottom=bottom, label='CSI', width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
bottom = [x + y for x, y in zip(bottom, csi_time)]
plt.bar(mu, bw_time, bottom=bottom, label='BW', width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
bottom = [x + y for x, y in zip(bottom, bw_time)]
plt.bar(mu, demul_time, bottom=bottom, label='Demul', width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
bottom = [x + y for x, y in zip(bottom, demul_time)]
plt.bar(mu, decode_time, bottom=bottom, label='Decode', width=bar_width, edgecolor=edgecolor, linewidth=linewidth)

plt.ylim(0, 3)
plt.xlabel('Numerologies')
plt.ylabel('CPU Time (ms)')
plt.title('u{}, cr{}, {}, w{}'.format(num_uplink, code_rate, modulation, num_workers), fontsize=titlesize)
plt.legend()
plt.savefig(o_filename, format='png', bbox_inches='tight')
