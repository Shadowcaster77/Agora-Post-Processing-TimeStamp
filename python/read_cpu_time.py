"""
Script Name: read_cpu_time.py
Author: Tom, cstandy
Description: Read from Agora's stdout screen log and print the processing time
             for each pipeline stage.
"""

import regex as re
import numpy as np
import math
from optparse import OptionParser

THRES = 1500

################################################################################
# Functions
################################################################################

def proc_time(filename):
    '''
    This func reads all the frames and should be used when the number of frames
    is less than 200.
    '''

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

    f.close()

    return total_time_list, fft_time_list, csi_time_list, bw_time_list, demul_time_list, decode_time_list

def proc_time_trimmed(filename, thres=1500):
    '''
    This func reads the middle frames and removes the leading and trailing n
    frames, respectively. n, as a threshold, is set to 1,500 by default.
    
    This script should be used when the number of frames is larger than 200.
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time(filename=filename)

    length = len(total_time)

    # Trimmed both leading and trailing frames
    total_time = total_time[thres:length-thres]
    fft_time = fft_time[thres:length-thres]
    csi_time = csi_time[thres:length-thres]
    bw_time = bw_time[thres:length-thres]
    demul_time = demul_time[thres:length-thres]
    decode_time = decode_time[thres:length-thres]

    return total_time, fft_time, csi_time, bw_time, demul_time, decode_time

def max_proc_time(filename):
    '''
    Find the frame with maximum processing time in total.
    Return: total processing time and processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time(filename=filename)
    index = total_time.index(max(total_time))
    # print("Num of frames in the log = {}".format(len(total_time)))
    # print("=> {} frames analyzed".format(len(total_time)))
    return total_time[index], fft_time[index], csi_time[index],\
           bw_time[index], demul_time[index], decode_time[index]

def max_proc_time_trimmed(filename, thres=THRES):
    '''
    Find the frame (among trimmed frame list) with maximum processing time in total.
    Return: total processing time and processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time_trimmed(filename=filename, thres=thres)
    index = total_time.index(max(total_time))
    # print("Num of frames in the log = {}".format(len(total_time) + 2*thres))
    # print("Discard leading {} frames and trailing {} frames".format(thres, thres))
    # print("=> {} frames analyzed".format(len(total_time)))
    return total_time[index], fft_time[index], csi_time[index],\
           bw_time[index], demul_time[index], decode_time[index]

def min_proc_time(filename):
    '''
    Find the frame with minimum processing time in total.
    Return: total processing time and processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time(filename=filename)
    index = total_time.index(min(total_time))
    return total_time[index], fft_time[index], csi_time[index],\
           bw_time[index], demul_time[index], decode_time[index]

def min_proc_time_trimmed(filename, thres=THRES):
    '''
    Find the frame (among trimmed frame list) with minimum processing time in total.
    Return: total processing time and processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time_trimmed(filename=filename, thres=thres)
    index = total_time.index(min(total_time))
    return total_time[index], fft_time[index], csi_time[index],\
           bw_time[index], demul_time[index], decode_time[index]

def avg_proc_time(filename):
    '''
    Calculate the average frame processing time.
    Return: average frame processing time and  average processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time(filename=filename)
    num_frames = len(total_time)
    avg_total_time = sum(total_time) / num_frames
    avg_fft_time = sum(fft_time) / num_frames
    avg_csi_time = sum(csi_time) / num_frames
    avg_bw_time = sum(bw_time) / num_frames
    avg_demul_time = sum(demul_time) / num_frames
    avg_decode_time = sum(decode_time) / num_frames

    return avg_total_time, avg_fft_time, avg_csi_time, avg_bw_time, avg_demul_time, avg_decode_time

def avg_proc_time_trimmed(filename, thres=THRES):
    '''
    Calculate the average frame processing time.
    Return: average frame processing time and  average processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time_trimmed(filename=filename, thres=thres)
    num_frames = len(total_time)
    avg_total_time = sum(total_time) / num_frames
    avg_fft_time = sum(fft_time) / num_frames
    avg_csi_time = sum(csi_time) / num_frames
    avg_bw_time = sum(bw_time) / num_frames
    avg_demul_time = sum(demul_time) / num_frames
    avg_decode_time = sum(decode_time) / num_frames

    return avg_total_time, avg_fft_time, avg_csi_time, avg_bw_time, avg_demul_time, avg_decode_time

def five9_proc_time(filename):
    '''
    Find the frame whose total processing time is the 99.999% largest.
    Return: total processing time and processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time(filename=filename)

    # Sort the frame proc time
    sorted_total_time = sorted(total_time)
    num_frames = len(total_time)
    five9_idx = int(num_frames * 0.99999)

    # Handle exceptions
    if five9_idx <= 0:
        five9_idx = 1

    five9_val = sorted_total_time[five9_idx - 1]
    index = total_time.index(five9_val)

    return total_time[index], fft_time[index], csi_time[index],\
           bw_time[index], demul_time[index], decode_time[index]

def five9_proc_time_trimmed(filename, thres=THRES):
    '''
    Find the frame whose total processing time is the 99.999% largest.
    Return: total processing time and processing time in each stage
    '''
    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time_trimmed(filename=filename, thres=thres)

    # Sort the frame proc time
    sorted_total_time = sorted(total_time)
    num_frames = len(total_time)
    five9_idx = int(num_frames * 0.99999)

    # Handle exceptions
    if five9_idx <= 0:
        five9_idx = 1

    five9_val = sorted_total_time[five9_idx - 1]
    index = total_time.index(five9_val)

    return total_time[index], fft_time[index], csi_time[index],\
           bw_time[index], demul_time[index], decode_time[index]

################################################################################
# Debug related func
################################################################################

def check_all_elements_identical(x):
    return x.count(x[0]) == len(x)

def check_deferred_frame(filename):
    print('Checking if defferred frames exist...')

    pattern = re.compile(r'deferring', re.IGNORECASE)
    defferred_frame = False

    with open(filename, 'r') as file:
        for _, line in enumerate(file, start=1):
            if pattern.search(line):
                defferred_frame = True
                print('[warning] Deferred frames exist!')
                break

    print('No deferred frames found.')
    return defferred_frame

def check_task_num(filename):
    '''
    This func reads all the frames and find the number of tasks fo each DSP
    stage.
    '''

    print('Checking if num of tasks is identical for all frames...')

    f = open(filename, 'r')
    lines = f.read()

    fft_count = re.findall('FFT \((\d+) tasks\):', lines)
    fft_count_list = list(map(int, fft_count))

    csi_count = re.findall('CSI \((\d+) tasks\):', lines)
    csi_count_list = list(map(float, csi_count))

    bw_count = re.findall('Beamweights \((\d+) tasks\):', lines)
    bw_count_list = list(map(float, bw_count))

    demul_count = re.findall('Demul \((\d+) tasks\):', lines)
    demul_count_list = list(map(float, demul_count))

    decode_count = re.findall('Decode \((\d+) tasks\):', lines)
    decode_count_list = list(map(float, decode_count))

    f.close()

    num_task_error = False

    if not check_all_elements_identical(fft_count_list):
        print('[warning] Num of FFT tasks is not identical for all frames!')
        num_task_error = True
    if not check_all_elements_identical(csi_count_list):
        print('[warning] Num of CSI tasks is not identical for all frames!')
        num_task_error = True
    if not check_all_elements_identical(bw_count_list):
        print('[warning] Num of BW tasks is not identical for all frames!')
        num_task_error = True
    if not check_all_elements_identical(demul_count_list):
        print('[warning] Num of DEMUL tasks is not identical for all frames!')
        num_task_error = True
    if not check_all_elements_identical(decode_count_list):
        print('[warning] Num of DECODE tasks is not identical for all frames!')
        num_task_error = True

    return num_task_error

def check_sum(filename):

    print('Checking if sum of time across all section equals to total time reported...')

    total_time, fft_time, csi_time, bw_time, demul_time, decode_time = proc_time(filename=filename)

    total_np = np.array(total_time)
    fft_np = np.array(fft_time)
    csi_np = np.array(csi_time)
    bw_np = np.array(bw_time)
    demul_np = np.array(demul_time)
    decode_np = np.array(decode_time)

    num_frames = len(total_time)
    sum_np = fft_np + csi_np + bw_np + demul_np + decode_np


    print('---')
    print(' . num_frames = {}'.format(num_frames))

    # Hard comparison
    hard_mismatch = np.sum(total_np != sum_np)
    print('---')
    print('Hard Mismatch:')
    print(' . num of hard mismatch = {}'.format(hard_mismatch))
    print(' . percentage of hard mismatch = {:.2%}'.format(hard_mismatch/num_frames))

    # Loose comparison
    loose_mismatch = 0
    abs_tol = 0.001
    for i in range(num_frames):
        if not math.isclose(total_np[i], sum_np[i], abs_tol=abs_tol):
            loose_mismatch = loose_mismatch + 1

    print('---')
    print('Loose Mismatch (thres = {}):'.format(abs_tol))
    print(' . num of loose match = {}'.format(loose_mismatch))
    print(' . percentage of loose mismatch = {:.2%}'.format(loose_mismatch/num_frames))
    print('---')

    return hard_mismatch, loose_mismatch

# debug funcs
def debug_funcs(filename):
    print('Debugging from log: {}'.format(filename))
    check_deferred_frame(filename=filename)
    num_task_error = check_task_num(filename=filename)
    if not num_task_error:
        check_sum(filename=filename)


################################################################################
# Main func
################################################################################

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", type="string", dest="file_name", help="File name as input", default="")
    parser.add_option("-t", "--trim", action="store_true", dest="trim", help="Trim the heading & trailing frames or not, default=False", default=False)
    parser.add_option("--thres", type="int", dest="thres", help="Trim the n heading & n trailing frames, default={}".format(THRES), default=THRES)
    parser.add_option("-s", "--stat", type="string", dest="stat", help="Choose statistic method: max, min, avg, five9s, default=max", default='max')
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Print debug message for sanity check", default=False)
    (options, args) = parser.parse_args()
    filename = options.file_name
    trim = options.trim
    stat = options.stat
    thres = options.thres
    debug = options.debug

    # Handle input error
    if not filename:
        parser.error('Must specify log filename with -f or --file, for more options, use -h')

    if debug:
        debug_funcs(filename=filename)
        exit(0)

    if trim:
        if stat == 'max':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = max_proc_time_trimmed(filename=filename, thres=thres)
        if stat == 'min':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = min_proc_time_trimmed(filename=filename, thres=thres)
        if stat == 'avg':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = avg_proc_time_trimmed(filename=filename, thres=thres)
        if stat == 'five9':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = five9_proc_time_trimmed(filename=filename, thres=thres)
    else:
        if stat == 'max':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = max_proc_time(filename=filename)
        if stat == 'min':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = min_proc_time(filename=filename)
        if stat == 'avg':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = avg_proc_time(filename=filename)
        if stat == 'five9':
            total_time, fft_time, csi_time, bw_time, demul_time, decode_time = five9_proc_time(filename=filename)
    
    sum = fft_time + csi_time + bw_time + demul_time + decode_time
    print("\"{}\" frame processing time = {:.3f} ms, which has".format(stat, total_time))
    print(". FFT time    = {:.3f} ms".format(fft_time))
    print(". CSI time    = {:.3f} ms".format(csi_time))
    print(". BW time     = {:.3f} ms".format(bw_time))
    print(". Demod. time = {:.3f} ms".format(demul_time))
    print(". Decode time = {:.3f} ms".format(decode_time))
    print('------------------------')
    print("* Sum of the previous = {:.3f} ms (double check)".format(sum))
    if trim:
        print("* Leading {} frames and trailing {} frames discarded".format(thres, thres))
