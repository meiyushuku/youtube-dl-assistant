import os
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