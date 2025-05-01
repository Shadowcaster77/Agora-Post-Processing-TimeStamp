################################################################################
# Plot the spectrogram in real-time in a waterfall manner by reading the latest
# binary file and overlay bounding boxes read from CSV files.
# Now includes pause button and uses watchdog + queue for efficient file
# handling.
#
# Author: Chung-Hsuan Tung (updated with async and pause button)
################################################################################

import sys, os
import numpy as np
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsRectItem, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg
from pyqtgraph import ColorBarItem, ColorMap
import matplotlib.pyplot as plt


def get_jet_colormap():
    cmap = plt.get_cmap('jet')
    lut = (np.array([cmap(i / 255.0)[:3] for i in range(256)]) * 255).astype(np.uint8)
    return ColorMap(pos=np.linspace(0.0, 1.0, 256), color=lut)

# calculate the noise power and refer the signal to that and get real power
def get_noise_offset(power, mode):
    threshold = np.median(np.quantile(power, q=0.7))
    noise_power_db = power.copy()
    noise_power_db[noise_power_db > threshold] = np.nan
    noise_power_db = np.nanmean(noise_power_db)
    offset = -noise_power_db + (-173.8)
    # offset = -108.78414924975709 # profiled val from 'sparse' config (100 MHz)
    # offset = -115.95924359478522 # profiled val from 'wb' config (500 MHz)
    print(f"Noise offset: {offset}")
    noise_figure_sim = 0
    noise_figure_ota = 20
    if not mode in ['sim', 'ota']:
        raise ValueError("Invalid mode. Choose 'sim' or 'ota'.")
    return offset + (noise_figure_ota if mode == 'ota' else noise_figure_sim)

class FileHandler(FileSystemEventHandler):
    def __init__(self, bin_queue, csv_queue):
        super().__init__()
        self.bin_queue = bin_queue
        self.csv_queue = csv_queue

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.bin'):
            self.bin_queue.put(event.src_path)
        elif event.src_path.endswith('.csv'):
            self.csv_queue.put(event.src_path)
        else:
            return

class SpectrogramGUI:
    def __init__(self, folder, max_rows=200):
        self.folder = folder
        self.spectrogram = []
        self.box_data = []
        self.box_items = []
        self.max_rows = max_rows
        self.fft_size = None
        self.paused = False
        self.sample_rate = 100e6

        # Frame/symbol counter to align spectrogram with boxes
        self.symbol_counter = 0
        self.num_symbol_per_frame = 50

        # Counter and param for noise offset
        self.mode = 'sim'
        self.noise_offset = 0
        self.noise_offset_counter = 0

        # Thread-safe queues for file ingestion
        self.pending_bin_files = Queue()
        self.pending_csv_files = Queue()

        # File observer setup
        event_handler = FileHandler(self.pending_bin_files,
                                    self.pending_csv_files)
        self.observer = Observer()
        self.observer.schedule(event_handler, folder, recursive=False)
        self.observer.start()

        # Set PyQtGraph theme (default was dark theme)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # GUI setup
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_widget = QWidget()
        self.main_widget.resize(800, 500)
        self.layout = QVBoxLayout(self.main_widget)

        self.win = pg.GraphicsLayoutWidget(title="Real-Time Spectrogram")
        self.layout.addWidget(self.win)
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

        # Bottom button to pause/resume
        self.toggle_button = QPushButton("Pause")
        self.toggle_button.clicked.connect(self.toggle_pause)
        self.layout.addWidget(self.toggle_button)
        self.main_widget.show()

        # Timer
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_spectrogram)
        self.timer.start(5)

    def toggle_pause(self):
        self.paused = not self.paused
        self.toggle_button.setText("Resume" if self.paused else "Pause")

    def _read_one_bin(self, file):
        try:
            data = np.fromfile(file, dtype=np.complex64)
            if self.fft_size is None:
                self.fft_size = data.shape[0]
                print(f"Detected FFT size: {self.fft_size}")
            if data.shape[0] == self.fft_size:
                power = 10 * np.log10(np.abs(data)**2 + 1e-12)
                self.spectrogram.append(power)
                self.spectrogram = self.spectrogram[-self.max_rows:]
                self.symbol_counter += 1
        except Exception as e:
            print(f"Error reading {file}: {e}")

    def _read_one_csv(self, file):
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
            meta = list(map(int, lines[1].strip().split(',')))
            frm_start, _, sym_start, _, sc_start, _, num_box = meta
            frame_offset = int(frm_start) * self.num_symbol_per_frame
            symbol_offset = int(sym_start) + frame_offset
            box_lines = lines[3:3 + num_box]
            for line in box_lines:
                left, top, right, bottom = map(int, line.strip().split(','))
                top += symbol_offset
                bottom += symbol_offset
                left += sc_start
                right += sc_start
                self.box_data.append({'left': left, 'top': top,
                                        'right': right, 'bottom': bottom})
        except Exception as e:
            print(f"Error reading {file}: {e}")

    def read_pending_files(self):
        # read the fft-ed i/q samples
        while not self.pending_bin_files.empty():
            self._read_one_bin(self.pending_bin_files.get())
        
        # read the bounding boxes
        while not self.pending_csv_files.empty():
            self._read_one_csv(self.pending_csv_files.get())

    def update_spectrogram(self):
        if self.paused:
            return

        self.read_pending_files()
        if not self.spectrogram:
            return

        img_array = np.array(self.spectrogram).T

        # only update the noise offset every 100 frames
        if self.noise_offset_counter % 100 == 0:
            self.noise_offset_counter = 0
            # Calculate noise offset based on the current image
            self.noise_offset = get_noise_offset(img_array, mode=self.mode)
        self.noise_offset_counter += 1

        img_array_calib = img_array + self.noise_offset

        # scale the symbol/sc to time/freq for real-world axis
        scale_x = self.sample_rate / self.fft_size
        scale_y = self.fft_size / self.sample_rate

        self.img.setImage(img_array_calib, autoLevels=False,
                          levels=[-180, -110])
        
        # force freq to be shifted
        transform = pg.QtGui.QTransform()
        transform.translate(-self.sample_rate / 2,
                            -len(self.spectrogram) * scale_y)
        transform.scale(scale_x, scale_y)
        self.img.setTransform(transform)

        self.colorbar.setLevels([-180, -110])
        
        # set time-freq range
        self.plot.setXRange(-self.sample_rate / 2,
                            self.sample_rate / 2, padding=0)
        self.plot.setYRange(-len(self.spectrogram) * scale_y, 0, padding=0)

        # clear old boxes
        for item in self.box_items:
            self.plot.removeItem(item)
        self.box_items.clear()

        # only draw the boxes that overlap with the current spectrogram
        visible_boxes = []
        symbol_top = self.symbol_counter
        symbol_bottom = symbol_top - len(self.spectrogram)

        for box in self.box_data:
            if box['bottom'] >= symbol_bottom and box['top'] <= symbol_top:
                visible_boxes.append(box)

        # draw the boxes
        for box in visible_boxes:
            x = (box['left'] - self.fft_size // 2) * scale_x
            width = (box['right'] - box['left']) * scale_x
            y = (box['top'] - self.symbol_counter) * scale_y
            height = (box['bottom'] - box['top']) * scale_y
            rect = QGraphicsRectItem(x, y, width, height)
            rect.setPen(pg.mkPen('r', width=1.5))
            self.plot.addItem(rect)
            self.box_items.append(rect)

    def run(self):
        try:
            sys.exit(self.app.exec_())
        finally:
            self.observer.stop()
            self.observer.join()

if __name__ == '__main__':
    folder_path = "../../../savannah_isac/files/sensing/"
    gui = SpectrogramGUI(folder_path, max_rows=2000)
    gui.run()
