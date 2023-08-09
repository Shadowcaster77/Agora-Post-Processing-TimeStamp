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

x5 = [1,2,4,8,16]
y5 = np.array([2.29, 1.345, 0.51, 0.31, 0.61])/4

x6 = [1,2,4,8,16]
y6 = np.array([3.67 ,2.08, 0.96, 0.49, 0.84])/4

x7 = [1,2,4,8,16]
y7 = np.array([5.52 ,3.009, 1.635, 0.69, 1.5523])/4

x8 = [1,2,4,8,16]
y8 = np.array([7.88 , 3.88, 2.59, 1.64, 2.125096])/4

plt.rc('lines', linewidth=3)
plt.rc('lines', markersize=12)

plt.plot(x5, y5, '-s', label = "25% Traffic")
plt.plot(x6, y6, '-o', label = "50% Traffic")
plt.plot(x7, y7, '-*', label = "75% Traffic", markersize=14)
plt.plot(x8, y8,'-v', label = "100% Traffic")

# plt.axhline(y=3, xmin=0, xmax=3, c="black", linewidth=1, zorder=0,linestyle='--', label='Agora 3 TTI deadline')
plt.axhline(y=0.375, xmin=0, xmax=3, c="red", zorder=0,linestyle='--', label='3 TTI')

plt.xlabel("Number of Worker Cores", fontsize=24)
plt.ylabel("Elapsed Time (ms)", fontsize=24)

yticks = np.arange(0, 1.1, 0.2)
plt.ylim(0, 1)
plt.yticks(yticks, fontsize=20)
plt.xticks( [1,2,4,8,16], fontsize=20)
plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
plt.title('1X1 SISO', fontsize=28)
# plt.show()

plt.savefig("../fig/1-1-Agora_MU3-CorevsTime-Elapsed.pdf",bbox_inches='tight')
