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
# Param settings
################################################################################

chan_type = ['SISO', 'MIMO'] # channel type
pol = ['H', 'V'] # polarization
mod_type = ['16QAM', '64QAM'] # modulation type
# code_rate = ['333', '500', '666'] # n/1000
# snr_ideal = ['5', '10', '13', '15', '20', '25', '30']

chan = chan_type[0]
p = pol[0]
mod = mod_type[1]

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
# plt.rc('figure', titlesize=20)  # fontsize of the figure title
# plt.rcParams.update({'font.size': 16})

FIG_SIZE_W = 5.8
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
input_file = input_filepath + 'result_conste_' + chan + '_' + mod + '_' + p + .mat
# input_file = input_filepath + 'result_conste_1.mat'

data = loadmat(input_file)
evm = data['evm']
real = data['real'][0]
imag = data['imag'][0]

#
# Output
#

# output_format = 'png'
# output_format = 'svg'
output_format = 'pdf'

output_filepath = './fig/'
output_fileprefix = output_filepath + 'conste_' + chan + '_' + mod + '_' + p

################################################################################
# Print EVM info
################################################################################

evm = evm[0][0] # depacakge
evm /= 100
print('EVM = {:.2%}'.format(evm))

################################################################################
# Create Reference Grid
################################################################################

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
    plt.scatter(*r, facecolors='tab:red', edgecolors='black', linewidth=markeredgewidth, zorder=15)

# Plot the constellation
if chan == 'SISO':
    plt.scatter(real, imag,
                facecolors='none',
                edgecolors=markeredgecolor,
                linewidth=markeredgewidth,
                zorder=10)
elif chan == 'MIMO':
    mid = int(len(real)/2) + 1
    plt.scatter(real[:mid], imag[:mid],
                facecolors='none',
                edgecolors='tab:blue',
                linewidth=markeredgewidth,
                zorder=10)
    
    plt.scatter(real[mid:], imag[mid:],
                facecolors='none',
                edgecolors='tab:orange',
                linewidth=markeredgewidth,
                zorder=10)
else:
    print('Must specify channel type! Available options: \'SISO\', \'MIMO\'')

l_bound = -1.5
h_bound = 1.5
step = 0.5

plt.xlim(l_bound, h_bound)
plt.ylim(l_bound, h_bound)
plt.xticks(np.arange(l_bound, h_bound + 0.01, step))
plt.yticks(np.arange(l_bound, h_bound + 0.01, step))
plt.title('EVM = {:.2%}'.format(evm), fontsize=28)
plt.xlabel('I')
plt.ylabel('Q')
plt.grid()
plt.savefig(output_fileprefix + '.' + output_format,
            format=output_format,
            bbox_inches='tight')
plt.clf()