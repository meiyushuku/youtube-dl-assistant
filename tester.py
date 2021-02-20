import os
import re
import time
import json
import codecs
import shutil

import videoinfo

video_id = "J9zp5D6JddI"
print(videoinfo.get_video_info(video_id)[0])
print("")
print(videoinfo.get_video_info(video_id)[1])
print("")
print(videoinfo.get_video_info(video_id)[2])
print("")
print(videoinfo.get_video_info(video_id)[3])
print("")

'''
with codecs.open("config.json", "r", "utf-8") as json_file:
    config = json.load(json_file)

print(config["confidential"]["google"]["youtubeApiKey"])
print(config["general"]["workDir"])



path = "D:\\Dropbox\\Workspace\\Programming\\DESKTOP-QVBHRG1\\youtube-dl-assistant testspace"
file_ext_isvideo = [".mkv", ".mp4"]
task_timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time())) # ISO 8601

def file_searcher():
    global file_count_total, file_name_list
    file_count_total = 0
    file_name_list = list()
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            file_name = file
            file_name_abs = os.path.join(path, file_name)
            file_size = os.path.getsize(file_name_abs)
            if file_size != 0:
                if str(os.path.splitext(file_name_abs)[1]).lower() in file_ext_isvideo:
                    if file_name.split()[0] == "youtube-dl":
                        file_count_total += 1
                        file_name_list.append(file_name_abs)

def file_renamer():
    global error_renamer, file_name_rename 
    error_renamer = 0
    try:
        rename_published_at = re.sub("[-:]", "", published_at)
        rename_ext = os.path.splitext(file_name_abs)[1]
        file_name_rename = os.path.join(os.path.split(file_name_abs)[0], rename_published_at) + " " + video_id + rename_ext
        #os.rename(file_name_abs, file_name_rename)
    except:
        error_renamer = 1

file_count = 0
file_searcher()
print("Working directory: %s" % path)
if file_count_total == 0:
    print("No pending files.")
else:
    print("Pending: %d" % file_count_total)
    input()
    for file_name_abs in file_name_list:
        file_count += 1
        video_id = os.path.split(file_name_abs)[1].split()[1]
        published_at = snippet.get_published_at(video_id)
        channel_id = snippet.get_channel_id(video_id)
        if snippet.error_snippet == 0:
            #csv_creator()
            file_renamer()
            #channel_folder_creator()
            #file_mover()
            #display()
            print("ya")
        else: 
            print('{:d}/{:d} Could not get video information of "{:s}."'.format(
                file_count,
                file_count_total,                
                os.path.split(file_name_abs)[1]
                )
            )
            print("")
'''