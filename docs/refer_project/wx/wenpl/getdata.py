# encoding=utf-8
'''
获取词库和对照库
'''
import jieba.posseg as pseg
import jieba
import sys
import urllib2
import json
import re
import copy
import datetime
import time
import calendar
import os

cwd = os.getcwd()

reload(sys)
sys.setdefaultencoding('utf-8')

# url1 = "/root/INTELLI-City/docs/refer_project/wx/wendata/dict/"
url1 = cwd + "/wendata/dict/"
time = "time.json"
stores = "store.json"
pro = "pro.json"
general = "general.json"
point = "points.json"
peoples = "intellence.json"

# 为了代码方便，先不写在文件里，测试用
api_platform = {
    "数据平台": 0,
    "动环系统": 1,
    "用户管理系统": 2
}


def getDate():
    pros = {}
    purl = url1+time
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    pros = toUTF8(jp)
    return pros


def getStore():
    store = {}
    surl = url1+stores
    fin = open(surl, 'r+')
    line = fin.readline()

    while line:
        j = json.loads(line)
        store[j.keys()[0].encode('utf-8')] = j[j.keys()[0]]
        line = fin.readline()
    fin.close()
    return store


def getPros():
    pros = {}
    purl = url1+pro
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    pros = toUTF8(jp)
    return pros


def getGenerals():
    generals = {}
    purl = url1+general
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    generals = toUTF8(jp)
    # print generals
    return generals


def getPoints():
    generals = {}
    purl = url1+point
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    generals = toUTF8(jp)
    return generals


def getPeople():
    people = {}
    purl = url1+peoples
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    people = toUTF8(jp)
    return people


def getPosition(type):
    purl = url1 + type + ".json"
    fin = open(purl, 'r+')
    p = fin.read()
    jp = json.loads(p)
    pros = toUTF8(jp)
    # print positions
    return pros


def getDict(url):
    try:
        data = open(url, "r+").read()
        # print data
        return data
    except Exception as e:
        print e

def toUTF8(origin):
    # change unicode type dict to UTF-8
    result = {}
    for x in origin.keys():
        val = origin[x].encode('utf-8')
        x = x.encode('utf-8')
        result[x] = val
    return result