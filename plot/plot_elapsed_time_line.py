"""
This script plot the elapsed time across traffic loads.

Author: cstandy
"""

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
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

    FIG_SIZE_W = 7
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

    # The elapsed time for each traffic load. 99.9% percentile in 100K samples.
    # --no-wait options
    x_axis = [1, 2, 3, 4, 5, 7, 9, 13, 17, 21, 25, 29, 33]
    # agora_1x1_400mhz = [np.nan, 7.2069, 4.1202, 2.3256, 1.7103, 2.5523, 4.9587]
    # agora_2x2_200mhz = [np.nan, 5.0115, 2.7782, 1.6467, 1.2990, 1.6930, 2.7745]
    # agora_4x4_100mhz = [np.nan, 5.2073, 2.8955, 1.6130, 0.8388, 0.8966, 2.0417]
    # our_1x1_400mhz = [np.nan, 1.4427, 0.8657, 0.5617, 0.4460, 0.4227, 0.6760]
    # our_2x2_200mhz = [np.nan, 1.5736, 0.8086, 0.4238, 0.3227, 0.2926, 0.4270]
    # our_4x4_100mhz = [np.nan, 2.1855, 1.2934, 0.5937, 0.3986, 0.3396, 0.4213]
    # sc_1x1_400mhz = [0.8260, np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    # sc_2x2_200mhz = [0.8577, np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    # sc_4x4_100mhz = [1.1132, np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]

    # # 99.9% cpu time
    # agora_2x2_100mhz = [np.nan, 3.0209, 1.7144, 0.8088, 0.7286, 0.3580, 0.2562]
    # mc_2x2_100mhz = [np.nan, 1.2559, 0.5573, 0.3124, 0.2220, 0.1499, 0.1331]
    # sc_2x2_100mhz = [ 0.2795, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

    # 99.9% elapsed time
    agora_8x8_20mhz = [np.nan, 13.9137, 7.5648, 5.1800, 4.1558, 3.1873, 2.7150,
                       1.9392, 1.9190, 2.1883, 2.8500, 2.2956, 3.0933]
    agora_2x2_100mhz = [np.nan, 3.2422, 1.8335, 1.3262, 0.8994, 0.6863, 0.8304,
                        0.7698, 0.8678, 0.9947, 1.0016, 1.8407, 2.1368]
    mc_2x2_100mhz = [np.nan, 1.3514, 0.5836, 0.4447, 0.3568, 0.3084, 0.2945,
                     0.2518, 0.2481, 0.2553, 0.2821, 0.3273, 0.3248]
    sc_2x2_100mhz = [0.3120, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
                     np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

    # remove the last two data points
    x_axis = x_axis[:-2]
    agora_8x8_20mhz = agora_8x8_20mhz[:-2]
    agora_2x2_100mhz = agora_2x2_100mhz[:-2]
    mc_2x2_100mhz = mc_2x2_100mhz[:-2]
    sc_2x2_100mhz = sc_2x2_100mhz[:-2]

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # plt.plot(x_axis, agora_1x1_400mhz, marker='o', label='Agora 1x1 400MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, agora_2x2_200mhz, marker='o', label='Agora 2x2 200MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, agora_4x4_100mhz, marker='o', label='Agora 4x4 100MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, our_1x1_400mhz, marker='o', label='Savannah-mc 1x1 400MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, our_2x2_200mhz, marker='o', label='Savannah-mc 2x2 200MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, our_4x4_100mhz, marker='o', label='Savannah-mc 4x4 100MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, sc_1x1_400mhz, marker='o', label='Savannah-sc 1x1 400MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, sc_2x2_200mhz, marker='o', label='Savannah-sc 2x2 200MHz', linewidth=3, markersize=10)
    # plt.plot(x_axis, sc_4x4_100mhz, marker='o', label='Savannah-sc 4x4 100MHz', linewidth=3, markersize=10)

    # plt.plot(x_axis, agora_8x8_20mhz, marker='x', label='Agora-FR1', linewidth=5, markersize=20, markeredgewidth=5, linestyle=':', color='tab:gray')
    # plt.plot(x_axis, agora_2x2_100mhz, marker='o', label='Agora-FR2', linewidth=5, markersize=20, color='tab:blue') # Agora
    # plt.plot(x_axis, mc_2x2_100mhz, marker='^', label='Savannah-mc-FR2', linewidth=5, markersize=20, color='tab:orange') # Savannah-mc
    # plt.plot(x_axis, sc_2x2_100mhz, marker='s', label='Savannah-sc-FR2', linewidth=0, markersize=20, color='tab:green') # Savannah-sc
    plt.plot(x_axis, agora_8x8_20mhz, marker='x', label='Agora-FR1', linewidth=5, markersize=20, markeredgewidth=5, linestyle=':', color='tab:gray')
    plt.plot(x_axis, agora_2x2_100mhz, marker='o', linewidth=5, markersize=20, color='tab:blue') # Agora
    plt.plot(x_axis, mc_2x2_100mhz, marker='^', linewidth=5, markersize=20, color='tab:orange') # Savannah-mc
    plt.plot(x_axis, sc_2x2_100mhz, marker='s', linewidth=0, markersize=20, color='tab:green') # Savannah-sc



    # Plot 3TTI deadline
    plt.axhline(y = 3, color = 'k', linestyle='--', linewidth=3)
    plt.figtext(0.79, 0.7, f'3 msec', fontsize=24, ha='center')
    plt.axhline(y = 0.375, color = 'r', linestyle='--', linewidth=3)
    plt.figtext(0.74, 0.35, f'0.375 msec', fontsize=24, ha='center')
    # plt.figtext(0.74, 0.31, f'0.375 msec', fontsize=24, ha='center')
    # plt.figtext(0.82, 0.31, f'0.375\nmsec', fontsize=24, ha='center')

    # plt.xlim(0.8, 40)
    # plt.ylim(0.125, 14)
    plt.xlim(-1, 27)
    plt.ylim(0.1, 10)
    # plt.xscale("log", base = 2)
    plt.yscale("log", base = 10)
    # ax.set_xticks([1, 2, 4, 8, 16, 32])
    ax.set_xticks([1, 5, 10, 15, 20, 25])
    # ax.set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5])
    ax.set_yticks([0.1, 0.5, 1, 5, 10])
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:.1f}'))
    plt.xlabel('Number of Cores')
    plt.ylabel('Elapsed Time (msec)')
    # plt.ylabel('CPU Time (ms)')
    # plt.grid()
    plt.grid(True, which="both", linestyle='--')
    plt.legend(fontsize=24)
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend().remove()
    plt.savefig(
        output_filepath + 'time_line.' + output_format,
        format=output_format,
        bbox_inches='tight')

    # # Create a separate legend plot
    # handles, labels = plt.gca().get_legend_handles_labels()
    # legend_fig = plt.figure(figsize=(12, 6))
    # legend_fig.legend(handles, labels, fontsize=24, loc='center', frameon=False, ncol=2)
    # legend_fig.savefig(output_filepath + "legend_time_line." + output_format,
    #                    format=output_format, bbox_inches='tight')
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
