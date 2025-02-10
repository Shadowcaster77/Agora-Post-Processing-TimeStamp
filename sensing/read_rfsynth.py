################################################################################
# Read raw I/Q samples and metadata from the RFSynth, a framework provided
# simulated signal genertion for multiple protocols (DSSS, BLE, WLAN) and plot
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
import json

import helper

filename = 'test'
rfsynth_dir = '../../rfsynth'
matlab_dir = rfsynth_dir + '/matlab'
json_path = matlab_dir + '/examples/' + filename + '.json' # metadata
data_path = matlab_dir + '/examples/' + filename + '.32cf' # raw I/Q samples


# Read metadata
metadata = helper.read_json_file(json_path)
# print(json.dumps(metadata, indent=2))
# print(metadata)

# Read raw I/Q samples
complex_values = helper.read_complex_samples(data_path)
complex_values = np.array(complex_values, dtype=np.complex64)

samp_rate = metadata['rxObj']['sampleRate_Hz']
freq_center = metadata['rxObj']['freqCenter_Hz']

num_samples = len(complex_values)
t = np.arange(num_samples) / samp_rate

f, t_spec, Sxx = signal.spectrogram(
    complex_values, fs=samp_rate, window='hamming', nperseg=1024, noverlap=512,
    mode='magnitude')
f_mhz = f / 1e6

plt.figure(figsize=(8, 6))
plt.pcolormesh(np.fft.fftshift(f_mhz), t_spec, 
               np.fft.fftshift(10 * np.log10(Sxx.T + 1e-12), axes=(1,)),
               shading='auto')  # Convert to dB
plt.colorbar(label="Power Spectral Density (dB)")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Time (s)")
plt.title("Spectrogram of Received Signal")
plt.tight_layout()
plt.savefig('rfsynth_spectrogram_' + filename + '.png')
