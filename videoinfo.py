import json
import codecs
from apiclient.discovery import build # pip install google-api-python-client

with codecs.open("config.json", "r", "utf-8") as json_file:
    config = json.load(json_file)

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = config["confidentials"]["google"]["youtubeApiKey"]
youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=YOUTUBE_API_KEY
    )

def get_video_info(video_id):
    video_info_list = list()
    items = youtube.videos().list(
        part = "snippet, contentDetails",
        id = video_id
        ).execute()["items"][0]
    video_info_list.append(items["snippet"]["channelTitle"]) # 0
    video_info_list.append(items["snippet"]["channelId"]) # 1
    video_info_list.append(items["snippet"]["publishedAt"]) # 2
    video_info_list.append(items["snippet"]["title"]) # 3
    video_info_list.append(items["snippet"]["description"]) # 4
    video_info_list.append(items["contentDetails"]["duration"]) # 5
    return video_info_list # Throw video_info_list to rename.