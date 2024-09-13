"""
This script plot the maximum traffic load supported in each configuration in 
a stacked bar chart.

Author: cstandy
"""

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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
    plt.rcParams.update({'hatch.linewidth': 2})

    FIG_SIZE_W = 12
    FIG_SIZE_H = 6

    edgecolor='black'

    bar_width = 0.5
    edgecolor = "black"
    linewidth = 2

#     hatches = ['////', 'xxxx', '....', '||||', '\\\\\\\\', '++++', 'oooo']
    hatches = ['//', '||', '..', 'xx', '\\\\', '++', 'oo']

    ############################################################################
    # Get statistics
    ############################################################################

    config = ['1x1\n100M', '1x1\n200M', '2x2\n100M',
              '1x1\n400M\n50%', '2x2\n200M\n44%', '4x4\n100M\n38%']

    # 99.9% frame time
    fft_time =     [0.0478, 0.0890, 0.0545, 0.0941, 0.0766, 0.0388]
    csi_time =     [0.0032, 0.0073, 0.0100, 0.0131, 0.0309, 0.0384]
    bw_time =      [0.0027, 0.0059, 0.0046, 0.0089, 0.0184, 0.0394]
    eq_time =      [0.0251, 0.0451, 0.0717, 0.0436, 0.0518, 0.0678]
    demul_time =   [0.0547, 0.1053, 0.0690, 0.1027, 0.0951, 0.0514]
    decode_time =  [0.0483, 0.0688, 0.0698, 0.0716, 0.0638, 0.0598]
    elapsed_time = [0.2149, 0.3578, 0.3120, 0.3539, 0.3652, 0.3335]
    misc = []
    for i in range(len(config)):
        misc.append(elapsed_time[i] - sum([fft_time[i], csi_time[i], bw_time[i], eq_time[i], demul_time[i], decode_time[i]]))

    ############################################################################
    # Plot 
    ############################################################################

    x = np.arange(len(config))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

    # Draw the hatch
    plt.bar(config, fft_time, label='FFT',
            zorder=3, hatch=hatches[0], color='white',
            width=bar_width, edgecolor='tab:blue', linewidth=linewidth)
    bottom = fft_time
    plt.bar(config, csi_time, bottom=bottom, label='CSI',
            zorder=3, hatch=hatches[1], color='white',
            width=bar_width, edgecolor='tab:brown', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, csi_time)]
    plt.bar(config, bw_time, bottom=bottom, label='Precode',
            zorder=3, hatch=hatches[2], color='white',
            width=bar_width, edgecolor='tab:purple', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, bw_time)]
    plt.bar(config, eq_time, bottom=bottom, label='Equal',
            zorder=3, hatch=hatches[3], color='white',
            width=bar_width, edgecolor='tab:orange', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, eq_time)]
    plt.bar(config, demul_time, bottom=bottom, label='Demod',
            zorder=3, hatch=hatches[4], color='white',
            width=bar_width, edgecolor='tab:green', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, demul_time)]
    plt.bar(config, decode_time, bottom=bottom, label='Decode',
            zorder=3, hatch=hatches[5], color='white',
            width=bar_width, edgecolor='tab:red', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, decode_time)]
    plt.bar(config, misc, bottom=bottom, label='Misc',
            zorder=3, hatch=hatches[6], color='white',
            width=bar_width, edgecolor='tab:gray', linewidth=linewidth)

    # Draw the bar
    plt.bar(config, fft_time, 
            zorder=3, color='none',
            width=bar_width, edgecolor=edgecolor,linewidth=linewidth)
    bottom = fft_time
    plt.bar(config, csi_time, bottom=bottom,
            zorder=3, color='none',
            width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, csi_time)]
    plt.bar(config, bw_time, bottom=bottom,
            zorder=3, color='none',
            width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, bw_time)]
    plt.bar(config, eq_time, bottom=bottom,
            zorder=3, color='none',
            width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, eq_time)]
    plt.bar(config, demul_time, bottom=bottom,
            zorder=3, color='none',
            width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, demul_time)]
    plt.bar(config, decode_time, bottom=bottom,
            zorder=3, color='none',
            width=bar_width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, decode_time)]
    plt.bar(config, misc, bottom=bottom,
            zorder=3, color='none',
            width=bar_width, edgecolor=edgecolor, linewidth=linewidth)

    # Plot 3TTI deadline & mark statistics
    plt.axhline(y = 0.375, color = 'r', linestyle='--', linewidth=3)
    plt.figtext(0.205, 0.70, f'0.375 msec', fontsize=22, ha='center',
                color='r')

    plt.ylim(0, 0.45)
    plt.ylabel('Time (msec)')
    plt.grid(zorder=0, linestyle='--')
    plt.legend(fontsize=22, loc='upper right', ncol=4, fancybox=True, frameon=True,
               bbox_to_anchor=(1.01, 1.15))
#     handles, labels = plt.gca().get_legend_handles_labels()
#     plt.legend().remove()
    plt.savefig(
        output_filepath + 'time_stacked_bar_traffic_load.' + output_format,
        format=output_format,
        bbox_inches='tight')
    
    # # Create a separate legend plot
    # legend_fig = plt.figure(figsize=(6, 0.5))
    # legend = legend_fig.legend(handles, labels, fontsize=20, loc='center', frameon=False, ncol=3)
    # legend_fig.savefig(
    #     output_filepath + 'legend_time_stacked_bar.' + output_format,
    #     format=output_format,
    #     bbox_inches='tight')
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
