"""
Script Name: read_elapsed_time.py
Author: cstandy, Tom
Description: Read from Agora's stdout screen log and print the elapsed time for 
             each frame.
"""

import regex as re
import numpy as np
import os
import glob
from optparse import OptionParser

DDL_3TTI = 0.375 # unit: ms
THRES = 1500

def elapsed_time(filename):
    '''
    Elapsed time means the time difference between the reception of the frame
    and the time it is finished processing (decoded).
    '''

    f = open(filename, 'r')
    lines = f.read()

    elapsed_time_ls = re.findall('Main \[frame \d+ \+ ([0-9]+\.[0-9]+) ms\]: Completed LDPC decoding \(\d+ UL symbols\)', lines)
    elapsed_time_ls = list(map(float, elapsed_time_ls))

    return elapsed_time_ls

def elapsed_time_after_pilot(filename):
    '''
    Elapsed time means the time difference between the end of FFT of all pilots
    and the time it is finished processing (decoded).
    '''

    f = open(filename, 'r')
    lines = f.read()

    fft_time_ls = re.findall('Main \[frame \d+ \+ ([0-9]+\.[0-9]+) ms\]: FFT-ed all pilots', lines)
    decode_time_ls = re.findall('Main \[frame \d+ \+ ([0-9]+\.[0-9]+) ms\]: Completed LDPC decoding \(\d+ UL symbols\)', lines)
    fft_time_ls = list(map(float, fft_time_ls))
    decode_time_ls = list(map(float, decode_time_ls))
    assert len(fft_time_ls) == len(decode_time_ls), "The number of frames is different between FFT and decoding!"
    elapsed_time_ls = [decode_time_ls[i] - fft_time_ls[i] for i in range(len(fft_time_ls))]

    return elapsed_time_ls

def elapsed_time_trimmed(filename, thres=1500):
    '''
    Elapsed time means the time difference between the reception of the frame
    and the time it is finished processing (decoded).
    '''

    elapsed_time_ls = elapsed_time(filename=filename)
    length = len(elapsed_time_ls)

    if thres * 2 >= length:
        print('Warning: The number of frames is less than 2 * thres, which is {}'.format(2 * thres))
        print('=> No frame is removed')
        return elapsed_time_ls

    return elapsed_time_ls[thres:length-thres]

def analyze_elapsed_time(elapsed_time_ls):
    elapsed_time_np = np.array(elapsed_time_ls)

    # number of time requirement violations
    num_vios = (elapsed_time_np > DDL_3TTI).sum()

    pct99_time = np.percentile(elapsed_time_np, 99)
    avg_time = np.mean(elapsed_time_np)

    # check if meeting the time requirement: 99.999% frames are processed within 3TTI
    prompt = (num_vios/len(elapsed_time_np) < 0.0001)

    return num_vios, pct99_time, avg_time, prompt

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", type="string", dest="file_name", help="file name as input", default="")
    parser.add_option("-t", "--trim", action="store_true", dest="trim", help="Trim the heading & trailing frames or not, default=False", default=False)
    parser.add_option("--thres", type="int", dest="thres", help="Trim the n heading & n trailing frames, default={}".format(THRES), default=THRES)
    parser.add_option("--postfft", action="store_true", dest="postfft", help="Calculate the elapsed time after the pilot, default=False", default=False)
    parser.add_option("-p", "--path", type="string", dest="path", help="Path to read the latest log file", default="")
    (options, args) = parser.parse_args()
    filename = options.file_name
    trim = options.trim
    thres = options.thres
    postfft = options.postfft
    path = options.path

    # Find the latest file given a file path
    if path:
        # List all files in the directory
        files = glob.glob(os.path.join(path, '*'))
        
        # Ensure the directory is not empty and files are present
        if not files:
            parser.error('No files found in the directory')

        # Find the file with the latest modification time
        latest_file = max(files, key=os.path.getmtime)

        if filename:
            print('Warning: Both -f and -p are specified. -p is used.')

        filename = latest_file

    # Handle input error
    if not filename:
        parser.error('Must specify log filename with -f or --file, for more options, use -h')
    elif not os.path.exists(filename):
        parser.error('File \"{}\" does not exist'.format(filename))

    if trim:
        elapsed_time_ls = elapsed_time_trimmed(filename=filename, thres=thres)
        print('Warning: The first and last {} frames are removed'.format(thres))
    elif postfft:
        elapsed_time_ls = elapsed_time_after_pilot(filename=filename)
        print('Warning: The elapsed time is calculated after the pilot')
    else:
        elapsed_time_ls = elapsed_time(filename=filename)
    num_vios, pct99_time, avg_time, prompt = analyze_elapsed_time(elapsed_time_ls)

    print('Reading from log: {}'.format(filename))
    print(' . Num of frames: {}'.format(len(elapsed_time_ls)))
    print(' . Num of violations: {}'.format(num_vios))
    print(' . Average elapsed time: {:.4f} ms'.format(avg_time))
    print(' . 99%-frame time = {:.4f} ms'.format(pct99_time))
    print(' . Meet time requirement? {}'.format(prompt))