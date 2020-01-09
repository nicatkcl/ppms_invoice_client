from collections import OrderedDict

from PyQt5 import QtCore, QtWidgets
from datetime import datetime

import pandas as pd


class BaseSession:
    def __init__(self, **kwargs):
        """
        Session base class that gets attributes from columns of
        a Pandas DataFrame.

        Attributes
        -----------
        session_type: str
        session_ref: str
        user: str
        system_type: str
        system: str
        date: str
        start_time: str
        final_amount: str
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def round_final_amount(self):
        return (
            "{0:.2f}".format(
                int((self.final_amount * 100) + 0.5) / float(100)
            )
        )            


class TrainingSession(BaseSession):
    """Class which encapsulates training sessions."""
    def __init__(self, duration, **kwargs):
        self.duration = duration
        super().__init__(**kwargs)


class AutoAssistSession(BaseSession):
    """
    Class which encapsulates both autonomous and
    assisted sessions.
    """

    def __init__(self, booked_time, used_time, notes, fee, subsidy, **kwargs):
        self.booked_time = booked_time
        self.used_time = used_time
        self.notes = notes
        self.fee = fee
        self.subsidy = subsidy
        if not isinstance(notes, str):
            self.notes = ""
        # if "cancelled too late" in self.notes:
        #     self.notes = ""
        super().__init__(**kwargs)
        self.initial_amount = self.final_amount - self.fee + self.subsidy


class InvoiceItem:
    """
    Representation of one line of invoice. An InvoiceItem consists
    of multiple sessions.
    """
    def __init__(self, bcode, group):
        self.bcode = bcode
        self.group = group
        addresses = {}
        addresses["to_email"] = [group.heademail]
        addresses["cc_email"] = [group.admemail]
        self.addresses = addresses
        self.sessions = []
        self.properties = None
        self.html = None

    def set_invoice_properties(self, sessions_df):
        session_types = sessions_df['Session Type'].unique()
        self.properties = {}
        for st in session_types:
            sessions = sessions_df[sessions_df['Session Type'] == st]

            properties = pd.Series(dtype='object')
            properties['Account Number'] = sessions['Account number'].values[0]
            properties['Group'] = sessions['Group'].values[0]
            properties['Sessions'] = len(sessions.index)
            properties['Hours booked'] = float(
                pd.to_numeric(sessions['Duration (booked)']).sum()
            ) / 60.0
            properties['Hours used'] = float(
                pd.to_numeric(sessions['Duration (used)']).sum()
            ) / 60.0
            properties['Rebate'] = float(
                pd.to_numeric(sessions['Rebate']).sum()
            )
            properties['Fees'] = float(
                pd.to_numeric(sessions['Fee']).sum()
            )
            properties['Final Amount'] = float(
                pd.to_numeric(sessions['Final Amount']).sum()
            )
            properties['Initial Amount'] = float(
                pd.to_numeric(sessions['Final Amount']).sum() +
                pd.to_numeric(sessions['Fee']).sum() -
                pd.to_numeric(sessions['Rebate']).sum()
            )
            self.properties[st] = properties      

    def sessions_from_dataframe(self, sessions_df):
        """
        Turn a Pandas DataFrame of sessions for a particular invoice
        (charges to one bcode) into Session class instances.
        """
        self.set_invoice_properties(sessions_df)
        self.num_auto_sessions = 0
        self.num_assist_sessions = 0
        self.num_train_sessions = 0
        for index, row in sessions_df.iterrows():
            kwargs = {
                'session_type': row['Session Type'],
                'session_ref': row['Reference'],
                'user': row['User'],
                'system_type': row['System Type'],
                'system': row['System'],
                'date': row['Date'],
                'start_time': row['Start time'],
                'final_amount': row['Final Amount']
            }

            if (
                ("autonomous" in row['Session Type']) or
                ("assisted" in row['Session Type'])
            ):
                if "autonomous" in row['Session Type']:
                    self.num_auto_sessions += 1
                if "assisted" in row['Session Type']:
                    self.num_assist_sessions += 1                    

                self.sessions.append(
                    AutoAssistSession(
                        row['Duration (booked)'],
                        row['Duration (used)'],
                        row['Notes'],
                        row['Fee'],
                        row['Subsidy'],
                        **kwargs
                    )
                )
            elif "training" in row['Session Type']:
                self.num_train_sessions += 1
                self.sessions.append(
                    TrainingSession(
                        row['Duration'],
                        **kwargs
                    )
                )
            self.num_sessions = len(self.sessions)

    def filter_by_session_type(self, session_type):
        filtered = []
        for session in self.sessions:
            if session_type in session.session_type:
                filtered.append(session)
        return filtered

    @property
    def final_amount(self):
        total = 0.0
        for session in self.sessions:
            total += session.final_amount
        return total

    def total_charge(self, sessions):
        total = 0.0
        for session in sessions:
            total += session.final_amount
        total = int((total * 100) + 0.5) / float(100)
        return "{0:.2f}".format(total)

    def final_total(self, autonomous, assisted, training):
        total = 0.0
        for auto in autonomous:
            total += auto.final_amount

        for assit in assisted:
            total += assit.final_amount

        for train in training:
            total += train.final_amount

        total = int((total * 100) + 0.5) / float(100)
        return "{0:.2f}".format(total)

    def check_for_adjustments(self, sessions):
        fee_flag = False
        subsidy_flag = False
        for session in sessions:
            if session.fee > 0.0:
                fee_flag = True
            if session.subsidy > 0.0:
                subsidy_flag = True
        return (fee_flag, subsidy_flag)

    def __str__(self):
        return "invoice for {0} with {1} sessions".format(
            self.bcode, self.num_sessions
        )

    def __repr__(self):
        return "invoice for {0} with {1} sessions".format(
            self.bcode, self.num_sessions
        )        


class Invoice:
    """
    A list of invoice items
    """
    def __init__(self, ref):
        self.ref = ref
        date = datetime.strptime(ref[17:25], "%Y%m%d")
        self.sessions_month = "December"
        if int(date.strftime("%m")) > 1:
            sessions_month = datetime.strptime(str(int(date.strftime("%m")) - 1), "%m")
            self.sessions_month = sessions_month.strftime("%B")
        self.invoice_date = {
            "invoice_year": date.strftime("%Y"),
            "invoice_month": date.strftime("%B"),
            "sessions_month": self.sessions_month,
            "invoice_date": date.strftime("%d/%m/%Y"),
        }
        self.items = []
        self.autonomous_items = 0
        self.assist_items = 0
        self.train_items = 0
        self.n_items = (len(self.items))

    def __getitem__(self, i):
        return self.items[i]

    def __setitem__(self, item):
        if isinstance(item, InvoiceItem):
            self.items.append(item)
            self.n_items = len(self.items)

    def __len__(self):
        return self.n_items

    @property
    def bcodes(self):
        bcodes = []
        for item in self.items:
            bcodes.append(item.bcode)
        return set(bcodes)

    @property
    def amounts(self):
        amounts = []
        for item in self.items:
            amounts.append(item.final_amount)
        return amounts

    @property
    def group_heads(self):
        groups = []
        for item in self.items:
            groups.append(item.group.heademail)
        return groups

    def append(self, item):
        self.items.append(item)
        if item.num_auto_sessions > 0:
            self.autonomous_items += 1
        if item.num_assist_sessions > 0:
            self.assist_items += 1
        if item.num_train_sessions > 0:
            self.train_items += 1

        self.n_items = len(self.items)

    def item_for_bcode(self, bcode):
        item = None
        for i in self.items:
            if i.bcode == bcode:
                item = i
        return item
