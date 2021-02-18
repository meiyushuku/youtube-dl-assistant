import os
import re
import time
import codecs
from apiclient.discovery import build

file_ext_isvideo = [".mkv", ".mp4"]

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = "AIzaSyAVKnfeGxZe3fMlpvNrlkrhD8hEs4DU6jE"
youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=YOUTUBE_API_KEY
    )

def get_channel_id(video_id):
    channel_id = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["channelId"]
    return channel_id

video_id = "gkdCcaRQVqg"
channel_id = get_channel_id(video_id)
print(channel_id)