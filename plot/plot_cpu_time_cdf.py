"""
This script plot the cpu time distributions.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

sys.path.append('..')
from python import read_cpu_time

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

cpu_time_ls = read_cpu_time.proc_time(log_path)[0]
# cpu_time_ls = read_cpu_time.proc_time_trimmed(log_path)
cpu_time_np = np.array(cpu_time_ls)

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

min_cpu_time = min(cpu_time_np)
max_cpu_time = max(cpu_time_np)
avg_cpu_time = np.mean(cpu_time_np)
five9_cpu_time = read_cpu_time.five9_proc_time(log_path)[0]

################################################################################
# Plot
################################################################################

fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

num_samples = len(cpu_time_ls)
cpu_time_sorted = np.sort(cpu_time_np)
cpu_time_prob = np.arange(1, num_samples + 1) / num_samples
plt.plot(cpu_time_sorted, cpu_time_prob,
         marker='o',
         linewidth=0)

# Plot 3TTI deadline & mark statistics
two9_cpu_time = np.percentile(cpu_time_np, 99)
plt.axvline(x = 0.375, color = 'r', linestyle='--', label = f'3TTI (0.375 ms)')
plt.axvline(x = five9_cpu_time, color = 'g', linestyle='--', label = f'99.999% ({five9_cpu_time:.3f} ms)')
plt.axvline(x = two9_cpu_time, color = 'b', linestyle='--', label = f'99% ({two9_cpu_time:.3f} ms)')

title = 'CPU Time CDF'
plt.xlim(min(cpu_time_sorted), max(cpu_time_sorted))
plt.title(title, fontsize=titlesize)
plt.xlabel('cpu time (ms)')
plt.ylabel('Num of frames')
plt.grid()
plt.legend()
plt.savefig(output_filepath + 'cpu_time_cdf_' + log_time + '.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()

################################################################################
# Print statistics
################################################################################

print(' . num of points = {}'.format(len(cpu_time_ls)))
print(' . min cpu time = {:.2f} ms'.format(min_cpu_time))
print(' . max cpu time = {:.2f} ms'.format(max_cpu_time))
print(' . avg cpu time = {:.2f} ms'.format(avg_cpu_time))
print(' . 99.999% cpu time = {:.2f} ms'.format(five9_cpu_time))
