
import os
import traceback
import sys
import time
from datetime import datetime
import requests
from collections import OrderedDict
import html

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QRunnable, QObject
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import pandas as pd
from namedentities import *

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

from .models import Invoice, InvoiceItem
from ..utils.recipient import recipient_from_group
from ..utils.html_convert import create_html
from ..utils import send_email   


class EmailError(Exception):
    pass


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        `tuple` (exctype, value, traceback.format_exc() )
    result
        `object` data returned from processing, anything
    progress
        `object` indicating % progress (will be `int` or `tuple`)
    custom_callback
        `object` any other type of signal (e.g. partial results)
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(object)
    custom_callback = pyqtSignal(object)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    Attributes
    ----------
    callback: function
        The function callback to run on this worker thread. Supplied args and 
        kwargs will be passed through to the runner.
    args: list
        Arguments to pass to the callback function
    kwargs: dict
        Keywords to pass to the callback function
    '''

    def __init__(self, callback, *args, **kwargs):
        super().__init__()

        # Store constructor arguments (re-used for processing)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['custom_callback'] = self.signals.custom_callback        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.callback(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


####
# Helpers for thread functions
def _interleave(list1, list2):
    return [val for pair in zip(list1, list2) for val in pair]

def _processMessageText(message_text, invoice_date, facility_info):
    """
    Takes message text from dialog and inserts facility info and formats
    into html.

    Arguments
    ---------
    message_text: str
        Message which needs parameters inserted
    invoice_data: dict
        A dictionary containing general information about the invoice
    facility_info: dict
        A dictionary containing general information about the facility
    
    Returns
    -------
    formattedbr: str
        Message text formatted as html.

    """
    month = invoice_date["sessions_month"]
    year = invoice_date["invoice_year"]
    f_name = facility_info["name"]
    f_email = "<a href='mailto:{email}'>{email}</a>".format(email=facility_info["email"])
    m_name = facility_info["manager_name"]
    m_email = "<a href='mailto:{email}'>{email}</a>".format(email=facility_info["manager_email"])

    formatted = message_text.format(
        MONTH=month, YEAR=year, F_NAME=f_name,
        F_EMAIL=f_email, M_NAME=m_name, M_EMAIL=m_email
    )
    nl = formatted.count("\n")
    formattedbr = formatted.replace("\n", "<br/>", nl)
    return formattedbr


def _getGroup(url, key, group_ref):
    """Set up a PUMAPI call with the action `getgroup`

    Arguments
    ----
        group_ref: str
            The grant code as a reference to the group in PPMS

    Returns
    -------
        A Recipient object
    """

    if "'" in group_ref:
        group_ref = group_ref.replace("'", "&#39;")

    data = {
        'action': 'getgroup',
        'unitlogin': group_ref,
        'apikey': key,
        'format': 'json'
    }
    resp = requests.post(url, data=data)
    if resp.status_code == 200 and resp.text:
        return recipient_from_group(resp.text)
    else:
        raise ValueError("Response not received from PPMS")


def _invoiceSummary(invoice, session_type='autonomous'):
    """
    Summarises invoice for autonomous, training sessions
    and assisted sessions for a particular grant code.

    Arguments
    ---------
    invoice: Pandas DataFrame
        DataFrame holding the entire invoice for a particular account code
    session_type: str
        The DataFrame is filtered by `Session Type` to collect sessions
        together.

    Returns
    -------
    summary: Pandas Series
        A Pandas Series containing information about sessions of a particular type.
        Columns for training sessions are:
        ['Account Number', 'Group', 'Sessions', 'Hours booked', 'Final Amount']
        Columns for autonomous and assisted sessions are:
        ['Account Number', 'Group', 'Sessions', 'Hours Booked',
        'Hours used', 'Rebate', 'Fees', 'Initial Amount', 'Final Amount']

    """
    sessions = invoice[invoice['Session Type'] == session_type]
    summary = None
    if not sessions.empty:
        if session_type == 'training':
            summary = pd.Series(dtype='object')
            summary['Account Number'] = sessions['Account number'].values[0]
            summary['Group'] = sessions['Group'].values[0]
            summary['Sessions'] = len(invoice.index)
            summary['Hours booked'] = float(
                pd.to_numeric(sessions['Duration']).sum()
            ) / 60.0
            summary['Final Amount'] = float(
                pd.to_numeric(sessions['Final Amount']).sum()
            )

        else:
            summary = pd.Series(dtype='object')
            summary['Account Number'] = sessions['Account number'].values[0]
            summary['Group'] = sessions['Group'].values[0]
            summary['Sessions'] = len(sessions.index)
            summary['Hours booked'] = float(
                pd.to_numeric(sessions['Duration (booked)']).sum()
            ) / 60.0
            summary['Hours used'] = float(
                pd.to_numeric(sessions['Duration (used)']).sum()
            ) / 60.0
            summary['Rebate'] = float(
                pd.to_numeric(sessions['Rebate']).sum()
            )
            summary['Fees'] = float(
                pd.to_numeric(sessions['Fee']).sum()
            )
            summary['Final Amount'] = float(
                pd.to_numeric(sessions['Final Amount']).sum()
            )
            summary['Initial Amount'] = float(
                pd.to_numeric(sessions['Final Amount']).sum() +
                pd.to_numeric(sessions['Fee']).sum() -
                pd.to_numeric(sessions['Rebate']).sum()
            )

    return summary

def _getInvoiceDetails(url, key, ref, bcode=None):
    """
    Uses a PPMS PUMAPI call ('getinvoicedetails') to get all sessions
    for a given invoice ref or for a specific grant code if `bcode` is
    supplied.

    Arguments
    ---------
    url: str
        The PPMS facility instance url.
    key: str
        The PPMS PUMAPI key for the facility.
    ref: str
        The invoice reference.
    bcode: str
        Optionally provide a specific account code.

    Returns
    -------
    invoice: Pandas DataFrame

    Raises
    ------
    ValueError
        If no response is received from the PPMS server or if the
        response contains an empty string.
    """

    data = {
        "action": "getinvoicedetails",
        "apikey": key,
        "invoiceid": ref,
    }
    a_df_header = 0
    if bcode:
        data['bcode'] = bcode
        a_df_header = 1

    resp = requests.post(url, data=data)
    if resp.status_code == 200 and resp.text:
        invoice_text = resp.text.split("\r\n", 2)[2]
        if "Autonomous" in resp.text and "Training" in resp.text:
            a = invoice_text[0:invoice_text.find("Training")]
            a_df = pd.read_csv(StringIO(a), sep=",", header=a_df_header)
            t = invoice_text[invoice_text.find("Training"):]
            t_df = pd.read_csv(StringIO(t), sep=",", header=1)
            invoice = pd.concat([a_df, t_df], axis=0, ignore_index=True, sort=True)
        else:
            invoice = pd.read_csv(StringIO(invoice_text), sep=",", header=1)

        return invoice
    else:
        raise ValueError("Response not received from PPMS")


####
# Functions run by worker threads

def _connect(url, key, progress_callback=None,
            custom_callback=None):
    """
    A callback used by a worker thread. Uses `getinvoicelist` PPMS
    PUMAPI call to get a list of invoice references.

    Arguments
    ---------
    url: str
        The PPMS facility instance url.
    key: str
        The PPMS PUMAPI key for the facility.
    progress_callback: PyQt progress signal
        A signal that can be used to update a progress bar.
    custom_callback: PyQt signal   
        A user defined signal.

    Returns:
    --------
    invoices : list of str
        A list of invoice references.

    Raises
    ------
    ValueError
        If no response is recieved from the PPMS server or if the
        response text contains an empty string.
    
    """

    draft = ["false", "true"]
    invoices = []
    for d in draft:
        data = {
            "action": "getinvoicelist",
            "apikey": key,
            "draft": d
        }
        response = requests.post(url, data=data)
        if response.status_code == 200 and response.text:
            refs = [r.strip("\n") for r in response.text.split("\r")]
            invoices.extend(refs[:-1])
        else:
            raise ValueError("Response not received from PPMS")

    return invoices[::-1]


def _fetchInvoice(url, key, ref, progress_callback=None,
                  custom_callback=None):
    """
    Use PPMS PUMAPI call `getinvoice` to get the entire invoice. Create
    an InvoiceItem for each account code and store in an Invoice instance
    ready for display in a PyQt TableWidget.

    Arguments
    ---------
    url: str
        The PPMS facility instance url.
    key: str
        The PPMS PUMAPI key for the facility.
    progress_callback: PyQt progress signal
        A signal that can be used to update a progress bar.
    custom_callback: PyQt signal   
        A user defined signal.

    Returns:
    --------
    invoice : instance of Invoice class
        A list of InvoiceItems.

    Raises
    ------
    ValueError
        If no response is recieved from the PPMS server or if the
        response text contains an empty string.
    """

    # organise the output by session type
    details = _getInvoiceDetails(url, key, ref)
    bcodes = sorted(details['Account number'].unique())
    session_types = sorted(details['Session Type'].unique())

    invoice = Invoice(ref)
    for bcode in bcodes[0:3]:
        item_details = details[details['Account number'] == bcode]
        group_ref = item_details['Group'].values[0]
        group = _getGroup(url, key, group_ref)
        group.bcode = bcode
        item = InvoiceItem(bcode, group)
        item.sessions_from_dataframe(item_details)
        invoice.append(item)

    return invoice

def _messageForBcode(item, ref, folder, message_text, facility_info,
                     invoice_columns, save_invoice=False,
                     progress_callback=None, custom_callback=None):

    """
    A thread callback which creates html for a speific InvoiceItem
    from the PyQt table.

    Arguments
    ---------
    item: instance of InvoiceItem
        The specific item in the invoice for which html is being
        created.
    ref: str
        The PPMS reference for the overall invoice.
    folder: str
        The directory into which the html will be saved. This is a
        setting defined in the general settings dialog.
    message_text: str
        Formatted html with a message from the facility to the account
        code owner.
    facility_info: dict
        Information about the facility from the facility info dialog.
    invoice_columns: dict
        Which specific columns will be included in the html table
        representation of the InvoiceItem. These are set in the invoice
        template dialog.
    save_invoice: bool
        If True, write the html to file.
    progress_callback: PyQt progress signal
        A signal that can be used to update a progress bar.
    custom_callback: PyQt signal   
        A user defined signal.        

    Returns:
    --------
    output : dict
        A dictionary containing the account code and the html for the
        InvoiceItem being processed.
    """                     

    if 'DRAFT' in ref:
        date = datetime.strptime(ref[17:25], "%Y%m%d")
    else:
        date = datetime.strptime(ref[17:], "%Y%m%d")

    sessions_month = "December"
    if int(date.strftime("%m")) > 1:
        sessions_month = datetime.strptime(str(int(date.strftime("%m")) - 1), "%m")
        sessions_month = sessions_month.strftime("%B")
    invoice_date = {
        "invoice_year": date.strftime("%Y"),
        "invoice_month": date.strftime("%B"),
        "sessions_month": sessions_month,
        "invoice_date":date.strftime("%d/%m/%Y"),
    }

    autonomous_sessions = item.filter_by_session_type("autonomous")
    assisted_sessions = item.filter_by_session_type("assisted")
    training_sessions = item.filter_by_session_type("training")

    autonomous_charge = item.total_charge(autonomous_sessions)
    assisted_charge = item.total_charge(assisted_sessions)
    training_charge = item.total_charge(training_sessions)
    final_charge = item.final_total(
        autonomous_sessions, assisted_sessions, training_sessions
    )
    fee_flag, subsidy_flag = item.check_for_adjustments(autonomous_sessions)

    # now turn details into html then into a string to be passed back to dialog
    s = [
        invoice_date["invoice_year"],
        invoice_date["sessions_month"],
        "invoice_{0}-{1}.html".format(ref, item.bcode)
    ]
    invoice_fname = os.path.join(*s)
    if '|' in invoice_fname:
        invoice_fname = invoice_fname.replace('|', '-')

    invoice_path = os.path.join(folder, invoice_fname)
    item.group.invoice = invoice_path

    invoice_data = {}
    invoice_data["invoice_ref"] = ref
    invoice_data["invoice_date"] = invoice_date
    invoice_data["invoice_path"] = invoice_path
    invoice_data["group"] = item.group
    invoice_data["autonomous_sessions"] = autonomous_sessions
    invoice_data["assisted_sessions"] = assisted_sessions
    invoice_data["training_sessions"] = training_sessions
    invoice_data["autonomous_charge"] = autonomous_charge
    invoice_data["assisted_charge"] = assisted_charge
    invoice_data["training_charge"] = training_charge
    invoice_data["final_charge"] = final_charge
    invoice_data["fee_flag"] = fee_flag
    invoice_data["subsidy_flag"] = subsidy_flag
    invoice_data["columns"] = invoice_columns

    invoice_message = _processMessageText(
        message_text, invoice_date, facility_info
    )
    invoice_data["message"] = invoice_message
    html = create_html(invoice_data, save_invoice=save_invoice)

    output = {}
    output["bcode"] = item.bcode
    output["html"] = html
    return output


def _sendEmail(items, sendto, ref, folder, message_text,
               facility_info, invoice_columns, email_settings,
               progress_callback=None, custom_callback=None):
    """
    Use Exchangelib module to send InvoiceItems to account owners.

    Arguments
    ---------
    items: list
        List of InvoiceItem instances.
    sendto: int
        Flag indicating whether to send email to everyone (0) or
        just admins (1).
    ref: str
        The PPMS reference for the overall invoice.
    folder: str
        The directory into which the html will be saved. This is a
        setting defined in the general settings dialog.
    message_text: str
        Formatted html with a message from the facility to the account
        code owner.
    facility_info: dict
        Information about the facility from the facility info dialog.
    invoice_columns: dict
        Which specific columns will be included in the html table
        representation of the InvoiceItem. These are set in the invoice
        template dialog.
    email_settings: dict
        Dictionary of settings for sending email using Microsoft exchange.
    progress_callback: PyQt progress signal
        A signal that can be used to update a progress bar.
    custom_callback: PyQt signal   
        A user defined signal.

    Raises
    ------
    EmailError
        An exception is raised to trigger the error message dialog.
    """
    for item in items:
        content = _messageForBcode(
            item, ref, folder, message_text,
            facility_info, invoice_columns, save_invoice=True
        )
        item.html = content["html"]
        if sendto == 1:
            item.group.send_only_admin = True

    try:
        send_email.send(items, ref, email_settings, progress=progress_callback)
    except:
        raise EmailError("Problem sending email")

def _writeToExcel(invoice_ref, invoice, facility_code, invoice_folder,
                  progress_callback=None, custom_callback=None):
    """Write the invoice to Excel using the KCL finance template.
    
    Arguments
    ---------
        invoice: Invoice instance
    """
    if 'DRAFT' in invoice_ref:
        ref_date = datetime.strptime(invoice_ref[17:25], "%Y%m%d")
    else:
        ref_date = datetime.strptime(invoice_ref[17:], "%Y%m%d")

    # get month and year from ref
    month = int(ref_date.strftime("%m")) - 1
    year = int(ref_date.strftime("%Y"))

    if month == 0:
        month = 12
        year = year - 1
    sess_month = datetime.strptime(str(month), "%m")
    sessions_month = sess_month.strftime("%B")
    sessions_year = str(year)

    bcodes = invoice.bcodes
    amounts = invoice.amounts
    group_heads = invoice.group_heads

    # make a list of equal length with NIC 
    # activity code and interleave
    nic_codes = [facility_code for i in range(len(invoice))]
    activity_codes = _interleave(bcodes, nic_codes)

    # make a list of equal length with NIC 
    # amounts and interleave
    nic_amounts = [a * -1 for a in amounts]
    charges = _interleave(amounts, nic_amounts)

    # include the 'account codes'
    transaction_account = [4213 for i in range(len(invoice))]
    nic_account = [4113 for i in range(len(nic_codes))]
    account_codes = _interleave(transaction_account, nic_account)

    # include description of transaction
    groups_for_descp = _interleave(group_heads, group_heads)
    description = [
        ('NIC charges for {} {} for {}'.
        format(sessions_month, sessions_year, groups_for_descp[i]))
        for i in range(len(groups_for_descp))
    ]

    # make the invoice from the lists
    print(len(description), len(charges), len(account_codes), len(activity_codes))
    invoice_df = pd.DataFrame({
        'Description': description,
        'Amounnt': charges,
        'account code': account_codes,
        'activity code': activity_codes
    })

    print(invoice_df.head())

    # create filepath
    filepath = '{0}\\{1} {0} NIC user charges new template.xlsx'.format(sessions_year, sessions_month)
    path = os.path.join(invoice_folder, filepath)
    # save invoice
    invoice_df.to_excel(path, sheet_name='Voucher Data', index=False)    


if __name__ == "__main__":

    data = {"action":"getinvoicedetails", "apikey":"1hG1wBx8Og2w5Edu", "invoiceid":"PPMS2-NICatKings-20191101-DRAFT", "bcode":"AC11372"}
    url = "https://ppms.eu/kcl/pumapi/"
    key = "1hG1wBx8Og2w5Edu"
    ref = "PPMS2-NICatKings-20191101"
    bcode = "NIC@KCL"
    result = _fetchInvoice(url, key, ref)
    print(result.item_for_bcode('AC11372'))
    # invoice = _getInvoiceDetails(url, key, ref)
    # folder = "C:\\Users\\Daniel\\Documents\\Programming\\NIC\\ppms-pyqt\\ppms_pyqt\\invoices"
    # invoice = _sessionsForBcode(bcode, url, key, ref, folder)
    # print(type(invoice))

    # data = {
    #     'action': 'getgroup',
    #     'unitlogin': "NICKings",
    #     'apikey': key,
    #     'format': 'json'
    # }
    # resp = requests.post(url, data=data)
    # print(resp.status_code)
    # print(resp.text)