import os
import re
import json

import common

import requests # pip install requests2
import gspread # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

def _insertgs_init(config, confidentials):
    global USER, DATABASE_API_URL, sheet1, sheet2
    try:
        USER = config["general"]["user"]
        SHEET_KEY_FILE = confidentials["google"]["sheetKeyFile"]
        SHEET_ID = confidentials["google"]["sheetId"]
        SCOPE = "https://spreadsheets.google.com/feeds"
        DATABASE_API_URL = confidentials["google"]["databeseApiUrl"]
        cert = ServiceAccountCredentials.from_json_keyfile_name(SHEET_KEY_FILE, SCOPE)
        client = gspread.authorize(cert)
        sheet1 = client.open_by_key(SHEET_ID).get_worksheet(0) # channelInfo
        sheet2 = client.open_by_key(SHEET_ID).get_worksheet(1) # videoInfo
        return True
    except:
        print("Error")
        input()
        return False

def video_exists(video_id):
    video_info_url = DATABASE_API_URL + "?method=getVideoInfoByVideoId&site=YT&videoId=" + video_id
    response = requests.get(video_info_url)
    if json.loads(response.text):
        video_exists = 1 # 1
    else:
        video_exists = 0 # 0
    return video_exists

'''
def video_exists(video_id):
    try:
        if sheet2.find(video_id):
            video_exists = 1
    except:
        video_exists = 0
    return video_exists

def channel_exists(channel_id):
    try:
        if sheet1.find(channel_id):
            channel_exists = 1
    except:
        channel_exists = 0
    return channel_exists
'''

def insert_video(video_info_list, video_id, file_name_abs): # Catch video_info_list from fileproc.
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
    insert_list.append(common.now_iso(2)) # lastUpdate
    insert_list.append(re.sub("[.]", "", os.path.splitext(file_name_abs)[1])) # extension
    sheet2.append_row(insert_list, table_range = "A:A")

#def insert_channel():