import sys
import json
import codecs
from rename import rename_exe

VERSION = "0.9.0"
print("youtube-dl-assistant-private")
print("Version %s (2021) Developed by Meiyu Shuku" % VERSION)
print("")

def switch():
    input_menu_orig = input("Type here >>> ")
    input_menu = input_menu_orig.strip()
    if input_menu == "rename":
        rename_exe()
    elif input_menu == "setting":
        chgdir()
        return switch()
    elif input_menu == "":
        print("Not entered.")
        return switch()
    else:
        print("Command is not defined.")
        return switch()

def chgdir():
    input_chgdir_orig = input("Type here >>> ")
    input_chgdir = input_chgdir_orig.strip()
    json_file_name = "config.json"
    config = read_json(json_file_name)
    config["general"]["workDir"] = input_chgdir
    write_json(json_file_name, config)
    print("Returned to menu.")

def read_json(json_file_name):
	with codecs.open(json_file_name, "rb", "utf-8") as json_file:
		json_data = json.load(json_file)
	return json_data

def write_json(json_file_name, config):
	with codecs.open(json_file_name, "w", "utf-8") as json_file:
		json.dump(config, json_file, ensure_ascii = False, indent = 4)

controller = 1
while controller:
    switch()
    print('Task is completed. Type "menu" to return to menu or exit by any other.')
    input_end_orig = input("Type here >>> ")
    input_end = input_end_orig.strip()
    if input_end == "menu":
        print("Returned to menu.")
        pass
    else:
        sys.exit()