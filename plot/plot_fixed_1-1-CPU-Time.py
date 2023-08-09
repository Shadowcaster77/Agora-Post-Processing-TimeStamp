import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=24)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=24)    # fontsize of the tick labels
plt.rc('ytick', labelsize=24)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

plt.subplots(figsize=(6,5))

x1 = [1,2,4,8,16]
y1 = np.array([1.275713, 0.707310, 0.323942, 0.189223, 0.118159])/4

x2 = [1,2,4,8,16]
y2 = np.array([2.074337, 1.148315, 0.556629, 0.311336, 0.186405,])/4

x3 = [1,2,4,8,16]
y3 = np.array([2.964847, 1.566505, 0.7554651, 0.417367, 0.297401])/4

x4 = [1,2,4,8,16]
y4 = np.array([4.035799, 2.037977, 1.219675, 0.577501, 0.400421])/4

plt.rc('lines', linewidth=3)
plt.rc('lines', markersize=10)

# plt.plot(x, y, '-^', label="Agora Simulation")
plt.plot(x1, y1, '-s', label = "25% Traffic")
plt.plot(x2, y2, '-o', label = "50% Traffic")
plt.plot(x3, y3, '-*', label = "75% Traffic", markersize=12)
plt.plot(x4, y4,'-v', label = "100% Traffic")

# plt.axhline(y=3, xmin=0, xmax=3, c="black", linewidth=1, zorder=0,linestyle='--', label='Agora 3 TTI deadline')
plt.axhline(y=0.375, xmin=0, xmax=3, c="red", zorder=0,linestyle='--', label='3 TTI')

plt.xlabel("Number of Worker Cores", fontsize=24)
plt.ylabel("CPU Time (ms)", fontsize=24)

yticks = np.arange(0, 1.1, 0.2)
plt.ylim(0, 1)
plt.yticks(yticks, fontsize=20)
plt.xticks( [1,2,4,8,16], fontsize=20)
plt.legend(loc="upper right", fontsize=20)
plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
plt.title('1x1 SISO', fontsize=28)

# plt.show()

plt.savefig("../fig/1-1-Agora_MU3-CorevsTime-CPU.pdf",bbox_inches='tight')
