import regex as re
from optparse import OptionParser
import numpy as np

def avg_evm_snr(filename):
    f = open(filename, 'r')
    lines = f.read()

    evm_values = []
    snr_values = []

    # Find EVM and True SNR values in each frame
    frames = re.findall(r'EVM\s+([\d.e+-]+).*?True SNR is:\s+([\d.+-]+)', lines, re.DOTALL)
    for evm, snr in frames:
        evm_values.append(float(evm))
        snr_values.append(float(snr))

    # Remove EVM values larger than 10 and their corresponding SNR
    filtered_values = [(evm, snr) for evm, snr in zip(evm_values, snr_values) if evm <= 1000000]
    evm_values, snr_values = zip(*filtered_values)

    # Remove SNR values equal to 0 and their corresponding EVM
    #filtered_values = [(evm, snr) for evm, snr in zip(evm_values, snr_values) if snr != 0]
    #evm_values, snr_values = zip(*filtered_values)

    # Calculate the average
    evm_average = sum(evm_values) / len(evm_values)
    snr_average = sum(snr_values) / len(snr_values)

    evm_values = np.array(evm_values)
    evm_values_1 = np.sort(evm_values)
    evm_length = np.shape(evm_values)[0]
    evm_values_2 = evm_values_1[int(evm_length*0.1): int(evm_length*0.7)]
    evm_rms = np.sqrt(np.mean(evm_values_2**2))

    snr_values = np.array(snr_values)
    snr_values_1 = np.sort(snr_values)
    snr_length = np.shape(snr_values)[0]
    snr_values_2 = snr_values_1[int(snr_length*0.3): int(snr_length*0.9)]
    snr_rms = np.mean(snr_values_2)

    return evm_rms, snr_rms

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
    (options, args) = parser.parse_args()
    file_str = options.file_name

    evm_rms, snr_rms = avg_evm_snr(file_str)
    
    print("Average True SNR:", snr_rms)
    print("rms EVM:", evm_rms)