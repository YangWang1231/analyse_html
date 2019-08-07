#!/usr/bin/python
 #coding:utf-8

import json

_config_data = None

def get_config():
    global _config_data
    if _config_data is None:
        with open('config.json','r') as json_config_file:
            _config_data = json.load(json_config_file)
    return _config_data

