# encoding=utf-8
import urllib2
import json


# 在没有匹配的时候调用外部问答
def connect_turing(sentence):
    import os
    cwd = os.getcwd()
    key_url = cwd + '/wendata/turkey'
    turing_url = r'http://www.tuling123.com/openapi/api?key='

    file = open(key_url, 'r+').read()
    json = json.loads(file)
    url = turing_url + json["turing_key"] + '&loc=杭州市' + '&info=' + sentence
    file.close()

    response = urllib2.urlopen(url).read()
    response = json.loads(response)['text']

    return response
