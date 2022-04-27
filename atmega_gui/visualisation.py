""" Visualization window """

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from atmega_gui.views.visualisation_ui import Ui_Dialog as visualisationUI
from atmega_gui.util import compare
from atmega_gui.bitmap import print_bitmap

class Window(QMainWindow, visualisationUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        # TODO
        self.btn_Load.clicked.connect(self.on_load)
        pass

    def on_load(self):
        """matrix = [[0 for i in range(32)] for j in range(32)]
        matrix[4][5] = 1
        matrix[7][9] = 3"""
        glist = [0 for i in range(1024)]
        compare("dump1.txt", "dump2.txt", glist)
        matrix = [glist[i*32:(i+1)*32] for i in range(32)]
        matrix[5][7] = 3
        print_bitmap(matrix, self.check_Zoom.isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
