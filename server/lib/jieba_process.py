# -*- coding: utf-8 -*-
import sys
import os
import json
import time


import jieba
import jieba.posseg as pseg


reload(sys)
sys.setdefaultencoding('utf-8')

# 拿到工作路径
cwd = os.getcwd()
dict_url = cwd + '/lib/data_base/'
intellence = dict_url + "intellence.json"


# main called function
def prepare_dicts():
    # people = getPeople()
    # cities = getPosition('cities')
    # towns = getPosition('towns')
    # stations = getPosition('stations')
    # devices = getPositpassion('devices')
    # positions = merge_positions([cities, towns, stations, devices])
    # points = getPoints()
    # pro = getPros()
    # general = getGenerals()
    # paraCategory = dict(positions, **people)
    # dict1 = dict(general, **pro)
    # dict2 = dict(dict1, **paraCategory)
    # st = getStore()  # store dict
    pass


# 动环数据获取
def get_people():
    people = {}