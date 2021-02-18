import os
import re
import time
import codecs
import shutil
from apiclient.discovery import build

file_ext_isvideo = [".mkv", ".mp4"]
csv_name = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time())) # ISO 8601

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = "AIzaSyAVKnfeGxZe3fMlpvNrlkrhD8hEs4DU6jE"
youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=YOUTUBE_API_KEY
    )

def get_published_at(video_id):
    published_at = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["publishedAt"]
    return published_at

def get_channel_id(video_id):
    channel_id = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["channelId"]
    return channel_id

def file_searcher():
    global path, file_count, file_name_list
    path = "."
    file_count = 0
    file_name_list = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_name = os.path.join(root, file)
            file_size = os.path.getsize(file_name) 
            if file_size != 0:
                if str(os.path.splitext(os.path.split(file_name)[1])[1]).lower() in file_ext_isvideo:
                    file_count += 1
                    file_name_list.append(file_name)

def channel_folder_creator():
    channel_folder = ".\\%s" % channel_id
    if not os.path.isdir(channel_folder):
        os.mkdir(channel_folder)
    file_name_abs = os.path.abspath(file_name)
    channel_folder_path = os.path.split(file_name_abs)[0] + "\\" + channel_id + "\\"
    shutil.move(file_name_abs, channel_folder_path)

def csv_creator():
    file_name_without_ext = os.path.splitext(os.path.split(file_name)[1])[0]
    csv_output = 'https://www.youtube.com/watch?v=' + video_id + ',"' + file_name_without_ext + '",,MKV,,,,,"",'
    writer = codecs.open(csv_name + ".csv", "a","utf-8")
    writer.write("%s\n" % csv_output)
    writer.close()

def file_renamer():
    file_name_abs = os.path.abspath(file_name)
    rename_path = os.path.split(file_name_abs)[0] + "\\" + channel_id + "\\"
    rename_published_at = re.sub("[-:]", "", published_at)
    rename_ext = os.path.splitext(os.path.split(file_name)[1])[1]
    file_name_abs_new = rename_path + os.path.split(file_name_abs)[1]
    os.rename(file_name_abs_new, rename_path + rename_published_at + " " + video_id + rename_ext)

file_searcher()
for file_name in file_name_list:
    video_id = file_name.split()[2]
    published_at = get_published_at(video_id)
    channel_id = get_channel_id(video_id)
    csv_creator()
    channel_folder_creator()
    file_renamer()

#input()