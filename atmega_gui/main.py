""" Main TEST ram client window """

from logging.handlers import QueueListener
from sys import platform, argv, exit

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox

from time import time

from atmega.ram import RAM
from atmega_gui.rx import Window_RX


class MainWindow:
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.show()
        try:
            self.ram = RAM()
        except:
            self.spawn_box("Connection error",
                "No device connected. Try the 'Test RS232' button")
            self.ram = None

    def openRX(self):
        self.RX_Dialog.show()

    def closeWindow(self):
        """ Clean up """
        if self.ram:
            self.ram.close()
        self.dialog.close()
        self.RX_Dialog.close()

    def setupUi(self, Dialog):
        """ Auto generated place holders """
        self.RX_Dialog = QtWidgets.QDialog()
        self.RX_ui = Window_RX()
        self.RX_ui.setupUi(self.RX_Dialog)
        Dialog.setObjectName("Dialog")
        Dialog.resize(389, 531)
        Dialog.setMinimumSize(QtCore.QSize(389, 531))
        Dialog.setMaximumSize(QtCore.QSize(389, 531))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 10, 91, 21))
        self.label.setObjectName("label")
        self.deviceListComboBox = QtWidgets.QComboBox(Dialog)
        self.deviceListComboBox.setGeometry(QtCore.QRect(20, 10, 111, 23))
        self.deviceListComboBox.setObjectName("deviceListComboBox")
        self.deviceListComboBox.addItem("")
        self.deviceListComboBox.addItem("")
        self.writeValueLineEdit = QtWidgets.QLineEdit(Dialog)
        self.writeValueLineEdit.setGeometry(QtCore.QRect(160, 70, 61, 23))
        self.writeValueLineEdit.setObjectName("lineEdit")
        self.resetButton = QtWidgets.QPushButton(Dialog)
        self.resetButton.setGeometry(QtCore.QRect(99, 220, 121, 41))
        self.resetButton.setObjectName("resetButton")
        self.readButton = QtWidgets.QPushButton(Dialog)
        self.readButton.setGeometry(QtCore.QRect(240, 130, 80, 23))
        self.readButton.setObjectName("readButton")
        self.addressLineEdit = QtWidgets.QLineEdit(Dialog)
        self.addressLineEdit.setGeometry(QtCore.QRect(20, 100, 61, 23))
        self.addressLineEdit.setObjectName("resetValueLineEdit_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 100, 61, 21))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 190, 371, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.resetValueLineEdit = QtWidgets.QLineEdit(Dialog)
        self.resetValueLineEdit.setGeometry(QtCore.QRect(20, 230, 61, 23))
        self.resetValueLineEdit.setObjectName("resetValueLineEdit_3")
        self.writeButton = QtWidgets.QPushButton(Dialog)
        self.writeButton.setGeometry(QtCore.QRect(240, 70, 80, 23))
        self.writeButton.setObjectName("writeButton")
        self.incrementCheckBox = QtWidgets.QCheckBox(Dialog)
        self.incrementCheckBox.setGeometry(QtCore.QRect(230, 220, 111, 21))
        self.incrementCheckBox.setObjectName("incrementCheckBox")
        self.complementCheckBox = QtWidgets.QCheckBox(Dialog)
        self.complementCheckBox.setGeometry(QtCore.QRect(230, 240, 121, 21))
        self.complementCheckBox.setObjectName("complementCheckBox")
        self.dumpButton = QtWidgets.QPushButton(Dialog)
        self.dumpButton.setGeometry(QtCore.QRect(100, 280, 121, 41))
        self.dumpButton.setObjectName("dumpButton")
        self.openWithCheckBox = QtWidgets.QCheckBox(Dialog)
        self.openWithCheckBox.setGeometry(QtCore.QRect(20, 380, 331, 21))
        self.openWithCheckBox.setObjectName("openWithCheckBox")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 420, 81, 21))
        self.label_3.setObjectName("label_3")
        self.baudrateComboBox = QtWidgets.QComboBox(Dialog)
        self.baudrateComboBox.setGeometry(QtCore.QRect(20, 420, 91, 23))
        self.baudrateComboBox.setObjectName("baudrateComboBox")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.baudrateComboBox.addItem("")
        self.testButton = QtWidgets.QPushButton(Dialog)
        self.testButton.setGeometry(QtCore.QRect(20, 470, 91, 41))
        self.testButton.setObjectName("testButton")
        self.rxButton = QtWidgets.QPushButton(Dialog)
        self.rxButton.setGeometry(QtCore.QRect(150, 470, 51, 41))
        self.rxButton.setObjectName("rxButton")
        self.rxButton.clicked.connect(self.openRX)
        self.exitButton = QtWidgets.QPushButton(Dialog)
        self.exitButton.setGeometry(QtCore.QRect(280, 470, 71, 41))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(self.closeWindow)
        self.readValueLineEdit = QtWidgets.QLineEdit(Dialog)
        self.readValueLineEdit.setGeometry(QtCore.QRect(160, 130, 61, 23))
        self.readValueLineEdit.setObjectName("lineEdit_4")
        self.readValueLineEdit.setDisabled(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate

        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.label.setText(_translate("Dialog", "Circuit teste"))
        self.label_2.setText(_translate("Dialog", "Adresse"))
        self.label_3.setText(_translate("Dialog", "Baudrate"))
        
        self.deviceListComboBox.setItemText(0, _translate("Dialog", "ATMega128"))
        self.deviceListComboBox.setItemText(1, _translate("Dialog", "ATMega32"))
        self.deviceListComboBox.activated.connect(self.on_device_change)

        self.resetButton.setText(_translate("Dialog", "Initialiser la RAM"))
        self.resetButton.clicked.connect(self.on_reset)

        self.readButton.setText(_translate("Dialog", "Lire"))
        self.readButton.clicked.connect(self.on_read)

        hex_value_validator = QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,2}"))
        hex_addr_validator = QRegExpValidator(QtCore.QRegExp("[0-9A-Fa-f]{1,4}"))
        self.writeValueLineEdit.setText(_translate("Dialog", "FF"))
        self.addressLineEdit.setText(_translate("Dialog", "3190"))
        self.resetValueLineEdit.setText(_translate("Dialog", "FF"))
        self.writeValueLineEdit.setValidator(hex_value_validator)
        self.addressLineEdit.setValidator(hex_addr_validator)

        self.writeButton.setText(_translate("Dialog", "Ecrire"))
        self.writeButton.clicked.connect(self.on_write)

        self.incrementCheckBox.setText(_translate("Dialog", "Incrementale"))
        self.complementCheckBox.setText(_translate("Dialog", "Complemente"))
        self.openWithCheckBox.setText(_translate("Dialog", "Afficher le resultat de la relecture (EditPlus 2)"))

        self.dumpButton.setText(_translate("Dialog", "Dumper la RAM"))
        self.dumpButton.clicked.connect(self.on_dump)

        self.baudrateComboBox.setItemText(0, _translate("Dialog", "9600"))
        self.baudrateComboBox.setItemText(1, _translate("Dialog", "19200"))
        self.baudrateComboBox.setItemText(2, _translate("Dialog", "38400"))
        self.baudrateComboBox.setItemText(3, _translate("Dialog", "1000000"))
        self.baudrateComboBox.activated.connect(self.on_baudrate_change)

        self.testButton.setText(_translate("Dialog", "Test_RS232"))
        self.testButton.clicked.connect(self.on_chip_test)

        self.rxButton.setText(_translate("Dialog", "RX"))

        self.exitButton.setText(_translate("Dialog", "Exit"))

    @staticmethod
    def spawn_box(title, text, icon=QMessageBox.Warning):
        """
            Spawn a message box
            :param title: title of the message box
            :param text: text of the message box
            :param icon: icon of the message box
        """
        box = QMessageBox()
        box.setWindowTitle(title)
        box.setText(text)
        box.setIcon(icon)
        box.exec()

    def on_write(self):
        """ Write callback function """
        str_address = self.addressLineEdit.text()
        str_value = self.writeValueLineEdit.text()
        if not str_address:
            self.spawn_box("Write error", "Empty address")
            return
        if not str_value:
            self.spawn_box("Write error", "Empty value")
            return
        address = int(str_address, base=16)
        value = int(str_value, base=16)
        try:
            self.ram.write(value, address)
        except:
            self.spawn_box("Write error", "Connection failed")

    def on_read(self):
        """ Read callback function """
        str_address = self.addressLineEdit.text()
        if not str_address:
            self.spawn_box("Read error", "Empty address")
            return
        address = int(str_address, base=16)
        try:
            val = self.ram.read(address)
        except:
            self.spawn_box("Read error", "Connection failed")
            return
        self.readValueLineEdit.setText(hex(val))

    def on_reset(self):
        """ Reset callback function """
        str_value = self.resetValueLineEdit.text()
        if not str_value:
            self.spawn_box("Reset error", "Empty reset value")
            return
        value = int(str_value, base=16)
        complement = self.complementCheckBox.isChecked()
        increment = self.incrementCheckBox.isChecked()
        try:
            self.ram.reset(value, increment, complement)
        except:
            self.spawn_box("Reset error", "Connection failed")
            return
        self.spawn_box("Reset", "Successfully done", QMessageBox.Information)
        
    def on_dump(self):
        """ Dump callback function """
        # TODO progress bar
        open = self.openWithCheckBox.isChecked()
        t1 = time()
        try:
            self.ram.dump_to_file("dump.txt")
        except:
            self.spawn_box("Dump error", "Connection failed")
            return
        self.spawn_box("Dump", f"Successfully done in {round(time() - t1, 2)}s", QMessageBox.Information)
        if open:
            if "linux" in platform:
                spawnlp(P_NOWAIT, "xdg-open", "xdg-open", "dump.txt")
            elif platform == "win32":
                spawnlp(P_NOWAIT, "start", "start", "dump.txt") # TODO test on windows
            else:
                self.spawn_box("Dump open error", f"Unknown {platform} operating system")

    def on_chip_test(self):
        """ Test callback function """
        try:
            self.ram = RAM(quality_test=True)
        except:
            self.ram = None
            self.spawn_box("Test error", "Connection failed")
            return
        self.spawn_box("RS232 test", "Successfully done")

    def on_baudrate_change(self):
        """ Baudrate change callback function """
        baudrate = int(self.baudrateComboBox.currentText())
        try:
            self.ram.change_baudrate(baudrate)
        except:
            self.spawn_box("Baudrate change error", "Connection failed")

    def on_device_change(self):
        """ Device change callback function """
        device = self.deviceListComboBox.currentText()
        if device == "ATmega128":
            self.ram.ram_size = 2**14
        else: # atmega32
            self.ram.ram_size = 2**11


def main():
    app = QtWidgets.QApplication(argv)
    gui = MainWindow()
    exit(app.exec_())


if __name__ == "__main__":
    main()