""" Visualization window """

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from atmega_gui.views.visualisation_ui import Ui_Dialog as visualisationUI
from atmega_gui.util import read_diff, spawn_box
from atmega_gui.bitmap import print_bitmap

class VisualizationUI(QMainWindow, visualisationUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.current_diff = ""
        self.diffs = []

    def connectSignalsSlots(self):
        self.btn_Load.clicked.connect(self.on_load)
        self.btn_ChargeIndx.clicked.connect(self.load_fich)

    def on_load(self):
        """ Callback that load the file """
        if self.radio_ResEnreg.isChecked():
            filename = self.txt_Path.text()
        else:
            filename = self.current_diff

        if not filename and not filename.isspace():
           spawn_box("Script reader", "Empty file given", QMessageBox.Warning)
           return

        diff_l, incr_l = read_diff(filename)

        if self.radio_Diff.isChecked():
            print_bitmap(diff_l, self.check_Zoom.isChecked())
        else:
            print_bitmap(incr_l, self.check_Zoom.isChecked())

    def load_fich(self):
        """ Callback that update the filename text field """
        file_name = QFileDialog.getOpenFileName(
            None, "", "", "Dumps (*.txt *_index.txt)")[0]
        self.txt_Path.setText(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VisualizationUI()
    win.show()
    sys.exit(app.exec())
