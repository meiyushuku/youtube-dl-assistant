import os
import time
import json
import codecs
import isodate # pip install isodate

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

def now(rep):
	if rep == 1: # ISO 8601 Basic
		time_ = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time()))
	elif rep == 2: # ISO 8601 Extended
		time_ = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
	elif rep == 3: # MariaDB DATETIME
		time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
	return time_

def d2s(dur):
	sec = int(isodate.parse_duration(dur).total_seconds())
	return sec