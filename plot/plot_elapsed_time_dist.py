"""
This script plot the elapsed time distributions.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
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
log_path = '../log/'
log_name = '2023-07-19_16-35-36.log'
print('Reading from log: {}...'.format(log_name))

elapsed_time_ls = read_elapsed_time.elapsed_time(log_path+log_name)
elapsed_time_np = np.array(elapsed_time_ls)

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

binwidth = 1
l_bound = 0
h_bound = 60
n, bins, _ = plt.hist(elapsed_time_np, bins=range(l_bound, h_bound, binwidth),
                    #   density=True,
                    #   color='white',
                      edgecolor=edgecolor,
                      linewidth=2,
                      zorder=10)

# print (np.sum(n*np.diff(bins))) # verify the integral is 1

plt.xlim(l_bound, h_bound+1)
plt.ylim(0, 5e3)
# plt.yticks(np.arange(0, 11, 5))
# plt.xticks(np.arange(l_bound, h_bound+1, step=2500))
title = 'Elapsed time distribution'
plt.title(title, fontsize=titlesize)
plt.xlabel('elapsed time (ms)')
plt.ylabel('Num of frames')
plt.grid()
plt.savefig(output_filepath + 'elapsed_time_dist.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()