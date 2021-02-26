import sys

import common

import mysql.connector as mydb # pip install mysql-connector-python

def connect():
  # DB接続に失敗した場合の例外対策
  try:
    resconn = mydb.connect(
      host = confidentials["insertRdb"]["host"],
      port = confidentials["insertRdb"]["port"],
      user = confidentials["insertRdb"]["user"],
      password = confidentials["insertRdb"]["password"],
      database = confidentials["insertRdb"]["database"]
    )
    print("conn successfully")
  except Exception as e:
    print('[DB Connection Error]', e)
    sys.exit(1) # プログラムをエラー終了
  # 接続が切れた場合に自動的に再接続する
  resconn.ping(reconnect = True)
  return resconn

def insert_data(_conn, _query):
    # INSERTのクエリかどうかを判別
    if _query.split(' ')[0].upper() != 'INSERT':
        print('[INSERT Error] Query is not insert.', _query)
        sys.exit(1)
    cur = _conn.cursor() # カーソル作成
    try:
        cur.execute(_query) # sqlの実行
        conn.commit() # コミットする
    except Exception as e:
        print('[Insert Data Error]', e)
        _conn.rollback() # ロールバックする
        sys.exit(1)

confidentials = common.read_json("doc/confidentials.json")

conn = connect()
channel_id = "125499995645377"
insert_sql = '''INSERT INTO channelInfo(site,channelId,channelName,isOfficial,count
) VALUES ("YT","{:s}","123","1","20")'''.format(channel_id)
insert_data(conn, insert_sql)