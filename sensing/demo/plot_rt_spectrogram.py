################################################################################
# Plot the spectrogram in real-time in a waterfall manner by reading the latest
# binary file from the savannah_isac folder.
#
# Author: Chung-Hsuan Tung
################################################################################

import sys, os, glob
import numpy as np
from PyQt5 import QtWidgets
import pyqtgraph as pg
from pyqtgraph import ColorBarItem, ColorMap
import matplotlib.pyplot as plt


def get_jet_colormap():
    cmap = plt.get_cmap('jet')
    lut = (np.array([cmap(i / 255.0)[:3] for i in range(256)]) * 255).astype(np.uint8)
    return ColorMap(pos=np.linspace(0.0, 1.0, 256), color=lut)


class SpectrogramGUI:
    def __init__(self, folder, max_rows=200):
        self.folder = folder
        self.spectrogram = []
        self.processed = set()
        self.max_rows = max_rows
        self.fft_size = None

        # Set PyQtGraph theme to white background
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # GUI setup
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(title="Real-Time Spectrogram")
        self.win.resize(1000, 600)
        self.plot = self.win.addPlot(title="Spectrogram")
        self.img = pg.ImageItem()
        self.img.setAutoDownsample(True)
        self.plot.addItem(self.img)
        self.plot.setAspectLocked(False)
        self.plot.invertY(False)  # Time increases upward

        # Axis labels
        self.plot.setLabel('bottom', 'Frequency', units='Hz')
        self.plot.setLabel('left', 'Time', units='s')

        # Colormap
        self.jet_colormap = get_jet_colormap()
        self.img.setLookupTable(self.jet_colormap.getLookupTable())

        # Colorbar setup
        self.colorbar = ColorBarItem(interactive=False, values=(0, 1),
                                     colorMap=self.jet_colormap)
        self.colorbar.setImageItem(self.img)
        self.colorbar.setLabel('right', text='Power', units='dB')
        self.win.addItem(self.colorbar)

        # Timer
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_spectrogram)
        self.timer.start(1)

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
                        power = np.fft.fftshift(power)  # fftshift
                        new_rows.append(power)
                        self.processed.add(f)
                except Exception as e:
                    print(f"Error loading {f}: {e}")
        return new_rows

    def update_spectrogram(self):
        new_rows = self.read_new_files()
        if new_rows:
            self.spectrogram.extend(new_rows)
            self.spectrogram = self.spectrogram[-self.max_rows:]
            img_array = np.array(self.spectrogram)
            img_array = img_array.T  # Transpose to match the plot orientation

            # Real-world axis scaling
            sample_rate = 100e6
            scale_x = sample_rate / self.fft_size # Hz/bin
            scale_y = self.fft_size / sample_rate # s/row

            self.img.setImage(
                img_array,
                autoLevels=False,
                levels=[-80, 0]
            )

            # force freq to be shifted
            transform = pg.QtGui.QTransform()
            transform.translate(-sample_rate / 2, -len(self.spectrogram) * scale_y)  # x=0 -> -50 MHz
            transform.scale(scale_x, scale_y)
            self.img.setTransform(transform)

            self.colorbar.setLevels([-80, 0])

            # set time-freq range
            self.plot.setXRange(-sample_rate / 2, sample_rate / 2, padding=0)
            self.plot.setYRange(-len(self.spectrogram) * scale_y, 0, padding=0)

    def run(self):
        self.win.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    folder_path = "../../../savannah_isac/files/sensing/"  # .bin files are here

    gui = SpectrogramGUI(folder_path, max_rows=200)
    gui.run()
