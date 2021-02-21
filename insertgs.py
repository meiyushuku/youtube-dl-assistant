import os
import re
import time
import json
import codecs
import gspread # pip install gspread
import requests # pip3 install requests2
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

with codecs.open("config.json", "r", "utf-8") as json_file:
    config = json.load(json_file)

USER = config["general"]["user"]
DATABASE_API_URL = config["confidentials"]["google"]["databeseApiUrl"]

def exists(video_id):
    video_info_url = DATABASE_API_URL + "?method=getVideoInfoByVideoId&site=YT&videoId=" + video_id
    response = requests.get(video_info_url)
    if json.loads(response.text):
        video_exists = 1
    else:
        video_exists = 0
    return video_exists

def insert(video_info_list, video_id, file_name_abs): # Catch video_info_list from rename.
    video_info_dict = dict()
    video_info_dict["method"] = "insertVideoInfo"
    video_info_dict["site"] = "YT"
    video_info_dict["channelId"] = video_info_list[1]
    video_info_dict["publishedAt"] = video_info_list[2]
    video_info_dict["videoId"] = video_id
    video_info_dict["title"] = video_info_list[3]
    video_info_dict["description"] = video_info_list[4]
    video_info_dict["customDescription"] = ""
    video_info_dict["duration"] = video_info_list[5]
    video_info_dict["user"] = USER
    video_info_dict["extension"] = re.sub("[.]", "", os.path.splitext(file_name_abs)[1])
    video_info_dict["ignoreIfExist"] = True
    video_info_dict_json = json.dumps(video_info_dict, ensure_ascii = False)
    response = requests.post(DATABASE_API_URL, json = video_info_dict)

'''
SHEET_KEY_FILE = config["confidentials"]["google"]["sheetKeyFile"]
SHEET_ID = config["confidentials"]["google"]["sheetId"]
SCOPE = "https://spreadsheets.google.com/feeds"

credentials = ServiceAccountCredentials.from_json_keyfile_name(SHEET_KEY_FILE, SCOPE)
client = gspread.authorize(credentials)

sheet = client.open_by_key(SHEET_ID).sheet1

def exists(video_id):
    video_exists = 0
    try:
        if sheet.find(video_id) != None:
            video_exists = 1
    except:
        pass
    return video_exists

def insert(video_info_list, video_id, file_name_abs): # Catch video_info_list from rename.
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
'''