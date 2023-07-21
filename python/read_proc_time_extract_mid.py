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

THRES = 1500

def proc_time(filename, thres):

    f = open(filename, 'r')
    lines = f.read()

    fft_time = re.findall('(?<=FFT \(\d*\ tasks\):\s+)[\d\.]+', lines)
    fft_time_list = list(map(float, fft_time))

    csi_time = re.findall('(?<=CSI \(\d*\ tasks\):\s+)[\d\.]+', lines)
    csi_time_list = list(map(float, csi_time))

    bw_time = re.findall('(?<=Beamweights \(\d*\ tasks\):\s+)[\d\.]+', lines)
    bw_time_list = list(map(float, bw_time))

    demul_time = re.findall('(?<=Demul \(\d*\ tasks\):\s+)[\d\.]+', lines)
    demul_time_list = list(map(float, demul_time))

    decode_time = re.findall('(?<=Decode \(\d*\ tasks\):\s+)[\d\.]+', lines)
    decode_time_list = list(map(float, decode_time))

    total_time = re.findall('(?<=Total:\s+)[\d\.]+', lines)
    total_time_list = list(map(float, total_time))

    total_time_list = total_time_list[thres:len(total_time_list)-thres]

    return total_time_list, fft_time_list, csi_time_list, bw_time_list, demul_time_list, decode_time_list

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--file", type="string", dest="file_name", help="file name as input", default="")
    (options, args) = parser.parse_args()
    file_str = options.file_name

    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time(filename=file_str, thres=THRES)
    
    thres = THRES
    max_index = total_time.index(max(total_time))
    # sum = fft_time[max_index+thres] + csi_time[max_index+thres]+\
    #       bw_time[max_index+thres]+demul_time[max_index+thres]+\
    #       decode_time[max_index+thres]
    print("Num of frames in the log = {}".format(len(total_time) + 2*thres))
    print("Discard leading {} frames and trailing {} frames".format(thres, thres))
    print("=> {} frames analyzed".format(len(total_time)))
    print("Max frame processing time = {:.2f} ms, which has".format(total_time[max_index]))
    print(". FFT time    = {:.2f} ms".format(fft_time[max_index+thres]))
    print(". CSI time    = {:.2f} ms".format(csi_time[max_index+thres]))
    print(". BW time     = {:.2f} ms".format(bw_time[max_index+thres]))
    print(". Demod. time = {:.2f} ms".format(demul_time[max_index+thres]))
    print(". Decode time = {:.2f} ms".format(decode_time[max_index+thres]))
    # print("Sum of the previous = {:.2f} ms (double check)".format(sum))
    # print(len(total_time))
    # print(len(fft_time))
    # print(len(bw_time))
    # print(len(csi_time))
    # print(len(demul_time))
    # print(len(decode_time))
