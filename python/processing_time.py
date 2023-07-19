import regex as re
from optparse import OptionParser


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




total_after = total[1500:len(total)-1500]


max_index = total_after.index(max(total_after))
print("max total time is: ", total_after[max_index])
print("max total time after is: ", total[max_index+1500])
print("\n")
print("max fft time is: ", fft_time[max_index+1500])
print("max csi time is: ", csi_time[max_index+1500])
print("max BW time is: ", BW_time[max_index+1500])
print("max demul time is: ", Demul_time[max_index+1500])
print("max decode time is: ", Decode_time[max_index+1500])
print("\n")
print("Double check, sum of the previous ", fft_time[max_index+1500]+csi_time[max_index+1500]+BW_time[max_index+1500]+
     Demul_time[max_index+1500]+Decode_time[max_index+1500])


# print(len(total))
# print(len(fft_time))
# print(len(BW_time))
# print(len(csi_time))
# print(len(Demul_time))
# print(len(Decode_time))
