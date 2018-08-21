import os


def get_google_credential_file():
    return os.getenv('CredentialsGoogleSheets')


def get_working_hours_spreadsheet_id():
    return os.getenv('WorkingHoursSpreadsheetId')


def get_invoice_spreadsheet_id():
    return os.getenv('InvoiceSpreadsheetId')