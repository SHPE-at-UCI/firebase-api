from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Which Spreadsheet to access
SHEET_ID = '1wGp2kCMkAYo31s4dTlfi8lrMfWsedWT-HV_ZpwsdsCg'
service = None

'''
	Reads in data from a spreadsheet at a specific sheet and range
'''
def _read(Spreadsheet, Sheet, Range):
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=Spreadsheet,range=Sheet+"!"+Range).execute()
	return result.get('values', [])
'''
	Writes data a spreadsheet at a specific sheet and range
'''
def _write(Spreadsheet, Sheet, Range, Data):
	body = {'values': [[Data]]}
	result = service.spreadsheets().values().update(
			spreadsheetId=Spreadsheet, range=Sheet+"!"+Range,
			valueInputOption="RAW", body=body).execute()
			
'''
	Server-side sign-in, should only force server to sign-in once when token.pickle is invalid or non-existant, so far only my UCI account is allowed to do so. I believe that if you test this with the token.pickle and credentials.json supplied, you won't need to sign-in to my account anyway, link to accessing the spreadsheet is supplied and shared to all UCI members witht the link
'''
def sign_in():
	global service
	if service != None:
		return

	creds = None
	if os.path.exists('sheets/token.pickle'):
		with open('sheets/token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('sheets/credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
			with open('sheets/token.pickle', 'wb') as token:
				pickle.dump(creds, token)
	service = build('sheets', 'v4', credentials=creds)
	
'''
	Add new data to end of spreadsheet
	
	 - only adds 1 item at a time, currently inefficient and not ideal if we send multiple at once, easy to change but unsure of yet
	 - First reads static location to get where current end of list is, then writes the data at that location
'''
def addNew(Data):
	add_pos = _read(SHEET_ID, "Sheet1", "B1")[0][0]
	_write(SHEET_ID, "Sheet1", add_pos, Data)

'''
	Find whether data exists and where it exists
	
	 - write to static cell location, then read from neighboring cell which gives row number of data or '-1' if the data was not found
'''
def find(Data):
	_write(SHEET_ID, "Sheet1", "B2", Data)
	return int(_read(SHEET_ID, "Sheet1", "B3")[0][0])
   

if __name__ == '__main__':
	import sys
	print(sys.argv)
	
	
	
	
	
	
	
	
