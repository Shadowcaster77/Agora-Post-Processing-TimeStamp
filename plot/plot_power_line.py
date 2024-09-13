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

    ref_power = 93.55
    pcie_power = 15.6

    # Given data
    cores = np.array([2, 3, 4, 5, 7, 9, 13, 17, 21, 25, 29, 33])  # Representing the number of cores
    agora_socket1 = np.array([98.34, 99.31, 98.69 , 98.29, 98.08, 98.84, 98.27, 99.32, 92.31, 97.25, 131.65, 162.17])
    agora_socket2 = np.array([117.71, 124.89, 135.12, 137.39, 157.48, 168.09, 200.89, 227.25, 234.66, 253.57, 253.38 +(131.65-97.25), 253.52+(162.17-99.32)])
    agora_socket2 = agora_socket2 - 93.55

    savannah_mc_socket1 = np.array([99.13, 97.93, 97.89, 99.1, 98.23, 99.14, 98.11, 98.83, 98.62, 97.92,	133.45, 162.18])
    savannah_mc_socket2 = np.array([118.34, 124.06, 131.38, 138.04, 152.38, 168.44, 198.45, 223.6, 234.98, 254.97, 253.75 +(133.45-99.32), 250.52+(162.18-98.83)])
    savannah_mc_socket2 = savannah_mc_socket2 - 93.55

    savannah_sc_socket1 = 94.2 - 61.07
    savannah_sc_socket2 = 118.24 - 93.55 + 15.6 - 15.6 # 15.6 is the standy power
    savannah_sc_total = savannah_sc_socket1 + savannah_sc_socket2 + 15.6

    # align the data points
    x_axis = [1, 2, 3, 4, 5, 7, 9, 13, 17, 21, 25, 29, 33]
    agora = np.insert(agora_socket2, 0, np.nan, axis=0)
    mc = np.insert(savannah_mc_socket2, 0, np.nan, axis=0)
    sc = np.array([savannah_sc_socket2, np.nan, np.nan, np.nan, np.nan, np.nan,
                   np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])

    # remove the last two data points
    x_axis = x_axis[:-2]
    agora = agora[:-2]
    mc = mc[:-2]
    sc = sc[:-2]

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.plot(x_axis, agora, marker='o', label='Agora', linewidth=5, markersize=20)
    plt.plot(x_axis, mc, marker='^', label='Savannah-mc', linewidth=5, markersize=20, linestyle=':')
    plt.plot(x_axis, sc, marker='s', label='Savannah-sc', linewidth=0, markersize=20)

    # Plot 3TTI deadline
    # plt.axhline(y = 0.375, color = 'r', linestyle='--', linewidth=3)
    # plt.figtext(0.74, 0.31, f'0.375 msec', fontsize=24, ha='center')
    # plt.figtext(0.82, 0.31, f'0.375\nmsec', fontsize=24, ha='center')

    # plt.xlim(0.8, 40)
    # plt.ylim(16, 256)
    # plt.xscale("log", base = 2)
    # plt.yscale("log", base = 10)
    # ax.set_xticks([1, 2, 4, 8, 16, 32])
    plt.xlim(-1, 27)
    plt.ylim(0, 200)
    ax.set_xticks([1, 5, 10, 15, 20, 25])
    # ax.set_yticks([1, 10, 100])
    ax.xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
    plt.xlabel('Number of Cores')
    plt.ylabel('Power (W)')
    # plt.grid()
    plt.grid(True, which="both", linestyle='--')
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend().remove()
    # plt.legend(fontsize=24)
    plt.savefig(
        output_filepath + 'power_line.' + output_format,
        format=output_format,
        bbox_inches='tight')
    
    # Create a separate legend plot
    handles, labels = plt.gca().get_legend_handles_labels()
    legend_fig = plt.figure(figsize=(12, 6))
    legend_fig.legend(handles, labels, fontsize=24, loc='center', frameon=False, ncol=4)
    legend_fig.savefig(output_filepath + "legend_power_line." + output_format,
                       format=output_format, bbox_inches='tight')
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
