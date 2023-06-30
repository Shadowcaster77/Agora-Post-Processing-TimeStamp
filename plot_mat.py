import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from brokenaxes import brokenaxes
from scipy.io import loadmat
import numpy as np

################################################################################
# Functions for plot attributes
################################################################################

def get_marker(mod):
    # marker = ['o', '^', 'x']
    marker = 'x'
    # if pol == 'H':
    #     marker = 'o'
    # if pol == 'V':
    #     marker = '^'

    if mod == '16QAM':
        marker = 'o'
    if mod == '64QAM':
        marker = '^'
    return marker

def get_color(mod):
    ''' color = 'tab:blue'
              'tab:orange'
              'tab:green'
              'tab:red'
              'tab:purple'
              'tab:brown'
              'tab:pink'
              'tab:gray'
              'tab:olive'
              'tab:cyan'''
    # if code_rate == '333':
    #     color = 'tab:blue'
    # if code_rate == '500':
    #     color = 'tab:green'
    # if code_rate == '666':
    #     color = 'tab:red'

    color = 'tab:green'
    if mod == '16QAM':
        color = 'tab:blue'
    if mod == '64QAM':
        color = 'tab:orange'
    return color

def get_linestyle(pol):
    ls = ':'
    if pol == 'H':
        ls = '-'
    if pol == 'V':
        ls = '--'
    return ls

################################################################################
# Font settings
################################################################################

# Font sizes
SMALL_SIZE = 15
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=17)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=16)    # fontsize of the tick labels
plt.rc('ytick', labelsize=16)    # fontsize of the tick labels
plt.rc('legend', fontsize=17)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# plt.rcParams.update({'font.size': 16})

################################################################################
# I/O format
################################################################################

#
# Input
#

# chan_type = 'MIMO'
chan_type = 'SISO'

input_filepath = './data/'
input_fileprefix = input_filepath + 'result_' + chan_type

data_v = loadmat(input_fileprefix + '_V.mat')
data_h = loadmat(input_fileprefix + '_H.mat')

snr_v = data_v['snrList']
evm_v = data_v['evmList']
ber_v = data_v['berList']
snr_h = data_h['snrList']
evm_h = data_h['evmList']
ber_h = data_h['berList']

#
# Output
#

# output_format = 'png'
# output_format = 'svg'
output_format = 'pdf'

output_filepath = './fig/'
output_fileprefix = output_filepath + chan_type

################################################################################
# Param settings
################################################################################

mod_t = ['16QAM', '64QAM'] # modulation type
pol = ['H', 'V'] # polarization
code_rate = ['333', '500', '666'] # n/1000
snr_ideal = ['5', '10', '13', '15', '20', '25', '30']
mcs = [3, 6]

num_mcs = len(snr_v)
num_snr = len(snr_v[0])

################################################################################
# Plot EVM
################################################################################

for mcs_idx in range(num_mcs):
    for p in pol:

        mod = mod_t[0] if mcs_idx < 3 else mod_t[1]
        cr = code_rate[mcs_idx % 3]
        marker = get_marker(mod) # marker: o, x, s, ^
        color = get_color(mod) # color: 
        line = get_linestyle(p) # line: -, --, :
        # label = 'MCS' + str(mcs_idx+1) + ': ' + mod + '-' + pol[0] + '-0.' + cr
        label = 'MCS-' + str(mcs_idx+1) + '-' + p # + ': ' + mod + '-0.' + cr

        snr = snr_v if p == 'V' else snr_h
        evm = evm_v if p == 'V' else evm_h

        if mcs_idx+1 in mcs:
            plt.plot(snr[mcs_idx], evm[mcs_idx], linestyle=line, marker=marker, label=label, color=color)

plt.xlim(10, 35)
plt.ylim(0, 50)
plt.xlabel('SNR (dB)')
plt.ylabel('EVM (%)')
# plt.title('EVM vs SNR')
plt.legend()
plt.grid()
plt.savefig(output_fileprefix + '_EVM.' + output_format, format=output_format, bbox_inches='tight')
plt.clf()

################################################################################
# Plot BER
################################################################################

for mcs_idx in range(num_mcs):
    for p in pol:

        mod = mod_t[0] if mcs_idx < 3 else mod_t[1]
        cr = code_rate[mcs_idx % 3]
        marker = get_marker(mod) # marker: o, x, s, ^
        color = get_color(mod) # color: 
        line = get_linestyle(p) # line: -, --, :
        # label = 'MCS' + str(mcs_idx+1) + ': ' + mod + '-' + pol[0] + '-0.' + cr
        label = 'MCS-' + str(mcs_idx+1) + '-' + p # + ': ' + mod + '-0.' + cr

        snr = snr_v if p == 'V' else snr_h
        ber = ber_v if p == 'V' else ber_h

        if mcs_idx+1 in mcs:
            plt.plot(snr[mcs_idx], ber[mcs_idx], linestyle=line, marker=marker, label=label, color=color)

plt.yscale('symlog', linthresh=1e-4)
plt.xlim(0, 35)
plt.ylim(top=1)
# plt.gca().yaxis.set_major_locator(plt.LogLocator(base=10, numticks=10)) # major grid (int)
plt.gca().yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=100)) # minor grid
plt.xlabel('SNR (dB)')
plt.ylabel('BER')
# plt.title('BER vs SNR')
plt.legend(loc='lower left')
plt.grid(True, which='both', ls='-')
plt.savefig(output_fileprefix + '_BER.' + output_format, format=output_format, bbox_inches='tight')
plt.clf()
