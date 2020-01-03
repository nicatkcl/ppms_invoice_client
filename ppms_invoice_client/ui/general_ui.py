# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ppms_pyqt\ui\general.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(618, 143)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.folder_edit = QtWidgets.QLineEdit(Dialog)
        self.folder_edit.setObjectName("folder_edit")
        self.gridLayout.addWidget(self.folder_edit, 0, 1, 1, 1)
        self.folder_btn = QtWidgets.QPushButton(Dialog)
        self.folder_btn.setObjectName("folder_btn")
        self.gridLayout.addWidget(self.folder_btn, 0, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.general_ok = QtWidgets.QPushButton(Dialog)
        self.general_ok.setObjectName("general_ok")
        self.horizontalLayout.addWidget(self.general_ok)
        self.general_cancel = QtWidgets.QPushButton(Dialog)
        self.general_cancel.setObjectName("general_cancel")
        self.horizontalLayout.addWidget(self.general_cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Invoice folder"))
        self.folder_btn.setText(_translate("Dialog", "..."))
        self.general_ok.setText(_translate("Dialog", "OK"))
        self.general_cancel.setText(_translate("Dialog", "Cancel"))
