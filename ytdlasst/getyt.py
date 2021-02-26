import os
import json

import common

import requests # pip install requests2
from apiclient.discovery import build # pip install google-api-python-client

def _getyt_init(confidentials):
    global youtube
    if "youtubeApiKey" in str(confidentials):
        if confidentials["google"]["youtubeApiKey"] != "":
            YOUTUBE_API_KEY = confidentials["google"]["youtubeApiKey"]
            TEST_URL = "https://www.googleapis.com/youtube/v3/videos?key=" + YOUTUBE_API_KEY
            resp = requests.get(TEST_URL)
            if json.loads(resp.text)["error"]["errors"][0]["reason"] != "badRequest":
                youtube = build(
                    "youtube", # YOUTUBE_API_SERVICE_NAME
                    "v3", # YOUTUBE_API_VERSION
                    developerKey = YOUTUBE_API_KEY
                    )
                return True
            else:
                print("API key not valid.")
                input()
        else:
            print("API key must be supplied.")
            input()
    else:
        print('Object "youtubeApiKey" not found in "confidentials.json."')
        input()

def get_video_info(video_id):
    video_info_list = []
    items = youtube.videos().list(
        part = "snippet, contentDetails",
        id = video_id
        ).execute()["items"][0]
    resp_save_dest = "data/resp/yt/v/"
    timestamp = common.now_iso(1) # UTC+0
    common.make_dir(resp_save_dest)
    common.write_json(resp_save_dest + timestamp + " " + video_id + ".json", items)
    video_info_list.append(items["snippet"]["channelTitle"]) # 0
    video_info_list.append(items["snippet"]["channelId"]) # 1
    video_info_list.append(items["snippet"]["publishedAt"]) # 2
    video_info_list.append(items["snippet"]["title"]) # 3
    video_info_list.append(items["snippet"]["description"]) # 4
    video_info_list.append(items["contentDetails"]["duration"]) # 5
    return video_info_list # Throw video_info_list to fileproc.