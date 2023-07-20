"""
Script Name: read_proc_time_extract_mid.py
Author: Tom, cstandy
Description: Read from Agora's stdout screen log and plot the processing time
             for each pipeline stage. This script reads the middle frames and
             removes the leading and trailing n frames, respectively. n, as a
             threshold, is set to 1,500 by default. This script is used when
             the number of frames is larger than 200.
"""

import regex as re
from optparse import OptionParser

thres = 1500

parser = OptionParser()
parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
(options, args) = parser.parse_args()
file_str = options.file_name


f = open(file_str, 'r')
lines = f.read()


fft = re.findall('(?<=FFT \(\d*\ tasks\):\s+)[\d\.]+',lines);
fft_time = list(map(float, fft))


csi = re.findall('(?<=CSI \(\d*\ tasks\):\s+)[\d\.]+',lines);
csi_time = list(map(float, csi))


BW = re.findall('(?<=Beamweights \(\d*\ tasks\):\s+)[\d\.]+',lines);
BW_time = list(map(float, BW))


Demul = re.findall('(?<=Demul \(\d*\ tasks\):\s+)[\d\.]+',lines);
Demul_time = list(map(float, Demul))


Decode = re.findall('(?<=Decode \(\d*\ tasks\):\s+)[\d\.]+',lines);
Decode_time = list(map(float, Decode))


a = re.findall('(?<=Total:\s+)[\d\.]+',lines);
total = list(map(float, a))

total_after = total[thres:len(total)-thres]


max_index = total_after.index(max(total_after))
print("max total time is: ", total_after[max_index])
print("max total time after is: ", total[max_index+thres])
print("\n")
print("max fft time is: ", fft_time[max_index+thres])
print("max csi time is: ", csi_time[max_index+thres])
print("max BW time is: ", BW_time[max_index+thres])
print("max demul time is: ", Demul_time[max_index+thres])
print("max decode time is: ", Decode_time[max_index+thres])
print("\n")
print("Double check, sum of the previous ", fft_time[max_index+thres]+csi_time[max_index+thres]+BW_time[max_index+thres]+
     Demul_time[max_index+thres]+Decode_time[max_index+thres])


# print(len(total))
# print(len(fft_time))
# print(len(BW_time))
# print(len(csi_time))
# print(len(Demul_time))
# print(len(Decode_time))
