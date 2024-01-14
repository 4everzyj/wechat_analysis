# coding:utf-8

import json

with open('config.json') as config_file:
    config = json.load(config_file)

MSG_XLSX_PATH = config['MSG_XLSX_PATH']
SAVE_DIR = config['SAVE_DIR']
TALKER = config['TALKER']
