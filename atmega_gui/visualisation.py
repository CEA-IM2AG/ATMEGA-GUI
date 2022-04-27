""" Visualization window """

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from atmega_gui.views.visualisation_ui import Ui_Dialog as visualisationUI
from atmega_gui.util import compare
from atmega_gui.bitmap import print_bitmap

class VisualizationUI(QMainWindow, visualisationUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.btn_Load.clicked.connect(self.on_load)
        self.btn_ChargeFich.clicked.connect(self.load_fich)

    def on_load(self):
        glist = [0 for i in range(1024)]
        compare("dump1.txt", "dump2.txt", glist)
        matrix = [glist[i*32:(i+1)*32] for i in range(32)]
        matrix[5][7] = 3
        print_bitmap(matrix, self.check_Zoom.isChecked())

    def load_fich(self):
        """ Callback that update the filename text field """
        file_name = QFileDialog.getOpenFileName(
            None, "", "", "Dumps (*.txt)")[0]
        self.txt_Path.setText(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VisualizationUI()
    win.show()
    sys.exit(app.exec())
