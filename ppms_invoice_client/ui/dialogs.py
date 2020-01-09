"""Dialogs accessible from the toolbar in the main window."""
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

from . import ppms_ui as ppms_UI
from . import email_ui as email_UI
from . import template_ui as template_UI
from . import facility_ui as facility_UI
from . import preview_ui as preview_UI
from . import general_ui as general_UI



class PPMSDialog(QtWidgets.QDialog):
    """A popup dialog holding URL and API key for PPMS"""
    def __init__(self, parent):
        super(PPMSDialog, self).__init__(parent)
        self.parent = parent       
        self.init_ui()

    def init_ui(self):
        self.ui = ppms_UI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.ppms_url.setText(self.parent.ppms_url)
        self.ui.ppms_apikey.setText(self.parent.ppms_key)

        self.ui.ppms_ok.clicked.connect(self.okClicked)
        self.ui.ppms_cancel.clicked.connect(self.cancelClicked)

    @pyqtSlot()
    def okClicked(self):
        self.parent.ppms_url = self.ui.ppms_url.text()
        self.parent.ppms_key = self.ui.ppms_apikey.text()
        self.close()

    @pyqtSlot()
    def cancelClicked(self):
        self.close()


class EmailDialog(QtWidgets.QDialog):
    """
    A popup dialog holding settings required for sending email
    using Microsoft exchange server."""
    def __init__(self, parent):
        super(EmailDialog, self).__init__(parent)
        self.parent = parent       
        self.init_ui()

    def init_ui(self):
        self.ui = email_UI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.exchange_username.setText(self.parent.exchange_username)
        self.ui.exchange_password.setText(self.parent.exchange_password)
        self.ui.smtp_server.setText(self.parent.smtp_server)
        self.ui.from_email.setText(self.parent.from_email)
        self.ui.test_chk.setChecked(self.parent.test_mode)
        self.ui.test_address.setText(self.parent.test_address)

        self.ui.email_ok.clicked.connect(self.okClicked)
        self.ui.email_cancel.clicked.connect(self.cancelClicked)

    @pyqtSlot()
    def okClicked(self):
        self.parent.exchange_username = self.ui.exchange_username.text()
        self.parent.exchange_password = self.ui.exchange_password.text()
        self.parent.smtp_server = self.ui.smtp_server.text()
        self.parent.from_email = self.ui.from_email.text()
        self.parent.test_mode = self.ui.test_chk.isChecked()
        self.parent.test_address = self.ui.test_address.text()
        self.close()

    @pyqtSlot()
    def cancelClicked(self):
        self.close()


class InvoiceTemplateDialog(QtWidgets.QDialog):
    """
    A popup dialog holding settings required for constructing an
    invoice summary email."""
    def __init__(self, parent):
        super(InvoiceTemplateDialog, self).__init__(parent)
        self.parent = parent       
        self.init_ui()

    def init_ui(self):
        self.ui = template_UI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.session_chk.setChecked(self.parent.session_chk)
        self.ui.user_chk.setChecked(self.parent.user_chk)
        self.ui.type_chk.setChecked(self.parent.type_chk)
        self.ui.system_chk.setChecked(self.parent.system_chk)
        self.ui.date_chk.setChecked(self.parent.date_chk)
        self.ui.start_chk.setChecked(self.parent.start_chk)
        self.ui.booked_chk.setChecked(self.parent.booked_chk)
        self.ui.used_chk.setChecked(self.parent.used_chk)
        self.ui.notes_chk.setChecked(self.parent.notes_chk)
        self.ui.init_amount_chk.setChecked(self.parent.init_amount_chk)
        self.ui.fees_chk.setChecked(self.parent.fees_chk)
        self.ui.final_amount_chk.setChecked(self.parent.final_amount_chk)
        self.ui.message_text.setPlainText(self.parent.message_text)

        self.ui.template_ok.clicked.connect(self.okClicked)
        self.ui.template_cancel.clicked.connect(self.cancelClicked)

    @pyqtSlot()
    def okClicked(self):
        self.parent.session_chk = self.ui.session_chk.isChecked()
        self.parent.user_chk = self.ui.user_chk.isChecked()
        self.parent.type_chk = self.ui.type_chk.isChecked()
        self.parent.system_chk = self.ui.system_chk.isChecked()
        self.parent.date_chk = self.ui.date_chk.isChecked()
        self.parent.start_chk = self.ui.start_chk.isChecked()
        self.parent.booked_chk = self.ui.booked_chk.isChecked()
        self.parent.used_chk = self.ui.used_chk.isChecked()
        self.parent.notes_chk = self.ui.notes_chk.isChecked()
        self.parent.init_amount_chk = self.ui.init_amount_chk.isChecked()
        self.parent.fees_chk = self.ui.fees_chk.isChecked()
        self.parent.final_amount_chk = self.ui.final_amount_chk.isChecked()
        self.parent.message_text = self.ui.message_text.toPlainText()

        self.close()

    @pyqtSlot()
    def cancelClicked(self):
        self.close()


class FacilityDialog(QtWidgets.QDialog):
    """A popup dialog holding name and email of facility manager"""
    def __init__(self, parent):
        super(FacilityDialog, self).__init__(parent)
        self.parent = parent       
        self.init_ui()

    def init_ui(self):
        self.ui = facility_UI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.facility_code.setText(self.parent.facility_code)
        self.ui.facility_name.setText(self.parent.facility_name)
        self.ui.facility_email.setText(self.parent.facility_email)
        self.ui.manager_name.setText(self.parent.manager_name)
        self.ui.manager_email.setText(self.parent.manager_email)

        self.ui.facility_ok.clicked.connect(self.okClicked)
        self.ui.facility_cancel.clicked.connect(self.cancelClicked)

    @pyqtSlot()
    def okClicked(self):
        self.parent.facility_code = self.ui.facility_code.text()
        self.parent.facility_name = self.ui.facility_name.text()
        self.parent.facility_email = self.ui.facility_email.text()
        self.parent.manager_name = self.ui.manager_name.text()
        self.parent.manager_email = self.ui.manager_email.text()
        self.close()

    @pyqtSlot()
    def cancelClicked(self):
        self.close()


class PreviewDialog(QtWidgets.QDialog):
    """A popup dialog showing a preview of the invoice to be emailed"""
    def __init__(self, parent, bcode, html=None):
        super(PreviewDialog, self).__init__(parent)
        self.parent = parent
        self.bcode = bcode
        self.init_ui()
        item = parent.invoice.item_for_bcode(bcode)
        self.renderHTML(html, item.addresses)

    def init_ui(self):
        self.ui = preview_UI.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.preview_cancel.clicked.connect(self.cancelClicked)

        self.ui.piemail_edit.textChanged.connect(self.piemailChanged)
        self.ui.ademail_edit.textChanged.connect(self.ademailChanged)

    def _addressesToString(self, addresses):
        return '; '.join([a for a in addresses])

    def _stringToAddresses(self, text):
        if ";" in text:
            return [t.strip(" ") for t in text.split(";")]
        elif "," in text:
            return [t.strip(" ") for t in text.split(",")]
        else:
            return [text]

    def piemailChanged(self, text):
        item = self.parent.invoice.item_for_bcode(self.bcode)
        piemail = self._stringToAddresses(text)
        item.addresses["to_email"] = piemail

    def ademailChanged(self, text):
        item = self.parent.invoice.item_for_bcode(self.bcode)
        admemail = self._stringToAddresses(text)
        item.addresses["cc_email"] = admemail

    def renderHTML(self, html, addresses):
        if html:
            to_email = self._addressesToString(addresses['to_email'])
            self.ui.piemail_edit.setText(to_email)
            cc_email = self._addressesToString(addresses['cc_email'])
            self.ui.ademail_edit.setText(cc_email)
            self.ui.invoice_preview.insertHtml(html)
            self.ui.invoice_preview.verticalScrollBar().setValue(
                self.ui.invoice_preview.verticalScrollBar().minimum()
            )

    @pyqtSlot()
    def cancelClicked(self):
        self.close()


class GeneralDialog(QtWidgets.QDialog):
    """A popup dialog holding general settings"""
    def __init__(self, parent, folder=None):
        super(GeneralDialog, self).__init__(parent)
        self.parent = parent       
        self.init_ui()

    def init_ui(self):
        self.ui = general_UI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.folder_edit.setText(self.parent.invoice_folder)

        self.ui.folder_btn.clicked.connect(self.selectFolder)
        self.ui.general_ok.clicked.connect(self.okClicked)
        self.ui.general_cancel.clicked.connect(self.cancelClicked)

    @pyqtSlot()
    def selectFolder(self):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.folder_edit.setText(folder)

    @pyqtSlot()
    def okClicked(self):
        self.parent.invoice_folder = self.ui.folder_edit.text()
        self.close()

    @pyqtSlot()
    def cancelClicked(self):
        self.close()

