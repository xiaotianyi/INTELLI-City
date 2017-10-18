# -*- coding: utf-8 -*-

import sys
import json
import re
import copy

import jieba
import jieba.posseg as pseg

from server.lib import nlp_process, jieba_process


reload(sys)
sys.setdefaultencoding('utf-8')


def pre_process(sentence):
    sentence = str(sentence).replace(' ', '')

    # 获取特殊的人名、地点、设备、采集点字段
    jieba_process.prepare_dicts()
    # 数组形式的时间[from, end]
    date_in_sentence = nlp_process.parse_datetime(sentence)

    print "Prepare data ready!"

    # 用结巴分词，拿到分词结果，list of [words, verb]
    divided_result = [[el.word, el.flag] for el in pseg.cut(sentence)]
    # print "divided_result", [utf_print(el[0]) for el in divided_result]

    query_match_result = query_match(divided_result)
    # 分词结果需要考虑是否带有人名、地点和时间等信息，有的话需要加入关键词表


def query_match(string_list):
    pass