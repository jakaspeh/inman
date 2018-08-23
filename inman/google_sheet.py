from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from inman.config import get_google_credential_file

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'


def get_raw_data_from_google_sheets(spreadsheet_id, tab, value_range):
    # Setup the Sheets API
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        path = get_google_credential_file()
        flow = client.flow_from_clientsecrets(path, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    range_name = tab + value_range
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                 range=range_name).execute()
    return result.get('values', [])