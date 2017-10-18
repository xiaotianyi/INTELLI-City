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


def connect_rest_api(paras, token):
    if paras == 0:
        pass
    elif paras == 1:
        pass
    else:
        pass

    url = ""
    web_flag = 0

    if url == 0:
        url = 'http://www.intellense.com:3080' + url
        web_flag = 1

    elif url == 1:
        web_flag = 1
        # return
    elif url == 2:
        web_flag = 2
        # return
    elif url == 3:
        web_flag = 3
        # return
    else:
        pass

    req = urllib2.Request(url)
    req.add_header('authorization', token) if web_flag else None
    response = urllib2.urlopen(req)

    return response.read(), web_flag

