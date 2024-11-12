"""
Script Name: estimate_data_rate.py
Author: cstandy
Description: Estimate the data rate of each DSP stage based on the 5G NR spec.
"""

from tabulate import tabulate

def get_mod_order(modulation):
    tab_mod_order = {
        'BPSK': 1,
        'QPSK': 2,
        '16QAM': 4,
        '64QAM': 6,
        '256QAM': 8
    }
    if not modulation in tab_mod_order.keys():
        raise ValueError('Invalid modulation order')
    else:
        return tab_mod_order[modulation]

if __name__ == '__main__':

    print('Estimate the data rate of each DSP stage based on the 5G NR spec.')
    print('* Support uplink RX (BS) only.')

    ############################
    # Setup/calculate parameters
    ############################
    # # Agora standard setup (except for the antenna count, which is a variable)
    # numerology = 0
    # scs = 15e3 * 2 ** numerology # Hz, subcarrier spacing
    # antenna_bs = 8
    # fft_size = 2048
    # bit_iq = 16 # 32 bits per I/Q sample (16-b I/16-b Q)
    # sampling_rate = scs * fft_size # Hz
    # num_prb = 100
    # num_data_sc = 12 * num_prb
    # bandwidth = num_data_sc * scs
    # modulation = '64QAM'
    # mod_order = get_mod_order(modulation)
    # code_rate = 0.333

    # Savannah standard setup
    numerology = 3
    scs = 15e3 * 2 ** numerology # Hz, subcarrier spacing
    antenna_bs = 2
    fft_size = 1024
    bit_iq = 16 # 32 bits per I/Q sample (16-b I/16-b Q)
    sampling_rate = scs * fft_size # Hz
    num_prb = 66
    num_data_sc = 12 * num_prb
    bandwidth = num_data_sc * scs
    modulation = '64QAM'
    mod_order = get_mod_order(modulation)
    code_rate = 438/1024

    ############################
    # Print the parameters
    ############################
    entires = [['Numerology', numerology],
               ['SCS (kHz)', scs/10**3],
               ['Antenna (BS)', antenna_bs],
               ['FFT size', fft_size],
               ['Sampling rate (MHz)', sampling_rate/10**6],
               ['Number of physical resource blocks (PRBs)', num_prb],
               ['Number of data subcarriers', num_data_sc],
               ['Bandwidth (MHz)', bandwidth/10**6],
               ['Modulation', modulation],
               ['Modulation order', mod_order],
               ['Code rate', '{}/1024'.format(code_rate*1024)]]
    headers = ['Name', 'Value']
    print(tabulate(entires, headers=headers, tablefmt="grid"))

    ############################
    # Estimate the data rate
    ############################
    data_rate_fronthaul = sampling_rate * (2 * bit_iq) * antenna_bs
    data_rate_after_fft = data_rate_fronthaul / fft_size * num_data_sc
    data_rate_after_demod = data_rate_after_fft * mod_order / (2 * bit_iq)
    data_rate_after_decode = data_rate_after_demod * code_rate

    entires = [['Fronthaul (Mbps)', data_rate_fronthaul/10**6],
               ['After FFT (Mbps)', data_rate_after_fft/10**6],
               ['After demodulation (Mbps)', data_rate_after_demod/10**6],
               ['After decoding (Mbps)', data_rate_after_decode/10**6]]
    headers = ['Location', 'Data rate']
    print(tabulate(entires, headers=headers, tablefmt="grid"))