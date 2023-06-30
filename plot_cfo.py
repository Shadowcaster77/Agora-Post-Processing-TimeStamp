################################################################################
# Plot CFO distribution as histogram. Output seperate figures for uplink and 
# downlink. Overall output two plots.
# author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.io import loadmat
import numpy as np

################################################################################
# Functions for plot attributes
################################################################################

def kilos(x, pos):
    'The two args are the value and tick position'
    return '%1.1f' % (x*1e-3)

################################################################################
# Font settings: tick size, linewidth, marker size
################################################################################

# Font sizes

# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=24)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=16)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# plt.rcParams.update({'font.size': 16})

FIG_SIZE_W = 6
FIG_SIZE_H = 4.5

edgecolor='black'

plt.figure(figsize=(FIG_SIZE_W, FIG_SIZE_H))

################################################################################
# I/O format
################################################################################

#
# Input
#

ul = True
# ul = False

input_filepath = './data/'
if ul:
    input_filename = 'CFO_TX2_RX3_trial1.mat' # uplink
else:
    input_filename = 'CFO_TX3_RX2_trial2.mat' # downlink
input_file = input_filepath + input_filename

data = loadmat(input_file)
cfo = data['cfoList'][0] # data is double-encapsulated

#
# Output
#

# output_format = 'png'
# output_format = 'svg'
output_format = 'pdf'

output_filepath = './fig/'
output_fileprefix = output_filepath

################################################################################
# Print CFO stats
################################################################################

avg_cfo = np.average(cfo)
print('Average CFO = {} Hz'.format(avg_cfo))

################################################################################
# Plot CFO
################################################################################

fig, ax = plt.subplots()
formatter = FuncFormatter(kilos)
ax.xaxis.set_major_formatter(formatter)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

binwidth = 500
l_bound = 90000 if ul else -100000
h_bound = 100000 if ul else -90000
n, bins, _ = plt.hist(cfo, bins=range(l_bound, h_bound, binwidth), density=True,
                      color='white',
                      edgecolor=edgecolor,
                      linewidth=2,
                      zorder=10)

# print (np.sum(n*np.diff(bins))) # verify the integral is 1

# plt.xlim(10, 35)
plt.ylim(0, 1e-3)
# plt.yticks(np.arange(0, 11, 5))
plt.xticks(np.arange(l_bound, h_bound+1, step=2500))
# plt.title(input_filename)
plt.xlabel('CFO (kHz)')
plt.ylabel('Probability Density')
plt.grid()
plt.savefig(output_fileprefix + 'CFO.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()