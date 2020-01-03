# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ppms_pyqt\ui\facility.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(332, 159)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.facility_name = QtWidgets.QLineEdit(Dialog)
        self.facility_name.setText("")
        self.facility_name.setObjectName("facility_name")
        self.gridLayout.addWidget(self.facility_name, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.facility_email = QtWidgets.QLineEdit(Dialog)
        self.facility_email.setText("")
        self.facility_email.setObjectName("facility_email")
        self.gridLayout.addWidget(self.facility_email, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.manager_name = QtWidgets.QLineEdit(Dialog)
        self.manager_name.setText("")
        self.manager_name.setObjectName("manager_name")
        self.gridLayout.addWidget(self.manager_name, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.manager_email = QtWidgets.QLineEdit(Dialog)
        self.manager_email.setText("")
        self.manager_email.setObjectName("manager_email")
        self.gridLayout.addWidget(self.manager_email, 3, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.facility_ok = QtWidgets.QPushButton(Dialog)
        self.facility_ok.setObjectName("facility_ok")
        self.horizontalLayout_5.addWidget(self.facility_ok)
        self.facility_cancel = QtWidgets.QPushButton(Dialog)
        self.facility_cancel.setObjectName("facility_cancel")
        self.horizontalLayout_5.addWidget(self.facility_cancel)
        self.gridLayout.addLayout(self.horizontalLayout_5, 4, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Facility Settings"))
        self.label_4.setText(_translate("Dialog", "Facility name "))
        self.label.setText(_translate("Dialog", "Facility email "))
        self.label_3.setText(_translate("Dialog", "Manager name "))
        self.label_2.setText(_translate("Dialog", "Manager email "))
        self.facility_ok.setText(_translate("Dialog", "OK"))
        self.facility_cancel.setText(_translate("Dialog", "Cancel"))
