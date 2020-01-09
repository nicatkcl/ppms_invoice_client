"""Main application definition"""

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot

import numpy as np

from . import main_ui as UI
from .dialogs import (
    PPMSDialog, EmailDialog,
    InvoiceTemplateDialog, FacilityDialog,
    PreviewDialog, GeneralDialog
)
from . import threads
from .progress import Progress


class Window(QtWidgets.QMainWindow):
    """The main GUI window."""
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.ui = UI.Ui_MainWindow()
        self.ui.setupUi(self)           

        # parameters
        self.invoice_folder = ""
        self.ppms_url = ""
        self.ppms_key = ""
        self.exchange_username = ""
        self.exchange_password = ""
        self.smtp_server = ""
        self.from_email = ""
        self.session_chk = False
        self.user_chk = False
        self.type_chk = False
        self.system_chk = False
        self.date_chk = False
        self.start_chk = False
        self.booked_chk = False
        self.used_chk = False
        self.notes_chk = False
        self.init_amount_chk = False
        self.fees_chk = False
        self.final_amount_chk = False
        self.message_text = ""
        self.facility_name = ""
        self.facility_email = ""
        self.manager_name = ""
        self.manager_email = ""
        self.invoice = None    

        # settings
        self.restoreSettings()

        # callbacks
        self.ui.actionPPMS.triggered.connect(self.ppmsSettings)
        self.ui.actionEmail.triggered.connect(self.emailSettings)
        self.ui.actionInvoice_template.triggered.connect(self.invoiceTemplateSettings)
        self.ui.actionFacility.triggered.connect(self.facilitySettings)
        self.ui.actionGeneral.triggered.connect(self.generalSettings)
        self.ui.connect_button.clicked.connect(self.connectClicked)
        self.ui.select_btn.clicked.connect(self.selectAll)
        self.ui.deselect_btn.clicked.connect(self.deselectAll)
        self.ui.reference_combo.currentIndexChanged.connect(self.referenceChanged)
        self.ui.email_button.clicked.connect(self.sendInvoices)

        # threadpool
        self.threadpool = QtCore.QThreadPool()

        # ui state
        self.ppms_dialog = None
        self.email_dialog = None
        # disbale the assisted and training tabs
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(2, False)        

    # events
    def closeEvent(self, event):
        """Respond to the window close event"""
        self.saveSettings()
        return super().closeEvent(event)

    # settings
    def saveSettings(self):
        """Save GUI settings"""
        settings = QtCore.QSettings("Dan", "ppms")
        settings.setValue('invoice_folder', self.invoice_folder)
        settings.setValue('ppms_url', self.ppms_url)
        settings.setValue('ppms_key', self.ppms_key)
        settings.setValue('exchange_username', self.exchange_username)
        settings.setValue('exchange_password', self.exchange_password)
        settings.setValue('smtp_server', self.smtp_server)
        settings.setValue('from_email', self.from_email)
        settings.setValue('test_mode', self.test_mode)
        settings.setValue('test_address', self.test_address)
        settings.setValue('session_chk', self.session_chk)
        settings.setValue('user_chk', self.user_chk)
        settings.setValue('type_chk', self.type_chk)
        settings.setValue('system_chk', self.system_chk)
        settings.setValue('date_chk', self.date_chk)
        settings.setValue('start_chk', self.start_chk)
        settings.setValue('booked_chk', self.booked_chk)
        settings.setValue('used_chk', self.used_chk)
        settings.setValue('notes_chk', self.notes_chk)
        settings.setValue('init_amount_chk', self.init_amount_chk)
        settings.setValue('fees_chk', self.fees_chk)
        settings.setValue('final_amount_chk', self.final_amount_chk)
        settings.setValue('message_text', self.message_text)
        settings.setValue('facility_code', self.facility_code)
        settings.setValue('facility_name', self.facility_name)
        settings.setValue('facility_email', self.facility_email)        
        settings.setValue('manager_name', self.manager_name)
        settings.setValue('manager_email', self.manager_email)

    def restoreSettings(self):
        """Retrieve stored GUI settings"""
        settings = QtCore.QSettings("Dan", "ppms")
        self.invoice_folder = settings.value("invoice_folder", type=str)
        self.ppms_url = settings.value("ppms_url", type=str)
        self.ppms_key = settings.value("ppms_key", type=str)
        self.exchange_username = settings.value("exchange_username", type=str)
        self.exchange_password = settings.value("exchange_password", type=str)
        self.smtp_server = settings.value("smtp_server", type=str)
        self.from_email = settings.value("from_email", type=str)
        self.test_mode = settings.value("test_mode", type=bool)
        self.test_address = settings.value("test_address", type=str)
        self.session_chk = settings.value("session_chk", type=bool)
        self.user_chk = settings.value("user_chk", type=bool)
        self.type_chk = settings.value("type_chk", type=bool)
        self.system_chk = settings.value("system_chk", type=bool)
        self.date_chk = settings.value("date_chk", type=bool)
        self.start_chk = settings.value("start_chk", type=bool)
        self.booked_chk = settings.value("booked_chk", type=bool)
        self.used_chk = settings.value("used_chk", type=bool)
        self.notes_chk = settings.value("notes_chk", type=bool)
        self.init_amount_chk = settings.value("init_amount_chk", type=bool)
        self.fees_chk = settings.value("fees_chk", type=bool)
        self.final_amount_chk = settings.value("final_amount_chk", type=bool)
        self.message_text = settings.value("message_text", type=str)
        self.facility_code = settings.value("facility_code", type=str)
        self.facility_name = settings.value("facility_name", type=str)
        self.facility_email = settings.value("facility_email", type=str)        
        self.manager_name = settings.value("manager_name", type=str)
        self.manager_email = settings.value("manager_email", type=str)

    # slots
    @pyqtSlot()
    def generalSettings(self):
        """Responds to actionGeneral"""
        self.general_dialog = GeneralDialog(self)
        if not self.general_dialog.isVisible():          
            self.general_dialog.show()
    
    @pyqtSlot()
    def ppmsSettings(self):
        """Responds to actionPPMS"""
        self.ppms_dialog = PPMSDialog(self)
        if not self.ppms_dialog.isVisible():          
            self.ppms_dialog.show()

    @pyqtSlot()
    def emailSettings(self):
        """Responds to actionEmail"""
        self.email_dialog = EmailDialog(self)
        if not self.email_dialog.isVisible():          
            self.email_dialog.show()

    @pyqtSlot()
    def invoiceTemplateSettings(self):
        """Responds to actionInvoice_template"""
        self.template_dialog = InvoiceTemplateDialog(self)
        if not self.template_dialog.isVisible():          
            self.template_dialog.show()

    @pyqtSlot()
    def facilitySettings(self):
        """Responds to actionFacility"""
        self.facility_dialog = FacilityDialog(self)
        if not self.facility_dialog.isVisible():          
            self.facility_dialog.show()

    @pyqtSlot()
    def connectClicked(self):
        """Responds to the connect button being clicked"""
        connect_worker = threads.Worker(
            threads._connect, self.ppms_url, self.ppms_key
        )
        connect_worker.signals.result.connect(self.onConnectComplete)
        connect_worker.signals.error.connect(self.onError)

        self.threadpool.start(connect_worker)

    @pyqtSlot()
    def referenceChanged(self):
        """Responds to reference_combo index change"""
        ref = self.ui.reference_combo.currentText()
        worker = threads.Worker(
            threads._fetchInvoice, self.ppms_url,
            self.ppms_key, ref
        )
        worker.signals.result.connect(self.onInvoicFetchComplete)
        self.threadpool.start(worker)

    @pyqtSlot()
    def detailsClicked(self):
        """Responds to Details button being clicked in a table row"""
        # get the table
        tab = self.ui.tabWidget.currentIndex()
        if tab == 0:
            table = self.ui.auto_table
        elif tab == 1:
            table = self.ui.assist_table
        elif tab == 2:
            table = self.ui.train_table
        
        # get the row number
        selected_rows = table.selectionModel().selectedRows()
        rid = selected_rows[0].row()
        bcode = table.item(rid, 1).text()
        item = self.invoice.item_for_bcode(bcode)
        ref = self.ui.reference_combo.currentText()

        facility_info = {}
        facility_info["name"] = self.facility_name
        facility_info["email"] = self.facility_email
        facility_info["manager_name"] = self.manager_name
        facility_info["manager_email"] = self.manager_email

        invoice_columns = {}
        invoice_columns["session_chk"] = self.session_chk
        invoice_columns["user_chk"] = self.user_chk
        invoice_columns["type_chk"] = self.type_chk
        invoice_columns["system_chk"] = self.system_chk
        invoice_columns["date_chk"] = self.date_chk
        invoice_columns["start_chk"] = self.start_chk
        invoice_columns["booked_chk"] = self.booked_chk
        invoice_columns["used_chk"] = self.used_chk
        invoice_columns["notes_chk"] = self.notes_chk
        invoice_columns["init_amount_chk"] = self.init_amount_chk
        invoice_columns["fees_chk"] = self.fees_chk
        invoice_columns["final_amount_chk"] = self.final_amount_chk

        worker = threads.Worker(
            threads._messageForBcode,
            item, ref, self.invoice_folder, self.message_text,
            facility_info, invoice_columns
        )
        worker.signals.result.connect(self.onDetailsComplete)
        worker.signals.error.connect(self.onError)

        self.threadpool.start(worker)

    @pyqtSlot()
    def checkBoxChanged(self):
        # get the table
        tab = self.ui.tabWidget.currentIndex()
        if tab == 0:
            table = self.ui.auto_table
        elif tab == 1:
            table = self.ui.assist_table
        elif tab == 2:
            table = self.ui.train_table
        
        # get the row number
        selected_rows = table.selectionModel().selectedRows()
        # if there are selected_rows (there won't be when 'select all' is used)
        if selected_rows:
            rid = selected_rows[0].row()
            chk = table.cellWidget(rid, 0)
            bcode = table.item(rid, 1).text()
            tables = [self.ui.auto_table, self.ui.assist_table, self.ui.train_table]
            for table in tables:
                for row in range(table.rowCount()):
                    if table.item(row, 1).text() == bcode:
                        if chk.isChecked():
                            table.cellWidget(row, 0).setChecked(True)
                        else:
                            table.cellWidget(row, 0).setChecked(False)

    @pyqtSlot()
    def selectAll(self):
        """Recieves signal from select_btn"""
        tables = [self.ui.auto_table, self.ui.assist_table, self.ui.train_table]
        for table in tables:
            for row in range(table.rowCount()):
                chk = table.cellWidget(row, 0)
                chk.setChecked(True)

    @pyqtSlot()
    def deselectAll(self):
        """Recieves signal from deselect_btn"""
        tables = [self.ui.auto_table, self.ui.assist_table, self.ui.train_table]
        for table in tables:
            for row in range(table.rowCount()):
                chk = table.cellWidget(row, 0)
                chk.setChecked(False)

    @pyqtSlot()
    def sendInvoices(self):
        ref = self.ui.reference_combo.currentText()
        sendto = self.ui.sendto_combo.currentIndex()
        copy_manager = self.ui.copy_chk.isChecked()
        tables = [self.ui.auto_table, self.ui.assist_table, self.ui.train_table]
        bcodes = []
        for table in tables:
            for row in range(table.rowCount()):
                chk = table.cellWidget(row, 0)
                if chk.isChecked():
                    bcodes.append(table.item(row, 1).text())

        bcodes = set(bcodes)
        items = []
        for bcode in bcodes:
            items.append(self.invoice.item_for_bcode(bcode))

        facility_info = {}
        facility_info["name"] = self.facility_name
        facility_info["email"] = self.facility_email
        facility_info["manager_name"] = self.manager_name
        facility_info["manager_email"] = self.manager_email

        invoice_columns = {}
        invoice_columns["session_chk"] = self.session_chk
        invoice_columns["user_chk"] = self.user_chk
        invoice_columns["type_chk"] = self.type_chk
        invoice_columns["system_chk"] = self.system_chk
        invoice_columns["date_chk"] = self.date_chk
        invoice_columns["start_chk"] = self.start_chk
        invoice_columns["booked_chk"] = self.booked_chk
        invoice_columns["used_chk"] = self.used_chk
        invoice_columns["notes_chk"] = self.notes_chk
        invoice_columns["init_amount_chk"] = self.init_amount_chk
        invoice_columns["fees_chk"] = self.fees_chk
        invoice_columns["final_amount_chk"] = self.final_amount_chk            

        email_settings = {}
        email_settings["username"] = self.exchange_username
        email_settings["password"] = self.exchange_password
        email_settings["server"] = self.smtp_server
        email_settings["from_address"] = self.from_email
        email_settings["test_mode"] = self.test_mode
        email_settings["test_address"] = self.test_address
        email_settings["copy_manager"] = copy_manager
        email_settings["manager_address"] = self.manager_email

        # progress bar
        self.email_progress = Progress(self, len(items) - 1, 'Sending email')

        # start the send email thread passing items and sendto flag
        worker = threads.Worker(
            threads._sendEmail,
            items, sendto, ref, self.invoice_folder, self.message_text,
            facility_info, invoice_columns, email_settings
        )
        worker.signals.progress.connect(self.updateEmailProgress)
        worker.signals.finished.connect(self.onEmailFinished)
        worker.signals.error.connect(self.onError)

        if not self.email_progress.isVisible():          
            self.email_progress.show()        

        self.threadpool.start(worker)   

    # signal recievers
    def onConnectComplete(self, result):
        """Recieves the result of the connect worker thread"""
        if result:
            self.ui.reference_combo.addItems(result)

        worker = threads.Worker(
            threads._fetchInvoice, self.ppms_url, self.ppms_key,
            result[0]
        )
        worker.signals.result.connect(self.onInvoicFetchComplete)
        worker.signals.error.connect(self.onError)

        self.threadpool.start(worker)

    def onInvoicFetchComplete(self, invoice):
        """Recieves the result of invoice fetch worker thread"""
        if invoice:
            self.invoice = invoice
            if invoice.autonomous_items > 0:
                num_auto = invoice.autonomous_items

                auto_table = self.ui.auto_table
                auto_table_header = auto_table.horizontalHeader()
                auto_table_cols = ["", "Account Number", "Group", "Sessions",
                                   "Hours booked","Hours used",
                                   "Initial Amount", "Rebate", "Fees",
                                   "Final Amount", ""]
                auto_table.setColumnCount(len(auto_table_cols))
                auto_table.setRowCount(num_auto)
                auto_table.setHorizontalHeaderLabels(auto_table_cols)

                rid = 0
                for i in invoice.items:
                    if i.num_auto_sessions > 0:
                        props = i.properties["autonomous"]
                        # add a checkbox to first column of each row
                        chk = QtWidgets.QCheckBox()
                        chk.stateChanged.connect(self.checkBoxChanged)
                        auto_table.setCellWidget(rid, 0, chk)
                        auto_table_header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

                        # add columns from invoice                
                        for cid, col in enumerate(auto_table_cols[1:-1]):
                            cid += 1
                            if ((col == "Account Number") or
                                (col == "Group") or
                                (col == "Sessions")):

                                cell = QtWidgets.QTableWidgetItem('{}'.format(props[col]))
                            else:
                                cell = QtWidgets.QTableWidgetItem('{:.2f}'.format(props[col]))

                            cell.setFlags(QtCore.Qt.ItemIsEnabled)
                            auto_table.setItem(rid, cid, cell)
                            auto_table_header.setSectionResizeMode(
                                0, QtWidgets.QHeaderView.ResizeToContents
                            )
                        
                        # add a push button to access list of sessions for each bcode
                        btn = QtWidgets.QPushButton()
                        btn.setText('Details')
                        btn.clicked.connect(self.detailsClicked)
                        auto_table.setCellWidget(rid, cid+1, btn)
                        auto_table_header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

                        rid += 1

            if invoice.assist_items > 0:
                self.ui.tabWidget.setTabEnabled(1, True)
                num_assist = invoice.assist_items

                assist_table = self.ui.assist_table
                assist_table_header = assist_table.horizontalHeader()
                assist_table_cols = ["", "Account Number", "Group", "Sessions",
                                     "Hours booked","Hours used",
                                     "Initial Amount", "Rebate", "Fees",
                                     "Final Amount", ""]
                assist_table.setColumnCount(len(assist_table_cols))
                assist_table.setRowCount(num_assist)
                assist_table.setHorizontalHeaderLabels(assist_table_cols)

                rid = 0
                for i in invoice.items:

                    if i.num_assist_sessions > 0:
                        props = i.properties["assisted"]
                        chk = QtWidgets.QCheckBox()
                        chk.stateChanged.connect(self.checkBoxChanged)
                        assist_table.setCellWidget(rid, 0, chk)
                        assist_table_header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
                        # loop needs rewriting to write out assist_items into
                        # table columns
                        for cid, col in enumerate(assist_table_cols[1:-1]):
                            cid += 1
                            if ((col == "Account Number") or
                                (col == "Group") or
                                (col == "Sessions")):

                                cell = QtWidgets.QTableWidgetItem('{}'.format(props[col]))
                            else:
                                cell = QtWidgets.QTableWidgetItem('{:.2f}'.format(props[col]))

                            cell.setFlags(QtCore.Qt.ItemIsEnabled)
                            assist_table.setItem(rid, cid, cell)
                            assist_table_header.setSectionResizeMode(
                                0, QtWidgets.QHeaderView.ResizeToContents
                            )

                        # add a push button to access list of sessions for each bcode
                        btn = QtWidgets.QPushButton()
                        btn.setText('Details')
                        btn.clicked.connect(self.detailsClicked)
                        assist_table.setCellWidget(rid, cid+1, btn)
                        assist_table_header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)                            

                        rid += 1

            if invoice.train_items > 0:
                self.ui.tabWidget.setTabEnabled(2, True)
                num_train = invoice.train_items

                train_table = self.ui.train_table
                train_table_header = train_table.horizontalHeader()
                train_table_cols = ["", "Account Number", "Group", "Sessions",
                                     "Hours booked", "Final Amount", ""]
                train_table.setColumnCount(len(train_table_cols))
                train_table.setRowCount(num_train)
                train_table.setHorizontalHeaderLabels(train_table_cols)

                rid = 0
                for i in invoice.items:
                    if i.num_train_sessions > 0:
                        props = i.properties["training"]
                        chk = QtWidgets.QCheckBox()
                        chk.stateChanged.connect(self.checkBoxChanged)
                        train_table.setCellWidget(rid, 0, chk)
                        train_table_header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
                                
                        for cid, col in enumerate(train_table_cols[1:-1]):
                            cid += 1
                            if ((col == "Account Number") or
                                (col == "Group") or
                                (col == "Sessions")):
                                cell = QtWidgets.QTableWidgetItem('{}'.format(props[col]))
                            else:
                                cell = QtWidgets.QTableWidgetItem('{:.2f}'.format(props[col]))

                            cell.setFlags(QtCore.Qt.ItemIsEnabled)
                            train_table.setItem(rid, cid, cell)
                            train_table_header.setSectionResizeMode(
                                0, QtWidgets.QHeaderView.ResizeToContents
                            )

                        # add a push button to access list of sessions for each bcode
                        btn = QtWidgets.QPushButton()
                        btn.setText('Details')
                        btn.clicked.connect(self.detailsClicked)
                        train_table.setCellWidget(rid, cid+1, btn)
                        train_table_header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)                            

                        rid += 1

    def onDetailsComplete(self, result):
        """Recieves the result of the sessionsForBcode thread"""
        if result:
            self.preview_dialog = PreviewDialog(
                self, result["bcode"], html=result["html"]
            )
            if not self.preview_dialog.isVisible():
                self.preview_dialog.show()

    def onError(self, err):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText(str(err[1]))
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)

    def updateEmailProgress(self, val):
        if self.email_progress.isVisible():
            self.email_progress.updateBar(val)

    def onEmailFinished(self):
        if self.email_progress.isVisible():
            self.email_progress.close()

        ref = self.ui.reference_combo.currentText()
        worker = threads.Worker(
            threads._writeToExcel, ref, self.invoice,
            self.facility_code, self.invoice_folder
        )
        worker.signals.error.connect(self.onError)

        self.threadpool.start(worker)           


