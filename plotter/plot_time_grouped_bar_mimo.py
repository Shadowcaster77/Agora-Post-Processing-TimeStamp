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
    plt.rcParams.update({'hatch.linewidth': 2})

    FIG_SIZE_W = 8
    FIG_SIZE_H = 6.5

    edgecolor='black'

    bar_width = 0.5
    edgecolor = "black"
    linewidth = 2

#     hatches = ['////', 'xxxx', '....', '||||', '\\\\\\\\', '++++', 'oooo']
    hatches = ['//', 'xx', '\\\\', '++', '--', '..', 'oo']
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:gray']

    ############################################################################
    # Get statistics
    ############################################################################

    # 100 MHz links, MCS17
    dsp_stages = [r'1$\times$1', r'2$\times$2', r'4$\times$4']
    config = ['Agora', 'Savannah-mc',
              'Savannah-mc (arma-vec)', 'Savannah-mc (arma-cube)']
    x_values = np.arange(len(dsp_stages))

    # Agora
    # 1x1: 2024-03-11_14-49-13.log (4 cores, 3 workers, relax 5 more slots)
    # 2x2: 2024-03-07_13-20-57.log (5 cores, 4 workers, relax 5 more slots)
    # 4x4: 2024-03-11_14-52-58.log (21 cores, 20 workers, relax 5 more slots)
    # Savannah-mc (avx512):
    # 1x1: 2024-03-11_14-37-24.log (4 cores, 3 workers)
    # 2x2: 2024-03-07_12-59-33.log (5 cores, 4 workers)
    # 4x4: 2024-03-10_20-52-48.log (21 cores, 20 workers)
    # Savannah-mc (arma-vec):
    # 1x1: 2024-08-02_01-01-17.log (4 cores, 3 workers)
    # 2x2: 2024-08-02_01-04-20.log (5 cores, 4 workers)
    # 4x4: 2024-08-02_01-07-41.log (21 cores, 20 workers)
    # Savannah-mc (arma-cube):
    # 1x1: 2024-08-03_20-06-22.log (4 cores, 3 workers)
    # 2x2: 2024-08-03_20-03-03.log (5 cores, 4 workers)
    # 4x4: 2024-08-03_19-52-02.log (21 cores, 20 workers, relax 15 more slots)


    # take average time over 103,000 frames (cropped to 100,000 frames)
    # mcs17

    # # BW Time, average time per frame
    # siso_time =     [0.1068*3, 0.0004*3]
    # mimo_2x2_time = [0.1346*4, 0.0011*4]
    # mimo_4x4_time = [0.0781*20, 0.0023*20]
    # siso_time =     [0.1068*3, 0.0004*3, 0.0006*3]
    # mimo_2x2_time = [0.1346*4, 0.0011*4, 0.0035*4]
    # mimo_4x4_time = [0.0781*20, 0.0023*20, 0.0104*20]
    siso_time =     [0.1068*3, 0.0004*3, 0.0006*3, 0.0006*3]
    mimo_2x2_time = [0.1346*4, 0.0011*4, 0.0035*4, 0.0196*4]
    mimo_4x4_time = [0.0781*20, 0.0023*20, 0.0104*20, 0.0808*20]

    # # EQ Time, average time per frame
    # siso_time =     [0.3796*3, 0.0087*3]
    # mimo_2x2_time = [0.3878*4, 0.0174*4]
    # mimo_4x4_time = [0.1113*20, 0.0087*20]
    # siso_time =     [0.3796*3, 0.0132*3, 0.0160*3]
    # mimo_2x2_time = [0.3878*4, 0.0174*4, 0.0292*4]
    # mimo_4x4_time = [0.1113*20, 0.0087*20, 0.0175*20]
    # siso_time =     [0.3796*3, 0.0132*3, 0.0160*3, 0.0156*3]
    # mimo_2x2_time = [0.3878*4, 0.0174*4, 0.0292*4, 0.0764*4]
    # mimo_4x4_time = [0.1113*20, 0.0087*20, 0.0175*20, 0.0429*20]

    # when reproduce on Jul 29, 2024, the siso eq time for avx512 is ~0.0132 ms
    # log: 2024-07-30_00-42-40.log (savannah-mc, 1x1, 4 cores, 3 workers)


    time = {
        'Agora': [siso_time[0], mimo_2x2_time[0], mimo_4x4_time[0]],
        'Savannah-mc': [siso_time[1], mimo_2x2_time[1], mimo_4x4_time[1]],
        'Savannah-mc (arma-vec)': [siso_time[2], mimo_2x2_time[2], mimo_4x4_time[2]],
        'Savannah-mc (arma-cube)': [siso_time[3], mimo_2x2_time[3], mimo_4x4_time[3]]
    }

    factor_agora = []
    factor_armavec = []
    factor_armacube = []
    for i in range(len(dsp_stages)):
        factor_agora.append(time[config[0]][i]/time[config[1]][i])
        factor_armavec.append(time[config[2]][i]/time[config[1]][i])
        factor_armacube.append(time[config[3]][i]/time[config[1]][i])

    ############################################################################
    # Plot 
    ############################################################################

    x = np.arange(len(dsp_stages))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

    # Draw the hatch
    multiplier = 0
    for attribute, val in time.items():
        offset = width * multiplier
        rects = ax.bar(x + offset - 0.3, val, width, label=attribute,
                       hatch = hatches[multiplier], zorder=3,
                       color='white', edgecolor=colors[multiplier], linewidth=linewidth)
        # ax.bar_label(rects, padding=3, fmt='{:.0%}')
        multiplier += 1

    # Draw the bar
    multiplier = 0
    for attribute, val in time.items():
        offset = width * multiplier
        rects = ax.bar(x + offset - 0.3, val, width,
                       zorder=3,
                       color='none', edgecolor=edgecolor, linewidth=linewidth)
        # ax.bar_label(rects, padding=3, fmt='{:.0%}')
        multiplier += 1

    # Plot relation between two sets of bars in factor_agoras
    for i, factor in enumerate(factor_agora):
        plt.annotate(r'{:.1f}$\times$'.format(factor),
            (i - 0.3, time['Agora'][i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center', fontsize=18)
    for i, factor in enumerate(factor_armavec):
        plt.annotate(r'{:.1f}$\times$'.format(factor),
            (i + 0.05, time['Savannah-mc (arma-vec)'][i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center', fontsize=18)
    for i, factor in enumerate(factor_armacube):
        offset = 0.35 if i == 0 else 0.3
        plt.annotate(r'{:.1f}$\times$'.format(factor),
            (i + offset, time['Savannah-mc (arma-cube)'][i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center', fontsize=18)

    # plt.ylim(0, 0.5)
    plt.ylim(0.001, 10)
    plt.yscale("log")
    plt.xticks(x_values, dsp_stages) # bring back the original x-axis labels
    plt.ylabel('Cumulative CPU Time (ms)')
    plt.grid(zorder=0, linestyle='--', which='both')
    plt.legend(fontsize=24, loc='lower left', ncol=2, fancybox=True, frameon=True,
               bbox_to_anchor=(-0.24, -0.28))
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend().remove()
    plt.savefig(
        output_filepath + 'time_grouped_bar_mimo.' + output_format,
        format=output_format,
        bbox_inches='tight')
    
    # Create a separate legend plot
    legend_fig = plt.figure(figsize=(6, 0.5))
    legend = legend_fig.legend(handles, labels, fontsize=40, loc='center', frameon=False, ncol=4)
    legend_fig.savefig(
        output_filepath + 'legend_time_grouped_bar_mimo_revised.' + output_format,
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
