import pandas as pd
from optparse import OptionParser
import numpy as np

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_name = options.file_name

df = pd.read_csv(file_name, header=None)
evm_values = df.iloc[1500:-1500, 1]  # Extract SNR values from the 1500th frame to the end-1500 frame
evm_values_secondrow = df.iloc[1500:-1500, 2]

#evm_values = evm_values[evm_values <= 20]  # Remove SNR values that are 0
evm_values = np.array(evm_values)
evm_values = np.sqrt((evm_values)/100) * 100

evm_values_secondrow = np.array(evm_values_secondrow)
evm_values_secondrow = np.sqrt((evm_values_secondrow)/100) * 100

evm_values_1 = np.sort(evm_values)
evm_length = np.shape(evm_values)[0]
evm_values_2 = evm_values_1[int(evm_length*0.1): int(evm_length*0.7)]
evm_rms = np.mean(evm_values_2)

evm_values_1_2nd = np.sort(evm_values_secondrow)
evm_length_2nd = np.shape(evm_values_secondrow)[0]
evm_values_2_2nd = evm_values_1_2nd[int(evm_length_2nd*0.1): int(evm_length_2nd*0.7)]
evm_rms_2nd = np.mean(evm_values_2_2nd)

#average_evm = np.mean(evm_values)

print("Average EVM - H:", evm_rms)
print("Average EVM - V:", evm_rms_2nd)
