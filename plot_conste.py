################################################################################
# Plot constellation map.
# author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.io import loadmat
import numpy as np

################################################################################
# Functions for plot attributes
################################################################################


################################################################################
# Font settings: tick size, linewidth, marker size
################################################################################

# Font sizes

# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=24)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=20)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# plt.rcParams.update({'font.size': 16})

FIG_SIZE_W = 6
FIG_SIZE_H = 6

markeredgecolor='tab:blue'
markeredgewidth=2

plt.figure(figsize=(FIG_SIZE_W, FIG_SIZE_H))
plt.rc('lines', linewidth=5)
plt.rc('lines', markersize=10)

################################################################################
# I/O format
################################################################################

#
# Input
#

input_filepath = './data/'
input_file = input_filepath + 'result_conste_11.mat'

data = loadmat(input_file)
evm = data['evm']
real = data['real']
imag = data['imag']

#
# Output
#

# output_format = 'png'
# output_format = 'svg'
output_format = 'pdf'

output_filepath = './fig/'
output_fileprefix = output_filepath

################################################################################
# Print EVM info
################################################################################

evm = evm[0][0] # depacakge
evm /= 100
print('EVM = {:.2%}'.format(evm))

################################################################################
# Create Reference Grid
################################################################################

mod_type = ['16QAM', '64QAM']
mod = mod_type[0]

ref_symbols = {
    '16QAM': {
        'I': np.array([-3, -1, 1, 3]) / np.sqrt(10),
        'Q': np.array([-3, -1, 1, 3]) / np.sqrt(10)
    },
    '64QAM': {
        'I': np.array([-7, -5, -3, -1, 1, 3, 5, 7]) / np.sqrt(42),
        'Q': np.array([-7, -5, -3, -1, 1, 3, 5, 7]) / np.sqrt(42)
    }
}

ref = []
for i in ref_symbols[mod]['I']:
    for q in ref_symbols[mod]['Q']:
        ref.append((i, q))

################################################################################
# Plot Constellation
################################################################################

# Plot the reference
for r in ref:
    plt.scatter(*r, facecolors='red', zorder=15)

# Plot the constellation
plt.scatter(real, imag,
            facecolors='none',
            edgecolors=markeredgecolor,
            linewidth=markeredgewidth,
            zorder=10)
            # marker=marker,
            # label=label,
            # color=color)

l_bound = -1.5
h_bound = 1.5
step = 0.5

plt.xlim(l_bound, h_bound)
plt.ylim(l_bound, h_bound)
plt.xticks(np.arange(l_bound, h_bound + 0.01, step))
plt.yticks(np.arange(l_bound, h_bound + 0.01, step))
# # plt.title(input_filename)
plt.xlabel('I')
plt.ylabel('Q')
plt.grid()
plt.savefig(output_fileprefix + 'conste.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()