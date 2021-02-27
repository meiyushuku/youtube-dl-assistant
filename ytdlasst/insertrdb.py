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

def channel_exists(channel_id):
    select_sql = '''SELECT 1 FROM `channel_info` WHERE `channel_id` = "{}" LIMIT 1'''.format(channel_id)
    res = select_data(conn, select_sql)
    if res:
        channel_exists = 1 # 1
    else:
        channel_exists = 0 # 0
    return channel_exists

def insert_video_info(video_info_list, file_name):
    _ = video_info_list[2]
    insert_sql = '''INSERT INTO `video_info`(
        site,
        channel_id,
        published_at,
        video_id,
        title,
        description,
        custom_description,
        duration,
        user,
        created_at,
        modified_at,
        extension
        ) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'''.format(
            "YT", # site
            video_info_list[1], # channel_id
            _.translate(_.maketrans("T", " ", "Z")), # published_at
            video_info_list[3], # video_id
            video_info_list[4], # title
            video_info_list[5], # description
            "", # custom_description
            common.d2s(video_info_list[6]), # duration
            config["general"]["user"], # user
            common.now(3), # created_at
            common.now(3), # modified_at
            re.sub("[.]", "", os.path.splitext(file_name)[1]) # extension
            )
    insert_data(conn, insert_sql)

def insert_channel_info(channel_id, channel_title):
    insert_sql = '''INSERT INTO `channel_info`(
        site,
        channel_id,
        channel_title,
        user
        ) VALUES ("{}", "{}", "{}", "{}")'''.format(
            "YT",
            channel_id,
            channel_title,
            config["general"]["user"]
            )
    insert_data(conn, insert_sql)

confidentials = common.read_json("doc/confidentials.json")
config = common.read_json("doc/config.json")
conn = connect()