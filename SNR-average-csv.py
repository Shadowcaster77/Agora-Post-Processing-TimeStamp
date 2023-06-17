import pandas as pd
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_name = options.file_name

df = pd.read_csv(file_name, header=None)
snr_values = df.iloc[1500:-1500, 1]  # Extract SNR values from the 1500th frame to the end-1500 frame
snr_values = snr_values[snr_values != 0]  # Remove SNR values that are 0

average_snr = snr_values.mean()

print("Average SNR:", average_snr)

