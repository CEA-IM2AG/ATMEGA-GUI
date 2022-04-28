# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../resources/qtui/Fenetre_RX.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(921, 473)
        Dialog.setMinimumSize(QtCore.QSize(921, 473))
        Dialog.setMaximumSize(QtCore.QSize(921, 473))
        self.btn_Browse = QtWidgets.QPushButton(Dialog)
        self.btn_Browse.setGeometry(QtCore.QRect(20, 20, 161, 31))
        self.btn_Browse.setObjectName("btn_Browse")
        self.txt_Path = QtWidgets.QLineEdit(Dialog)
        self.txt_Path.setGeometry(QtCore.QRect(190, 20, 471, 31))
        self.txt_Path.setObjectName("txt_Path")
        self.btn_Demarer = QtWidgets.QPushButton(Dialog)
        self.btn_Demarer.setGeometry(QtCore.QRect(20, 70, 121, 31))
        self.btn_Demarer.setObjectName("btn_Demarer")
        self.btn_Pause = QtWidgets.QPushButton(Dialog)
        self.btn_Pause.setGeometry(QtCore.QRect(160, 70, 71, 31))
        self.btn_Pause.setObjectName("btn_Pause")
        self.btn_Stop = QtWidgets.QPushButton(Dialog)
        self.btn_Stop.setGeometry(QtCore.QRect(250, 70, 121, 31))
        self.btn_Stop.setObjectName("btn_Stop")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(19, 119, 881, 331))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.Affichage = QtWidgets.QTextBrowser(self.gridLayoutWidget)
        self.Affichage.setObjectName("Affichage")
        self.gridLayout.addWidget(self.Affichage, 0, 0, 1, 1)
        self.pgb = QtWidgets.QProgressBar(Dialog)
        self.pgb.setEnabled(True)
        self.pgb.setGeometry(QtCore.QRect(540, 80, 171, 16))
        self.pgb.setProperty("value", 0)
        self.pgb.setTextVisible(False)
        self.pgb.setObjectName("pgb")
        self.pgbLabel = QtWidgets.QLabel(Dialog)
        self.pgbLabel.setGeometry(QtCore.QRect(720, 80, 181, 16))
        self.pgbLabel.setText("")
        self.pgbLabel.setObjectName("pgbLabel")
        self.btn_Visualisation = QtWidgets.QPushButton(Dialog)
        self.btn_Visualisation.setGeometry(QtCore.QRect(390, 70, 131, 31))
        self.btn_Visualisation.setObjectName("btn_Visualisation")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_Browse.setText(_translate("Dialog", "Charger un Script"))
        self.btn_Demarer.setText(_translate("Dialog", "Démarer"))
        self.btn_Pause.setText(_translate("Dialog", "Pause"))
        self.btn_Stop.setText(_translate("Dialog", "Stopper"))
        self.btn_Visualisation.setText(_translate("Dialog", "Visualisation"))
