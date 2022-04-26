""" RX scripting window """

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from atmega_gui.views.Fenetre_RX_ui import Ui_Dialog as rxUI

class RxWindow(QMainWindow, rxUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.log = print

    def connectSignalsSlots(self):
        """ Implement all the actions on each component """
        self.btn_Demarer.clicked.connect(self.on_start)
        self.btn_Pause.clicked.connect(self.on_pause)
        self.btn_Stop.clicked.connect(self.on_stop)
        self.btn_Browse.clicked.connect(self.loadscript)

    def on_start(self):
        """ Start callback function """
        self.log("Start button clicked")
        filename = self.txt_Path.text()
        self.log(filename)
        if filename:
            self.script_exe.exec_file(filename)

    def on_pause(self):
        """ Pause callback function """
        self.log("Pause button clicked")

    def on_stop(self):
        """ Stop callback function """
        self.log("Stop button clicked")

    def loadscript(self):
        script_name = QFileDialog.getOpenFileName(
            None, "", "", "Scripts (*.sc.py *.txt)")[0]
        self.txt_Path.setText(script_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RxWindow()
    win.show()
    sys.exit(app.exec())
