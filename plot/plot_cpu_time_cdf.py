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
# log_time = '2023-07-19_16-35-36' # deferred log
# log_time = '2023-07-25_18-21-23' # normal log
log_time = '2023-07-27_13-33-53' # origin log
log_name = log_time + '.log'
print('Reading from log: {}...'.format(log_name))

cpu_time_ls = read_cpu_time.proc_time(log_path+log_name)[0]
# cpu_time_ls = read_cpu_time.proc_time_trimmed(log_path+log_name)
cpu_time_np = np.array(cpu_time_ls)

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

num_samples = len(cpu_time_ls)
cpu_time_sorted = np.sort(cpu_time_np)
cpu_time_prob = np.arange(1, num_samples + 1) / num_samples
plt.plot(cpu_time_sorted, cpu_time_prob,
         marker='o',
         linewidth=0)

title = 'CPU Time CDF'
plt.xlim(1, 2.5)
plt.title(title, fontsize=titlesize)
plt.xlabel('cpu time (ms)')
plt.ylabel('Num of frames')
plt.grid()
plt.savefig(output_filepath + 'cpu_time_cdf_' + log_time + '.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()

################################################################################
# Print statistics
################################################################################

min_cpu_time = min(cpu_time_np)
max_cpu_time = max(cpu_time_np)
avg_cpu_time = np.mean(cpu_time_np)
five9_cpu_time = read_cpu_time.five9_proc_time(log_path+log_name)[0]

print(' . num of points = {}'.format(len(cpu_time_ls)))
print(' . min cpu time = {:.2f}'.format(min_cpu_time))
print(' . max cpu time = {:.2f}'.format(max_cpu_time))
print(' . avg cpu time = {:.2f}'.format(avg_cpu_time))
print(' . 99.999% elapsed time = {:.2f}'.format(five9_cpu_time))