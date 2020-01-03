# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ppms_invoice_client\ui\email.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(359, 177)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.exchange_username = QtWidgets.QLineEdit(Dialog)
        self.exchange_username.setText("")
        self.exchange_username.setObjectName("exchange_username")
        self.gridLayout.addWidget(self.exchange_username, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.smtp_server = QtWidgets.QLineEdit(Dialog)
        self.smtp_server.setText("")
        self.smtp_server.setObjectName("smtp_server")
        self.gridLayout.addWidget(self.smtp_server, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.from_email = QtWidgets.QLineEdit(Dialog)
        self.from_email.setText("")
        self.from_email.setObjectName("from_email")
        self.gridLayout.addWidget(self.from_email, 3, 2, 1, 1)
        self.exchange_password = QtWidgets.QLineEdit(Dialog)
        self.exchange_password.setText("")
        self.exchange_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.exchange_password.setObjectName("exchange_password")
        self.gridLayout.addWidget(self.exchange_password, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.email_ok = QtWidgets.QPushButton(Dialog)
        self.email_ok.setObjectName("email_ok")
        self.horizontalLayout_5.addWidget(self.email_ok)
        self.email_cancel = QtWidgets.QPushButton(Dialog)
        self.email_cancel.setObjectName("email_cancel")
        self.horizontalLayout_5.addWidget(self.email_cancel)
        self.gridLayout.addLayout(self.horizontalLayout_5, 6, 0, 1, 3)
        self.test_address = QtWidgets.QLineEdit(Dialog)
        self.test_address.setObjectName("test_address")
        self.gridLayout.addWidget(self.test_address, 5, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.test_chk = QtWidgets.QCheckBox(Dialog)
        self.test_chk.setText("")
        self.test_chk.setObjectName("test_chk")
        self.gridLayout.addWidget(self.test_chk, 4, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Email Settings"))
        self.label_5.setText(_translate("Dialog", "Test address"))
        self.label.setText(_translate("Dialog", "Exchange username"))
        self.label_2.setText(_translate("Dialog", "Exchange password"))
        self.label_4.setText(_translate("Dialog", "From address"))
        self.label_3.setText(_translate("Dialog", "SMTP server"))
        self.email_ok.setText(_translate("Dialog", "OK"))
        self.email_cancel.setText(_translate("Dialog", "Cancel"))
        self.label_6.setText(_translate("Dialog", "Test mode"))
