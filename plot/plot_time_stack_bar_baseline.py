"""
This script plot the CPU time breakdown of Agora/our work in a groupped bar chart.

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

    FIG_SIZE_W = 5
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

    # 2x2, 100 MHz
    config = ['Agora\n(5 cores)', 'Savannah-5c']
    x_values = np.arange(len(config))

    # average frame time
    fft_time =     [0.0150, 0.0153]
    csi_time =     [0.0064, 0.0026]
    bw_time =      [0.1346, 0.0011]
    eq_time =      [0.3878, 0.0174]
    demul_time =   [0.0201, 0.0175]
    decode_time =  [0.2140, 0.2205]
    elapsed_time = [0.8622, 0.3140]

    # # 99.9% frame time
    # fft_time =     [0.0403, 0.0150]
    # csi_time =     [0.0045, 0.0026]
    # bw_time =      [0.1380, 0.0011]
    # eq_time =      [0.3908, 0.0176]
    # demul_time =   [0.0210, 0.0174]
    # decode_time =  [0.2141, 0.1588]
    # elapsed_time = [0.8994, 0.3568]
    misc = []
    for i in range(len(config)):
        misc.append(elapsed_time[i] - sum([fft_time[i], csi_time[i], bw_time[i], eq_time[i], demul_time[i], decode_time[i]]))

    ############################################################################
    # Plot 
    ############################################################################

    x = np.arange(len(config))  # the label locations
    width = 0.4  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

    # Draw the hatch
    plt.bar(x_values,fft_time, label='FFT',
            zorder=3, hatch=hatches[0], color='white',
            width=width, edgecolor='tab:blue', linewidth=linewidth)
    bottom = fft_time
    plt.bar(x_values,csi_time, bottom=bottom, label='CSI',
            zorder=3, hatch=hatches[1], color='white',
            width=width, edgecolor='tab:brown', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, csi_time)]
    plt.bar(x_values,bw_time, bottom=bottom, label='Precode',
            zorder=3, hatch=hatches[2], color='white',
            width=width, edgecolor='tab:purple', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, bw_time)]
    plt.bar(x_values,eq_time, bottom=bottom, label='Equal',
            zorder=3, hatch=hatches[3], color='white',
            width=width, edgecolor='tab:orange', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, eq_time)]
    plt.bar(x_values,demul_time, bottom=bottom, label='Demod',
            zorder=3, hatch=hatches[4], color='white',
            width=width, edgecolor='tab:green', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, demul_time)]
    plt.bar(x_values,decode_time, bottom=bottom, label='Decode',
            zorder=3, hatch=hatches[5], color='white',
            width=width, edgecolor='tab:red', linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, decode_time)]
    plt.bar(x_values,misc, bottom=bottom, label='Misc',
            zorder=3, hatch=hatches[6], color='white',
            width=width, edgecolor='tab:gray', linewidth=linewidth)

    # Draw the bar
    plt.bar(x_values,fft_time,
            zorder=3, color='none',
            width=width, edgecolor=edgecolor,linewidth=linewidth)
    bottom = fft_time
    plt.bar(x_values,csi_time, bottom=bottom,
            zorder=3, color='none',
            width=width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, csi_time)]
    plt.bar(x_values,bw_time, bottom=bottom,
            zorder=3, color='none',
            width=width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, bw_time)]
    plt.bar(x_values,eq_time, bottom=bottom,
            zorder=3, color='none',
            width=width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, eq_time)]
    plt.bar(x_values,demul_time, bottom=bottom,
            zorder=3, color='none',
            width=width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, demul_time)]
    plt.bar(x_values,decode_time, bottom=bottom,
            zorder=3, color='none',
            width=width, edgecolor=edgecolor, linewidth=linewidth)
    bottom = [x + y for x, y in zip(bottom, decode_time)]
    plt.bar(x_values,misc, bottom=bottom,
            zorder=3, color='none',
            width=width, edgecolor=edgecolor, linewidth=linewidth)

    # Plot 3TTI deadline & mark statistics
    plt.axhline(y = 0.375, color = 'r', linestyle='--', linewidth=3, zorder=10)
    plt.figtext(0.66, 0.43, f'0.375 msec', fontsize=24, ha='center')

    plt.xlim(-0.5, 1.5)
    plt.ylim(0, 1)
    plt.xticks(x_values, config) # bring back the original x-axis labels
    plt.ylabel('Time (msec)')
    plt.grid(zorder=0, linestyle='--')
    plt.legend(fontsize=24, loc='upper right', ncol=1, fancybox=True, frameon=True,
               bbox_to_anchor=(1.31, 0.9))
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend().remove()
    plt.savefig(
        output_filepath + 'time_stacked_bar_baseline.' + output_format,
        format=output_format,
        bbox_inches='tight')
    
    # Create a separate legend plot
    legend_fig = plt.figure(figsize=(6, 0.5))
    legend = legend_fig.legend(handles, labels, fontsize=20, loc='center', frameon=False, ncol=1)
    legend_fig.savefig(
        output_filepath + 'legend_time_stacked_bar.' + output_format,
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
