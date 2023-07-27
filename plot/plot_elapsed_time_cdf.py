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
# log_time = '2023-07-19_16-35-36' # deferred log
# log_time = '2023-07-25_18-21-23' # normal log
log_time = '2023-07-27_13-33-53' # origin log
log_name = log_time + '.log'
print('Reading from log: {}...'.format(log_name))

elapsed_time_ls = read_elapsed_time.elapsed_time(log_path+log_name)
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

num_samples = len(elapsed_time_ls)
elapsed_time_sorted = np.sort(elapsed_time_np)
elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
plt.plot(elapsed_time_sorted, elapsed_time_prob,
         marker='o',
         linewidth=0)

# print (np.sum(n*np.diff(bins))) # verify the integral is 1

plt.xlim(1, 2.5)
title = 'Elapsed Time CDF'
plt.title(title, fontsize=titlesize)
plt.xlabel('elapsed time (ms)')
plt.ylabel('Num of frames')
plt.grid()
plt.savefig(output_filepath + 'elapsed_time_cdf_' + log_time + '.' + output_format,
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
print(' . min elapsed time = {:.2f}'.format(min_elapsed_time))
print(' . max elapsed time = {:.2f}'.format(max_elapsed_time))
print(' . avg elapsed time = {:.2f}'.format(avg_elapsed_time))
print(' . 99.999% elapsed time = {:.2f}'.format(five9_elapsed_time))
