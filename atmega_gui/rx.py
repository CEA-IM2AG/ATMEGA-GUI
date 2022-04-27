""" RX scripting window """

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from atmega_gui.views.Fenetre_RX_ui import Ui_Dialog as rxUI
from atmega_gui.visualisation import VisualizationUI
from atmega_gui.util import ScriptExe, TextWorker
from PyQt5.QtWidgets import QMessageBox
from atmega_gui.util import spawn_box, play_sound


class RxWindow(QMainWindow, rxUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.script_exe = ScriptExe()
        self.worker = None
        self.visualisation_ui = VisualizationUI(self)

    def connectSignalsSlots(self):
        """ Implement all the actions on each component """
        self.btn_Demarer.clicked.connect(self.on_start)
        self.btn_Pause.clicked.connect(self.on_pause)
        self.btn_Stop.clicked.connect(self.on_stop)
        self.btn_Browse.clicked.connect(self.on_load)

    def on_script_start(self):
        """ Callback called when the script is started """
        self.script_exe.running = True
        self.script_exe.stop = False
        self.script_exe.pause = False

    def on_script_stop(self):
        """ Callback called when the script is stopped """
        self.script_exe.running = False
        self.script_exe.stop = False
        self.script_exe.pause = False
        spawn_box("Script execution", "stopped", QMessageBox.Information)

    def on_start(self):
        """ Start callback function """
        if self.script_exe.running:
            spawn_box("Script reader", "A script is running. Cannot start a new one",
                        QMessageBox.Warning)
            return
        elif self.script_exe.pause:
            spawn_box("Script reader", "The script is paused. Cannot start a new one",
                        QMessageBox.Warning)
            return
        filename = self.txt_Path.text()
        self.visualisation_ui.show()
        if filename:
            self.worker = TextWorker(
                    lambda *args, **kwargs: self.script_exe.exec_file(*args, **kwargs), filename)
            self.worker.signal.output.connect(self.Affichage.append)
            self.worker.sound.output.connect(play_sound)
            self.worker.started.connect(self.on_script_start)
            self.worker.finished.connect(self.on_script_stop)
            self.worker.start()
        else:
            spawn_box("Script reader", "Empty file given", QMessageBox.Warning)

    def on_pause(self):
        """ Pause callback function """
        if not self.script_exe.running:
            spawn_box("Script reader", "The script is not running. Nothing to pause",
                        QMessageBox.Warning)
            return
        self.script_exe.pause = not self.script_exe.pause

    def on_stop(self):
        """ Stop callback function """
        if not self.script_exe.running:
            spawn_box("Script reader", "The script is not running. Nothing to stop",
                        QMessageBox.Warning)
            return
        self.script_exe.stop = True

    def on_load(self):
        """ Callback that update the filename text field """
        script_name = QFileDialog.getOpenFileName(
            None, "", "", "Scripts (*.sc.py *.txt)")[0]
        self.txt_Path.setText(script_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RxWindow()
    win.show()
    sys.exit(app.exec())
