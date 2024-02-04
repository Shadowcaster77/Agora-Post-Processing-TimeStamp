"""
This script plot the elapsed time directly.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

sys.path.append('..')
from python import read_elapsed_time

################################################################################
# Functions for plot attributes
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

def plot(elapsed_time_np, log_path, output_format='png',
         output_filepath='../fig/', xkcd=False, trim=False, thres=1500):

    log_name = log_path.split("/")[-1] # e.g. 2023-07-19_16-35-36.log
    log_time = log_name.split(".")[0] # e.g. 2023-07-19_16-35-36

    print('Plot elapsed time trend from log: {}'.format(log_name))

    ############################################################################
    # Font settings: tick size, linewidth, marker size
    ############################################################################

    # Enable comic style
    if xkcd:
        plt.xkcd()
    
    # Mark trimmed or not in the output filename
    if trim:
        log_time = log_time + '_trim{}'.format(thres)

    # Font sizes
    titlesize = 28
    # plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    # plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=28)     # fontsize of the x and y labels
    plt.rc('xtick', labelsize=24)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=24)    # fontsize of the tick labels
    # plt.rc('legend', fontsize=16)    # legend fontsize
    # plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    # plt.rcParams.update({'font.size': 16})

    FIG_SIZE_W = 6
    FIG_SIZE_H = 6

    edgecolor='black'

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.plot(elapsed_time_np, 'b.', markersize=1, label='Elapsed time')

    # plt.ylim(0, 5e3)
    # plt.xticks(np.arange(l_bound, h_bound, step=0.1))
    title = 'Elapsed time for each frame'
    plt.title(title, fontsize=titlesize)
    plt.xlabel('Frame index')
    plt.ylabel('elapsed time (ms)')
    plt.grid()
    plt.savefig(output_filepath + 'elapsed_time_trend_' + log_time + '.' + output_format,
                format=output_format,
                bbox_inches='tight')
    plt.clf()

################################################################################
# Print statistics
################################################################################

def print_elapsed_time_stat(elapsed_time_np):
    min_elapsed_time = min(elapsed_time_np)
    max_elapsed_time = max(elapsed_time_np)
    avg_elapsed_time = np.mean(elapsed_time_np)
    five9_elapsed_time = np.percentile(elapsed_time_np, 99.999)

    print(' . num of points = {}'.format(len(elapsed_time_np)))
    print(' . min elapsed time = {:.4f} ms'.format(min_elapsed_time))
    print(' . max elapsed time = {:.4f} ms'.format(max_elapsed_time))
    print(' . avg elapsed time = {:.4f} ms'.format(avg_elapsed_time))
    print(' . 99.999% elapsed time = {:.4f} ms'.format(five9_elapsed_time))

if __name__ == '__main__':
    # Input
    parser = OptionParser()
    parser.add_option("-f", "--file", type="string", dest="file_name", help="File name as input", default="")
    parser.add_option("-t", "--trim", action="store_true", dest="trim", help="Trim the heading & trailing frames or not, default=False", default=False)
    parser.add_option("--thres", type="int", dest="thres", help="Trim the n heading & n trailing frames, default={}".format(read_elapsed_time.THRES), default=read_elapsed_time.THRES)
    parser.add_option("--output_format", type="string", dest="output_format", help="Output format (png, svg, pdf), default=png", default="png")
    parser.add_option("--output_filepath", type="string", dest="output_filepath", help="Output file path, default=../fig/", default="../fig/")
    parser.add_option("--xkcd", action="store_true", dest="xkcd", help="Enable xkcd style, default=False", default=False)
    (options, args) = parser.parse_args()

    # Input file path
    log_path = options.file_name # e.g., /home/ct297/workspace/agora_single-core-sim/log/2023-07-19_16-35-36.log

    # Handle input error
    if not log_path:
        parser.error('Must specify log path with -f or --file, for more options, use -h')

    # Process options
    trim = options.trim # default=False
    thres = options.thres # default=1500

    # Output options
    output_format = options.output_format # png (default), svg, pdf
    output_filepath = options.output_filepath # ../fig/
    xkcd = options.xkcd # default=False

    elapsed_time_np = read_elapsed_time_from_file(log_path, trim, thres)
    plot(elapsed_time_np, log_path, output_format, output_filepath, xkcd, trim, thres)
    print_elapsed_time_stat(elapsed_time_np)
