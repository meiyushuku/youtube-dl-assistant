import os
import re
import json

import common

import requests # pip install requests2


confidentials = common.read_json("doc/confidentials.json")
config = common.read_json("doc/config.json")
DATABASE_API_URL = confidentials["insertGs"]["databeseApiUrl"]


video_id = "bPxtLb4oeXc"

video_info_url = DATABASE_API_URL + "?method=getVideoInfoByVideoId&site=YT&videoId=" + video_id
response = requests.get(video_info_url)

con = json.loads(response.text)

common.write_json(video_id + ".json", con)