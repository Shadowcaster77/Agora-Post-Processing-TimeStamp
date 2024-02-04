'''
This file contains the common functions for plotting cpu/elapsed time.
'''

import numpy as np
import sys

sys.path.append('..')
from python import read_elapsed_time

################################################################################
# Read from log and return numpy array
################################################################################

def read_elapsed_time_from_file(log_path, trim, thres):
    '''
    Elapsed time means the time difference between the reception of the frame
    and the time it is finished processing (decoded).
    '''
    if trim:
        elapsed_time_ls = read_elapsed_time.elapsed_time_trimmed(log_path, thres)
    else:
        elapsed_time_ls = read_elapsed_time.elapsed_time(log_path)

    elapsed_time_np = np.array(elapsed_time_ls)

    return elapsed_time_np

def read_cpu_time_from_file(log_path, trim, thres):
    '''
    CPU time means the time difference between the start and the end of the
    decoding process.
    '''
    if trim:
        cpu_time_ls = read_elapsed_time.elapsed_time_trimmed(log_path, thres)
    else:
        cpu_time_ls = read_elapsed_time.elapsed_time(log_path)

    cpu_time_np = np.array(cpu_time_ls)

    return cpu_time_np

################################################################################
# Print statistics
################################################################################

def print_elapsed_time_stat(elapsed_time_np, deadline=0.375):
    num_samples = len(elapsed_time_np)
    min_elapsed_time = min(elapsed_time_np)
    max_elapsed_time = max(elapsed_time_np)
    avg_elapsed_time = np.mean(elapsed_time_np)
    five9_elapsed_time = np.percentile(elapsed_time_np, 99.999)
    pct_meet_deadline = np.sum(elapsed_time_np <= deadline) / num_samples * 100

    print(' . num of points = {}'.format(len(elapsed_time_np)))
    print(' . min elapsed time = {:.4f} ms'.format(min_elapsed_time))
    print(' . max elapsed time = {:.4f} ms'.format(max_elapsed_time))
    print(' . avg elapsed time = {:.4f} ms'.format(avg_elapsed_time))
    print(' . 99.999% elapsed time = {:.4f} ms'.format(five9_elapsed_time))
    print(' . {:.2f}% of the frames meet 3TTI deadline of {:.3f} ms'.format(
        pct_meet_deadline, deadline))
    
def print_cpu_time_stat(cpu_time_np):
    min_cpu_time = min(cpu_time_np)
    max_cpu_time = max(cpu_time_np)
    avg_cpu_time = np.mean(cpu_time_np)
    five9_cpu_time = np.percentile(cpu_time_np, 99.999)

    print(' . num of points = {}'.format(len(cpu_time_np)))
    print(' . min cpu time = {:.2f} ms'.format(min_cpu_time))
    print(' . max cpu time = {:.2f} ms'.format(max_cpu_time))
    print(' . avg cpu time = {:.2f} ms'.format(avg_cpu_time))
    print(' . 99.999% cpu time = {:.2f} ms'.format(five9_cpu_time))
