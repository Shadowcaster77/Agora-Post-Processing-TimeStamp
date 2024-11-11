"""
This script plot the elapsed time distributions in complementary CDF.

Author: cstandy
"""

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

import plot_time_utils

sys.path.append('..')
from analyzer import read_elapsed_time

DEADLINE_3TTI=0.375

def plot(output_format='png', output_filepath='../fig/', xkcd=False):

    ############################################################################
    # Font settings: tick size, linewidth, marker size
    ############################################################################

    # Enable comic style
    if xkcd:
        plt.xkcd()

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

    FIG_SIZE_W = 12
    FIG_SIZE_H = 7

    edgecolor='black'

    ############################################################################
    # Get statistics
    ############################################################################

    # mcs 10
    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-02-29_15-35-31.log'
    # elapsed_time_np_1x1_50mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)
    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-02-29_15-31-07.log'
    # elapsed_time_np_2x2_50mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)

    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-02-29_15-13-45.log'
    # elapsed_time_np_1x1_100mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)
    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-02-29_23-36-26.log'
    # elapsed_time_np_2x2_100mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 10000)
    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-03-03_02-12-56.log'
    # elapsed_time_np_4x4_100mhz_6ul = plot_time_utils.read_elapsed_time_from_file(log_path, True, 10000)

    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-02-29_14-58-56.log'
    # elapsed_time_np_1x1_200mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)

    # mcs 17
    log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-03-06_19-18-24.log'
    elapsed_time_np_1x1_100mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)
    log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-03-06_20-25-08.log'
    elapsed_time_np_2x2_100mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 50000)
    log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-03-06_21-23-04.log'
    elapsed_time_np_4x4_100mhz_6ul = plot_time_utils.read_elapsed_time_from_file(log_path, True, 50000)

    log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-03-06_18-44-52.log'
    elapsed_time_np_1x1_200mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)

    num_samples = 100000

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # elapsed_time_sorted = np.sort(elapsed_time_np_1x1_50mhz)
    # elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
    # elapsed_time_prob_c = 1 - elapsed_time_prob
    # plt.plot(elapsed_time_sorted, elapsed_time_prob_c, marker='o', linewidth=2,
    #          mfc='none', mec='tab:blue', mew=2, markersize=14,
    #          color='tab:blue', label='1x1, 50 MHz')
    
    elapsed_time_sorted = np.sort(elapsed_time_np_1x1_100mhz)
    elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
    elapsed_time_prob_c = 1 - elapsed_time_prob
    plt.plot(elapsed_time_sorted, elapsed_time_prob_c, marker='o', linewidth=3,
             mfc='none', mec='tab:blue', mew=3, markersize=14,
             color='tab:blue', label='1x1, 100 MHz')

    elapsed_time_sorted = np.sort(elapsed_time_np_1x1_200mhz)
    elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
    elapsed_time_prob_c = 1 - elapsed_time_prob
    plt.plot(elapsed_time_sorted, elapsed_time_prob_c, marker='x', linewidth=3,
             mfc='none', mec='tab:orange', mew = 3, markersize=15,
             color='tab:orange', label='1x1, 200 MHz')

    # elapsed_time_sorted = np.sort(elapsed_time_np_2x2_50mhz)
    # elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
    # elapsed_time_prob_c = 1 - elapsed_time_prob
    # plt.plot(elapsed_time_sorted, elapsed_time_prob_c, marker='s', linewidth=2,
    #          mfc='none', mec='tab:red', mew = 2, markersize=15,
    #          color='tab:red', label='2x2, 50 MHz')

    elapsed_time_sorted = np.sort(elapsed_time_np_2x2_100mhz)
    elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
    elapsed_time_prob_c = 1 - elapsed_time_prob
    plt.plot(elapsed_time_sorted, elapsed_time_prob_c, marker='^', linewidth=3,
             mfc='none', mec='tab:green', mew = 3, markersize=15,
             color='tab:green', label='2x2, 100 MHz')
    
    # elapsed_time_sorted = np.sort(elapsed_time_np_4x4_100mhz_6ul)
    # elapsed_time_prob = np.arange(1, num_samples + 1) / num_samples
    # elapsed_time_prob_c = 1 - elapsed_time_prob
    # plt.plot(elapsed_time_sorted, elapsed_time_prob_c, marker='s', linewidth=2,
    #          mfc='none', mec='tab:brown', mew = 2, markersize=14,
    #          color='tab:brown', label='4x4, 100 MHz, 6UL')

    # Plot 3TTI deadline & mark statistics
    plt.axvline(x = 0.375, color = 'r', linestyle='--', linewidth=3)
    plt.figtext(0.425, 0.82, f'0.375 msec', fontsize=24, ha='center')
    plt.axhline(y = 1 - 0.999, color = 'black', linestyle='--', linewidth=3)
    plt.figtext(0.77, 0.36, f'99.9th Percentile', fontsize=24, ha='center')

    # plt.xlim(min(elapsed_time_np), 0.4)
    plt.xlim(0, 1.4)
    # plt.xlim(0.1, 10)
    plt.ylim(10e-6, 1)
    plt.yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1, 1])
    # plt.xscale("log")
    plt.yscale("log")
    # title = 'Elapsed Time CDF'
    # plt.title(title, fontsize=titlesize)
    plt.xlabel('Elapsed Time (ms)')
    plt.ylabel('Complementary CDF')
    # plt.grid()
    plt.grid(True, which="both", linestyle='--')
    plt.legend(fontsize=24)
    plt.savefig(
        output_filepath + 'elapsed_time_ccdf.' + output_format,
        format=output_format,
        bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    # Input
    parser = OptionParser()
    parser.add_option("--output_format", type="string", dest="output_format", help="Output format (png, svg, pdf), default=png", default="png")
    parser.add_option("--output_filepath", type="string", dest="output_filepath", help="Output file path, default=../fig/", default="../fig/")
    parser.add_option("--xkcd", action="store_true", dest="xkcd", help="Enable xkcd style, default=False", default=False)
    (options, args) = parser.parse_args()

    # Output options
    output_format = options.output_format # png (default), svg, pdf
    output_filepath = options.output_filepath # ../fig/
    xkcd = options.xkcd # default=False

    plot(output_format, output_filepath, xkcd)
