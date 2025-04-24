#!/bin/bash

# this is only useful under a virtual environment
export PYQT_QT_DIR=/home/ct297/.local/share/virtualenvs/util_agora-zvhatobm/lib/python3.8/site-packages/PyQt5/Qt5/lib/
export LD_LIBRARY_PATH=$PYQT_QT_DIR:$LD_LIBRARY_PATH
export QT_OPENGL=software
exec python "$@"

