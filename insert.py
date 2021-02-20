import json
import codecs
import gspread # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

with codecs.open("config.json", "r", "utf-8") as json_file:
    config = json.load(json_file)

SHEET_AUTH_FILE = config["confidentials"]["google"]["sheetAuthFile"]
SHEET_ID = config["confidentials"]["google"]["sheetId"]
SCOPE = "https://spreadsheets.google.com/feeds"

credentials = ServiceAccountCredentials.from_json_keyfile_name(SHEET_AUTH_FILE, SCOPE)
client = gspread.authorize(credentials)

sheet = client.open_by_key(SHEET_ID).sheet1

listtitle = ["姓名", "電話"]
listdata = ["123", "456"]
sheet.append_row(listtitle)
sheet.append_row(listdata)
values = ['A','B','C','D']
sheet.insert_row(values, 3)