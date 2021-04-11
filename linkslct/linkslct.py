import os
import re
import sys
import codecs

import common

import mysql.connector as mydb # pip install mysql-connector-python

def check_confidentials():
    try:
        confidentials = common.read_json("confidentials.json")
        confidentials_error = 0
    except:
        confidentials_error = 1
    return confidentials_error

def connect():
    try:
        conn = mydb.connect(
            host = confidentials["insertRdb"]["host"],
            port = confidentials["insertRdb"]["port"],
            user = confidentials["insertRdb"]["user"],
            password = confidentials["insertRdb"]["password"],
            database = confidentials["insertRdb"]["database"]
        )
    except Exception as e:
        print("[DB Connection Error]", e)
        sys.exit(1)
    conn.ping(reconnect = True)
    return conn

def read_txt(txt_file_name):
    with codecs.open(txt_file_name, "r", "utf-8") as txt_file:
        lines = txt_file.readlines()
    return lines

def write_txt(txt_file_name, content):
    with codecs.open(txt_file_name, "w", "utf-8") as txt_file:
        lines = txt_file.writelines(content)

def write_log(message):
    writer = codecs.open("log.txt", "a","utf-8")
    writer.write("%s\n" % message)
    writer.close()

def select_data(_conn, _query):
    if _query.split()[0].upper() != "SELECT":
        print("[SELECT Error] Query is not select.", _query)
        sys.exit(1)
    cur = _conn.cursor()
    res = []
    try:
        cur.execute(_query)
        res = cur.fetchall()
    except Exception as e:
        print("[Select Data Error]", e)
    return res

def video_exists(video_id):
    select_sql = '''SELECT 1 FROM `video_info` WHERE `video_id` = "{}" LIMIT 1'''.format(video_id)
    res = select_data(conn, select_sql)
    if res:
        video_exists = 1 # 1
    else:
        video_exists = 0 # 0
    return video_exists

txt_file_name = "dl.txt"

if os.path.isfile("confidentials.json"):
    if check_confidentials() == 0:
        confidentials = common.read_json("confidentials.json")
        work_dir = "."
        if os.path.isdir(work_dir):
            conn = connect()
            link_list = []
            for line in read_txt(txt_file_name):
                line = line.replace("\r", "").replace("\n", "")
                if line.strip() != "":
                    video_id = line.split("youtu.be/")[1]
                    if video_exists(video_id) == 1:
                        message = str('{:s} [LINK] "{:s}" Video already exists.'.format(
                            common.now(2),
                            video_id
                            )
                        )
                        write_log(message)
                        print(message)
                    else:
                        link = "https://youtu.be/" + video_id + "\n"
                        if link not in link_list:
                            link_list.append(link)
                        else:
                            message = str('{:s} [LINK] "{:s}" Link already exists.'.format(
                                common.now(2),
                                video_id
                                )
                            )
                            write_log(message)
                            print(message)
            write_txt(txt_file_name, link_list)
            input()
        else:
            print("Working path must be a directory.")
            input()
    else:
        print('"confidentials.json." with invalid JSON format.')
        input()
else:
    print('"confidentials.json" not found.')
    input()