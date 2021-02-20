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
    video_info_list.clear()
    channel_title = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["channelTitle"]
    channel_id = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["channelId"]   
    published_at = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["publishedAt"]
    title = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["title"]
    description = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["description"]
    duration = youtube.videos().list(
        part = "contentDetails",
        id = video_id
        ).execute()["items"][0]["contentDetails"]["duration"]
    video_info_list.append(channel_title) # 0
    video_info_list.append(channel_id) # 1
    video_info_list.append(published_at) # 2
    video_info_list.append(title) # 3
    video_info_list.append(description) # 4
    video_info_list.append(duration) # 5
    return video_info_list




'''
def get_published_at(video_id):
    published_at = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["publishedAt"]
    return published_at

def get_channel_id(video_id):
    channel_id = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["channelId"]
    return channel_id

def get_title(video_id):
    title = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["title"]
    return title

def get_description(video_id):
    description = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["description"]
    return description

def get_channel_title(video_id):
    channel_title = youtube.videos().list(
        part = "snippet",
        id = video_id
        ).execute()["items"][0]["snippet"]["channelTitle"]
    return channel_title

def get_duration(video_id):
    duration = youtube.videos().list(
        part = "contentDetails",
        id = video_id
        ).execute()["items"][0]["contentDetails"]["duration"]
    return duration
'''
'''
video_id = "J9zp5D6JddI"
print(get_published_at(video_id))
print("")
print(get_channel_id(video_id))
print("")
print(get_title(video_id))
print("")
print(get_description(video_id))
print("")
print(get_channel_title(video_id))
print("")
print(get_duration(video_id))
print("")
'''