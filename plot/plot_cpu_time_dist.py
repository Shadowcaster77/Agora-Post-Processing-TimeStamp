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

print('Reading from log: {}'.format(log_name))

cpu_time_ls = read_cpu_time.proc_time(log_path)[0]
# cpu_time_ls = read_cpu_time.proc_time_trimmed(log_path+log_time)
cpu_time_np = np.array(cpu_time_ls)

print('Read the log for cpu time... Done')

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

# binwidth = 0.01
# l_bound = 1.2
# h_bound = 1.71
binwidth = 0.01
l_bound = min(cpu_time_np)
h_bound = max(cpu_time_np)
n, bins, _ = plt.hist(cpu_time_np, bins=np.arange(l_bound, h_bound, binwidth),
                    #   density=True,
                    #   color='white',
                      edgecolor=edgecolor,
                      linewidth=2,
                      zorder=10)

# print (np.sum(n*np.diff(bins))) # verify the integral is 1

plt.xlim(l_bound, h_bound)
plt.ylim(0, 5e3)
# plt.yticks(np.arange(0, 11, 5))
# plt.xticks(np.arange(l_bound, h_bound, step=0.1))
title = 'CPU time distribution'
plt.title(title, fontsize=titlesize)
plt.xlabel('cpu time (ms)')
plt.ylabel('Num of frames')
plt.grid()
plt.savefig(output_filepath + 'cpu_time_dist_' + log_time + '.' +
            output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()

################################################################################
# Print statistics
################################################################################

min_cpu_time = min(cpu_time_np)
max_cpu_time = max(cpu_time_np)
avg_cpu_time = np.mean(cpu_time_np)
five9_cpu_time = read_cpu_time.five9_proc_time(log_path)[0]

print(' . num of points = {}'.format(len(cpu_time_ls)))
print(' . min cpu time = {:.2f} ms'.format(min_cpu_time))
print(' . max cpu time = {:.2f} ms'.format(max_cpu_time))
print(' . avg cpu time = {:.2f} ms'.format(avg_cpu_time))
print(' . 99.999%% cpu time = {:.2f} ms'.format(five9_cpu_time))
