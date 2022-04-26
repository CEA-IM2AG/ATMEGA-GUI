#!/usr/bin/env python

""" Bootstrap atmega gui """
import sys

from PyQt5.QtWidgets import QApplication
from atmega_gui.main import MainWindow

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())
