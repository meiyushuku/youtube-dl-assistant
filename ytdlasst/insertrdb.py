import os
import re
import sys
import json

import common

import mysql.connector as mydb # pip install mysql-connector-python

from getyt import get_video_info
from getyt import _getyt_init

def connect():
    try:
        conn = mydb.connect(
            host = confidentials["insertRdb"]["host"],
            port = confidentials["insertRdb"]["port"],
            user = confidentials["insertRdb"]["user"],
            password = confidentials["insertRdb"]["password"],
            database = confidentials["insertRdb"]["database"]
        )
        print("conn successfully") #
    except Exception as e:
        print("[DB Connection Error]", e)
        sys.exit(1)
    conn.ping(reconnect = True)
    return conn

def insert_data(_conn, _query):
    if _query.split()[0].upper() != "INSERT":
        print("[INSERT Error] Query is not insert.", _query)
        sys.exit(1)
    cur = _conn.cursor()
    try:
        cur.execute(_query)
        _conn.commit()
    except Exception as e:
        print("[Insert Data Error]", e)
        _conn.rollback()
        sys.exit(1)

def insert_channel_info():
    channel_id = common.now_iso(1)
    insert_sql = '''INSERT INTO channelInfo(
        site,
        channelId,
        channelName,
        isOfficial,
        count
        ) VALUES ("YT", "{:s}", "123", "1", "20")'''.format(
            channel_id
            )
    insert_data(conn, insert_sql)

def insert_video_info(video_info_list, file_name):
    insert_sql = '''INSERT INTO videoInfo(
        site,
        channelId,
        publishedAt,
        videoId,
        title,
        description,
        customDescription,
        duration,
        user,
        extension
        ) VALUES ("{:s}", "{:s}", "{:s}", "{:s}", "{:s}", "{:s}", "{:s}", "{:s}", "{:s}", "{:s}")'''.format(
            "YT",
            video_info_list[1],
            video_info_list[2],
            video_info_list[3],
            video_info_list[4],
            video_info_list[5],
            "",
            video_info_list[6],
            config["general"]["user"],
            #common.now_iso(2),
            re.sub("[.]", "", os.path.splitext(file_name)[1])
            )
    insert_data(conn, insert_sql)


confidentials = common.read_json("doc/confidentials.json")
config = common.read_json("doc/config.json")
conn = connect()

'''
video_id = "fKp66a5MCco"
file_name = "D:/123\\youtube-dl fKp66a5MCco 248 乃木坂46掛橋沙耶香、衣装脱ぎ捨てボクサーに！岡山出身の4期生がCM単独初出演　鋭いパンチ連発！.mkv"

_getyt_init(confidentials)
video_info_list = []
video_info_list = get_video_info(video_id)
insert_video_info(video_info_list, file_name)
'''