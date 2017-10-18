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


# main called function
def prepare_dicts():
    # people = getPeople()
    # cities = getPosition('cities')
    # towns = getPosition('towns')
    # stations = getPosition('stations')
    # devices = getPositpassion('devices')

    # TODO 需要对cities, towns, stations, devices进行转化
    # positions = merge_positions([cities, towns, stations, devices])

    # points = getPoints()
    # pro = getPros()
    # general = getGenerals()
    # paraCategory = dict(positions, **people)
    # dict1 = dict(general, **pro)
    # dict2 = dict(dict1, **paraCategory)
    # st = getStore()  # store dict

    # 加载各支持字典
    platform_dict = get_dict("intellence.json")
    pro_dict = get_dict("pro.json")
    general_dict = get_dict("general.json")
    words_dict = dict(pro_dict, general_dict)
    all_dicts = dict(words_dict, **platform_dict)

    # 加载api字典
    api_dict = get_dict("api.json")


# 各路存储的字典
def get_dict(file_name):
    url = dict_url + file_name
    file = open(url, 'r+').read()
    json = json.loads(file)
    result = to_utf8(json)
    file.close()
    return result


# change unicode type dict to UTF-8
def to_utf8(uni_dict):
    utf_result = {}
    for key, value in enumerate(uni_dict):
        utf_result[key.encode('utf-8')] = value.encode('utf-8')
    return utf_result