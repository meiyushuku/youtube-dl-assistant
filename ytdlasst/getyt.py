import time
import common
from apiclient.discovery import build # pip install google-api-python-client

confidentials = common.json_reader("doc/confidentials.json")

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = confidentials["google"]["youtubeApiKey"]
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
    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time())) # UTC+0
    resp_save_dest = "data/resp/yt/v/"
    common.make_dir(resp_save_dest)
    common.json_writer(resp_save_dest + timestamp + " " + video_id + ".json", items)
    video_info_list.append(items["snippet"]["channelTitle"]) # 0
    video_info_list.append(items["snippet"]["channelId"]) # 1
    video_info_list.append(items["snippet"]["publishedAt"]) # 2
    video_info_list.append(items["snippet"]["title"]) # 3
    video_info_list.append(items["snippet"]["description"]) # 4
    video_info_list.append(items["contentDetails"]["duration"]) # 5
    return video_info_list # Throw video_info_list to fileproc.