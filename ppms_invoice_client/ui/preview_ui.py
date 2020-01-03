# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ppms_invoice_client\ui\preview.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 681)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.invoice_preview = QtWidgets.QTextEdit(Dialog)
        self.invoice_preview.setReadOnly(True)
        self.invoice_preview.setObjectName("invoice_preview")
        self.gridLayout.addWidget(self.invoice_preview, 1, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.piemail_edit = QtWidgets.QLineEdit(Dialog)
        self.piemail_edit.setObjectName("piemail_edit")
        self.horizontalLayout_2.addWidget(self.piemail_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.ademail_edit = QtWidgets.QLineEdit(Dialog)
        self.ademail_edit.setObjectName("ademail_edit")
        self.horizontalLayout_3.addWidget(self.ademail_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.preview_cancel = QtWidgets.QPushButton(Dialog)
        self.preview_cancel.setObjectName("preview_cancel")
        self.horizontalLayout.addWidget(self.preview_cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Invoice Preview"))
        self.label.setText(_translate("Dialog", "To"))
        self.label_2.setText(_translate("Dialog", "CC"))
        self.preview_cancel.setText(_translate("Dialog", "Close"))
