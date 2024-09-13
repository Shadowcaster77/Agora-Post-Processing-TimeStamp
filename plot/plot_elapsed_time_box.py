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

    # Read from MCS 17, 2x2 MIMO, 100 MHz, 100K frame across number of cores
    log_path = '/home/ct297/workspace/agora_single-core-sim-hw-ldpc/log/'

    # Elapsed time
    agora_1c = np.nan
    log_file = log_path + '2024-03-07_13-45-19' + '.log'
    agora_2c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_13-30-50' + '.log'
    agora_3c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_17-41-00' + '.log'
    agora_4c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_13-20-57' + '.log'
    agora_5c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_17-45-39' + '.log'
    agora_7c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_13-24-48' + '.log'
    agora_9c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_17-58-25' + '.log'
    agora_13c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_13-13-23' + '.log'
    agora_17c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_18-02-28' + '.log'
    agora_21c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_18-05-38' + '.log'
    agora_25c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    # log_file = log_path + '2024-03-08_18-09-01' + '.log'
    # agora_29c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    # log_file = log_path + '2024-03-07_13-08-58' + '.log'
    # agora_33c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)

    mc_1c = np.nan
    log_file = log_path + '2024-03-07_13-04-31' + '.log'
    mc_2c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_13-01-30' + '.log'
    mc_3c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_18-27-23' + '.log'
    mc_4c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_12-59-33' + '.log'
    mc_5c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_18-25-24' + '.log'
    mc_7c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_12-55-53' + '.log'
    mc_9c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_18-22-09' + '.log'
    mc_13c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-07_12-53-39' + '.log'
    mc_17c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_18-19-12' + '.log'
    mc_21c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    log_file = log_path + '2024-03-08_18-17-04' + '.log'
    mc_25c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    # log_file = log_path + '2024-03-08_18-14-24' + '.log'
    # mc_29c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)
    # log_file = log_path + '2024-03-07_12-35-20' + '.log'
    # mc_33c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 1500)

    log_file = log_path + '2024-03-06_20-25-08' + '.log'
    sc_1c = plot_time_utils.read_elapsed_time_from_file(log_file, True, 50000)

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

    # The elapsed time for each traffic load. 99.9% percentile in 100K samples.
    # --no-wait options
    x_axis = [1, 2, 3, 4, 5, 7, 9, 13, 17, 21, 25]

    # Scale the width of the boxplot
    # w = 0.05
    # width = lambda p, w: 10**(np.log10(p)+w/2.)-10**(np.log10(p)-w/2.)

    color_agora = 'tab:blue'
    l = 2
    bp1 = ax.boxplot(
        [agora_1c, agora_2c, agora_3c, agora_4c, agora_5c, agora_7c, agora_9c,
         agora_13c, agora_17c, agora_21c, agora_25c],
        positions=x_axis, widths=1.5, #widths=width(x_axis, w),
        patch_artist=True, showfliers=False,
        boxprops=dict(facecolor="white", color=color_agora, linewidth=l),
        whiskerprops=dict(color=color_agora, linewidth=l),
        capprops=dict(color=color_agora, linewidth=l),
        medianprops=dict(color='black', linewidth=l+1))
    for patch in bp1['boxes']:
        # patch.set_hatch(hatches[j])
        patch.set_facecolor(color_agora)
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .3))
    
    color_mc = 'tab:orange'
    bp2 = plt.boxplot(
        [mc_1c, mc_2c, mc_3c, mc_4c, mc_5c, mc_7c, mc_9c, mc_13c, mc_17c,
         mc_21c, mc_25c],
        positions=x_axis, widths=1.5, #widths=width(x_axis, w),
        patch_artist=True, showfliers=False,
        boxprops=dict(facecolor="white", color=color_mc, linewidth=l),
        whiskerprops=dict(color=color_mc, linewidth=l),
        capprops=dict(color=color_mc, linewidth=l),
        medianprops=dict(color='black', linewidth=l+1))
    for patch in bp2['boxes']:
        # patch.set_hatch(hatches[j])
        patch.set_facecolor(color_mc)
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .3))
    
    color_sc = 'tab:green'
    bp3 = plt.boxplot(
        [sc_1c, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 
         np.nan, np.nan, np.nan, np.nan],
        positions=x_axis, widths=1.5, #widths=width(x_axis, w),
        patch_artist=True, showfliers=False,
        boxprops=dict(facecolor="white", color=color_sc, linewidth=l),
        whiskerprops=dict(color=color_sc, linewidth=l),
        capprops=dict(color=color_sc, linewidth=l),
        medianprops=dict(color='black', linewidth=l+1))
    for patch in bp3['boxes']:
        # patch.set_hatch(hatches[j])
        patch.set_facecolor(color_sc)
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .3))
    
    median_agora = [np.median(agora_1c), np.median(agora_2c),
                    np.median(agora_3c), np.median(agora_4c),
                    np.median(agora_5c), np.median(agora_7c),
                    np.median(agora_9c), np.median(agora_13c),
                    np.median(agora_17c), np.median(agora_21c),
                    np.median(agora_25c)]
    median_mc = [np.median(mc_1c), np.median(mc_2c), np.median(mc_3c),
                 np.median(mc_4c), np.median(mc_5c), np.median(mc_7c),
                 np.median(mc_9c), np.median(mc_13c), np.median(mc_17c),
                 np.median(mc_21c), np.median(mc_25c)]

    plt.plot(x_axis, median_agora, c=color_agora, linestyle='--', linewidth=l, label='Agora')
    plt.plot(x_axis, median_mc, c=color_mc, linestyle='--', linewidth=l, label='Savannah-mc')
    plt.plot([], [], c=color_sc, linestyle='--', linewidth=l, label='Savannah-sc')

    # Plot 3TTI deadline
    plt.axhline(y = 0.375, color = 'r', linestyle='--', linewidth=3)
    plt.figtext(0.75, 0.34, f'0.375 msec', fontsize=24, ha='center')

    plt.xlim(-2, 28)
    # plt.ylim(0.1, 14)
    # plt.ylim(0, 4)
    # plt.xscale("log", base = 2)
    plt.yscale("log", base = 10)
    # ax.set_xticks([1, 2, 4, 8, 16, 32])
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.set_yticks([0.1, 0.5, 1, 5, 10])
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:.1f}'))
    plt.xlabel('Num of Cores')
    plt.ylabel('Elapsed Time (ms)')
    # plt.ylabel('CPU Time (ms)')
    # plt.grid()
    plt.grid(True, which="both", linestyle='--')
    leg = ax.legend(fontsize=24)
    # change the line width for the legend
    for line in leg.get_lines():
        line.set_linewidth(8.0)
        line.set_linestyle('-')
    plt.savefig(
        output_filepath + 'time_elapsed_box.' + output_format,
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
