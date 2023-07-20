import matplotlib.pyplot as plt
import sys

sys.path.append('..')
from python import read_avg_evm_snr

def get_evm_snr_seq(mod, pol, code_rate, snr_ideal):
    snr = []
    evm = []
    for s in snr_ideal:
        file_path = path + mod + '-' + pol + '-' + code_rate + '/SNR-' + s + '.txt'
        print(file_path)

        # Make up for Tom's missing script
        if mod == '64QAM' and pol == 'H' and code_rate == '333' and s == '25':
            _evm = 6.276
            _snr = 25 # ideal value
        else:
            _evm, _snr = read_avg_evm_snr.avg_evm_snr(filename=file_path)

        snr.append(_snr)
        evm.append(_evm)
    return evm, snr

def get_maker(code_rate):
    # marker = ['o', '^', 'x']
    if code_rate == '333':
        marker = 'o'
    if code_rate == '500':
        marker = '^'
    if code_rate == '666':
        marker = 'x'
    return marker

def get_linestyle(mod):
    if mod == '16QAM':
        ls = '-'
    if mod == '64QAM':
        ls = '--'
    return ls

################################################################################
# Plot settings
################################################################################

path = '../data/wintech/WinTech-H/'
mod_t = ['16QAM', '64QAM'] # modulation type
pol = ['H', 'V'] # polarization
code_rate = ['333', '500', '666'] # n/1000
snr_ideal = ['5', '10', '13', '15', '20', '25', '30']
o_filename = '../fig/evm_vs_snr.png'
# o_filename = 'evm_vs_snr.svg'


# python3 average_EVM_SNR.py --file WinTech-H/16QAM-H-333/SNR-30.txt

# file_path = path + mod_t[1] + '-' + pol[0] + '-' + code_rate[0] + '/SNR-' + snr_ideal[5] + '.txt'
# print(file_path)
# evm_rms, snr_rms = average_EVM_SNR.avg_evm_snr(filename=file_path)
# print("setting: ", file_path)
# print("measured SNR: ", snr_rms)
# print("measured EVM: ", evm_rms)

# quit(0)

# python3 average_EVM_SNR.py --file WinTech-H/16QAM-H-333/SNR-30.txt

i = 1
for mod in mod_t:
    for cr in code_rate:

        evm, snr = get_evm_snr_seq(mod=mod, pol=pol[0], code_rate=cr, snr_ideal=snr_ideal)
        # print(snr)
        # print(evm)

        marker = get_maker(cr) # marker: o, x, s, ^
        line = get_linestyle(mod) # line: -, --, :
        label = 'MCS' + str(i) + ': ' + mod + '-' + pol[0] + '-0.' + cr

        # Plot the sequence
        plt.plot(snr, evm, linestyle=line, marker=marker, label=label)
        i = i + 1

plt.xlim(0, 35)
# plt.ylim(0, 100)
plt.xlabel('SNR (dB)')
plt.ylabel('EVM (%)')
plt.title('EVM vs SNR')
plt.legend()
plt.savefig(o_filename, format='png')
# plt.savefig(o_filename, format='svg')
