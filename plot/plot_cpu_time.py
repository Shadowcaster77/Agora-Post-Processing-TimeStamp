import matplotlib.pyplot as plt
import numpy as np


labels = ['1', '2', '4', '8', '12', '20', '48']

frame_time =        [2.45728, 2.45728, 2.45728, 2.45728, 2.45728, 2.45728, 2.45728]
ind = np.arange(7)


fft_time =          np.array([0.0519446, 0.0280576, 0.0146701, 0.00689509, 0.0046584, 0.00305218, 0.00399502])
CSI_time =          np.array([0.0313615, 0.0158758, 0.0128886, 0.00623334, 0.00411392, 0.00160559, 0.00114666])
BeamWeight_time =   np.array([1.32689, 0.831042, 0.46941, 0.259544, 0.156687, 0.108638, 0.144757])
Demul_time =        np.array([1.10252, 0.659944, 0.487749, 0.426632, 0.462148, 0.441271, 0.555268])
Decode_time =       np.array([0.546144, 0.24337, 0.0904153, 0.0405382, 0.0277673, 0.0161959, 0.00974093])
width = 0.25       # the width of the bars: can also be len(x) sequence
# 20 cores, 1/3 Code rate, Scheduling deferred at U:46


fig, ax = plt.subplots()

ax.bar(x=ind, height=frame_time, width=0.30,align='center', label='Frame_time')

ax.bar(labels, fft_time, width,  label='FFT')
ax.bar(labels, CSI_time, width, bottom = fft_time, label='CSI')
ax.bar(labels, BeamWeight_time, width, bottom=fft_time + CSI_time, label='BeamWeight')
ax.bar(labels, Demul_time, width, bottom=fft_time + CSI_time + BeamWeight_time, label='Demul')
ax.bar(labels, Decode_time, width, bottom=fft_time + CSI_time + BeamWeight_time + Demul_time, label='Decode')
ax.axhline(y=1.5, xmin=0, xmax=3, c="black", linewidth=2, zorder=0, label='3TTI deadline')
# ax.axhline(y=1.50, xmin=0, xmax=3, c="red", linewidth=2, zorder=0, label='Concordia 1.5ms deadline')


ax.set_ylabel('Time in ms')
ax.set_xlabel('Number of Cores')
ax.set_title('1*1 Case Overall Latency (Total 56 symbols); w.r.t. 3U tasks')
ax.legend()

plt.tight_layout()
plt.show()