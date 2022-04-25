""" Visualization window """

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from views.visualisation_ui import Ui_Dialog as visualisationUI

class Window(QMainWindow, visualisationUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        # TODO
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
