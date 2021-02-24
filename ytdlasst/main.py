import threading
import time
import sys
import common
import globalvar as glo
from fileproc import main

VERSION = "0.9.0"
print("youtube-dl-assistant-private")
print("Version %s (2021) Developed by Meiyu Shuku" % VERSION)
print("")

'''
def switch():
    input_menu_orig = input("Type here >>> ")
    input_menu = input_menu_orig.strip()
    if input_menu == "exit":
        sys.exit()
    elif input_menu == "":
        print("Not entered.")
        return switch()
    else:
        print("Command is not defined.")
        return switch()
'''

ignore_temp = common.read_json("ignore.json")
ignore_temp["ignore"] = ""
common.write_json("ignore.json", ignore_temp)
while True:
    main()