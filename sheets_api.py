import pickle
import os  # .path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

flush_limit = int(os.getenv("FLUSH_LIMIT"))

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Which spreadsheet to access
sheet_name = "test"
SHEET_ID = "1wGp2kCMkAYo31s4dTlfi8lrMfWsedWT-HV_ZpwsdsCg"

# Runtime API sign-in information
service = None
creds = None


def _read(spreadsheet, sheet, a_range):
    """
    Reads in data from a spreadsheet at a specific sheet and range
    """
    values = service.spreadsheets().values()
    result = values.get(
        spreadsheetId=spreadsheet, range=sheet + "!" + a_range
    ).execute()
    return result.get("values", [])


def _write(spreadsheet, sheet, a_range, data):
    """
    Writes data a spreadsheet at a specific sheet and range
    """
    body = {"values": data}
    values = service.spreadsheets().values()
    values.update(
        spreadsheetId=spreadsheet,
        range=sheet + "!" + a_range,
        valueInputOption="RAW",
        body=body,
    ).execute()


def sign_in():
    """
    Server-side sign-in, should only force server to sign-in once when token.pickle is
    invalid or non-existent, so far only my UCI account is allowed to do so. I believe
    that if you test this with the token.pickle and credentials.json supplied, you
    won't need to sign-in to my account anyway, link to accessing the spreadsheet is
    supplied and shared to all UCI members with the link
    """
    global service, creds
    if service is not None:
        if creds.expired:
            print("Credentials have expired, refreshing credentials and service")
            creds.refresh(Request())
            with open("sheets/token.pickle", "wb") as token:
                pickle.dump(creds, token)
            service = build("sheets", "v4", credentials=creds)
        return

    if os.path.exists("sheets/token.pickle"):
        print("Loading credentials from saved pickle")
        with open("sheets/token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        print("Credentials don't exist or have expired")
        # creds.expired updates datetime.timedelta(hours=7, minutes=5) from expiration
        if creds and creds.expired and creds.refresh_token:
            print("Using refresh token to gain access token")
            creds.refresh(Request())
        else:
            print("Performing first time token generation")
            flow = InstalledAppFlow.from_client_secrets_file(
                "sheets/credentials.json", SCOPES
            )
            creds = flow.run_local_server(host="localhost", port=8080, prompt="consent")
            with open("sheets/token.pickle", "wb") as token:
                pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)


def addSingle(data):
    """
    Add new data to end of spreadsheet

     - only adds 1 item at a time, currently inefficient and not ideal if we send
     multiple at once, easy to change but unsure of yet
     - First reads static location to get where current end of list is, then writes
     the data at that location
     - add multiple adds multiple pieces of data to the end of the spreadsheet
    """
    add_pos = _read(SHEET_ID, sheet_name, "B1")[0][0]
    _write(SHEET_ID, sheet_name, add_pos, [[data]])


def addMultiple(data):
    add_pos = _read(SHEET_ID, sheet_name, "B1")[0][0]
    _write(SHEET_ID, sheet_name, add_pos, data)


def find(data):
    """
    Find whether data exists and where it exists

     - write to static cell location, then read from neighboring cell which gives row
     number of data or '-1' if the data was not found
    """
    _write(SHEET_ID, sheet_name, "B2", [[data]])
    return int(_read(SHEET_ID, sheet_name, "B3")[0][0])


class buffer:
    """
    Special set data structure, to make sure we can add our data and
    return it in a good format for addMultiple
    """

    def __init__(self, data=set()):
        self.data = set(data)

    def __repr__(self):
        return "sheets_api.buffer(" + repr(self.data) + ")"

    def __str__(self):
        return "flush limit " + str(flush_limit) + ", " + str(self.data)

    def __len__(self):
        return len(self.data)

    def add(self, item):
        if type(item) == list:
            item = tuple(item)
        elif type(item) != tuple:
            item = (item,)
        self.data.add(item)

    def is_filled(self):
        return len(self) >= flush_limit

    def process(self):
        data = self.data
        self.__init__()

        data = list(data)
        for i in range(len(self)):
            data[i] = list(data[i])
        return data


if __name__ == "__main__":
    import sys

    print(sys.argv)
