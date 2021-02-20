import os
import re
import time
import json
import codecs
#import rename
import videoinfo
import gspread # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

with codecs.open("config.json", "r", "utf-8") as json_file:
    config = json.load(json_file)

USER = config["general"]["user"]
SHEET_AUTH_FILE = config["confidentials"]["google"]["sheetAuthFile"]
SHEET_ID = config["confidentials"]["google"]["sheetId"]
SCOPE = "https://spreadsheets.google.com/feeds"

credentials = ServiceAccountCredentials.from_json_keyfile_name(SHEET_AUTH_FILE, SCOPE)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SHEET_ID).sheet1

def inserter(video_id, file_name_abs):
    videoinfo_list = list()
    videoinfo_list.clear()
    channel_id = videoinfo.get_channel_id(video_id)
    published_at = videoinfo.get_published_at(video_id)   
    title = videoinfo.get_title(video_id)
    description = videoinfo.get_description(video_id)
    duration = videoinfo.get_duration(video_id)
    last_update = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time())) # ISO 8601
    videoinfo_list.append("YT") # site
    videoinfo_list.append(channel_id)
    videoinfo_list.append(published_at)
    videoinfo_list.append(video_id)
    videoinfo_list.append(title)
    videoinfo_list.append(json.dumps(description, ensure_ascii = False))
    videoinfo_list.append("") # customDescription
    videoinfo_list.append(duration)
    videoinfo_list.append(USER)
    videoinfo_list.append(last_update)
    videoinfo_list.append(re.sub("[.]", "", os.path.splitext(file_name_abs)[1])) # extension
    sheet = client.open_by_key(SHEET_ID).sheet1
    sheet.insert_row(videoinfo_list, 1)