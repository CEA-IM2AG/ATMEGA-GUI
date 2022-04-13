""" RX scripting window """


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class Window_RX:
    def setupUi(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.resize(921, 473)
        dialog.setMinimumSize(QtCore.QSize(921, 473))
        dialog.setMaximumSize(QtCore.QSize(921, 473))
        self.pushButton = QtWidgets.QPushButton(dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.loadscript)
        self.filenameLineEdit = QtWidgets.QLineEdit(dialog)
        self.filenameLineEdit.setGeometry(QtCore.QRect(150, 20, 471, 31))
        self.filenameLineEdit.setObjectName("lineEdit")
        self.startButton = QtWidgets.QPushButton(dialog)
        self.startButton.setGeometry(QtCore.QRect(20, 70, 121, 31))
        self.startButton.setObjectName("pushButton_2")
        self.pauseButton = QtWidgets.QPushButton(dialog)
        self.pauseButton.setGeometry(QtCore.QRect(160, 70, 61, 31))
        self.pauseButton.setObjectName("pushButton_3")
        self.stopButton = QtWidgets.QPushButton(dialog)
        self.stopButton.setGeometry(QtCore.QRect(240, 70, 121, 31))
        self.stopButton.setObjectName("pushButton_4")
        self.gridLayoutWidget = QtWidgets.QWidget(dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(19, 119, 881, 331))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Charger un Script"))
        self.startButton.setText(_translate("Dialog", "Demarer"))
        self.startButton.clicked.connect(self.on_start)
        self.pauseButton.setText(_translate("Dialog", "Pause"))
        self.pauseButton.clicked.connect(self.on_pause)
        self.stopButton.setText(_translate("Dialog", "Stopper"))
        self.stopButton.clicked.connect(self.on_stop)

    def loadscript(self):
        script_name = QFileDialog.getOpenFileName(
            None, "", "", "Scripts (*.sc.py *.txt)", None)[0]
        self.filenameLineEdit.setText(script_name)

    def on_start(self):
        """ Start callback function """
        print("Start button clicked")

    def on_stop(self):
        """ Stop callback function """
        print("Stop button clicked")

    def on_pause(self):
        """ Pause callback function """
        print("Pause button clicked")