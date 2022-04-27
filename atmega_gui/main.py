""" Main TEST ram client window """

from PyQt5 import QtCore
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from time import time

import logging
import sys

from atmega.ram import RAM

from atmega_gui.views.Fenetre_main_ui import Ui_Dialog as MainUI
from atmega_gui.rx import RxWindow
from atmega_gui.util import spawn_box

log = logging.getLogger("ATMEGA GUI")


class MainWindow(QMainWindow, MainUI):
    def __init__(self, parent=None):
        """ Initialisation of the window and subwindows """
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        # RX subwindow
        self.RX_ui = RxWindow(self)
        # Connection à la carte
        try:
            self.ram = RAM(timeout=1)
        except:
            self.ram = None
            log.info("No ram found")
            spawn_box("Connection error", "No device found", QMessageBox.Critical)

    def connectSignalsSlots(self):
        """ Implement all the actions on each component """
        # combos
        self.combo_Circuit.activated.connect(self.on_device_change)
        self.combo_Baudrate.activated.connect(self.on_baudrate_change)
        # buttons
        self.btn_RX.clicked.connect(self.openRX)
        self.btn_Exit.clicked.connect(self.closeWindow)
        self.btn_InitRAM.clicked.connect(self.on_reset)
        self.btn_Lire.clicked.connect(self.on_read)
        self.btn_Ecrire.clicked.connect(self.on_write)
        self.btn_DumpRAM.clicked.connect(self.on_dump)
        self.btn_TestRS.clicked.connect(self.on_chip_test)
        # validators
        hex_value_validator = QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,2}"))
        hex_addr_validator = QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,4}"))
        self.txt_Ecrire.setValidator(hex_value_validator)
        self.txt_InitRAM.setValidator(hex_value_validator)
        self.txt_Adresse.setValidator(hex_addr_validator)

    def closeWindow(self):
        """ Close all subwindows """
        self.RX_ui.close()
        if self.ram is not None: # Restauration de l'appareil
            self.ram.close()
        self.close()

    def openRX(self):
        """ Open RX subwindow """
        self.RX_ui.show()

    def on_device_change(self):
        """ Device change callback function """
        device = self.combo_Circuit.currentText()
        if device == "ATmega128":
            self.ram.ram_size = 2**14
        else: # atmega32
            self.ram.ram_size = 2**11

    def on_reset(self):
        """ Reset callback function """
        str_value = self.txt_InitRAM.text()
        if not str_value:
            spawn_box("Reset error", "Empty reset value")
            return
        value = int(str_value, base=16)
        complement = self.check_Comple.isChecked()
        increment = self.check_Incre.isChecked()
        try:
            self.ram.reset(value, increment, complement)
        except Exception as e:
            log.warn(e)
            spawn_box("Reset error", "Connection failed")
            return
        spawn_box("Reset", "Successfully done", QMessageBox.Information)

    def on_read(self):
        """ Read callback function """
        str_address = self.txt_Adresse.text()
        if not str_address:
            spawn_box("Read error", "Empty address")
            return
        address = int(str_address, base=16)
        try:
            val = self.ram.read(address)
        except Exception as e:
            log.warn(e)
            spawn_box("Read error", "Connection failed")
            return
        self.txt_Lire.setText(hex(val))

    def on_write(self):
        """ Write callback function """
        str_address = self.txt_Adresse.text()
        str_value = self.txt_Ecrire.text()
        if not str_address:
            spawn_box("Write error", "Empty address")
            return
        if not str_value:
            spawn_box("Write error", "Empty value")
            return
        address = int(str_address, base=16)
        value = int(str_value, base=16)
        try:
            self.ram.write(value, address)
        except Exception as e:
            print(e)
            spawn_box("Write error", "Connection failed")

    def on_dump(self):
        """ Dump callback function """
        # TODO progress bar
        open = self.check_EditPlus2.isChecked()
        t1 = time()
        try:
            self.ram.dump_to_file("dump.txt")
        except Exception as e:
            log.warn(e)
            spawn_box("Dump error", "Connection failed")
            return
        spawn_box("Dump", f"Successfully done in {round(time() - t1, 2)}s",
                        QMessageBox.Information)
        if open:
            if "linux" in sys.platform:
                from os import spawnlp, P_NOWAIT
                spawnlp(P_NOWAIT, "xdg-open", "xdg-open", "dump.txt")
            elif sys.platform == "win32":
                pass # TODO windows implementation
            else:
                spawn_box("Dump open error", f"Unknown {sys.platform} operating system",
                        QMessageBox.Critical)

    def on_chip_test(self):
        """ Test callback function """
        baudrate = int(self.combo_Baudrate.currentText())
        try:
            if self.ram is None:
                self.ram = RAM(quality_test=True, timeout=1)
            else:
                self.ram = RAM(quality_test=True, timeout=1, baudrate=baudrate)
        except Exception as e:
            log.warn(e)
            self.ram = None
            spawn_box("Test error", "Connection failed")
            return
        spawn_box("RS232 test", f"Successfully done using port {self.ram.serial.port}",
                     QMessageBox.Information)

    def on_baudrate_change(self):
        """ Baudrate change callback function """
        baudrate = int(self.combo_Baudrate.currentText())
        try:
            self.ram.change_baudrate(baudrate)
        except Exception as e:
            log.warn(e)
            spawn_box("Baudrate change error", "Connection failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
