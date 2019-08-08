#!/usr/bin/python
 #coding:utf-8

import json



def init_config():
    config = None
    with open('config.json','r') as json_config_file:
        config  = json.load(json_config_file)
    return config

_config_data = init_config()