import pandas as pd
from optparse import OptionParser
import numpy as np

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_name = options.file_name

df = pd.read_csv(file_name, header=None)
snr_values = df.iloc[1500:-1500, 1]  # Extract SNR values from the 1500th frame to the end-1500 frame
snr_values_2nd = df.iloc[1500:-1500, 2]

'''
snr_values = snr_values[snr_values != 0]  # Remove SNR values that are 0

average_snr = snr_values.mean()
'''

snr_values = np.array(snr_values)
snr_values_2nd = np.array(snr_values_2nd)

snr_values_1 = np.sort(snr_values)
snr_length = np.shape(snr_values)[0]
snr_values_2 = snr_values_1[int(snr_length*0.3): int(snr_length*0.9)]
snr_rms = np.mean(snr_values_2)




print("Average SNR-H:", snr_rms)

