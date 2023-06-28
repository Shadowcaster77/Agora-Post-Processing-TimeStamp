import pandas as pd
from optparse import OptionParser
import numpy as np

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_name = options.file_name

df = pd.read_csv(file_name, header=None)
ber_values = df.iloc[1500:-1500, 1]  # Extract BER values from the 1500th frame to the end-1500 frame
ber_values_column2 = df.iloc[1500:-1500, 2]

ber_values = ber_values.to_numpy()

ber_values_1 = np.sort(ber_values)
ber_length = np.shape(ber_values)[0]
ber_values_2 = ber_values_1[int(ber_length*0.1): int(ber_length*0.7)]
ber_rms = np.mean(ber_values_2)


ber_values_column2 = ber_values_column2.to_numpy()

ber_values_1_column2 = np.sort(ber_values_column2)
ber_length_column2 = np.shape(ber_values_column2)[0]
ber_values_2_column2 = ber_values_1_column2[int(ber_length_column2*0.1): int(ber_length_column2*0.7)]
ber_rms_column2 = np.mean(ber_values_2_column2)

#average_ber = ber_values.mean()

print("Average BER:", ber_rms)
print("Average BER:", ber_rms_column2)
# Calculate the differences between consecutive BER values
#differences = ber_values.diff()

# Find the frames where abrupt value changes occur
#abrupt_change_frames = differences[abs(differences) > 0.4].index.tolist()

# print("Frames with abrupt value changes:", abrupt_change_frames)

