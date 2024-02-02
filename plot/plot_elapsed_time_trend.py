"""
This script plot the elapsed time directly.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

sys.path.append('..')
from python import read_elapsed_time

################################################################################
# Functions for plot attributes
################################################################################

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

edgecolor='black'

################################################################################
# I/O format
################################################################################

#
# Input
#
parser = OptionParser()
parser.add_option("-f", "--file", type="string", dest="file_name", help="File name as input", default="")
(options, args) = parser.parse_args()
log_path = options.file_name # e.g., /home/ct297/workspace/agora_single-core-sim/log/2023-07-19_16-35-36.log
log_name = log_path.split("/")[-1] # e.g. 2023-07-19_16-35-36.log
log_time = log_name.split(".")[0] # e.g. 2023-07-19_16-35-36

# Handle input error
if not log_path:
    parser.error('Must specify log path with -f or --file, for more options, use -h')

print('Reading from log: {}'.format(log_time))

elapsed_time_ls = read_elapsed_time.elapsed_time(log_path)
elapsed_time_np = np.array(elapsed_time_ls)

#
# Output
#

output_format = 'png'
# output_format = 'svg'
# output_format = 'pdf'

output_filepath = '../fig/'

################################################################################
# Plot 
################################################################################

fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.plot(elapsed_time_np, 'b.', markersize=1, label='Elapsed time')

# plt.ylim(0, 5e3)
# plt.xticks(np.arange(l_bound, h_bound, step=0.1))
title = 'Elapsed time for each frame'
plt.title(title, fontsize=titlesize)
plt.xlabel('Frame index')
plt.ylabel('elapsed time (ms)')
plt.grid()
plt.savefig(output_filepath + 'elapsed_time_trend_' + log_time + '.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()

################################################################################
# Print statistics
################################################################################

min_elapsed_time = min(elapsed_time_np)
max_elapsed_time = max(elapsed_time_np)
avg_elapsed_time = np.mean(elapsed_time_np)
five9_elapsed_time = np.percentile(elapsed_time_np, 99.999)

print(' . num of points = {}'.format(len(elapsed_time_ls)))
print(' . min elapsed time = {:.2f} ms'.format(min_elapsed_time))
print(' . max elapsed time = {:.2f} ms'.format(max_elapsed_time))
print(' . avg elapsed time = {:.2f} ms'.format(avg_elapsed_time))
print(' . 99.999% elapsed time = {:.2f} ms'.format(five9_elapsed_time))
