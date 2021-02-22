import os
import re
import time
import json
import gspread # pip install gspread
from doc import tool
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

config = tool.json_reader("doc/config.json")
confidentials = tool.json_reader("doc/confidentials.json")

USER = config["general"]["user"]
SHEET_KEY_FILE = confidentials["google"]["sheetKeyFile"]
SHEET_ID = confidentials["google"]["sheetId"]
SCOPE = "https://spreadsheets.google.com/feeds"

cert = ServiceAccountCredentials.from_json_keyfile_name(SHEET_KEY_FILE, SCOPE)
client = gspread.authorize(cert)

sheet = client.open_by_key(SHEET_ID).sheet1

def exists(video_id):
    video_exists = 0
    try:
        if sheet.find(video_id) != None:
            video_exists = 1
    except:
        pass
    return video_exists

def insert(video_info_list, video_id, file_name_abs): # Catch video_info_list from fproc.
    insert_list = list()
    insert_list.append("YT") # site
    insert_list.append(video_info_list[1]) # channelId
    insert_list.append(video_info_list[2]) # publishedAt
    insert_list.append(video_id) # videoId
    insert_list.append(video_info_list[3]) # title
    insert_list.append(json.dumps(video_info_list[4], ensure_ascii = False)) # description
    insert_list.append("") # customDescription
    insert_list.append(video_info_list[5]) # duration
    insert_list.append(USER) # user
    insert_list.append(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))) # lastUpdate
    insert_list.append(re.sub("[.]", "", os.path.splitext(file_name_abs)[1])) # extension
    sheet = client.open_by_key(SHEET_ID).sheet1
    sheet.append_row(insert_list, table_range = "A:A")