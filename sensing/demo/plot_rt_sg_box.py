################################################################################
# Plot the spectrogram in real-time in a waterfall manner by reading the latest
# binary file and overlay bounding boxes read from CSV files.
#
# Usage: must first delete the old files in the folder, then run this script
# with the dumpToFile() in DoSensingTime.cc and imag_proc_partition() in
# DoSensingFreq.cc enabled.
#
# The code supports up to 1e6-10e6 sampling rate (for the speed issue). 1e6 with
# no delay, and 10e6 with significant (and visible) delay.
#
# Author: Chung-Hsuan Tung (with bounding box overlay updated)
################################################################################

import sys, os, glob
import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
import pyqtgraph as pg
from pyqtgraph import ColorBarItem, ColorMap
import matplotlib.pyplot as plt


def get_jet_colormap():
    cmap = plt.get_cmap('jet')
    lut = (np.array([cmap(i / 255.0)[:3] for i in range(256)]) * 255).astype(np.uint8)
    return ColorMap(pos=np.linspace(0.0, 1.0, 256), color=lut)

def get_noise_offset(power, mode):
    threshold = np.median(np.quantile(power, q=0.7))
    noise_power_db = power.copy()
    noise_power_db[noise_power_db > threshold] = np.nan
    noise_power_db = np.nanmean(noise_power_db)
    offset = -noise_power_db + (-173.8)
    print(f"Noise offset: {offset}")
    if mode == 'sim':
        noise_figure = 0
    elif mode == 'ota':
        noise_figure = 20
    else:
        raise ValueError("Invalid mode. Choose 'sim' or 'ota'.")
    return offset + noise_figure

class SpectrogramGUI:
    def __init__(self, folder, max_rows=200):
        self.folder = folder
        self.spectrogram = []
        self.processed = set()
        self.processed_boxes = set()
        self.box_data = []
        self.box_items = []
        self.max_rows = max_rows
        self.fft_size = None

        # Set PyQtGraph theme
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # GUI setup
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(title="Real-Time Spectrogram")
        self.win.resize(1000, 600)
        self.plot = self.win.addPlot(title="Waterfall Spectrogram")
        self.img = pg.ImageItem()
        self.img.setAutoDownsample(True)
        self.plot.addItem(self.img)
        self.plot.setAspectLocked(False)
        self.plot.invertY(False)

        # Axis labels
        self.plot.setLabel('bottom', 'Frequency', units='Hz')
        self.plot.setLabel('left', 'Time', units='s')

        # Colormap
        self.jet_colormap = get_jet_colormap()
        self.img.setLookupTable(self.jet_colormap.getLookupTable())

        # Colorbar
        self.colorbar = ColorBarItem(interactive=False, values=(0, 1),
                                     colorMap=self.jet_colormap)
        self.colorbar.setImageItem(self.img)
        self.colorbar.setLabel('right', text='Power', units='dB')
        self.win.addItem(self.colorbar)

        # Timer
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_spectrogram)
        self.timer.start(10)

        # Counter for noise offset
        self.noise_offset = 0
        self.noise_offset_counter = 0

        # Frame/symbol counter to align spectrogram with boxes
        self.symbol_counter = 0
        self.num_symbol_per_frame = 50

        # customed parameters (should match the parameters in the sensing code)
        self.sample_rate = 1e6
        self.mode = 'sim'  # 'sim' or 'ota'

    def read_new_files(self):
        files = sorted(glob.glob(os.path.join(self.folder, "*.bin")))
        new_rows = []

        for f in files:
            if f not in self.processed:
                try:
                    data = np.fromfile(f, dtype=np.complex64)
                    if self.fft_size is None:
                        self.fft_size = data.shape[0]
                        print(f"Detected FFT size: {self.fft_size}")
                    if data.shape[0] == self.fft_size:
                        power = 10 * np.log10(np.abs(data)**2 + 1e-12)
                        # power = np.fft.fftshift(power)
                        new_rows.append(power)
                        self.processed.add(f)
                    self.symbol_counter += 1
                except Exception as e:
                    print(f"Error loading {f}: {e}")
        return new_rows

    def read_new_boxes(self):
        box_files = sorted(glob.glob(os.path.join(self.folder, "box_*.csv")))

        for bf in box_files:
            if bf not in self.processed_boxes:
                try:
                    with open(bf, 'r') as f:
                        lines = f.readlines()
                    meta = list(map(int, lines[1].strip().split(',')))
                    frame_start, frame_end, symbol_start, symbol_end, subcarrier_start, subcarrier_end, num_box = meta
                    
                    # Adjust the box coordinates based on the metadata
                    frame_offset = int(frame_start) * self.num_symbol_per_frame
                    symbol_offset = int(symbol_start) + frame_offset

                    box_lines = lines[3:3 + num_box]
                    for line in box_lines:
                        left, top, right, bottom = map(int, line.strip().split(','))
                        top += symbol_offset
                        bottom += symbol_offset
                        left += subcarrier_start
                        right += subcarrier_start
                        self.box_data.append({'left': left, 'top': top,
                                              'right': right, 'bottom': bottom})
                    self.processed_boxes.add(bf)
                except Exception as e:
                    print(f"Error loading {bf}: {e}")

    def update_spectrogram(self):
        new_rows = self.read_new_files()
        self.read_new_boxes()

        if new_rows:
            self.spectrogram.extend(new_rows)
            self.spectrogram = self.spectrogram[-self.max_rows:]
            img_array = np.array(self.spectrogram).T

            if self.noise_offset_counter % 100 == 0:
                self.noise_offset_counter = 0
                if len(img_array) > 0:
                    self.noise_offset = get_noise_offset(img_array,
                                                         mode=self.mode)
                    img_array_calib = img_array + self.noise_offset
            else:
                img_array_calib = img_array + self.noise_offset
            self.noise_offset_counter += 1

            scale_x = self.sample_rate / self.fft_size
            scale_y = self.fft_size / self.sample_rate

            self.img.setImage(img_array_calib, autoLevels=False,
                              levels=[-180, -110])

            transform = pg.QtGui.QTransform()
            transform.translate(-self.sample_rate / 2,
                                -len(self.spectrogram) * scale_y)
            transform.scale(scale_x, scale_y)
            self.img.setTransform(transform)

            self.colorbar.setLevels([-180, -110])
            self.plot.setXRange(-self.sample_rate / 2, self.sample_rate / 2,
                                padding=0)
            self.plot.setYRange(-len(self.spectrogram) * scale_y, 0, padding=0)

            # Clear old boxes
            for item in self.box_items:
                self.plot.removeItem(item)
            self.box_items.clear()

            # Draw boxes
            for box in self.box_data:
                x = (box['left'] - self.fft_size // 2) * scale_x
                width = (box['right'] - box['left']) * scale_x
                y = (box['top'] - self.symbol_counter) * scale_y
                height = (box['bottom'] - box['top']) * scale_y
                rect = QtWidgets.QGraphicsRectItem(x, y, width, height)
                rect.setPen(pg.mkPen('r', width=1.5))
                self.plot.addItem(rect)
                self.box_items.append(rect)

    def run(self):
        self.win.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    folder_path = "../../../savannah_isac/files/sensing/"  # Adjust as needed
    gui = SpectrogramGUI(folder_path, max_rows=2000)
    gui.run()
