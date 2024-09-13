"""
This script plot the cpu time directly.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

import plot_time_utils

sys.path.append('..')
from python import read_cpu_time

def plot(cpu_time_np, fft_time_np, csi_time_np, bw_time_np, equal_time_np,
         demul_time_np, decode_time_np, log_path, output_format='png',
         output_filepath='../fig/', xkcd=False, trim=False, thres=1500):

    log_name = log_path.split("/")[-1] # e.g. 2023-07-19_16-35-36.log
    log_time = log_name.split(".")[0] # e.g. 2023-07-19_16-35-36

    print('Plot cpu time trend from log: {}'.format(log_name))

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

    # fig, ax = plt.subplots(7, figsize=(12, 12))
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # ax[0].plot(cpu_time_np, 'b.', markersize=1, label='cpu time (ms)')
    # ax[0].legend()
    # ax[0].grid()

    # ax[1].plot(fft_time_np, 'g.', markersize=1, label='fft time (ms)')
    # ax[1].legend()
    # ax[1].grid()

    # ax[2].plot(csi_time_np, 'r.', markersize=1, label='csi time (ms)')
    # ax[2].legend()
    # ax[2].grid()

    # ax[3].plot(bw_time_np, 'c.', markersize=1, label='bw time (ms)')
    # ax[3].legend()
    # ax[3].grid()

    # ax[4].plot(equal_time_np, 'm.', markersize=1, label='equal time (ms)')
    # ax[4].legend()
    # ax[4].grid()

    # ax[5].plot(demul_time_np, 'y.', markersize=1, label='demul time (ms)')
    # ax[5].legend()
    # ax[5].grid()

    # ax[6].plot(decode_time_np, 'k.', markersize=1, label='decode time (ms)')
    # ax[6].legend()
    # ax[6].grid()

    # plt.tight_layout()

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.plot(cpu_time_np, 'b.', markersize=1, label='cpu time (ms)')
    plt.plot(fft_time_np, 'g.', markersize=1, label='fft time (ms)')
    plt.plot(csi_time_np, 'r.', markersize=1, label='csi time (ms)')
    plt.plot(bw_time_np, 'c.', markersize=1, label='bw time (ms)')
    plt.plot(equal_time_np, 'm.', markersize=1, label='equal time (ms)')
    plt.plot(demul_time_np, 'y.', markersize=1, label='demul time (ms)')
    plt.plot(decode_time_np, 'k.', markersize=1, label='decode time (ms)')
    plt.title('CPU Time Trend', fontsize=titlesize)
    plt.xlabel('Frame index')
    plt.ylabel('Time (ms)')
    plt.legend(markerscale=10)
    # plt.xlim(4100, 4200)
    # plt.ylim(0, 0.6)
    plt.grid()

    plt.savefig(output_filepath + 'cpu_time_trend_' + log_time + '.' + output_format,
                format=output_format,
                bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    # Input
    parser = OptionParser()
    parser.add_option("-f", "--file", type="string", dest="file_name", help="File name as input", default="")
    parser.add_option("-t", "--trim", action="store_true", dest="trim", help="Trim the heading & trailing frames or not, default=False", default=False)
    parser.add_option("--thres", type="int", dest="thres", help="Trim the n heading & n trailing frames, default={}".format(read_cpu_time.THRES), default=read_cpu_time.THRES)
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

    cpu_time_np, fft_time_np, csi_time_np, bw_time_np, equal_time_np, demul_time_np, decode_time_np = plot_time_utils.read_cpu_time_from_file(log_path, trim, thres)
    plot(cpu_time_np, fft_time_np, csi_time_np, bw_time_np, equal_time_np, demul_time_np, decode_time_np, log_path, output_format, output_filepath, xkcd, trim, thres)
    plot_time_utils.print_cpu_time_stat(cpu_time_np)
