import os
import re
import time
import json
import codecs
import shutil
import insertgs
import videoinfo

with codecs.open("config.json", "r", "utf-8") as json_file:
    config = json.load(json_file)

path = config["general"]["workDir"]
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

def csv_creator():
    try:
        file_name_without_ext = os.path.splitext(os.path.split(file_name_abs)[1])[0]
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
        rename_ext = os.path.splitext(file_name_abs)[1]
        file_name_rename = os.path.join(os.path.split(file_name_abs)[0], rename_published_at) + " " + video_id + rename_ext
        os.rename(file_name_abs, file_name_rename)
    except:
        error_renamer = 1

def channel_folder_creator():
    global error_creator
    error_creator = 0
    try: 
        if error_renamer == 0:
            if not os.path.isdir(os.path.join(path, channel_id)):
                os.mkdir(os.path.join(path, channel_id))
        else:
            return
    except:
        error_creator = 1

def file_mover():
    global error_mover
    error_mover = 0
    try:
        if error_renamer == 0 and error_creator == 0:
            shutil.move(file_name_rename, os.path.join(path, channel_id))
        else:
            return
    except:
        error_mover = 1

def display():
    if error_renamer == 1:
        message = str('{:d}/{:d} Could not rename "{:s}," file "{:s}" already exists.'.format(
            file_count,
            file_count_total,
            os.path.split(file_name_abs)[1],
            os.path.split(file_name_rename)[1]
            )
        )
        log_writer(message)
        print(message)
        print("")
    elif error_creator == 1:
        message = str('{:d}/{:d} Could not create channel folder, file "{:s}" already exists. "{:s}" has been renamed as "{:s}."'.format(
            file_count,
            file_count_total,
            channel_id,
            os.path.split(file_name_abs)[1],
            os.path.split(file_name_rename)[1]
            )
        )
        log_writer(message)
        print(message)
        print("")
    elif error_mover == 1:
        message = str('{:d}/{:d} Could not move "{:s}" to "{:s}", file with same name already exists there. "{:s}" has been renamed as "{:s}.'.format(
            file_count,
            file_count_total,
            os.path.split(file_name_rename)[1],
            channel_id,
            os.path.split(file_name_abs)[1],
            os.path.split(file_name_rename)[1]
            )
        )
        log_writer(message)
        print(message)
        print("")
    else:
        message = str('{:d}/{:d} Successfully. "{:s}" renamed as "{:s}" and moved to "{:s}."'.format(
            file_count,
            file_count_total,
            os.path.split(file_name_abs)[1],
            os.path.split(file_name_rename)[1],
            channel_id
            )
        )
        log_writer(message)
        print(message)
        print("")

def log_writer(message):
    writer = codecs.open("log.txt", "a","utf-8")
    if file_count == 1:
        writer.write("%s\n" % task_timestamp)
        writer.write("%s\n" % message)
    else:
        writer.write("%s\n" % message)
    writer.close()

def rename_exe():
    global file_count, file_name_abs, video_id, channel_id, published_at
    file_count = 0
    file_searcher()
    print("Working directory: %s" % path)
    if file_count_total == 0:
        print("No pending files.")
    else:
        print("Pending: %d" % file_count_total)
        input("Type here >>> ")
        for file_name_abs in file_name_list:
            file_count += 1
            video_id = os.path.split(file_name_abs)[1].split()[1]
            error_apis = 0
            try:
                video_info_list = list()
                video_info_list = videoinfo.get_video_info(video_id) # Catch video_info_list from videoinfo.
                channel_id = video_info_list[1]
                published_at = video_info_list[2]
            except:
                error_apis = 1
            try:
                if error_apis == 0:
                    insertgs.insert(video_info_list, video_id, file_name_abs) # Throw video_info_list to insertgs.
            except:
                error_apis = 2
            if error_apis == 0:
                csv_creator()
                file_renamer()
                channel_folder_creator()
                file_mover()
                display()
            elif error_apis == 1:
                message = str('{:d}/{:d} Could not get video information of "{:s}."'.format(
                    file_count,
                    file_count_total,                
                    os.path.split(file_name_abs)[1]
                    )
                )
                log_writer()
                print(message)
                print("")
            elif error_apis == 2:
                message = str('{:d}/{:d} Could not insert video information of "{:s} to sheet."'.format(
                    file_count,
                    file_count_total,                
                    os.path.split(file_name_abs)[1]
                    )
                )
                log_writer()
                print(message)
                print("")