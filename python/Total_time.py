import regex as re
from optparse import OptionParser
import numpy as np


parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_str = options.file_name


f = open(file_str, 'r')
lines = f.read()


total_time_s = re.findall('Main \[frame \d+ \+ ([0-9]+\.[0-9]+) ms\]: Completed LDPC decoding \(\d+ UL symbols\)',lines);


total_time = list(map(float, total_time_s))

violates = (total_process_per_slot > 0.375).sum()


p99 = np.percentile(total_process_per_slot, 99)


binary_meet_goal = (violates/len(total_process_per_slot) < 0.0001)
