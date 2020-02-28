## Prerequisites

Install Python > 3.6

Install either [virtualenv](https://virtualenv.pypa.io/en/stable/) or [pipenv](https://pipenv.kennethreitz.org/en/latest/)

Clone or download the repository:

```
git clone https://github.com/nicatkcl/ppms_invoice_client.git
```

Make a virtual environment following the instructions for virtualenv and run:

```
pip install -r requirements.txt
```

Or run

```
pipenv shell
```

From the project root folder and then

```
pipenv install
```

## Getting started

To run the app type the following in a terminal:

```
python -m ppms_email_client.app
```

## Configuration

The app needs some configuration before it can be used. These can be set in the "settings" menu option. There are several menus -

1. General
   1. Here you can set the folder where invoices (html) are going to be saved.
2. PPMS
   1. PPMS URL - the URL to your PPMS instance
   2. PPMS API KEY - the API key you generate in your PPMS instance as an admin
3. Email
   1. Exchange username - your username on the exchange email server
   2. Exchange password - your password for the exchange email server
   3. SMTP server - the address of the exchange server (e.g. outlook.office365.com)
   4. From address - the email address which will appear in the 'From' field
   5. Test mode - set the client to test mode. This will send invoices to the test email address rather than to the account code holders.
   6. Test address - the email address to use in test mode.
4. Facility
   1. Facility account code - the PPMS account code.for the facility (no invoices will be generated for this code).
   2. Facility name - the name of your facility.
   3. Facility email - email address of the facility.
   4. Manager name - the name of the facility manager.
   5. Manager email - email address of facility manager.
5. Invoice template - create a template of the invoice to be sent to invoice recipients. The checkboxes allow selection of which columns of the invoice to include in the message. The instructions include keywords that can be used to insert values from the other settings menus. For example, including M_NAME in your message text will insert the 'Manager name' from the 'Facility' settings menu.

## Generating invoices

**Make sure to run the following in test mode first to make sure the invoice emails are being formatted as you want.**

Select the rows from the master invoice table that you want to generate invoices for. From the 'send to' drop down select who is going to receive the invoices by email. Use the 'copy manager' check box to choose whether to copy in the facility manager. Press the 'send invoices' button to generate and email the invoices. You find the email message content saved as html in the 'invoices folder' along with an xlsx format file with a summary that can be provide to your finance department.

