import os
import re
import sys
import json

import common

import mysql.connector as mydb # pip install mysql-connector-python

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

def select_data(_conn, _query):
    if _query.split(" ")[0].upper() != "SELECT":
        print("[SELECT Error] Query is not select.", _query)
        sys.exit(1)
    cur = _conn.cursor()
    res = []
    try:
        cur.execute(_query)
        res = cur.fetchall()
    except Exception as e:
        print('[Select Data Error]', e)
    return res

def video_exists(video_id):
    select_sql = '''SELECT 1 FROM videoInfo WHERE videoId = "{}" LIMIT 1'''.format(video_id)
    res = select_data(conn, select_sql)
    if "1" in str(res):
        video_exists = 1 # 1
    else:
        video_exists = 0 # 0
    return video_exists

def insert_video_info(video_info_list, file_name):
    _ = video_info_list[2]
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
        created,
        updated,
        extension
        ) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'''.format(
            "YT", # site
            video_info_list[1], # channelId
            _.translate(_.maketrans("T", " ", "Z")), # publishedAt
            video_info_list[3], # videoId
            video_info_list[4], # title
            video_info_list[5], # description
            "", # customDescription
            common.d2s(video_info_list[6]), # duration
            config["general"]["user"], # user
            common.now(3),
            common.now(3),
            re.sub("[.]", "", os.path.splitext(file_name)[1]) # extension
            )
    insert_data(conn, insert_sql)

confidentials = common.read_json("doc/confidentials.json")
config = common.read_json("doc/config.json")
conn = connect()