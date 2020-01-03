# -*- coding: utf-8 -*-

import os
from exchangelib import (
    DELEGATE, Account, Credentials,
    Configuration, Message, HTMLBody,
    Mailbox
)


def send(recipients, invoice_ref, email_settings, progress=None):
    """Construct email from Recipient object and send.

    Parameters
    -----------
    recipients : list
        A list of recipient objects
    invoice_ref : str
        Identifier of the invoice being emailed
    email_settings : dict
        configuration settings for exchange server
    progress: PyQt progress bar
    """
    username = email_settings["username"]
    password = email_settings["password"]

    credentials = Credentials(username=username, password=password)

    config = Configuration(
        server=email_settings["server"],
        credentials=credentials
    )
    account = Account(
        primary_smtp_address=email_settings["from_address"],
        config=config,
        autodiscover=False,
        access_type=DELEGATE
    )
    cc_address = None
    for rid, recipient in enumerate(recipients):
        print(recipient.bcode)

        if email_settings["test_mode"]:
            to_address = [
                Mailbox(email_address=email_settings["test_address"])
            ]
        else:
            to_address = [
                Mailbox(email_address=address)
                for address in recipient.addresses["to_email"]
            ]
            cc_address = [
                Mailbox(email_address=address)
                for address in recipient.addresses["cc_email"]
            ]
            if email_settings["copy_manager"]:
               cc_address.append(
                   Mailbox(email_address=email_settings["manager_address"])
               )

            if recipient.group.send_only_admin:
                address = [
                    Mailbox(email_address=address)
                    for address in recipient.addresses["cc_email"]
                ]
                cc_address = ""
 
        m = Message(
            account=account,
            folder=account.sent,
            subject=(
                'NIC@KCL: Invoice {0}'
                .format(invoice_ref)
            ),
            to_recipients=to_address,
            cc_recipients=[]
        )
        if cc_address:
            m.cc_recipients = cc_address

        print("address: {}".format(m.to_recipients))
        print("cc_address: {}".format(m.cc_recipients))
        m.body = HTMLBody(recipient.html)
        m.send_and_save()
        progress.emit(rid)
