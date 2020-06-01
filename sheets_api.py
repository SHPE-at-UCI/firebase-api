from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Which Spreadsheet to access
sheet_name = "Sheet1"
SHEET_ID = '1wGp2kCMkAYo31s4dTlfi8lrMfWsedWT-HV_ZpwsdsCg'

# Runtime API sign-in information
service = None
creds = None

'''
	Reads in data from a spreadsheet at a specific sheet and range
'''
def _read(Spreadsheet, Sheet, Range):
    values = service.spreadsheets().values()
    result = values.get(spreadsheetId=Spreadsheet,range=Sheet+"!"+Range).execute()
    return result.get('values', [])
'''
	Writes data a spreadsheet at a specific sheet and range
'''
def _write(Spreadsheet, Sheet, Range, Data):
    body = {'values': Data}
    values = service.spreadsheets().values()
    result = values.update(spreadsheetId=Spreadsheet, range=Sheet+"!"+Range, valueInputOption="RAW", body=body).execute()
    

'''
	Server-side sign-in, should only force server to sign-in once when token.pickle is invalid or non-existant, so far only my UCI account is allowed to do so. I believe that if you test this with the token.pickle and credentials.json supplied, you won't need to sign-in to my account anyway, link to accessing the spreadsheet is supplied and shared to all UCI members witht the link
'''
def sign_in():
    global service, creds    
    if service != None:
        if(creds.expired):
            print("Credentials have expired, refreshing credentials and service")
            creds.refresh(Request())
            with open('sheets/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            service = build('sheets', 'v4', credentials=creds)   
        return
    
    if os.path.exists('sheets/token.pickle'):
        print("Loading credentials from saved pickle")
        with open('sheets/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        print("Credentials don't exist or have expired")
        #creds.expired updates datetime.timedelta(hours=7, minutes=5) from expiration
        # if creds and creds.expired and creds.refresh_token:
        #     print("Using refresh token to gain access token")
        #     creds.refresh(Request())
        # else:
        print("Performing first time token generation")
        flow = InstalledAppFlow.from_client_secrets_file('sheets/credentials.json', SCOPES)
        creds = flow.run_local_server(host='localhost', port=8080, prompt='consent')
            
        with open('sheets/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
				
    service = build('sheets', 'v4', credentials=creds)
	
'''
	Add new data to end of spreadsheet
	
	 - only adds 1 item at a time, currently inefficient and not ideal if we send multiple at once, easy to change but unsure of yet
	 - First reads static location to get where current end of list is, then writes the data at that location
	 - addmultiple adds multiple pieces of data to the end of the spreadsheet
'''
def addSingle(Data):
    add_pos = _read(SHEET_ID, sheet_name, "B1")[0][0]
    _write(SHEET_ID, sheet_name, add_pos, [[Data]])

def addMultiple(Data):
    add_pos = _read(SHEET_ID, sheet_name, "B1")[0][0]
    _write(SHEET_ID, sheet_name, add_pos, Data)
'''
	Find whether data exists and where it exists
	
	 - write to static cell location, then read from neighboring cell which gives row number of data or '-1' if the data was not found
'''
def find(Data):
    _write(SHEET_ID, sheet_name, "B2", [[Data]])
    return int(_read(SHEET_ID, sheet_name, "B3")[0][0])
	
'''
	Special set data structure, to make sure we can add our data and
	return it in a good format for addMultiple
'''
class buffer:
    def __init__(self):
        self.data = set()#TODO we can change this value to be bigger, smaller values are just faster to test
        self.flush_limit = 3
    def __str__(self):
        return "flush limit "+str(self.flush_limit)+", "+str(self.data)
    def __len__(self):
        return len(self.data)
    def add(self, item):
        if(type(item)==list):
            item = tuple(item)
        elif(type(item)!=tuple):
       	    item = (item,)
        self.data.add(item)
    def is_filled(self):
        return len(self)>=self.flush_limit
    def process(self):
        data = self.data
        self.__init__()

        data = list(data)
        for i in range(len(self)):
            data[i] = list(data[i])
        return data
   

if __name__ == '__main__':
    import sys
    print(sys.argv)
	
	
	
	
	
	
	
	
