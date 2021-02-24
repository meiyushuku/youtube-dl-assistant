import os
import re
import codecs
import shutil
import getyt
import common
import insertgs
import globalvar as glo

config = common.read_json("doc/config.json")

path = config["general"]["workDir"]
isvideo = config["general"]["isVideo"]

glo._init()
glo.set_list("")
ignore_list = glo.get_list()
ignore_temp = common.read_json("ignore.json")

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
                if str(os.path.splitext(file_name_abs)[1]).lower() in isvideo:
                    if file_name.split()[0] == "youtube-dl":
                        if file_name_abs not in ignore_temp["ignore"]:
                            file_count_total += 1
                            file_name_list.append(file_name_abs)

def file_renamer():
    global error_renamer, file_name_rename 
    error_renamer = 0
    try:
        rename_published_at = re.sub("[-:]", "", published_at)
        rename_ext = os.path.splitext(file_name_abs)[1]
        file_name_rename = os.path.join(os.path.split(file_name_abs)[0], rename_published_at) + " " + video_id + rename_ext
        os.rename(file_name_abs, file_name_rename)
    except:
        add_ingnore(file_name_abs)
        error_renamer = 1

def channel_folder_creator():
    global error_creator
    error_creator = 0
    try: 
        if error_renamer == 0: 
            common.make_dir(os.path.join(path, channel_id))
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
        message = str('{:s} "{:s}" Could not rename.'.format(
            common.now_iso(2),
            video_id
            )
        )
        write_log(message)
        print(message)
        print("")
    elif error_creator == 1:
        message = str('{:s} "{:s}" Could not create folder "{:s}."'.format(
            common.now_iso(2),
            video_id,
            channel_id
            )
        )
        write_log(message)
        print(message)
        print("")
    elif error_mover == 1:
        message = str('{:s} "{:s}" Could not move file to "{:s}."'.format(
            common.now_iso(2),
            video_id,
            channel_id
            )
        )
        write_log(message)
        print(message)
        print("")
    else:
        message = str('{:s} "{:s}" Successfully. Destination folder: "{:s}."'.format(
            common.now_iso(2),
            video_id,
            channel_id
            )
        )
        write_log(message)
        print(message)
        print("")

def write_log(message):
    writer = codecs.open("doc/log.txt", "a","utf-8")
    writer.write("%s\n" % message)
    writer.close()

def add_ingnore(ident):
    ignore_list.append(ident)
    ignore_temp["ignore"] = ignore_list
    common.write_json("ignore.json", ignore_temp)

def main():
    global file_name_abs, video_id, channel_id, published_at
    dir_error = 0
    try:
        file_searcher()
    except:
        dir_error = 1
    if dir_error == 1:
        pass
    else:
        if file_count_total == 0:
            pass
        else:
            for file_name_abs in file_name_list:
                #print(ignore_list)
                #print(common.read_json("ignore.json"))
                video_id = os.path.split(file_name_abs)[1].split()[1]
                if insertgs.video_exists(video_id) == 1:
                    if file_name_abs not in ignore_temp["ignore"]:
                        add_ingnore(file_name_abs)
                        message = str('{:s} "{:s}" Video already exists.'.format(
                            common.now_iso(2),
                            video_id
                            )
                        )
                        write_log(message)
                        print(message)
                        print("")
                else:
                    error_apis = 0
                    try:
                        video_info_list = list()
                        video_info_list = getyt.get_video_info(video_id) # Catch video_info_list from getyt.
                        channel_id = video_info_list[1]
                        published_at = video_info_list[2]
                    except:
                        error_apis = 1
                    try:
                        if error_apis == 0:
                            insertgs.insert_video(video_info_list, video_id, file_name_abs) # Throw video_info_list to insertgs.
                    except:
                        error_apis = 2
                    if error_apis == 0:
                        if file_name_abs not in ignore_temp["ignore"]:
                            file_renamer()
                            channel_folder_creator()
                            file_mover()
                            display()
                    elif error_apis == 1:
                        if file_name_abs not in ignore_temp["ignore"]:
                            add_ingnore(file_name_abs)
                            message = str('{:s} "{:s}" Could not get video information.'.format(
                                common.now_iso(2),           
                                video_id
                                )
                            )
                            write_log(message)
                            print(message)
                            print("")
                    elif error_apis == 2:
                        if file_name_abs not in ignore_temp["ignore"]:
                            add_ingnore(file_name_abs)
                            message = str('{:s} "{:s}" Could not insert video information to sheet.'.format(
                                common.now_iso(2),           
                                video_id
                                )
                            )
                            write_log(message)
                            print(message)
                            print("")