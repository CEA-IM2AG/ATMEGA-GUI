# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualisation.ui'
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
        self.radio_ResCourant.setGeometry(QtCore.QRect(20, 20, 141, 21))
        self.radio_ResCourant.setObjectName("radio_ResCourant")
        self.radio_ResEnreg = QtWidgets.QRadioButton(Dialog)
        self.radio_ResEnreg.setGeometry(QtCore.QRect(20, 50, 151, 31))
        self.radio_ResEnreg.setObjectName("radio_ResEnreg")
        self.txt_Path = QtWidgets.QLineEdit(Dialog)
        self.txt_Path.setGeometry(QtCore.QRect(300, 50, 421, 31))
        self.txt_Path.setObjectName("txt_Path")
        self.btn_ChargeFich = QtWidgets.QPushButton(Dialog)
        self.btn_ChargeFich.setGeometry(QtCore.QRect(190, 50, 101, 31))
        self.btn_ChargeFich.setObjectName("btn_ChargeFich")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(30, 130, 301, 101))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.radio_Diff = QtWidgets.QRadioButton(self.frame)
        self.radio_Diff.setGeometry(QtCore.QRect(20, 40, 111, 21))
        self.radio_Diff.setObjectName("radio_Diff")
        self.radio_Incre = QtWidgets.QRadioButton(self.frame)
        self.radio_Incre.setGeometry(QtCore.QRect(20, 10, 121, 31))
        self.radio_Incre.setObjectName("radio_Incre")
        self.check_Zoom = QtWidgets.QCheckBox(self.frame)
        self.check_Zoom.setGeometry(QtCore.QRect(20, 70, 85, 21))
        self.check_Zoom.setObjectName("check_Zoom")
        self.btn_Load = QtWidgets.QPushButton(self.frame)
        self.btn_Load.setGeometry(QtCore.QRect(200, 30, 80, 41))
        self.btn_Load.setObjectName("btn_Load")
        self.btn_NextFrame = QtWidgets.QPushButton(Dialog)
        self.btn_NextFrame.setGeometry(QtCore.QRect(580, 210, 41, 41))
        self.btn_NextFrame.setObjectName("btn_NextFrame")
        self.btn_PrevFrame = QtWidgets.QPushButton(Dialog)
        self.btn_PrevFrame.setGeometry(QtCore.QRect(540, 210, 41, 41))
        self.btn_PrevFrame.setObjectName("btn_PrevFrame")
        self.txt_ChoixImage = QtWidgets.QLineEdit(Dialog)
        self.txt_ChoixImage.setGeometry(QtCore.QRect(380, 220, 61, 31))
        self.txt_ChoixImage.setObjectName("txt_ChoixImage")
        self.lbl_ImagesTotal = QtWidgets.QLabel(Dialog)
        self.lbl_ImagesTotal.setGeometry(QtCore.QRect(450, 220, 81, 31))
        self.lbl_ImagesTotal.setObjectName("lbl_ImagesTotal")
        self.btn_SaveImage = QtWidgets.QPushButton(Dialog)
        self.btn_SaveImage.setGeometry(QtCore.QRect(670, 160, 141, 41))
        self.btn_SaveImage.setObjectName("btn_SaveImage")
        self.btn_SaveTout = QtWidgets.QPushButton(Dialog)
        self.btn_SaveTout.setGeometry(QtCore.QRect(670, 210, 141, 41))
        self.btn_SaveTout.setObjectName("btn_SaveTout")
        self.btn_Graph = QtWidgets.QPushButton(Dialog)
        self.btn_Graph.setGeometry(QtCore.QRect(670, 110, 141, 41))
        self.btn_Graph.setObjectName("btn_Graph")
        self.btn_PlayPause = QtWidgets.QPushButton(Dialog)
        self.btn_PlayPause.setGeometry(QtCore.QRect(580, 120, 41, 41))
        self.btn_PlayPause.setObjectName("btn_PlayPause")
        self.txt_Framerate = QtWidgets.QLineEdit(Dialog)
        self.txt_Framerate.setGeometry(QtCore.QRect(470, 130, 51, 31))
        self.txt_Framerate.setObjectName("txt_Framerate")
        self.lbl_s = QtWidgets.QLabel(Dialog)
        self.lbl_s.setGeometry(QtCore.QRect(530, 130, 31, 31))
        self.lbl_s.setObjectName("lbl_s")

        self.retranslateUi(Dialog)
        self.radio_ResCourant.toggled['bool'].connect(self.txt_Path.setDisabled)
        self.radio_ResEnreg.toggled['bool'].connect(self.txt_Path.setEnabled)
        self.radio_ResCourant.toggled['bool'].connect(self.btn_ChargeFich.setDisabled)
        self.radio_ResEnreg.toggled['bool'].connect(self.btn_ChargeFich.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.radio_ResCourant.setText(_translate("Dialog", "Resultat courant"))
        self.radio_ResEnreg.setText(_translate("Dialog", "Resultat enregistre"))
        self.btn_ChargeFich.setText(_translate("Dialog", "Charger fichier"))
        self.radio_Diff.setText(_translate("Dialog", "Differentielle"))
        self.radio_Incre.setText(_translate("Dialog", "Incementale"))
        self.check_Zoom.setText(_translate("Dialog", "Zoom"))
        self.btn_Load.setText(_translate("Dialog", "Load"))
        self.btn_NextFrame.setText(_translate("Dialog", ">"))
        self.btn_PrevFrame.setText(_translate("Dialog", "<"))
        self.txt_ChoixImage.setText(_translate("Dialog", "1"))
        self.lbl_ImagesTotal.setText(_translate("Dialog", "/"))
        self.btn_SaveImage.setText(_translate("Dialog", "Enregistrer image"))
        self.btn_SaveTout.setText(_translate("Dialog", "Tout enregistrer"))
        self.btn_Graph.setText(_translate("Dialog", "Graphique de fautes"))
        self.btn_PlayPause.setText(_translate("Dialog", "Play"))
        self.txt_Framerate.setText(_translate("Dialog", "0.5"))
        self.lbl_s.setText(_translate("Dialog", "s"))