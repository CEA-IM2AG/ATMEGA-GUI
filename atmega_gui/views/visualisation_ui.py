# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../resources/qtui/visualisation.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(851, 286)
        Dialog.setMinimumSize(QtCore.QSize(851, 286))
        Dialog.setMaximumSize(QtCore.QSize(851, 286))
        self.radio_ResCourant = QtWidgets.QRadioButton(Dialog)
        self.radio_ResCourant.setGeometry(QtCore.QRect(20, 20, 161, 21))
        self.radio_ResCourant.setObjectName("radio_ResCourant")
        self.radio_ResEnreg = QtWidgets.QRadioButton(Dialog)
        self.radio_ResEnreg.setGeometry(QtCore.QRect(20, 50, 161, 31))
        self.radio_ResEnreg.setChecked(True)
        self.radio_ResEnreg.setObjectName("radio_ResEnreg")
        self.txt_Path = QtWidgets.QLineEdit(Dialog)
        self.txt_Path.setGeometry(QtCore.QRect(330, 50, 421, 31))
        self.txt_Path.setObjectName("txt_Path")
        self.btn_ChargeIndx = QtWidgets.QPushButton(Dialog)
        self.btn_ChargeIndx.setGeometry(QtCore.QRect(190, 50, 131, 31))
        self.btn_ChargeIndx.setObjectName("btn_ChargeIndx")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(30, 130, 301, 101))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.radio_Diff = QtWidgets.QRadioButton(self.frame)
        self.radio_Diff.setGeometry(QtCore.QRect(20, 40, 131, 21))
        self.radio_Diff.setObjectName("radio_Diff")
        self.radio_Incre = QtWidgets.QRadioButton(self.frame)
        self.radio_Incre.setGeometry(QtCore.QRect(20, 10, 131, 31))
        self.radio_Incre.setChecked(True)
        self.radio_Incre.setObjectName("radio_Incre")
        self.check_Zoom = QtWidgets.QCheckBox(self.frame)
        self.check_Zoom.setGeometry(QtCore.QRect(20, 70, 101, 21))
        self.check_Zoom.setObjectName("check_Zoom")
        self.btn_Load = QtWidgets.QPushButton(self.frame)
        self.btn_Load.setGeometry(QtCore.QRect(200, 30, 80, 41))
        self.btn_Load.setObjectName("btn_Load")
        self.btn_NextFrame = QtWidgets.QPushButton(Dialog)
        self.btn_NextFrame.setGeometry(QtCore.QRect(490, 160, 41, 41))
        self.btn_NextFrame.setObjectName("btn_NextFrame")
        self.btn_PrevFrame = QtWidgets.QPushButton(Dialog)
        self.btn_PrevFrame.setGeometry(QtCore.QRect(450, 160, 41, 41))
        self.btn_PrevFrame.setObjectName("btn_PrevFrame")
        self.txt_ChoixImage = QtWidgets.QLineEdit(Dialog)
        self.txt_ChoixImage.setGeometry(QtCore.QRect(430, 220, 61, 31))
        self.txt_ChoixImage.setObjectName("txt_ChoixImage")
        self.lbl_ImagesTotal = QtWidgets.QLabel(Dialog)
        self.lbl_ImagesTotal.setGeometry(QtCore.QRect(500, 220, 81, 31))
        self.lbl_ImagesTotal.setObjectName("lbl_ImagesTotal")
        self.btn_SaveTout = QtWidgets.QPushButton(Dialog)
        self.btn_SaveTout.setGeometry(QtCore.QRect(660, 170, 151, 41))
        self.btn_SaveTout.setObjectName("btn_SaveTout")
        self.pgb = QtWidgets.QProgressBar(Dialog)
        self.pgb.setEnabled(True)
        self.pgb.setGeometry(QtCore.QRect(450, 90, 171, 16))
        self.pgb.setProperty("value", 0)
        self.pgb.setTextVisible(False)
        self.pgb.setObjectName("pgb")

        self.retranslateUi(Dialog)
        self.radio_ResCourant.toggled['bool'].connect(self.txt_Path.setDisabled)
        self.radio_ResEnreg.toggled['bool'].connect(self.txt_Path.setEnabled)
        self.radio_ResCourant.toggled['bool'].connect(self.btn_ChargeIndx.setDisabled)
        self.radio_ResEnreg.toggled['bool'].connect(self.btn_ChargeIndx.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.radio_ResCourant.setText(_translate("Dialog", "R??sultat courant"))
        self.radio_ResEnreg.setText(_translate("Dialog", "R??sultat enregistr??"))
        self.btn_ChargeIndx.setText(_translate("Dialog", "Charger index"))
        self.radio_Diff.setText(_translate("Dialog", "Diff??rentielle"))
        self.radio_Incre.setText(_translate("Dialog", "Incr??mentale"))
        self.check_Zoom.setText(_translate("Dialog", "Zoom"))
        self.btn_Load.setText(_translate("Dialog", "Load"))
        self.btn_NextFrame.setText(_translate("Dialog", ">"))
        self.btn_PrevFrame.setText(_translate("Dialog", "<"))
        self.txt_ChoixImage.setText(_translate("Dialog", "1"))
        self.lbl_ImagesTotal.setText(_translate("Dialog", "/"))
        self.btn_SaveTout.setText(_translate("Dialog", "Tout enregistrer"))
