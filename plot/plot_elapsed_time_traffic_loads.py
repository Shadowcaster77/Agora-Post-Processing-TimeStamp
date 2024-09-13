"""
This script plot the elapsed time across traffic loads.

Author: cstandy
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import sys

import plot_time_utils

sys.path.append('..')
from python import read_elapsed_time

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

    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-02-29_15-35-31.log'
    # elapsed_time_np_1x1_50mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)
    # log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/2024-02-29_15-31-07.log'
    # elapsed_time_np_2x2_50mhz = plot_time_utils.read_elapsed_time_from_file(log_path, True, 1500)

    num_samples = 100000

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    data_1x1_100mhz = [0.0960, 0.1357, 0.1812, 0.2152]
    data_1x1_200mhz = [0.1245, 0.2172, 0.2842, 0.3646]
    data_2x2_100mhz = [0.1448, 0.2225, 0.3126, 0.3154]
    data_1x1_400mhz = [0.1679, 0.3429, 0.5517, 0.8260]
    data_2x2_200mhz = [0.2337, 0.3798, 0.5529, 0.8862]
    data_4x4_100mhz = [0.2536, 0.4885, 0.8711, 0.9330]

    plt.plot(data_1x1_100mhz, marker='o', label='1x1 100MHz', linewidth=3, markersize=10)
    plt.plot(data_1x1_200mhz, marker='o', label='1x1 200MHz', linewidth=3, markersize=10)
    plt.plot(data_2x2_100mhz, marker='o', label='2x2 100MHz', linewidth=3, markersize=10)
    plt.plot(data_1x1_400mhz, marker='o', label='1x1 400MHz', linewidth=3, markersize=10)
    plt.plot(data_2x2_200mhz, marker='o', label='2x2 200MHz', linewidth=3, markersize=10)
    plt.plot(data_4x4_100mhz, marker='o', label='4x4 100MHz', linewidth=3, markersize=10)

    # Plot 3TTI deadline
    plt.axhline(y = 0.375, color = 'r', linestyle='--', linewidth=3)
    plt.figtext(0.22, 0.34, f'0.375 msec', fontsize=24, ha='center')

    # plt.xlim(min(elapsed_time_np), 0.4)
    # plt.xlim(0, 2)
    # plt.xlim(0.1, 10)
    # plt.ylim(10e-6, 1)
    # plt.yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1, 1])
    # plt.xscale("log")
    # plt.yscale("log")
    # title = 'Elapsed Time CDF'
    # plt.title(title, fontsize=titlesize)
    plt.xlabel('Traffic Loads')
    plt.ylabel('Elapsed Time (ms)')
    # plt.grid()
    plt.grid(True, which="both")
    plt.legend(fontsize=24)
    plt.savefig(
        output_filepath + 'elapsed_time_traffic_loads.' + output_format,
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
