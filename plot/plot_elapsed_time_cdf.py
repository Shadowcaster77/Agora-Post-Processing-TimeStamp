"""
This script plot the elapsed time distributions.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

sys.path.append('..')
from python import read_elapsed_time

DEADLINE_3TTI=0.375

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
# Get statistics
################################################################################

num_samples = len(elapsed_time_ls)
min_elapsed_time = min(elapsed_time_np)
max_elapsed_time = max(elapsed_time_np)
avg_elapsed_time = np.mean(elapsed_time_np)
five9_elapsed_time = np.percentile(elapsed_time_np, 99.999)
pct_meet_deadline = np.sum(elapsed_time_np <= DEADLINE_3TTI) / num_samples * 100

################################################################################
# Plot 
################################################################################

fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

elapsed_time_sorted = np.sort(elapsed_time_np)
elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
plt.plot(elapsed_time_sorted, elapsed_time_prob,
         marker='o',
         linewidth=0)

# print (np.sum(n*np.diff(bins))) # verify the integral is 1

# Plot 3TTI deadline & mark statistics
two9_elapsed_time = np.percentile(elapsed_time_np, 99)
plt.axvline(x = 0.375, color = 'r', linestyle='--', label = f'3TTI (0.375 ms)')
plt.axvline(x = five9_elapsed_time, color = 'g', linestyle='--', label = f'99.999% ({five9_elapsed_time:.3f} ms)')
plt.axvline(x = two9_elapsed_time, color = 'b', linestyle='--', label = f'99% ({two9_elapsed_time:.3f} ms)')
# Adding a caption
plt.figtext(0.5, 0.5, f'{pct_meet_deadline:.2f}% meet 3TTI', fontsize=10, ha='center')

# plt.xlim(min(elapsed_time_np), 0.4)
plt.xlim(min(elapsed_time_np), max(elapsed_time_np))
title = 'Elapsed Time CDF'
plt.title(title, fontsize=titlesize)
plt.xlabel('elapsed time (ms)')
plt.ylabel('Num of frames')
plt.grid()
plt.legend()
plt.savefig(
    output_filepath + 'elapsed_time_cdf_' + log_time + '.' + output_format,
    format=output_format,
    bbox_inches='tight')
plt.clf()


################################################################################
# Print statistics
################################################################################

print(' . num of points = {}'.format(len(elapsed_time_ls)))
print(' . min elapsed time = {:.2f} ms'.format(min_elapsed_time))
print(' . max elapsed time = {:.2f} ms'.format(max_elapsed_time))
print(' . avg elapsed time = {:.2f} ms'.format(avg_elapsed_time))
print(' . 99.999% elapsed time = {:.2f} ms'.format(five9_elapsed_time))
print(' . {:.2f}% of the frames meet 3TTI deadline of {:.3f} ms'.format(
    pct_meet_deadline, DEADLINE_3TTI))
