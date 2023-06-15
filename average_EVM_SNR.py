import regex as re
from optparse import OptionParser
import numpy as np

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_str = options.file_name


f = open(file_str, 'r')
lines = f.read()

evm_values = []
snr_values = []

# Find EVM and True SNR values in each frame
frames = re.findall(r'EVM\s+([\d.e+-]+).*?True SNR is:\s+([\d.+-]+)', lines, re.DOTALL)
for evm, snr in frames:
    evm_values.append(float(evm))
    snr_values.append(float(snr))


# print(evm_values)

evm_values = evm_values[1500:-1500]
snr_values = snr_values[1500:-1500]


# Calculate the average
evm_average = sum(evm_values) / len(evm_values)
snr_average = sum(snr_values) / len(snr_values)


evm_values = np.array(evm_values)
evm_rms = np.sqrt(np.mean(evm_values**2))


print("Average EVM:", evm_average)
print("Average True SNR:", snr_average)

print("rms EVM:", evm_rms)
