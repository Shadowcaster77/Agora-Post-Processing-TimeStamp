################################################################################
# Plot BER and EVM over SNR, respectively. Output seperate figures for
# 16QAM/64QAM. Overall output four plots.
# author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
from scipy.io import loadmat
import numpy as np

################################################################################
# Functions for plot attributes
################################################################################

def get_marker(chan):
    # marker = ['o', '^', 'x']
    marker = 'x'
    # if pol == 'H':
    #     marker = 'o'
    # if pol == 'V':
    #     marker = '^'

    if chan == 'SISO':
        marker = 'o'
    if chan == 'MIMO':
        marker = '^'
    return marker

def get_color(pol):
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
    color = 'tab:green'
    if pol == 'H':
        color = 'tab:blue'
    if pol == 'V':
        color = 'tab:orange'
    return color

def get_linestyle(pol):
    ls = ':'
    if pol == 'H':
        ls = '-'
    if pol == 'V':
        ls = '--'
    return ls

def get_evm_req(mod):
    res = 0
    if mod == '16QAM':
        res = 12.5
    if mod == '64QAM':
        res = 8
    return res

################################################################################
# Font settings: tick size, linewidth, marker size
################################################################################

# Font sizes

titlesize=28
# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=24)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=20)    # legend fontsize
# plt.rcParams.update({'font.size': 16})

FIG_SIZE_W = 6
FIG_SIZE_H = 6

markeredgecolor='black'
markeredgewidth=2

plt.figure(figsize=(FIG_SIZE_W, FIG_SIZE_H))
plt.rc('lines', linewidth=3)
plt.rc('lines', markersize=15)
# plt.rc('lines', markeredgecolor=markeredgecolor)
# plt.rc('lines', markeredgewidth=markeredgewidth)

################################################################################
# Param settings
################################################################################

chan_type = ['SISO', 'MIMO'] # channel type
pol = ['H', 'V'] # polarization
mod_type = ['16QAM', '64QAM'] # modulation type
# code_rate = ['333', '500', '666'] # n/1000
# snr_ideal = ['5', '10', '13', '15', '20', '25', '30']

###
# MCS | modulation | code_rate 
#  1      16qam         1/3
#  2      16qam         1/2
#  3      16qam         2/3
#  4      64qam         1/3
#  5      64qam         1/2
#  6      64qam         2/3
mcs = [3, 6] # Target MCS to plot

################################################################################
# I/O filename/format
################################################################################

#
# Input
#

input_filepath = './data/'
input_fileprefix = input_filepath + 'result_'

#
# Output
#

# output_format = 'png'
# output_format = 'svg'
output_format = 'pdf'

output_filepath = './fig/'

################################################################################
# Read data & pre-processing
################################################################################

#
# Read data
#

# Input files:
#     result_MIMO_H.mat
#     result_MIMO_V.mat
#     result_SISO_H.mat
#     result_SISO_V.mat
#     dimension - [chan_type][polarization]

# In each file, format:
#    dict:  snrList, evmList, berList
# In each list:
#    dimension - [mcs][snr_ideal], snr_ideal is the x axis

# read data as dict: [chan_type][pol]
data_in = {}
for chan in chan_type:
    data_in[chan] = {}
    for p in pol:
        data_temp = loadmat('{0}result_{1}_{2}.mat'.format(input_filepath, chan, p))
        data_in[chan][p] = {}
        data_in[chan][p]['snr'] = data_temp['snrList']
        data_in[chan][p]['evm'] = data_temp['evmList']
        data_in[chan][p]['ber'] = data_temp['berList']

#
# Pre-processing
#

# retreive mcs dimension
snr_temp = data_in[chan_type[0]][pol[0]]['snr']
num_mcs = len(snr_temp)
# num_snr = len(snr_temp[0])

# re-format data into diemension [mod_type][chan_type][pol]
# 1. init data dict
data = {}
for mod in mod_type:
    data[mod] = {}
    for chan in chan_type:
        data[mod][chan] = {}
        for p in pol:
            data[mod][chan][p] = {}

# 2. read based on mcs
for chan in chan_type:
    for p in pol:
        for mcs_idx in range(num_mcs):
            # accumulate evm
            # mcs 1-3: 16QAM, mcs 4-6: 64QAM
            if mcs_idx+1 in mcs:
                mod = mod_type[0] if mcs_idx < 3 else mod_type[1]
                data[mod][chan][p]['snr'] = data_in[chan][p]['snr'][mcs_idx]
                data[mod][chan][p]['evm'] = data_in[chan][p]['evm'][mcs_idx]
                data[mod][chan][p]['ber'] = data_in[chan][p]['ber'][mcs_idx]


################################################################################
# Plot EVM
################################################################################

for mod in mod_type:
    # Plot based on modulation scheme

    # First loop can plot everything escept for the marker edge
    for chan in chan_type:
        for p in pol:
            # cr = code_rate[mcs_idx % 3]
            marker = get_marker(chan) # marker: o, x, s, ^
            color = get_color(p) # color: default scheme
            line = get_linestyle(p) # line: -, --, :
            label = chan + ', ' + p + '-pol'

            snr = data[mod][chan][p]['snr']
            evm = data[mod][chan][p]['evm']

            plt.plot(snr, evm, linestyle=line, marker=marker, label=label, color=color)
            # if chan == 'MIMO' and mod == '64QAM':
            #     print(snr)
            #     print(evm)
            #     print('--')
    
    # Standard EVM
    evm_req = get_evm_req(mod)
    plt.axhline(y = evm_req, color = 'r', linestyle = '--', zorder=0)

    plt.xlim(5, 35)
    plt.ylim(0, 50)
    plt.xticks(np.arange(5, 36, step=5))
    plt.xlabel('SNR (dB)')
    plt.ylabel('EVM (%)')
    plt.title(mod, fontsize=titlesize)
    plt.legend()
    plt.grid()
    plt.savefig(output_filepath + 'EVM_' + mod + '.' + output_format,
                format=output_format,
                bbox_inches='tight')
    plt.clf()

# ################################################################################
# # Plot BER
# ################################################################################

# fig, ax = plt.subplots()

# for mod in mod_type:
#     # Plot based on modulation scheme

#     # First loop can plot everything escept for the marker edge
#     for chan in chan_type:
#         for p in pol:
#             # cr = code_rate[mcs_idx % 3]
#             marker = get_marker(p) # marker: o, x, s, ^
#             color = get_color(p) # color: default scheme
#             line = get_linestyle(chan) # line: -, --, :
#             label = chan + '-' + p

#             snr = data[mod][chan][p]['snr']
#             ber = data[mod][chan][p]['ber']

#             plt.plot(snr, ber, linestyle=line, marker=marker, label=label, color=color)

#     # Second loop brings the marker to front
#     for chan in chan_type:
#         for p in pol:
#             # cr = code_rate[mcs_idx % 3]
#             marker = get_marker(p) # marker: o, x, s, ^
#             color = get_color(p) # color: default scheme
#             line = get_linestyle(chan) # line: -, --, :
#             label = chan + '-' + p

#             snr = data[mod][chan][p]['snr']
#             ber = data[mod][chan][p]['ber']

#             plt.scatter(snr, ber, linestyle='-', marker=marker, color=color,
#                         edgecolors=markeredgecolor,
#                         linewidth=markeredgewidth,
#                         zorder=10)
    
#     plt.yscale('symlog', linthresh=1e-4)
#     plt.xlim(0, 35)
#     plt.ylim(top=1)
#     plt.xticks(np.arange(0, 36, step=5))

#     ## Modify y-axis labels
#     y_ticks = ax.get_yticks()
#     y_labels = [item.get_text() for item in ax.get_yticklabels()]
#     y_labels[0] = '$< 10^{-5}$'
#     ax.set_yticks(y_ticks)
#     ax.set_yticklabels(y_labels)

#     # plt.gca().yaxis.set_major_locator(plt.LogLocator(base=10, numticks=10)) # major grid (int)
#     # plt.gca().yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=10)) # minor grid
#     plt.xlabel('SNR (dB)')
#     plt.ylabel('BER', labelpad=-20) # move axis title closer to the axis
#     # plt.title('BER vs SNR')
#     plt.legend(loc='lower left')
#     plt.grid(True, which='both', ls='-')
#     plt.savefig(output_filepath + 'BER_' + mod + '.' + output_format,
#                 format=output_format,
#                 bbox_inches='tight')
#     plt.clf()
