""" Visualization window """

import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from atmega_gui.views.visualisation_ui import Ui_Dialog as visualisationUI
from atmega_gui.util import read_diff, spawn_box, read_index_diff, write_index
from atmega_gui.bitmap import print_bitmap

class VisualizationUI(QMainWindow, visualisationUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.session_diffs = []
        self.saved_diff = []
        self.current_diff_index = 0

    def connectSignalsSlots(self):
        # Buttons mapping
        self.btn_Load.clicked.connect(self.on_load_frame)
        self.btn_ChargeIndx.clicked.connect(self.on_load_indexes)
        self.btn_PrevFrame.clicked.connect(self.on_prev)
        self.btn_NextFrame.clicked.connect(self.on_next)
        self.btn_SaveTout.clicked.connect(self.on_save_all)
        self.radio_ResCourant.toggled['bool'].connect(self.on_source_toggle)
        # Validator
        int_validator = QRegExpValidator(QtCore.QRegExp("[0-9]+"))
        self.txt_ChoixImage.setValidator(int_validator)

    def on_load_frame(self):
        """ Callback that load the file """
        try:
            filename = self.saved_diff[self.current_diff_index]
        except:
            spawn_box("Visualisation error", "Index out of bounds", QMessageBox.Warning)
            return

        if not filename and not filename.isspace():
            spawn_box("Visualisation error", "Empty file given", QMessageBox.Warning)
            return

        try:
            diff_l, incr_l = read_diff(filename)
        except Exception as e:
            print(e)
            spawn_box("Visualisation error", f"Could not open {filename}", QMessageBox.Warning)
            return

        if self.radio_Diff.isChecked():
            print_bitmap(diff_l, self.check_Zoom.isChecked())
        else:
            print_bitmap(incr_l, self.check_Zoom.isChecked())

    def on_source_toggle(self):
        """ Callback called when current result is checked """
        if self.radio_ResCourant.isChecked():
            self.saved_diff = self.session_diffs
            self.lbl_ImagesTotal.setText("/ "+str(len(self.session_diffs)))

    def on_save_all(self):
        """ Save all the diffs """
        if self.session_diffs:
            try:
                filename = write_index(self.session_diffs)
            except:
                spawn_box("Error", "Permission denied")
                return
            spawn_box("Write", f"Session dumped into {filename}")
        else:
            spawn_box("Error", "Empty session")

    def on_load_indexes(self):
        """ Callback that update the filename text field """
        file_name = QFileDialog.getOpenFileName(
            None, "", "", "Dumps (*_index.txt)")[0]
        self.txt_Path.setText(file_name)

        try:
            index_list = read_index_diff(file_name)
        except:
            spawn_box("Error", "Could not open index file", QMessageBox.Warning)
            return

        if len(index_list) == 0:
            spawn_box("Error", "Empty index file", QMessageBox.Warning)
            return

        if self.current_diff_index >= len(index_list):
            self.current_diff_index = 0
            self.txt_ChoixImage.setText("1")

        self.saved_diff = index_list
        self.lbl_ImagesTotal.setText("/ "+str(len(self.saved_diff)))

    def on_prev(self):
        """ Callback that updates the frame """
        index = int(self.txt_ChoixImage.text()) - 2

        if 0 <= index < len(self.saved_diff):
            self.current_diff_index = index
        else:
            self.current_diff_index = 0

        self.txt_ChoixImage.setText(str(self.current_diff_index + 1))

    def on_next(self):
        """ Callback that updates the frame """
        index = int(self.txt_ChoixImage.text())

        if 0 <= index < len(self.saved_diff):
            self.current_diff_index = index
        else:
            self.current_diff_index = len(self.saved_diff) - 1

        self.txt_ChoixImage.setText(str(self.current_diff_index + 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VisualizationUI()
    win.show()
    sys.exit(app.exec())
