# -*- coding: utf-8 -*-

import sys
import json
import re
import copy

import jieba
import jieba.posseg as pseg

from server.lib import NLP_process, jieba_process


reload(sys)
sys.setdefaultencoding('utf-8')


def pre_process(sentence):
    sentence = str(sentence).replace(' ', '')

    # 获取特殊的人名、地点、设备、采集点字段
    jieba_process.prepare_dicts()
    date_in_sentence = parse_data(sentence)

    # 拿到分词结果，list of [words, verb]
    divided_result = [[el.word, el.flag] for el in pseg.cut(sentence)]
    # print "divided_result", [utf_print(el[0]) for el in divided_result]

    # 分词结果需要考虑是否带有人名、地点和时间等信息，有的话需要加入关键词表


# 需要放入UTILITY, 用于打印类似于/ex17之类的utf字段
def utf_print(element):
    return unicode(element, "utf8", errors="ignore")