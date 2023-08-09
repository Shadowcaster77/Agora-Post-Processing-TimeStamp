import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

labels = ['SISO\n8 cores', 'MIMO\n8 cores', 'SISO\n16 cores', 'MIMO\n16 cores']

frame_time =        [0.125, 0.125, 0.125, 0.125]
ind = np.arange(4)


fft_time =          np.array([0.00976518, 0.0103554, 0.00360239, 0.0056336])/4
CSI_time =          np.array([0.000779213, 0.00292072, 0.000176031, 0.000850083])/4
BeamWeight_time =   np.array([0.0481351, 0.0850282, 0.0305746, 0.059081])/4
Demul_time =        np.array([0.0406309, 0.047928, 0.0253214, 0.0288503])/4
Decode_time =       np.array([0.0899127, 0.164644, 0.0584844, 0.152354])/4
width = 0.25       # the width of the bars: can also be len(x) sequence
# 20 cores, 1/3 Code rate, Scheduling deferred at U:46


fig, ax = plt.subplots(figsize=(6,5))

# ax.bar(x=ind, height=frame_time, width=0.30,align='center', label='Frame_time')
plt.rc('lines', linewidth=3)
plt.rc('lines', markersize=10)

ax.bar(labels, fft_time, width,  label='FFT')
ax.bar(labels, CSI_time, width, bottom = fft_time, label='CSI')
ax.bar(labels, BeamWeight_time, width, bottom=fft_time + CSI_time, label='BeamWeight')
ax.bar(labels, Demul_time, width, bottom=fft_time + CSI_time + BeamWeight_time, label='Demul')
ax.bar(labels, Decode_time, width, bottom=fft_time + CSI_time + BeamWeight_time + Demul_time, label='Decode')
# ax.axhline(y=0.125, xmin=0, xmax=3, c="Black", zorder=0,linestyle='--', label='1 TTI')

ax.set_ylabel('CPU Time (ms)', fontsize=24)
yticks = np.arange(0, 0.26, 0.05)
plt.yticks(yticks)
plt.ylim(0, 0.25)
ax.legend(fontsize=20, ncol=1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
plt.title('25% Traffic Load', fontsize=28)

# plt.show()
plt.savefig("../fig/25-barplot.pdf",bbox_inches='tight')
