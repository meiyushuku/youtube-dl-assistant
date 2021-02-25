import os
import json

import common

import requests # pip install requests2
from apiclient.discovery import build # pip install google-api-python-client

confidentials = common.read_json("doc/confidentials.json.")

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
                return False
        else:
            print("API key must be supplied.")
            input()
            return False
    else:
        print('Object "youtubeApiKey" not found in "confidentials.json."')
        input()
        return False

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

def get_channel_info(channel_id):
    items = youtube.channels().list(
    part = "contentDetails",
    id = channel_id
    ).execute()
    return items

def get_playlist(playlist_id):
    items = youtube.playlistItems().list(
    part = "snippet,contentDetails,status",
    playlistId = playlist_id,
    maxResults = 50
    ).execute()
    return items

_getyt_init(confidentials)
channel_id = "UCPn4XA6Gb2u8y_FXXtrHW7w" # CHIAI
resp = get_channel_info(channel_id)
common.write_json("test.json", resp)

playlist_id = resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
print(playlist_id)

resp2 = get_playlist("UUPn4XA6Gb2u8y_FXXtrHW7w")
common.write_json("test2.json", resp2["items"][0])

