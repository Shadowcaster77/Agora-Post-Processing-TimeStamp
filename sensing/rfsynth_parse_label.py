################################################################################
# Read the metadata from RFSynth, a framework provided simulated signal
# generation for multiple protocols (DSSS, BLE, WLAN), and parse the ground
# truth labels for the time-frequency diagram.
# 
# Reference: https://ieeexplore.ieee.org/abstract/document/10632847
# RFSynth code: https://github.com/ucsdwcsng/rfsynth
#
# Author: Chung-Hsuan Tung
################################################################################

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import scipy.signal as signal
import json

import helper

filename = 'test'
rfsynth_dir = '../../rfsynth'
matlab_dir = rfsynth_dir + '/matlab'
json_path = matlab_dir + '/examples/' + filename + '.json' # metadata
data_path = matlab_dir + '/examples/' + filename + '.32cf' # raw I/Q samples
cfg_path = matlab_dir + '/examples/config.yml' # configuration

singal_types = ['WlanNonHT80211g', 'Bluetooth', 'Ds3', 'WidebandThermalWgn']

################################################################################
# Parse the label from the generated json file and input config yaml file

# Metadata is the generated json file from RFSynth
metadata = helper.read_json_file(json_path)

samp_rate = metadata['rxObj']['sampleRate_Hz']
freq_center = metadata['rxObj']['freqCenter_Hz']

# Config is the input yaml to RFSynth
config = helper.read_yaml_file(cfg_path)
print(json.dumps(config, indent = 2))

# Helper class to record the energy block, i.e., transmission
class Transmission:
    def __init__(self, transmission):
        self.time_start = transmission['time_start']
        self.time_stop = transmission['time_stop']
        self.freq_lo = transmission['freq_lo']
        self.freq_hi = transmission['freq_hi']
        self.time_length_s = transmission['timeLength_s']
        self.bandwidth_hz = transmission['bandwidth_Hz']

    def print(self):
        print('--')
        print('time_start = {}'.format(self.time_start))
        print('time_stop = {}'.format(self.time_stop))
        print('freq_lo = {}'.format(self.freq_lo))
        print('freq_hi = {}'.format(self.freq_hi))
        print('time_length_s = {}'.format(self.time_length_s))
        print('bandwidth_hz = {}'.format(self.bandwidth_hz))

# Read the transmission from metadata
energy_list = []

for i in range(len(metadata['sourceArray'])):
    signal_type = config['signals'][i]['type']
    source = metadata['sourceArray'][i]
    print('=====')
    print('signal type = {}'.format(signal_type))
    if signal_type == 'WidebandThermalWgn':
        continue
    if type(source['signalArray']['transmissionArray']) == list:
        for transmission in source['signalArray']['transmissionArray']:
            energy_list.append(Transmission(transmission))
            energy_list[-1].print()
    elif type(source['signalArray']['transmissionArray']) == dict:
    # the case that only one transmission
        transmission = source['signalArray']['transmissionArray']
        energy_list.append(Transmission(transmission))
        energy_list[-1].print()

################################################################################
# Read IQ samples and plot spectrogram

# Read raw I/Q samples
complex_values = helper.read_complex_samples(data_path)
complex_values = np.array(complex_values, dtype=np.complex64)

f, t_spec, Sxx = signal.spectrogram(
    complex_values, fs=samp_rate, window='hamming', nperseg=1024, noverlap=512,
    mode='magnitude')
f_mhz = f / 1e6
t_ms = t_spec * 1e3

fig, ax = plt.subplots(figsize=(8, 6))
plt.rc('axes', labelsize=28)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)   # fontsize of the tick labels
plt.rc('ytick', labelsize=20)   # fontsize of the tick labels
im = ax.pcolormesh(np.fft.fftshift(f_mhz), t_ms, 
                   np.fft.fftshift(10 * np.log10(Sxx.T + 1e-12), axes=(1,)),
                   shading='auto')  # Convert to dB
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Time (ms)")
ax.set_title("Spectrogram (RFSynth)", size=28)

for e in energy_list:
    freq_lo = e.freq_lo
    freq_hi = e.freq_hi
    time_start = e.time_start
    time_stop = e.time_stop
    ax.add_patch(patches.Rectangle(((freq_lo-freq_center)/1e6, time_start*1e3), 
                                   (freq_hi-freq_lo)/1e6,
                                   (time_stop-time_start)*1e3,
                                   fill=None, edgecolor='r', lw=1))

plt.colorbar(im, label="Power Spectral Density (dB)")
plt.tight_layout()
plt.savefig('figs/rfsynth_spectrogram_' + filename + '_labeled.png')
