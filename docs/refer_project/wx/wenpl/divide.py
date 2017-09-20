# encoding=utf-8
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
from parsedate import parseDate
from getdata import*
from showAll import*

jieba.load_userdict('/root/INTELLI-City/docs/refer_project/wx/wendata/dict/dict1.txt')
jieba.load_userdict('/root/INTELLI-City/docs/refer_project/wx/wendata/dict/dict_manual.txt')
jieba.load_userdict('/root/INTELLI-City/docs/refer_project/wx/wendata/dict/dict_date.txt')
jieba.load_userdict('/root/INTELLI-City/docs/refer_project/wx/wendata/dict/dict2.txt')


reload(sys)
sys.setdefaultencoding('utf-8')

# sentence = "杭州市 报警数量"  
# sentence = sentence.replace(' ', '')


def mergePositions(l):
    positions = {}
    for x in l:
        for y in x:
            positions[y] = 'position'
    return positions



def divide(str):
    # print str
    # return the unicode format result
    words = pseg.cut(str)
    li = []
    for w in words:

        li.append([w.word.encode('utf-8'), w.flag.encode('utf-8')])
    return li


def filt(li, type):
    # get the specific words depending on the type you want
    rli = []
    for w in li:
        if w[1] == type:
            rli.append(w[0])
    return rli


def paraFilter(store):
    # check parameters in store
    dictionary = {}
    for x in store.keys():
        dictionary[x] = []
        for y in x.split(" "):
            j = []
            j = re.findall(r'\w+', y)
            if j != []:
                dictionary[x].append(j)
    # print dictionary
    return dictionary


def getQueryTypeSet(li, dictionary, para, pro, paraCategory):
    # calculate the types of the query words
    # showp()
    qType = []
    Nkey = 0
    hasPosition = 0
    hasName = 0
    paradic = {}
    # print "dict", dictionary
    # print pro
    for w in li:
        word = w[0]
        print "word", word
        if word in dictionary.keys():
            qType.append(dictionary[word])
            if word in pro:
                Nkey += 1
            if word in paraCategory.keys():
                paradic[paraCategory[word]] = word
    print "qType", qType
    print "Nkey", Nkey
    print "para", para
    for x in paradic.values():
        para.append(x)
    if Nkey == 0:
        return 0
    return qType


def pointquery(li,points,devices,stations,para):
    #"获取某个监测点的数据"
    point=""
    device=""
    station=""
    for w in li:
        word=w[0]
        # print 1
        if points.has_key(word):
            point=word
        elif devices.has_key(word):
            device=word
        elif stations.has_key(word):
            station=word
    if point!="" and station!="" and device!="":
        url ="/data/point_info_with_real_time?station_name="+station+"&device_name="+device+"&point_name="+point
        return getResult(url)
    else:
        return 0

        
def getPrefixHit(qType, store):
    # calculate the hit times of each prefix sentences in store
    count = {}
    setType = set(qType)
    for i in range(len(store.keys())):
        setStore = set(store.keys()[i].split(' '))
        count[store.keys()[i]] = len(setStore & setType)
    return count


def ranking(count, qType):
    # calculate the probability
    setType = set(qType)
    N = len(setType)
    p = {}
    for x in count.keys():
        p[x] = float(count[x] / float(N))
    p = sort(p)
    return p


def sort(p):
    #对命中率进行排序
    dicts = sorted(p.iteritems(), key=lambda d: d[1], reverse=True)
    return dicts
    # print dicts


def revranking(count):
    # showDict(count)
    p = {}
    for x in count.keys():
        p[x] = float(count[x] / float(len(x.split(" "))))
    # showDict(p)
    p = sort(p)
    # print p
    return p


def excuteREST(p, rp, st, para, paraDict, qType, remember):

    #执行查询
    # p:正排序后的store匹配度列表
    # rp:反排序后的store匹配度列表
    # st:store字典
    # para:输入语句中的参数列表
    # paraDict: store中参数列表
    # print showList()
    # p[[[],[]],[]]
    # st{:}
    p = resort(p, rp)
    # print p
    writeData(p)
    url = ""
    print "para", para
    if len(para) == 0:
        for x in p:
            if len(paraDict[x[0]]) == 0:
                url = st[x[0]]
                print "line 181", url, x[0]
                remember.append(x)
                break
    elif len(para) == 1:
        for x in p:
            if len(paraDict[x[0]]) == 1:
                # print paraDict[x[0]][0][0]
                if qType.count(paraDict[x[0]][0][0]) == 1:
                    url = st[x[0]] + para[0]
                    remember.append(x)
                    break
        if url == "":
            return 0

    elif len(para) == 2:
        for x in p:
            if len(paraDict[x[0]]) == 2:
                url = st[x[0]][0] + para[0] + st[x[0]][1] + para[1][0]+st[x[0]][2]+para[1][1]
                remember.append(x)
                break
        if url == "":
            return 0


    # url=st[p[0][0]]
    # if len(para)!=0:
    # 	url+=para[0]

    return getResult(url)


def getResult(url):
    #与服务器建立连接，获取json数据并返回
    turl = '/root/INTELLI-City/docs/refer_project/wx/wendata/token'
    fin1 = open(turl, 'r+')
    token = fin1.read()
    web_flag = 0
    if url[:4] != "http":
        url = 'http://www.intellense.com:3080' + url
        web_flag = 1
    print "url", url
    
    req = urllib2.Request(url)
    req.add_header('authorization', token) if web_flag else None
    response = urllib2.urlopen(req)
    print "response", response.read()

    #     req = urllib2.Request(url)
    #     print "req", req
    #     req.add_header('authorization', token) if web_flag else None
    #     response = urllib2.urlopen(req)
    #     print "response", response
    # else:
    #     return "请打开网址" + url

    fin1.close()


    # try:
    #     response = urllib2.urlopen(req)["message"]
    #     print "response", response
    # except Exception as e:
    #     return 0

    return response.read()


def resort(l1, l2):
    # 反向检查匹配度
    # print l2
    l1 = copy.deepcopy(l1)
    l2 = copy.deepcopy(l2)

    nl = []
    g = -1
    group = -1
    gdict = {}
    newlist = []
    for x in l1:
        if g != x[1]:
            group += 1
            g = x[1]
            nl.append([])
            nl[group].append(x)
        else:
            nl[group].append(x)
    for g in nl:
        for x in g:
            for y in range(len(l2)):
                if x[0] == l1[y][0]:
                    gdict[x] = y
                    break
        sublist = sort(gdict)
        for x in sublist:
            newlist.append(x[0])
    return newlist


def writeData(list):
    url = 'test.txt'
    fout = open(url, 'w+')
    for item in list:
        fout.write(item[0] + " " + str(item[1]) + '\n')
    fout.close()


def connectTuring(a):
    #在没有匹配的时候调用外部问答
    kurl = '/root/INTELLI-City/docs/refer_project/wx/wendata/turkey'
    fin = open(kurl, 'r+')
    key = fin.read()
    url = r'http://www.tuling123.com/openapi/api?key=' + key + '&info=' + a
    reson = urllib2.urlopen(url)
    reson = json.loads(reson.read())
    fin.close()
    # print reson['text'],'\n'
    return reson['text']


def toUTF8(origin):
    # change unicode type dict to UTF-8
    result = {}
    for x in origin.keys():
        val = origin[x].encode('utf-8')
        x = x.encode('utf-8')
        result[x] = val
    return result


def showDict(l):
    for x in l.keys():
        print x + ' ' + str(l[x])


def showList(l):
    for x in l:
        print x


def test(sentence):
    # print "test1 sentence", sentence
    sentence = sentence.replace(' ', '')
    # print "test2 sentence", sentence
    people = getPeople()
    # print "test3 people", people
    cities = getPosition('cities')
    # print "test4 cities", cities
    towns = getPosition('towns')
    # print "test5 towns", towns
    stations = getPosition('stations')
    # print "test6 stations", stations
    devices = getPosition('devices')
    # print "test7 devices", devices
    positions = mergePositions([cities, towns, stations, devices])
    # print "test8 positions", positions
    points = getPoints()
    # print "test9 points", points
    pro = getPros()
    # print "test10 pro", pro
    general = getGenerals()
    # print "test11 general", general
    paraCategory = dict(positions, **people)
    # print "test12 paraCategory", paraCategory
    dict1 = dict(general, **pro)
    # print "test dict1", dict1
    dict2 = dict(dict1, **paraCategory)
    # print "test dict2", dict2
    st = getStore()  # store dict
    # print "get store", st
    para = []
    # print "test para", para
    keyphrase = pro.keys()
    paraDict = paraFilter(st)
    # print "test paraDict", paraDict
    date = parseDate(sentence)
    # print "test date", date
    ftype=0
    remember=[]
    divide_result = divide(sentence)  # list

    sentence_result = getQueryTypeSet(
        divide_result,
        dict2,
        para,
        pro,
        paraCategory)  # set
    for el in sentence_result:
        print "sentence_result", unicode(el, "utf8", errors="ignore")
    point_result = pointquery(divide_result, points, devices, stations, para)
    print "test point_result", point_result
    if point_result != 0:
        print "inn1"
        # print   "-----------------------------这是结果哦--------------------------------"
        # print get_point_info_with_real_time(json.loads(point_result))
        return get_point_info_with_real_time(json.loads(point_result))
    elif sentence_result == 0:
        # print   "-----------------------------这是结果哦--------------------------------"
        # print connectTuring(sentence)
        print "inn Turing"
        return connectTuring(sentence)
    else:
        print "inn3"
        if date != 0:
            sentence_result.append('time')
        hit_result = getPrefixHit(sentence_result, st)  # dict
        # print "hit_result", hit_result
        rank_result = ranking(hit_result, sentence_result)  # dict
        # print "rank_result", rank_result
        reranking_result = revranking(hit_result)
        # print "reranking_result", reranking_result[0]
        if date != 0:
            para.append(date)
        print "para", para
        excute_result = excuteREST(
            rank_result,
            reranking_result,
            st,
            para,
            paraDict,
            sentence_result,
            remember)
        print "excute_result", excute_result
        if excute_result == 0:
            print "inn turing"
            return connectTuring(sentence)
        # b=filt(a,'v')
        else:
            print "none return"
            # print "json.loads", json.loads(excute_result)
            re_info = showResult(json.loads(excute_result), remember[0]) if isinstance(excute_result, dict) else excute_result
            if re_info == "":
                # print   "-----------------------------这是结果哦--------------------------------"
                # print '没有相关数据信息'
                return '没有相关数据信息'
            else:
                # print   "-----------------------------这是结果哦--------------------------------"
                # print re_info
                return re_info

# test()
def showReply(sentence):
    sentence=str(sentence)
    print "sentence", sentence
    try:
        return test(sentence)
    except Exception as e:
        return '我好像不太明白·_·'

# print showReply("查询工单")

