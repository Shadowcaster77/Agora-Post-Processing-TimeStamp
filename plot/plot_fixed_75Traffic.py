import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

labels = ['SISO\n8 cores', 'MIMO\n8 cores', 'SISO\n16 cores', 'MIMO\n16 cores']

frame_time =        [0.125, 0.125, 0.125, 0.125]
ind = np.arange(4)


fft_time =          np.array([0.0166823, 0.0379041, 0.0124646, 0.0205392])/4
CSI_time =          np.array([0.00039021, 0.00140518, 0.000224343, 0.00141966])/4
BeamWeight_time =   np.array([0.0484188, 0.0895861, 0.0282272, 0.0565404])/4
Demul_time =        np.array([0.116526, 0.135502, 0.064267, 0.0838328])/4
Decode_time =       np.array([0.23535, 0.509059, 0.192218, 0.374865])/4
width = 0.25       # the width of the bars: can also be len(x) sequence
# 20 cores, 1/3 Code rate, Scheduling deferred at U:46


fig, ax = plt.subplots(figsize=(6,5))

# ax.bar(x=ind, height=frame_time, width=0.30,align='center', label='Frame_time')

ax.bar(labels, fft_time, width,  label='FFT')
ax.bar(labels, CSI_time, width, bottom = fft_time, label='CSI')
ax.bar(labels, BeamWeight_time, width, bottom=fft_time + CSI_time, label='BeamWeight')
ax.bar(labels, Demul_time, width, bottom=fft_time + CSI_time + BeamWeight_time, label='Demul')
ax.bar(labels, Decode_time, width, bottom=fft_time + CSI_time + BeamWeight_time + Demul_time, label='Decode')

ax.set_ylabel('CPU Time (ms)', fontsize=24)
yticks = np.arange(0, 0.26, 0.05)
plt.yticks(yticks)
plt.ylim(0, 0.25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
plt.title('75% Traffic Load', fontsize=28)

plt.savefig("../fig/75-barplot.pdf",bbox_inches='tight')
