"""
This script plot the elapsed time distributions.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

import plot_time_utils

sys.path.append('..')
from analyzer import read_elapsed_time

DEADLINE_3TTI=0.375

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
    # Get statistics
    ############################################################################

    num_samples = len(elapsed_time_np)
    two9_elapsed_time = np.percentile(elapsed_time_np, 99)
    three9_elapsed_time = np.percentile(elapsed_time_np, 99.9)
    four9_elapsed_time = np.percentile(elapsed_time_np, 99.99)
    five9_elapsed_time = np.percentile(elapsed_time_np, 99.999)
    pct_meet_deadline = np.sum(elapsed_time_np <= DEADLINE_3TTI) / num_samples * 100

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    elapsed_time_sorted = np.sort(elapsed_time_np)
    elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
    plt.plot(elapsed_time_sorted, elapsed_time_prob, marker='o', linewidth=0)

    # print (np.sum(n*np.diff(bins))) # verify the integral is 1

    # Plot 3TTI deadline & mark statistics
    plt.axvline(x = 0.375, color = 'r', linestyle='--',
                linewidth=3, label = f'3TTI (0.375 ms)')
    plt.axvline(x = two9_elapsed_time, color = 'b', linestyle=':',
                linewidth=3, label = f'99% ({two9_elapsed_time:.3f} ms)')
    plt.axvline(x = three9_elapsed_time, color = 'c', linestyle=':',
                linewidth=3, label = f'99.9% ({three9_elapsed_time:.3f} ms)')
    plt.axvline(x = four9_elapsed_time, color = 'g', linestyle=':',
                linewidth=3, label = f'99.99% ({four9_elapsed_time:.3f} ms)')
    # plt.axvline(x = five9_elapsed_time, color = 'y', linestyle='--', label = f'99.999% ({five9_elapsed_time:.3f} ms)')
    # Adding a caption
    # plt.figtext(0.5, 0.5, f'{pct_meet_deadline:.2f}% meet 3TTI', fontsize=16, ha='center')

    # plt.xlim(min(elapsed_time_np), 0.4)
    # plt.xlim(0, max(elapsed_time_np))
    plt.xlim(0.1, 10)
    if (max(elapsed_time_np) > 10):
        print(f'Warning: max elapsed time {max(elapsed_time_np)} > 10 ms')
    plt.xscale("log")
    # title = 'Elapsed Time CDF'
    # plt.title(title, fontsize=titlesize)
    plt.xlabel('Elapsed Time (ms)')
    plt.ylabel('Probability')
    # plt.grid()
    plt.grid(True, which="both")
    plt.legend(fontsize=16)
    plt.savefig(
        output_filepath + 'elapsed_time_cdf_' + log_time + '.' + output_format,
        format=output_format,
        bbox_inches='tight')
    plt.clf()

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

    elapsed_time_np = plot_time_utils.read_elapsed_time_from_file(log_path, trim, thres)
    plot(elapsed_time_np, log_path, output_format, output_filepath, xkcd, trim, thres)
    plot_time_utils.print_elapsed_time_stat(elapsed_time_np)
