import os
import re
import time
import json
import codecs
import requests # pip3 install requests2

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
    response = requests.post(DATABASE_API_URL, json = video_info_dict)