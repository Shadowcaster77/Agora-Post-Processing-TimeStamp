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


total_after = total[2000:len(total)-500]
fft_time = fft_time[2000:len(fft_time)-500]
csi_time = csi_time[2000:len(csi_time)-500]
BW_time = BW_time[2000:len(BW_time)-500]
Demul_time = Demul_time[2000:len(Demul_time)-500]
Decode_time = Decode_time[2000:len(Decode_time)-500]




total.remove(max(total_after))


rm_index1 = total_after.index(max(total_after))
total_after.remove(max(total_after))
fft_time.remove(fft_time[rm_index1])
csi_time.remove(csi_time[rm_index1])
BW_time.remove(BW_time[rm_index1])
Demul_time.remove(Demul_time[rm_index1])
Decode_time.remove(Decode_time[rm_index1])


rm_index2 = total_after.index(max(total_after))
total_after.remove(max(total_after))
fft_time.remove(fft_time[rm_index2])
csi_time.remove(csi_time[rm_index2])
BW_time.remove(BW_time[rm_index2])
Demul_time.remove(Demul_time[rm_index2])
Decode_time.remove(Decode_time[rm_index2])


rm_index3 = total_after.index(max(total_after))
total_after.remove(max(total_after))
fft_time.remove(fft_time[rm_index3])
csi_time.remove(csi_time[rm_index3])
BW_time.remove(BW_time[rm_index3])
Demul_time.remove(Demul_time[rm_index3])
Decode_time.remove(Decode_time[rm_index3])


rm_index4 = total_after.index(max(total_after))
total_after.remove(max(total_after))
fft_time.remove(fft_time[rm_index4])
csi_time.remove(csi_time[rm_index4])
BW_time.remove(BW_time[rm_index4])
Demul_time.remove(Demul_time[rm_index4])
Decode_time.remove(Decode_time[rm_index4])


rm_index5 = total_after.index(max(total_after))
total_after.remove(max(total_after))
fft_time.remove(fft_time[rm_index5])
csi_time.remove(csi_time[rm_index5])
BW_time.remove(BW_time[rm_index5])
Demul_time.remove(Demul_time[rm_index5])
Decode_time.remove(Decode_time[rm_index5])




max_index = total_after.index(max(total_after))


print("max total time is: ", total_after[max_index])
# print("max total time after is: ", total[max_index+2000])
print("\n")
print("max fft time is: ", fft_time[max_index])
print("max csi time is: ", csi_time[max_index])
print("max BW time is: ", BW_time[max_index])
print("max demul time is: ", Demul_time[max_index])
print("max decode time is: ", Decode_time[max_index])
print("\n")
print("Double check, sum of the previous ", fft_time[max_index]+csi_time[max_index]+BW_time[max_index]+
     Demul_time[max_index]+Decode_time[max_index])


# print(len(total))
