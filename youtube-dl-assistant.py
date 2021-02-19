import os
import re
import time
import codecs
import shutil
from apiclient.discovery import build

file_ext_isvideo = [".mkv", ".mp4"]
task_timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time())) # ISO 8601

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = "AIzaSyAVKnfeGxZe3fMlpvNrlkrhD8hEs4DU6jE"
youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=YOUTUBE_API_KEY
    )

def get_published_at(video_id):
    global error_get_published_at
    error_get_published_at = 0
    try:
        published_at = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["publishedAt"]
        return published_at
    except:
        error_get_published_at = 1

def get_channel_id(video_id):
    global error_get_channel_id
    error_get_channel_id = 0
    try:
        channel_id = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["channelId"]
        return channel_id
    except:
        error_get_channel_id = 1

def file_searcher():
    global file_count_total, file_name_list
    path = "."
    file_count_total = 0
    file_name_list = list()
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            file_name = file
            file_size = os.path.getsize(file_name) 
            if file_size != 0:
                if str(os.path.splitext(os.path.split(file_name)[1])[1]).lower() in file_ext_isvideo:
                    if file_name.split()[0] == "youtube-dl":
                        file_count_total += 1
                        file_name_list.append(file_name)

def csv_creator():
    try:
        file_name_without_ext = os.path.splitext(os.path.split(file_name)[1])[0]
        csv_output = 'https://www.youtube.com/watch?v=' + video_id + ',"' + file_name_without_ext + '",,MKV,,,,,"",'
        writer = codecs.open(task_timestamp + ".csv", "a","utf-8")
        writer.write("%s\n" % csv_output)
        writer.close()
    except:
        print("Error code: 101")

def file_renamer():
    global error_renamer, file_name_rename 
    error_renamer = 0
    try:
        rename_published_at = re.sub("[-:]", "", published_at)
        rename_ext = os.path.splitext(file_name)[1]
        file_name_rename = rename_published_at + " " + video_id + rename_ext
        os.rename(file_name, file_name_rename)
    except:
        error_renamer = 1

def channel_folder_creator():
    global error_creator
    error_creator = 0
    try: 
        if error_renamer == 0:
            if not os.path.isdir(channel_id):
                os.mkdir(channel_id)
        else:
            return
    except:
        error_creator = 1

def file_mover():
    global error_mover
    error_mover = 0
    try:
        if error_renamer == 0 and error_creator == 0:
            shutil.move(file_name_rename, channel_id)
        else:
            return
    except:
        error_mover = 1

def display():
    global message
    if error_renamer == 1:
        message = str('{:d}/{:d} Could not rename "{:s}," file "{:s}" already exists.'.format(
            file_count,
            file_count_total,
            file_name,
            file_name_rename,
            )
        )
        log_writer()
        print(message)
        print("")
    elif error_creator == 1:
        message = str('{:d}/{:d} Could not create channel folder, file "{:s}" already exists. "{:s}" has been renamed as "{:s}."'.format(
            file_count,
            file_count_total,
            channel_id,
            file_name,
            file_name_rename,
            )
        )
        log_writer()
        print(message)
        print("")
    elif error_mover == 1:
        message = str('{:d}/{:d} Could not move "{:s}" to "{:s}", file with same name already exists there. "{:s}" has been renamed as "{:s}.'.format(
            file_count,
            file_count_total,
            file_name_rename,
            channel_id,
            file_name,
            file_name_rename
            )
        )
        log_writer()
        print(message)
        print("")
    else:
        message = str('{:d}/{:d} Successfully. "{:s}" renamed as "{:s}" and moved to "{:s}."'.format(
            file_count,
            file_count_total,
            file_name,
            file_name_rename,
            channel_id
            )
        )
        log_writer()
        print(message)
        print("")

def log_writer():
    writer = codecs.open("log.txt", "a","utf-8")
    if file_count == 1:
        writer.write("%s\n" % task_timestamp)
        writer.write("%s\n" % message)
    else:
        writer.write("%s\n" % message)
    writer.close()

file_count = 0
file_searcher()
if file_count_total == 0:
    print("No pending files.")
else:
    print("Pending: %d" % file_count_total)
    input()
    for file_name in file_name_list:
        file_count += 1
        video_id = file_name.split()[1]
        published_at = get_published_at(video_id)
        channel_id = get_channel_id(video_id)
        if error_get_published_at == 0 and error_get_channel_id == 0:
            csv_creator()
            file_renamer()
            channel_folder_creator()
            file_mover()
            display()
        else: 
            print('Could not get video information of "%s"' % file_name)
            print("")
    print("Task is completed.")
input()