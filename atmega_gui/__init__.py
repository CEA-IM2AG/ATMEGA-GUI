#!/usr/bin/env python

""" Bootstrap atmega gui """
import sys
import logging

from PyQt5.QtWidgets import QApplication
from atmega_gui.main import MainWindow

logging.basicConfig(level=logging.DEBUG)

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())
