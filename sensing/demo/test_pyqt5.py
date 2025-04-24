################################################################################
# Test the package of PyQt5 and if the GUI (X11) is working.
#
# Author: Chung-Hsuan Tung
################################################################################

from PyQt5.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)
label = QLabel("Qt is working!")
label.show()
app.exec_()
