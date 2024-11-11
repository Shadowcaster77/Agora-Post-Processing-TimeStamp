"""
This script plot the elapsed time in groupped box plot.

Author: cstandy
"""

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
from optparse import OptionParser
import numpy as np
import pandas as pd
import seaborn as sns
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

    # Colors for each box in the group
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']
    legend_labels = ['1x1, 100MHz', '1x1, 200MHz', '2x2, 100MHz'] #, '1x1, 400MHz', '2x2, 200MHz', '4x4, 100MHz']
    hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']

    # Creating legend patches
    legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, legend_labels)]

    ############################################################################
    # Get statistics
    ############################################################################

    df_100mhz = pd.read_excel('../data/time_elapsed_mu3_traffic_loads.xlsx', sheet_name='100MHz')
    df_200mhz = pd.read_excel('../data/time_elapsed_mu3_traffic_loads.xlsx', sheet_name='200MHz')
    df_400mhz = pd.read_excel('../data/time_elapsed_mu3_traffic_loads.xlsx', sheet_name='400MHz')

    legend_labels = ['1x1, 100MHz',
                     '1x1, 200MHz',
                     '2x2, 100MHz',]
                #      '1x1, 400MHz',
                #      '2x2, 200MHz',
                #      '4x4, 100MHz']

    # average, 99%, 99.9%
    data = {
        '25%': [[0.0623, 0.0911, 0.0960],
                [0.0944, 0.1025, 0.1245],
                [0.1114, 0.1233, 0.1448],
                [0.1522, 0.1590, 0.1679],
                [0.1761, 0.1880, 0.2337],
                [0.2368, 0.2480, 0.2538],],
        '50%': [[0.1027, 0.1220, 0.1357],
                [0.1521, 0.1769, 0.2172],
                [0.1688, 0.1760, 0.2225],
                [0.2561, 0.2851, 0.3429],
                [0.2810, 0.2911, 0.3798],
                [0.3638, 0.3754, 0.4885]],
        '75%': [[0.1389, 0.1547, 0.1812],
                [0.2027, 0.2312, 0.2842],
                [0.2317, 0.2455, 0.3126],
                [0.3428, 0.3649, 0.5517],
                [0.3897, 0.4059, 0.5529],
                [0.4945, 0.5080, 0.8711]],
        '100%': [[0.1718, 0.1855, 0.2152], 
                 [0.2498, 0.2791, 0.3646],
                 [0.2943, 0.3056, 0.3154],
                 [0.4511, 0.4787, 0.8260],
                 [0.5025, 0.5162, 0.8862],
                 [0.7009, 0.9101, 0.9330]]
    }

    # min, first quartile , median, 3rd quartile, 99.9% for mcs28
    data = {
        '25%': [[0.0682, 0.0763, 0.0847, 0.0950, 0.1123],
                [0.0879, 0.0926, 0.0938, 0.0956, 0.1245],
                [0.0994, 0.1104, 0.1126, 0.1164, 0.1535],
                [0.1460, 0.1508, 0.1519, 0.1532, 0.1679],
                [0.1624, 0.1730, 0.1753, 0.1781, 0.2337],
                [0.2293, 0.2344, 0.2361, 0.2384, 0.2538]],
        '50%': [[0.0902, 0.1018, 0.1049, 0.1130, 0.1378],
                [0.1355, 0.1464, 0.1490, 0.1562, 0.2172],
                [0.1633, 0.1693, 0.1707, 0.1724, 0.2277],
                [0.2356, 0.2478, 0.2520, 0.2611, 0.3429],
                [0.2663, 0.2776, 0.2805, 0.2835, 0.3798],
                [0.3500, 0.3607, 0.3628, 0.3656, 0.4885]],
        '75%': [[0.1202, 0.1371, 0.1392, 0.1468, 0.1739],
                [0.1865, 0.1949, 0.1982, 0.2079, 0.2842],
                [0.2210, 0.2306, 0.2337, 0.2368, 0.3200],
                [0.3277, 0.3385, 0.3414, 0.3447, 0.5517],
                [0.3689, 0.3846, 0.3886, 0.3934, 0.5529],
                [0.4743, 0.4900, 0.4931, 0.4964, 0.8711]],
        '100%': [[0.1493, 0.1724, 0.1736, 0.1782, 0.2149],
                 [0.2359, 0.2441, 0.2467, 0.2508, 0.3646],
                 [0.2772, 0.2918, 0.2938, 0.2962, 0.3154],
                 [0.4196, 0.4386, 0.4486, 0.4598, 0.8260],
                 [0.4895, 0.4982, 0.5010, 0.5040, 0.8862],
                 [0.6012, 0.6258, 0.6298, 0.8595, 0.9330]],
    }

    # min, first quartile , median, 3rd quartile, 99.9% for mcs17
    data = {
        '25%': [[0.0566, 0.0598, 0.0611, 0.0630, 0.0977],
                [0.1053, 0.1149, 0.1186, 0.1279, 0.1651],
                [0.1019, 0.1139, 0.1157, 0.1182, 0.1540]],
                # [0.1828, 0.1943, 0.1975, 0.2027, 0.2920],
                # [0.1668, 0.1768, 0.1792, 0.1823, 0.2434],
                # [0.2329, 0.2416, 0.2438, 0.2465, 0.6513]],
        '50%': [[0.0865, 0.0967, 0.1013, 0.1092, 0.1401],
                [0.1762, 0.1865, 0.1896, 0.1984, 0.2646],
                [0.1672, 0.1714, 0.1724, 0.1736, 0.2265]],
                # [0.2520, 0.2672, 0.2708, 0.2776, 0.4387],
                # [0.2737, 0.2833, 0.2858, 0.2889, 0.4009],
                # [0.3589, 0.3679, 0.3699, 0.3727, 0.4945]],
        '75%': [[0.1196, 0.1320, 0.1376, 0.1453, 0.1869],
                [0.1940, 0.2069, 0.2100, 0.2172, 0.3005],
                [0.2237, 0.2329, 0.2354, 0.2379, 0.3159]],
                # [0.3475, 0.3615, 0.3646, 0.3680, 0.7428],
                # [0.3815, 0.3918, 0.3949, 0.3990, 0.6922],
                # [0.4821, 0.4997, 0.5031, 0.5066, 0.8611]],
        '100%': [[0.1500, 0.1671, 0.1706, 0.1762, 0.2271],
                 [0.2409, 0.2507, 0.2533, 0.2567, 0.3489],
                 [0.2881, 0.2937, 0.2954, 0.2976, 0.3120]],
                #  [0.4461, 0.4622, 0.4723, 0.4826, 0.9419],
                #  [0.4909, 0.5034, 0.5070, 0.5116, 0.9636],
                #  [0.6263, 0.6427, 0.6459, 0.6491, 1.1125]],
    }

    ############################################################################
    # Plot 
    ############################################################################

    fig, ax = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

    # Number of boxes per category
    num_boxes = len(next(iter(data.values())))

    pos = []
    l=3

    # Plotting the box figure with self-configured horizontal shift
    for i, (category, stats_list) in enumerate(data.items()):
        positions = []
        for j, stats in enumerate(stats_list):
            # Position of the box in the category
            position = i - 0.2 + (j * 0.2)

            # Box
            # box = ax.boxplot([[stats[0], stats[0], stats[0], stats[1], stats[2]]],
            #                  positions=[position], widths=0.1, manage_ticks=False, patch_artist=True)
            box = ax.boxplot([[stats[0], stats[1], stats[2], stats[3], stats[4]]],
                             positions=[position], widths=0.15, whis=200,
                             manage_ticks=False, patch_artist=True,
                             boxprops=dict(facecolor="white", color=colors[j], linewidth=l),
                             whiskerprops=dict(color=colors[j], linewidth=l),
                             capprops=dict(color=colors[j], linewidth=l),
                             medianprops=dict(color='black', linewidth=l+1))
            
            positions.append(position)


            
            alpha = 0.3 if stats[4] > 0.375 else 0.9

        #     for k, v in box.items():
        #         plt.setp(box.get(k), color=colors[j], alpha=alpha, linewidth=2)
        
            box['medians'][0].set_color('black')

            # Set box face color
            for patch in box['boxes']:
                # patch.set_hatch(hatches[j])
                patch.set_facecolor(colors[j])
                r, g, b, a = patch.get_facecolor()
                patch.set_facecolor((r, g, b, .3))
        pos.append(positions)

    for j in range(len(pos[0])):
        ax.plot([pos[0][j], pos[1][j], pos[2][j], pos[3][j]],
                [data["25%"][j][2], data["50%"][j][2],
                 data["75%"][j][2], data["100%"][j][2]],
                 linestyle='--', linewidth=3, color=colors[j])

    # Customizing the axes
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data.keys())

    # Plot 3TTI deadline
    plt.axhline(y = 0.375, color = 'r', linestyle='--', linewidth=3)
    plt.figtext(0.33, 0.77, f'0.375 msec', fontsize=24, ha='center')

    # plt.xlim(min(elapsed_time_np), 0.4)
    # plt.xlim(0, 2)
    # plt.xlim(0.1, 10)
    plt.ylim(0, 0.4)
    # plt.yticks([10e-6, 10e-5, 10e-4, 10e-3, 10e-2, 10e-1, 1])
    # plt.xscale("log")
    # plt.yscale("log")
    # title = 'Elapsed Time CDF'
    # plt.title(title, fontsize=titlesize)
    plt.xlabel('Traffic Loads')
    plt.ylabel('Elapsed time (msec)')
    # plt.grid()
    plt.grid(True, which="both", linestyle='--')
    # Adding the legend
    ax.legend(handles=legend_patches, fontsize=24)
    # plt.legend().remove()
    plt.savefig(
        output_filepath + 'elapsed_time_groupped_box.' + output_format,
        format=output_format,
        bbox_inches='tight')

    # # Create a separate legend plot
    # handles, labels = plt.gca().get_legend_handles_labels()
    # legend_fig = plt.figure(figsize=(12, 6))
    # legend_fig.legend(handles=legend_patches, fontsize=24, loc='center', frameon=False, ncol=1)
    # legend_fig.savefig(output_filepath + "legend." + output_format,
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
