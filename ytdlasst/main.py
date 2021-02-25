import threading
import os
import sys
import time
import common
from fileproc import main

def ignore_init():
    ignore_init = {}
    ignore_init["ignore"] = ""
    common.write_json("doc/ignore.json", ignore_init)

VERSION = "0.9.0"
print("youtube-dl-assistant")
print("Version %s (2021) Developed by Meiyu Shuku" % VERSION)
print("")
print("Loading...")
print("")

config = common.read_json("doc/config.json")
work_dir = config["general"]["workDir"]
is_video = config["general"]["isVideo"]

if os.path.isdir(work_dir):
    ignore_init()
    while True:
        main(work_dir, is_video)
else:
    print("dir_error")
    input()