import threading
import time

import sys
import json
import codecs
from mttkinter import mtTkinter as tk # pip install mttkinter
from tkinter import filedialog

def read_json(json_file_name):
	with codecs.open(json_file_name, "rb", "utf-8") as json_file:
		json_data = json.load(json_file)
	return json_data

def write_json(json_file_name, config):
	with codecs.open(json_file_name, "w", "utf-8") as json_file:
		json.dump(config, json_file, ensure_ascii = False, indent = 4)


def chgdir():
    input_chgdir_orig = input("Type here >>> ")
    input_chgdir = input_chgdir_orig.strip()
    json_file_name = "configtest.json"
    config = read_json(json_file_name)
    config["general"]["workDir"] = input_chgdir
    write_json(json_file_name, config)





input()