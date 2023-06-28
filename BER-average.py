import pandas as pd
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_name = options.file_name

df = pd.read_csv(file_name, header=None)
ber_values = df.iloc[1500:-1500, 1]  # Extract BER values from the 1500th frame to the end-1500 frame

average_ber = ber_values.mean()

print("Average BER:", average_ber)

# Calculate the differences between consecutive BER values
differences = ber_values.diff()

# Find the frames where abrupt value changes occur
abrupt_change_frames = differences[abs(differences) > 0.4].index.tolist()

# print("Frames with abrupt value changes:", abrupt_change_frames)

