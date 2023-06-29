import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from brokenaxes import brokenaxes
from scipy.io import loadmat
import numpy as np

def get_marker(code_rate):
    # marker = ['o', '^', 'x']
    if code_rate == '333':
        marker = 'o'
    if code_rate == '500':
        marker = '^'
    if code_rate == '666':
        marker = 'x'
    return marker

def get_color(code_rate):
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
    if code_rate == '333':
        color = 'tab:blue'
    if code_rate == '500':
        color = 'tab:green'
    if code_rate == '666':
        color = 'tab:red'
    return color

def get_linestyle(mod):
    if mod == '16QAM':
        ls = '-'
    if mod == '64QAM':
        ls = '--'
    return ls

################################################################################
# Plot settings
################################################################################

# Font sizes
SMALL_SIZE = 15
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=18)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('legend', fontsize=13)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# plt.rcParams.update({'font.size': 16})

mod_t = ['16QAM', '64QAM'] # modulation type
pol = ['H', 'V'] # polarization
code_rate = ['333', '500', '666'] # n/1000
snr_ideal = ['5', '10', '13', '15', '20', '25', '30']

data = loadmat('result_MIMO_V.mat')

snr = data['snrList']
evm = data['evmList']
ber = data['berList']

num_mcs = len(snr)
num_snr = len(snr[0])

################################################################################
# EVM
################################################################################

for mcs_idx in range(num_mcs):

    mod = mod_t[0] if mcs_idx < 3 else mod_t[1]
    cr = code_rate[mcs_idx % 3]
    marker = get_marker(cr) # marker: o, x, s, ^
    color = get_color(cr) # color: blue, green, red
    line = get_linestyle(mod) # line: -, --, :
    # label = 'MCS' + str(mcs_idx+1) + ': ' + mod + '-' + pol[0] + '-0.' + cr
    label = 'MCS-' + str(mcs_idx+1) # + ': ' + mod + '-0.' + cr

    plt.plot(snr[mcs_idx], evm[mcs_idx], linestyle=line, marker=marker, label=label, color=color)

plt.xlim(0, 35)
plt.ylim(0, 250)
plt.xlabel('SNR (dB)')
plt.ylabel('EVM (%)')
# plt.title('EVM vs SNR')
plt.legend()
plt.grid()
# plt.savefig('evm_vs_snr.png', format='png', bbox_inches='tight')
plt.savefig('evm_vs_snr.pdf', format='pdf', bbox_inches='tight')
# plt.savefig('evm_vs_snr.svg', format='svg', bbox_inches='tight')
plt.clf()

################################################################################
# BER
################################################################################

for mcs_idx in range(num_mcs):

    mod = mod_t[0] if mcs_idx < 3 else mod_t[1]
    cr = code_rate[mcs_idx % 3]
    marker = get_marker(cr) # marker: o, x, s, ^
    color = get_color(cr) # color: blue, green, red
    line = get_linestyle(mod) # line: -, --, :
    # label = 'MCS' + str(mcs_idx+1) + ': ' + mod + '-' + pol[0] + '-0.' + cr
    label = 'MCS-' + str(mcs_idx+1) # + ': ' + mod + '-0.' + cr

    plt.semilogy(snr[mcs_idx], ber[mcs_idx], linestyle=line, marker=marker, label=label, color=color)

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
# plt.savefig('ber_vs_snr.png', format='png', bbox_inches='tight')
plt.savefig('ber_vs_snr.pdf', format='pdf', bbox_inches='tight')
# plt.savefig('ber_vs_snr.svg', format='svg', bbox_inches='tight')
plt.clf()
