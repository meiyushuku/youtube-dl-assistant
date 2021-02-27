import os
import re
import codecs
import shutil

import common
from getyt import get_video_info
import insertgs
import insertrdb

ignore_list = []

def rename_file(file_name, work_dir, published_at, video_id, ignore_temp):
    global error_renamer, file_name_rename
    error_renamer = 0
    try:
        published_at_iso_basic = re.sub("[-:]", "", published_at)
        ext = os.path.splitext(file_name)[1]
        file_name_rename = os.path.join(work_dir, published_at_iso_basic) + " " + video_id + ext
        os.rename(file_name, file_name_rename)
    except:
        add_ingnore(file_name, ignore_temp)
        error_renamer = 1

def create_channel_folder(work_dir, channel_id):
    global error_creator
    error_creator = 0
    try: 
        if error_renamer == 0: 
            common.make_dir(os.path.join(work_dir, channel_id))
        else:
            return
    except:
        error_creator = 1

def move_file(work_dir, channel_id):
    global error_mover
    error_mover = 0
    try:
        if error_renamer == 0 and error_creator == 0:
            shutil.move(file_name_rename, os.path.join(work_dir, channel_id))
        else:
            return
    except:
        error_mover = 1

def display(video_id, channel_id):
    if error_renamer == 1:
        message = str('{:s} [FILE] "{:s}" Could not rename.'.format(
            common.now_iso(2),
            video_id
            )
        )
        write_log(message)
        print(message)
    elif error_creator == 1:
        message = str('{:s} [FILE] "{:s}" Could not create folder "{:s}."'.format(
            common.now_iso(2),
            video_id,
            channel_id
            )
        )
        write_log(message)
        print(message)
    elif error_mover == 1:
        message = str('{:s} [FILE] "{:s}" Could not move file to "{:s}."'.format(
            common.now_iso(2),
            video_id,
            channel_id
            )
        )
        write_log(message)
        print(message)
    else:
        message = str('{:s} [FILE] "{:s}" Successfully. Destination folder: "{:s}."'.format(
            common.now_iso(2),
            video_id,
            channel_id
            )
        )
        write_log(message)
        print(message)

def write_log(message):
    writer = codecs.open("doc/log.txt", "a","utf-8")
    writer.write("%s\n" % message)
    writer.close()

def add_ingnore(ident, ignore_temp):
    ignore_list.append(ident)
    ignore_temp["ignore"] = ignore_list
    common.write_json("doc/ignore.json", ignore_temp)

def main(work_dir, is_video):
    ignore_temp = common.read_json("doc/ignore.json")
    for file in os.listdir(work_dir):
        if os.path.isfile(os.path.join(work_dir, file)):
            _ = file
            file_name = os.path.join(work_dir, _)
            file_size = os.path.getsize(file_name)
            if file_size != 0:
                if os.path.splitext(file_name)[1].lower() in is_video:
                    if _.split()[0] == "youtube-dl":
                        if file_name not in ignore_temp["ignore"]:
                            video_id = os.path.split(file_name)[1].split()[1]
                            if insertgs.video_exists(video_id) == 1:
                                add_ingnore(file_name, ignore_temp)
                                message = str('{:s} [FILE] "{:s}" Video already exists.'.format(
                                    common.now_iso(2),
                                    video_id
                                    )
                                )
                                write_log(message)
                                print(message)
                            else:
                                error_apis = 0
                                try:
                                    video_info_list = []
                                    video_info_list = get_video_info(video_id) # Catch video_info_list from getyt.
                                    channel_id = video_info_list[1]
                                    published_at = video_info_list[2]
                                except:
                                    error_apis = 1
                                try:
                                    if error_apis == 0:
                                        insertgs.insert_video(video_info_list, file_name) # Throw video_info_list to insertgs.
                                        insertrdb.insert_video_info(video_info_list, file_name)
                                except:
                                    error_apis = 2
                                if error_apis == 0:
                                    rename_file(file_name, work_dir, published_at, video_id, ignore_temp)
                                    create_channel_folder(work_dir, channel_id)
                                    move_file(work_dir, channel_id)
                                    display(video_id, channel_id)
                                elif error_apis == 1:
                                    add_ingnore(file_name, ignore_temp)
                                    message = str('{:s} [FILE] "{:s}" Could not get video information.'.format(
                                        common.now_iso(2),           
                                        video_id
                                        )
                                    )
                                    write_log(message)
                                    print(message)
                                elif error_apis == 2:
                                    add_ingnore(file_name, ignore_temp)
                                    message = str('{:s} [FILE] "{:s}" Could not insert video information to sheet.'.format(
                                        common.now_iso(2),           
                                        video_id
                                        )
                                    )
                                    write_log(message)
                                    print(message)