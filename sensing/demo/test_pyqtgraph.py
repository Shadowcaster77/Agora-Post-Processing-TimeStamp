################################################################################
# Test the package of PyQt5 and if the GUI (X11) is working.
#
# Author: Chung-Hsuan Tung
################################################################################

import sys
from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np

app = QtWidgets.QApplication(sys.argv)

win = pg.GraphicsLayoutWidget(title="PyQtGraph Test")
win.resize(600, 400)
plot = win.addPlot(title="Sine Wave Example")

x = np.linspace(0, 2 * np.pi, 1000)
y = np.sin(x)

plot.plot(x, y, pen='r')

win.show()
sys.exit(app.exec_())
