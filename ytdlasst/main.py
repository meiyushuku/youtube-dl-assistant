#import threading
import os
import sys
import time
import json

import common
from getyt import _getyt_init
from insertgs import _insertgs_init
from fileproc import main

VERSION = "0.9.0"
print("youtube-dl-assistant")
print("Version %s (2021) Developed by Meiyu Shuku" % VERSION)
print("")

def check_config():
    try:
        config = common.read_json("doc/config.json")
        config_error = 0
    except:
        config_error = 1
    return config_error

def check_confidentials():
    try:
        confidentials = common.read_json("doc/confidentials.json.")
        confidentials_error = 0
    except:
        confidentials_error = 1
    return confidentials_error

def ignore_init():
    ignore_init = {}
    ignore_init["ignore"] = ""
    common.write_json("doc/ignore.json", ignore_init)

if os.path.isfile("doc/config.json"):
    if check_config() == 0:
        if os.path.isfile("doc/confidentials.json."):
            if check_confidentials() == 0:
                config = common.read_json("doc/config.json")
                confidentials = common.read_json("doc/confidentials.json.")
                work_dir = config["general"]["workDir"]
                is_video = config["general"]["isVideo"]
                if os.path.isdir(work_dir):
                    if _getyt_init(confidentials) == True:
                        if _insertgs_init(config, confidentials) == True:
                            ignore_init()
                            while True:
                                main(work_dir, is_video)
                else:
                    print("Working path must be a directory.")
                    input()
            else:
                print('"confidentials.json." with invalid JSON format.')
                input()    
        else:
            print('"confidentials.json" not found.')
            input()
    else:
        print('"config.json" with invalid JSON format.')
        input()
else:
    print('"config.json" not found.')
    input()

sys.exit()