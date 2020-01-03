# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ppms_pyqt\ui\ppms.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(335, 124)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ppms_url = QtWidgets.QLineEdit(Dialog)
        self.ppms_url.setText("")
        self.ppms_url.setObjectName("ppms_url")
        self.gridLayout.addWidget(self.ppms_url, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.ppms_apikey = QtWidgets.QLineEdit(Dialog)
        self.ppms_apikey.setText("")
        self.ppms_apikey.setObjectName("ppms_apikey")
        self.gridLayout.addWidget(self.ppms_apikey, 1, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.ppms_ok = QtWidgets.QPushButton(Dialog)
        self.ppms_ok.setObjectName("ppms_ok")
        self.horizontalLayout_5.addWidget(self.ppms_ok)
        self.ppms_cancel = QtWidgets.QPushButton(Dialog)
        self.ppms_cancel.setObjectName("ppms_cancel")
        self.horizontalLayout_5.addWidget(self.ppms_cancel)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PPMS Settings"))
        self.label.setText(_translate("Dialog", "PPMS URL"))
        self.label_2.setText(_translate("Dialog", "PPMS API KEY"))
        self.ppms_ok.setText(_translate("Dialog", "OK"))
        self.ppms_cancel.setText(_translate("Dialog", "Cancel"))
