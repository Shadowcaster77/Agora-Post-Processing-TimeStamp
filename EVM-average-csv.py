import pandas as pd
from optparse import OptionParser
import numpy as np

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_name = options.file_name

df = pd.read_csv(file_name, header=None)
evm_values = df.iloc[1500:-1500, 1]  # Extract SNR values from the 1500th frame to the end-1500 frame
evm_values = evm_values[evm_values <= 20]  # Remove SNR values that are 0
evm_values = np.array(evm_values)
evm_values = np.sqrt((evm_values)/100) * 100

average_evm = np.mean(evm_values)

print("Average EVM:", average_evm)

