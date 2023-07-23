"""
This script plot the cpu time distributions.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
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
log_path = '../log/'
log_name = '2023-07-19_16-35-36.log'
print('Reading from log: {}...'.format(log_name))

cpu_time_ls, _, _, _, _, _ = read_cpu_time.proc_time(log_path+log_name)
# cpu_time_ls = read_cpu_time.proc_time_trimmed(log_path+log_name)
cpu_time_np = np.array(cpu_time_ls)

#
# Output
#

# output_format = 'png'
# output_format = 'svg'
output_format = 'pdf'

output_filepath = '../fig/'

################################################################################
# Plot 
################################################################################

fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

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
plt.ylim(0, 6e3)
# plt.yticks(np.arange(0, 11, 5))
# plt.xticks(np.arange(l_bound, h_bound+1, step=2500))
title = 'CPU time distribution'
plt.title(title, fontsize=titlesize)
plt.xlabel('cpu time (ms)')
plt.ylabel('Num of frames')
plt.grid()
plt.savefig(output_filepath + 'cpu_time_dist.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()