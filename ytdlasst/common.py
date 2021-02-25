import os
import time
import json
import codecs

def read_json(json_file_name):
	with codecs.open(json_file_name, "rb", "utf-8") as json_file:
		json_data = json.load(json_file)
		return json_data

def write_json(json_file_name, content):
	with codecs.open(json_file_name, "w", "utf-8") as json_file:
		json.dump(content, json_file, ensure_ascii = False, indent = 4)

def make_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def now_iso(rep): # ISO 8601
	if rep == 1:
		time_ = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time()))
	elif rep == 2:
		time_ = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
	return time_