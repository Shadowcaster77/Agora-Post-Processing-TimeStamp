"""
This script plot the maximum traffic load supported in each configuration in 
a groupped bar chart.

Author: cstandy
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

    mimo_size = ['1x1', '2x2', '4x4']
    traffic_load = {
        '100 MHz': (1, 1, 0.375),
        '200 MHz': (1, 0.4375, 0),
        '400 MHz': (0.5, 0, 0),
    }

    hatches = ['/', 'o', '.']

    ############################################################################
    # Plot 
    ############################################################################

    x = np.arange(len(mimo_size))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

    for attribute, val in traffic_load.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, val, width, label=attribute, hatch = hatches[multiplier])
        ax.bar_label(rects, padding=3, fmt='{:.0%}')
        multiplier += 1

    # plt.xlim(min(elapsed_time_np), 0.4)
    # plt.xlim(0, 1.6)
    # plt.xlim(0.1, 10)
    # plt.ylim(10e-6, 1)
    plt.xticks(x + width, mimo_size)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    # plt.yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1, 1])
    # plt.xscale("log")
    # plt.yscale("log")
    # title = 'Elapsed Time CDF'
    # plt.title(title, fontsize=titlesize)
    plt.xlabel('MIMO Dimension')
    plt.ylabel('Traffic Loads')
    plt.grid()
    # plt.grid(True, which="both")
    plt.legend(fontsize=20)
    plt.savefig(
        output_filepath + 'traffic_load_bar.' + output_format,
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
