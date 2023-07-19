################################################################################
# Plot BER and EVM over SNR, respectively. Output seperate figures for
# SISO/MIMO. Overall output four plots.
# author: Chung-Hsuan Tung
################################################################################

import matplotlib.pyplot as plt
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
    # if code_rate == '333':
    #     color = 'tab:blue'
    # if code_rate == '500':
    #     color = 'tab:green'
    # if code_rate == '666':
    #     color = 'tab:red'

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

################################################################################
# Font settings: tick size, linewidth, marker size
################################################################################

# Enable comic style
# plt.xkcd()

# Font sizes

titlesize=28
# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=24)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # legend fontsize
# plt.rcParams.update({'font.size': 16})

FIG_SIZE_W = 6
FIG_SIZE_H = 6

markeredgecolor='black'
markeredgewidth=2

# plt.figure(figsize=(FIG_SIZE_W, FIG_SIZE_H))
plt.rc('lines', linewidth=3)
plt.rc('lines', markersize=12)
# plt.rc('lines', markeredgecolor=markeredgecolor)
# plt.rc('lines', markeredgewidth=markeredgewidth)

################################################################################
# I/O format
################################################################################

#
# Input
#

# chan = 'MIMO'
chan = 'SISO'

input_filepath = '../data/'
input_fileprefix = input_filepath + 'result_' + chan

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

output_filepath = '../fig/'
output_fileprefix = output_filepath + chan

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

# for mcs_idx in range(num_mcs):
#     for p in pol:

#         mod = mod_t[0] if mcs_idx < 3 else mod_t[1]
#         cr = code_rate[mcs_idx % 3]
#         marker = get_marker(p) # marker: o, x, s, ^
#         color = get_color(mod) # color: default scheme
#         line = get_linestyle(p) # line: -, --, :
#         # label = 'MCS' + str(mcs_idx+1) + ': ' + mod + '-' + pol[0] + '-0.' + cr
#         label = 'MCS-' + str(mcs_idx+1) + '-' + p # + ': ' + mod + '-0.' + cr

#         snr = snr_v if p == 'V' else snr_h
#         evm = evm_v if p == 'V' else evm_h

#         if mcs_idx+1 in mcs:
#             plt.plot(snr[mcs_idx], evm[mcs_idx],
#                      linestyle=line,
#                      marker=marker,
#                      label=label,
#                      color=color)

# # use second plot to set marker in front
# for mcs_idx in range(num_mcs):
#     for p in pol:

#         mod = mod_t[0] if mcs_idx < 3 else mod_t[1]
#         cr = code_rate[mcs_idx % 3]
#         marker = get_marker(p) # marker: o, x, s, ^
#         color = get_color(mod) # color: default scheme
#         line = get_linestyle(p) # line: -, --, :
#         # label = 'MCS' + str(mcs_idx+1) + ': ' + mod + '-' + pol[0] + '-0.' + cr
#         label = 'MCS-' + str(mcs_idx+1) + '-' + p # + ': ' + mod + '-0.' + cr

#         snr = snr_v if p == 'V' else snr_h
#         evm = evm_v if p == 'V' else evm_h

#         if mcs_idx+1 in mcs:
#             plt.scatter(snr[mcs_idx], evm[mcs_idx],
#                        linestyle='-',
#                        marker=marker,
#                        color=color,
#                        edgecolors='black',
#                        linewidth=1.5,
#                        zorder=5)

# plt.xlim(10, 35)
# plt.ylim(0, 50)
# plt.xticks(np.arange(10, 36, step=5))
# plt.xlabel('SNR (dB)')
# plt.ylabel('EVM (%)')
# # plt.title('EVM vs SNR')
# plt.legend()
# plt.grid()
# plt.savefig(output_fileprefix + '_EVM.' + output_format, format=output_format, bbox_inches='tight')
# plt.clf()

################################################################################
# Plot BER
################################################################################

fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

for mcs_idx in range(num_mcs):
    for p in pol:

        mod = mod_t[0] if mcs_idx < 3 else mod_t[1]
        cr = code_rate[mcs_idx % 3]
        marker = get_marker(mod) # marker: o, x, s, ^
        color = get_color(p) # color: default scheme
        line = get_linestyle(p) # line: -, --, :
        # label = 'MCS' + str(mcs_idx+1) + ': ' + mod + '-' + pol[0] + '-0.' + cr
        label = mod + ', ' + p + '-pol' # + ': ' + mod + '-0.' + cr

        snr = snr_v if p == 'V' else snr_h
        ber = ber_v if p == 'V' else ber_h

        if mcs_idx+1 in mcs:
            # remove outliers
            for i in range(num_snr):
                if ber[mcs_idx][i] < 1e-4 and snr[mcs_idx][i] > 25:
                    ber[mcs_idx][i] = 0

            plt.plot(snr[mcs_idx], ber[mcs_idx],
                     linestyle=line,
                     marker=marker,
                     label=label,
                     color=color)

plt.yscale('symlog', linthresh=1e-4)
plt.xlim(5, 35)
plt.ylim(top=1)
plt.xticks(np.arange(5, 36, step=5))

## Modify y-axis labels
y_ticks = ax.get_yticks()
y_labels = [item.get_text() for item in ax.get_yticklabels()]
y_labels[0] = '$< 10^{-5}$'
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels)

# plt.gca().yaxis.set_major_locator(plt.LogLocator(base=10, numticks=10)) # major grid (int)
# plt.gca().yaxis.set_minor_locator(plt.LogLocator(base=10, subs='all', numticks=10)) # minor grid
plt.xlabel('SNR (dB)')
plt.ylabel('BER', labelpad=-20) # move axis title closer to the axis
plt.title(chan, fontsize=titlesize)
plt.legend(loc='center right')
plt.grid(True, which='both', ls='-')
plt.savefig(output_fileprefix + '_BER.' + output_format, format=output_format, bbox_inches='tight')
plt.clf()
