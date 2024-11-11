import matplotlib.pyplot as plt
import numpy as np

############################################################################
# Font settings: tick size, linewidth, marker size
############################################################################

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

FIG_SIZE_W = 10
FIG_SIZE_H = 5

edgecolor='black'

bar_width = 0.5
edgecolor = "black"
linewidth = 2

#     hatches = ['////', 'xxxx', '....', '||||', '\\\\\\\\', '++++', 'oooo']
hatches = ['//', '||', '..', 'xx', '\\\\', '++', 'oo']

############################################################################
# Plot
############################################################################

mcs = list(range(29))
zc_length = [8, 10, 13, 16, 20, 26, 30, 36, 40, 44, 44, 52, 60, 64, 72, 80, 88,
             88, 96, 104, 112, 128, 128, 144, 160, 160, 176, 176, 192]
cb_length = [176, 220, 286, 352, 440, 572, 660, 792, 880, 968, 968, 1144, 1320,
             1408, 1584, 1760, 1936, 1936, 2112, 2288, 2464, 2816, 2816, 3168,
             3520, 3520, 3872, 3872, 4224]
code_rate = [120, 157, 193, 251, 308, 379, 449, 526, 602, 679, 340, 378, 434, 490, 553, 616,
             658, 438, 466, 517, 567, 616, 666, 719, 772, 822, 873, 910, 948]

cb_length = np.array(cb_length)

fig, ax1 = plt.subplots(figsize=(FIG_SIZE_W, FIG_SIZE_H))

ax1.plot(mcs, cb_length/1000, marker='o', markersize=12, linewidth=4,
         label="CB length", color="black", zorder=10)  # Plot with markers

ax1.set_xlabel("MCS Index", fontsize=24)
ax1.set_ylabel("Code Block Size (kbits)", fontsize=24)

ax1.grid(color='grey', linestyle='--', linewidth=0.5)

plt.xlim([-1, 29])
plt.ylim([0, 8 ])
plt.xticks([0, 5, 10, 15, 20, 25, 28], fontsize=20)
plt.yticks([0, 2, 4, 6, 8], fontsize=20)

####################
# Second y-axis

# Create a second y-axis with the same x-axis (sharing the same x-axis)
ax2 = ax1.twinx()

# Plot the data for the right y-axis
ax2.plot(mcs, code_rate, marker='s', markersize=10, linewidth=4,
         label="Code Rate", color="tab:gray", alpha=1, linestyle="--", zorder=5)


plt.ylabel(r"Code Rate $\times$ 1,024 (bits)", fontsize=24)  # Right y-axis label

for line in ax2.get_yticklines():
    line.set_color('tab:gray')
    # line.set_alpha(0.5)
# ax2.yaxis.label.set_alpha(0.5)
ax2.yaxis.label.set_color('tab:gray')
# ax2.spines['right'].set_alpha(0.5)
ax2.spines['right'].set_color('tab:gray')
# ax2.set_yscale('log')

lighter_color = "#bbbbbb"

ax2.grid(False)  # Disable the grid for the second axis
ax1.tick_params(labelsize=20)
ax2.set_yticks([0, 256, 512, 768, 1024])
ax2.set_ylim([0, 1024])
ax2.tick_params(axis='both', which='major', labelsize=20)
ax2.tick_params(axis='y', which='major', labelsize=20, colors='tab:gray')
# plt.legend(fontsize=15)
# Show the plot

ax1.axvline(x=9.5, color='k', linewidth=1, linestyle="--")
ax1.axvline(x=16.5, color='k', linewidth=1, linestyle="--")

ax1.text(2.5, 7, '$Q_m=2$', fontsize=22, color="tab:green")
ax1.text(10.7, 7, '$Q_m=4$', fontsize=22, color="tab:orange")
ax1.text(20.5, 7, '$Q_m=6$', fontsize=22, color="tab:red")

ax1.axvspan(-0.5, 9.5, color='tab:green', alpha=0.2)
ax1.axvspan(9.5, 16.5, color='tab:orange', alpha=0.2)
ax1.axvspan(16.5, 28.5, color='tab:red', alpha=0.2)

# plt.axvspan(-0.5, 9.5, alpha=0.5, hatch="\\\\\\\\", edgecolor="green", facecolor="none", zorder=0)
# plt.axvspan(9.5, 16.5, alpha=0.5, hatch="////", edgecolor="orange", facecolor="none", zorder=0)
# plt.axvspan(16.5, 28.5, alpha=0.5, hatch="xxxx", edgecolor="red", facecolor="none", zorder=0)

plt.savefig("../fig/mcs_vs_CB.pdf", bbox_inches='tight')
