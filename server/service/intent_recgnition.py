# -*- coding: utf-8 -*-

import sys
import json
import re
import copy

import jieba
import jieba.posseg as pseg

from server.lib import nlp_process, jieba_process
from service_call import connect_turing, connect_rest_api


reload(sys)
sys.setdefaultencoding('utf-8')


def rule_based_intent_recognition(sentence):
    sentence = str(sentence).replace(' ', '')

    prepared_dict = pre_process(sentence)

    # 用结巴分词，拿到分词结果，list of [words, verb]
    divided_result = [[el.word, el.flag] for el in pseg.cut(sentence)]
    # print "divided_result", [utf_print(el[0]) for el in divided_result]

    # query_match主要是为了把分词结果里面的词语和我们的词库比对，找到相匹配的字段
    query_match_result = query_match(divided_result)

    # 没有用到，获取某个监测点的数据
    # point_result = point_query(divide_result, points, devices, stations, para)
    # if query_match_result:
    #     pass

    if query_match_result:
        hit_result = get_prefix_hit(query_match_result, api_dict, date)  # dict
        rank_result = api_rank(hit_result, query_match_result)  # dict
        return connect_rest_api(rank_result, *args)

    else:
        return connect_turing(sentence)


def pre_process(sentence):
    # 获取特殊的人名、地点、设备、采集点字段
    jieba_process.prepare_dicts()
    # 数组形式的时间[from, end]
    date_in_sentence = nlp_process.parse_datetime(sentence)
    print "Data Prepared Ready!"
    return {"date": date_in_sentence, }


# TODO paras就没什么用处，需要修改掉
def query_match(string_list, all_keywords, pro, api_dict, paras):
    # 跟专业词汇库比对，存入match_result
    match_result = []
    # 是否含有pro的单词
    pro_flag = 0
    # api词汇里含有的单词单独拿出来存入
    api_key_dict = {}

    for words in string_list:
        if words[0] in all_keywords.keys():
            # 分词结果需要考虑是否带有人名、地点和时间等信息，有的话需要加入关键词表
            match_result.append(all_keywords[words[0]])

            # 是不是含有专业词汇
            pro_flag = pro_flag + 1 if words[0] in pro else pro_flag
            # api词汇存入新的词典
            if words[0] in api_dict.keys():
                paras.append(words[0])

        return match_result if pro_flag else None


def point_query():
    return


def get_prefix_hit():
    return


def api_rank():
    return
