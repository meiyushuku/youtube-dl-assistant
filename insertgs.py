import os
import re
import time
import json
import codecs
import gspread # pip install gspread
import videoinfo
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

with codecs.open("config.json", "r", "utf-8") as json_file:
    config = json.load(json_file)

USER = config["general"]["user"]
SHEET_KEY_FILE = config["confidentials"]["google"]["sheetKeyFile"]
SHEET_ID = config["confidentials"]["google"]["sheetId"]
SCOPE = "https://spreadsheets.google.com/feeds"

credentials = ServiceAccountCredentials.from_json_keyfile_name(SHEET_KEY_FILE, SCOPE)
client = gspread.authorize(credentials)

def insert(video_id, file_name_abs):
    insert_list = list()
    insert_list.clear()
    insert_list.append("YT") # site
    insert_list.append(videoinfo.get_video_info(video_id)[1]) # channelId
    insert_list.append(videoinfo.get_video_info(video_id)[2]) # publishedAt
    insert_list.append(video_id) # videoId
    insert_list.append(videoinfo.get_video_info(video_id)[3]) # title
    insert_list.append(json.dumps(videoinfo.get_video_info(video_id)[4], ensure_ascii = False)) # description
    insert_list.append("") # customDescription
    insert_list.append(videoinfo.get_video_info(video_id)[5]) # duration
    insert_list.append(USER) # user
    insert_list.append(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))) # lastUpdate
    insert_list.append(re.sub("[.]", "", os.path.splitext(file_name_abs)[1])) # extension
    sheet = client.open_by_key(SHEET_ID).sheet1
    sheet.insert_row(insert_list, 1)