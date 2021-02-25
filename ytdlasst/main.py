VERSION = "0.9.0"
print("youtube-dl-assistant")
print("Version %s (2021) Developed by Meiyu Shuku" % VERSION)
print("")

import threading
import os
import sys
import time
import json
import common

from getyt import _getyt_init

from fileproc import main

def ignore_init():
    ignore_init = {}
    ignore_init["ignore"] = ""
    common.write_json("doc/ignore.json", ignore_init)

config = common.read_json("doc/config.json")
work_dir = config["general"]["workDir"]
is_video = config["general"]["isVideo"]

if os.path.isdir(work_dir):
    if os.path.isfile("doc/confidentials.json"):
        with codecs.open("doc/confidentials.json", "rb", "utf-8") as json_file:
            confidentials = json.load(json_file)
        if _getyt_init(confidentials) == True:
            if _insertgs_init(confidentials) == True:
                ignore_init()
                while True:
                main(work_dir, is_video)
    else:
        print('"confidentials.json" not found.')
        input()
else:
    print("Working path must be a directory.")
    input()

