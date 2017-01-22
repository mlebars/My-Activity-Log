from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from duolingo import get_today_points

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret_951984310246-lrmka2unc2cal7bqh03qgb2h59lp35b7.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Test'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1uHpYnbfyHAB9g61TTZ3IwdG8tAX3p4wuQdEMUR1X77U'
    rangeName = 'January!A2:G2'
    
    values = [get_today_points()]
    body = {'values':values}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=rangeName, valueInputOption='RAW', body=body).execute()


if __name__ == '__main__':
    main()
