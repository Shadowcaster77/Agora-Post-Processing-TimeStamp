################################################################################
# Read raw I/Q samples and metadata from the RFSynth, a framework provided
# simulated signal generation for multiple protocols (DSSS, BLE, WLAN), and plot
# the spectrogram.
# 
# Reference: https://ieeexplore.ieee.org/abstract/document/10632847
# RFSynth code: https://github.com/ucsdwcsng/rfsynth
#
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

import helper

filename = input("Enter the rfsynth id (e.g., test): ") or 'test'
# filename = 'sparse'
rfsynth_dir = '../../rfsynth'
matlab_dir = rfsynth_dir + '/matlab'
json_path = matlab_dir + '/examples/data/' + filename + '.json' # metadata
data_path = matlab_dir + '/examples/data/' + filename + '.32cf' # raw I/Q samples

################################################################################
# Read metadata
metadata = helper.read_json_file(json_path)
# print(json.dumps(metadata, indent=2))
# print(metadata)

################################################################################
# Read raw I/Q samples
complex_values = helper.read_complex_samples(data_path)
complex_values = np.array(complex_values, dtype=np.complex64)

samp_rate = metadata['rxObj']['sampleRate_Hz']
freq_center = metadata['rxObj']['freqCenter_Hz']

num_samples = len(complex_values)
t = np.arange(num_samples) / samp_rate

f, t_spec, Sxx = signal.spectrogram(
    complex_values, fs=samp_rate, window='hamming', nperseg=1024, noverlap=0,
    scaling='density', mode='psd', return_onesided=False)
f_mhz = f / 1e6
t_ms = t_spec * 1e3

################################################################################
# Plot
plt.figure(figsize=(6.4, 4.8))
plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)   # fontsize of the tick labels
plt.rc('ytick', labelsize=20)   # fontsize of the tick labels
plt.xticks(np.arange(min(f_mhz), max(f_mhz)+1, 25))
plt.yticks(np.arange(min(t_ms), max(t_ms)+1, 5))
# plt.yticks([0, 5, 10, 15, 20])
plt.xlim([min(f_mhz), max(f_mhz)+0.1])
plt.ylim([min(t_ms), max(t_ms)+0.05])
plt.pcolormesh(np.fft.fftshift(f_mhz), t_ms,
               np.fft.fftshift(10 * np.log10(Sxx.T), axes=(1,)),
               vmax=-135,
               vmin=-175,
               shading='auto',
               linewidth=0,
               cmap='jet')  # Convert to dB
plt.colorbar(label="Power Spectral Density (dB)")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Time (ms)")
# plt.title("Spectrogram (RFSynth)", size=28)
plt.tight_layout()
plt.savefig('figs/rfsynth_spectrogram_' + filename + '.png')
# plt.savefig('figs/rfsynth_spectrogram_' + filename + '.pdf', format='pdf')
