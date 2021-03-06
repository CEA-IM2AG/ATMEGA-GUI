""" Main TEST ram client window """

from PyQt5 import QtCore
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox

from time import time

import logging
import sys

from atmega.ram import RAM
from atmega.ram import list_devices

from atmega_gui.views.Fenetre_main_ui import Ui_Dialog as MainUI
from atmega_gui.rx import RxWindow
from atmega_gui.util import spawn_box
import atmega_gui.variable as variable

log = logging.getLogger("ATMEGA GUI")


class MainWindow(QMainWindow, MainUI):
    def __init__(self, parent=None):
        """ Initialisation of the window and subwindows """
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        # Connection à la carte
        self.port = None
        try:
            variable.device = RAM(timeout=1)
            self.port = variable.device.serial.port
            index = self.combo_Circuit_2.findText(self.port)
            self.combo_Circuit_2.removeItem(index)
            self.combo_Circuit_2.insertItem(0, self.port)
            self.combo_Circuit_2.setCurrentText(self.port)
        except Exception as e:
            variable.device = None
            log.info(f"No FTDI device found: {e}")
        log.info(f"Final port: {self.port}")
        # RX subwindow
        self.RX_ui = RxWindow(self)

    def connectSignalsSlots(self):
        """ Implement all the actions on each component """
        # combos
        self.resetPorts()
        self.combo_Circuit_2.activated.connect(self.on_port_change)        
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
        self.btn_Actualiser.clicked.connect(self.resetPorts)
        # validators
        hex_value_validator = QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,2}"))
        hex_addr_validator = QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,4}"))
        self.txt_Ecrire.setValidator(hex_value_validator)
        self.txt_InitRAM.setValidator(hex_value_validator)
        self.txt_Adresse.setValidator(hex_addr_validator)

    def resetPorts(self):
        devices = list_devices()
        self.combo_Circuit_2.clear()
        if len(devices) != 0:
            self.port = devices[0]
            self.combo_Circuit_2.removeItem(0)  # remove "No device" item
        else:
            self.combo_Circuit_2.addItem("Aucun port.")
        self.combo_Circuit_2.addItems(devices)

    def closeWindow(self):
        """ Close all subwindows """
        self.RX_ui.close()
        if variable.device is not None: # Restauration de l'appareil
            variable.device.close()
        self.close()

    def openRX(self):
        """ Open RX subwindow """
        self.RX_ui.show()

    def on_port_change(self):
        """ Device change callback function """
        self.port = self.combo_Circuit_2.currentText()

    def on_device_change(self):
        """ Device change callback function """
        if variable.device is None:
            spawn_box("No device", "No device selected.")
            return
        device = self.combo_Circuit.currentText()
        if device == "ATmega128":
            variable.device.ram_size = 2**14
        else: # atmega32
            variable.device.ram_size = 2**11

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
            variable.device.reset(value, increment, complement)
        except Exception as e:
            log.warn(e)
            spawn_box("Reset error", f"Connection failed\n\n{e}")
            return
        spawn_box("Reset", "Successfully done", QMessageBox.Information)

    def on_read(self):
        """ Read callback function """
        if variable.device is None:
            spawn_box("No device", "No device selected.")
            return
        str_address = self.txt_Adresse.text()
        if not str_address:
            spawn_box("Read error", "Empty address")
            return
        address = int(str_address, base=16)
        try:
            val = variable.device.read(address)
        except Exception as e:
            log.warn(e)
            spawn_box("Read error", f"Connection failed\n\n{e}")
            return
        self.txt_Lire.setText(hex(val))

    def on_write(self):
        """ Write callback function """
        if variable.device is None:
            spawn_box("No device", "No device selected.")
            return
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
            variable.device.write(value, address)
        except Exception as e:
            spawn_box("Write error", f"Connection failed\n\n{e}")

    def on_dump(self):
        """ Dump callback function """
        if variable.device is None:
            spawn_box("No device", "No device selected.")
            return
        # TODO progress bar
        open = self.check_EditPlus2.isChecked()
        t1 = time()
        try:
            variable.device.dump_to_file("dump.txt", bar=self.pgb)
        except Exception as e:
            log.warn(e)
            spawn_box("Dump error", f"Connection failed\n\n{e}")
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
                spawn_box(f"Dump open error\n\n{e}", f"Unknown {sys.platform} operating system",
                        QMessageBox.Critical)

    def on_chip_test(self):
        """ Test callback function """
        baudrate = int(self.combo_Baudrate.currentText())
        self.port = self.combo_Circuit_2.currentText()
        try:
            if variable.device is None:
                variable.device = RAM(port=self.port, quality_test=True, timeout=1)
            else:
                variable.device.close()
                variable.device = RAM(port=self.port, quality_test=True, timeout=1, baudrate=baudrate)
        except Exception as e:
            log.warn(e)
            variable.device = None
            spawn_box("RS232 test", f"Could not connect to device {self.port}:\n\n{e}", QMessageBox.Warning)
            return
        if variable.device is not None or variable.device.serial.port is not None:
            spawn_box("RS232 test", f"Successfully done using port {self.port}",
                      QMessageBox.Information)
            

    def on_baudrate_change(self):
        """ Baudrate change callback function """
        if variable.device is None:
            spawn_box("No device", "No device selected.")
            return
        baudrate = int(self.combo_Baudrate.currentText())
        try:
            variable.device.change_baudrate(baudrate)
        except Exception as e:
            log.warn(e)
            spawn_box("Baudrate change error", f"Connection failed\n\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
